#!/usr/bin/env python3
"""对 Obsidian Vault 做只读完整性检查，不修改任何文件。"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_PARTS = {".git", ".github", ".obsidian", ".idea", ".claude"}
REQUIRED_FIELDS = {"category", "priority", "status", "tags"}
VALID_PRIORITIES = {"P0", "P1", "P2"}
VALID_STATUSES = {"未学习", "看过", "能回答", "需复习"}

QUESTION_RE = re.compile(r"^##\s+(\d+)\.\s+(.+?)\s*$", re.MULTILINE)
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)
WIKILINK_RE = re.compile(r"!?\[\[([^\]]+)\]\]")
FIELD_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):", re.MULTILINE)


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def markdown_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if not any(part in EXCLUDED_PARTS for part in path.relative_to(ROOT).parts)
    )


def is_knowledge_note(path: Path) -> bool:
    parts = path.relative_to(ROOT).parts
    return len(parts) > 1 and re.fullmatch(r"\d{2}-.+", parts[0]) is not None


def split_frontmatter(text: str) -> tuple[str | None, str]:
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text
    return text[4:end], text[end + 5 :]


def remove_code_examples(text: str) -> str:
    """移除代码示例，避免把示例中的 Wikilink 当成真实链接。"""
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def frontmatter_value(frontmatter: str, key: str) -> str | None:
    match = re.search(rf"^{re.escape(key)}:\s*(.*?)\s*$", frontmatter, re.MULTILINE)
    return match.group(1) if match else None


def resolve_note(
    source: Path,
    target: str,
    notes_by_stem: dict[str, list[Path]],
) -> tuple[Path | None, str | None]:
    cleaned = target.strip().replace("\\", "/")
    if not cleaned:
        return source, None

    target_path = Path(cleaned)
    if target_path.suffix != ".md":
        target_path = target_path.with_suffix(".md")

    candidates = [ROOT / target_path, source.parent / target_path]
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve(), None

    matches = notes_by_stem.get(Path(cleaned).stem, [])
    if len(matches) == 1:
        return matches[0], None
    if len(matches) > 1:
        return None, f"目标文件名不唯一：{cleaned}"
    return None, f"目标文件不存在：{cleaned}"


def main() -> int:
    errors: list[str] = []
    files = markdown_files()
    texts: dict[Path, str] = {}
    headings: dict[Path, set[str]] = {}
    notes_by_stem: dict[str, list[Path]] = defaultdict(list)

    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            errors.append(f"{relative(path)}：不是有效的 UTF-8 文件（{exc}）")
            continue
        texts[path.resolve()] = text
        headings[path.resolve()] = {value.strip() for value in HEADING_RE.findall(text)}
        notes_by_stem[path.stem].append(path.resolve())

    question_ids: dict[int, list[tuple[Path, str]]] = defaultdict(list)
    question_count = 0

    for path, text in texts.items():
        frontmatter, _ = split_frontmatter(text)
        if is_knowledge_note(path):
            if frontmatter is None:
                errors.append(f"{relative(path)}：缺少或未闭合 YAML Frontmatter")
            else:
                fields = set(FIELD_RE.findall(frontmatter))
                missing = sorted(REQUIRED_FIELDS - fields)
                if missing:
                    errors.append(f"{relative(path)}：缺少 Frontmatter 字段 {', '.join(missing)}")

                priority = frontmatter_value(frontmatter, "priority")
                if priority not in VALID_PRIORITIES:
                    errors.append(f"{relative(path)}：priority 值无效：{priority!r}")

                status = frontmatter_value(frontmatter, "status")
                if status not in VALID_STATUSES:
                    errors.append(f"{relative(path)}：status 值无效：{status!r}")

        for number, title in QUESTION_RE.findall(text):
            question_count += 1
            question_ids[int(number)].append((path, title))

        for raw_link in WIKILINK_RE.findall(remove_code_examples(text)):
            link = raw_link.split("|", 1)[0].strip()
            target_text, separator, heading = link.partition("#")
            target_path, error = resolve_note(path, target_text, notes_by_stem)
            if error:
                errors.append(f"{relative(path)}：Wikilink `{raw_link}` {error}")
                continue
            if separator and heading.strip() and target_path is not None:
                target_headings = headings.get(target_path.resolve(), set())
                if heading.strip() not in target_headings:
                    errors.append(
                        f"{relative(path)}：Wikilink `{raw_link}` 的标题锚点不存在"
                    )

    for number, locations in sorted(question_ids.items()):
        if len(locations) > 1:
            detail = "; ".join(
                f"{relative(path)} -> {title}" for path, title in locations
            )
            errors.append(f"题号 {number} 重复：{detail}")

    if errors:
        print(f"Obsidian Vault 检查失败：{len(errors)} 个问题", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "Obsidian Vault 检查通过："
        f"{len(files)} 个 Markdown 文件，{question_count} 道编号题，"
        f"{sum(len(WIKILINK_RE.findall(remove_code_examples(text))) for text in texts.values())} 个 Wikilink。"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
