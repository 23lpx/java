#!/usr/bin/env python3
"""只读生成版本敏感内容复核队列，不修改 Obsidian Vault。"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_PARTS = {".git", ".github", ".obsidian", ".idea", ".claude"}
VALID_PRIORITIES = {"P0", "P1", "P2"}
VALID_VERIFIED = {"已校验", "待校验"}
PRIORITY_WEIGHTS = {"P0": 30, "P1": 15, "P2": 5}
PRIORITY_ORDER = {"P0": 0, "P1": 1, "P2": 2}
TOP_LEVEL_FIELD_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]*:")

RISK_RULES = (
    (
        "版本/API",
        re.compile(
            r"\b(?:JDK|JVM|Java|HotSpot|Spring|MyBatis|MySQL|Redis|"
            r"PageHelper|Maven|Docker|Nginx|HTTP|TCP|JWT|RFC)\b|支付宝|版本",
            re.IGNORECASE,
        ),
        20,
    ),
    (
        "并发/内存",
        re.compile(
            r"线程安全|并发|竞态|原子|volatile|CAS|AQS|锁|死锁|可见性|内存模型",
            re.IGNORECASE,
        ),
        20,
    ),
    (
        "事务/一致性",
        re.compile(
            r"事务|一致性|幂等|回滚|MVCC|隔离级别|持久化|主从|集群|分布式",
            re.IGNORECASE,
        ),
        20,
    ),
    (
        "实现细节",
        re.compile(r"底层|源码|实现细节|内部实现|默认行为|默认配置"),
        15,
    ),
    (
        "绝对化措辞",
        re.compile(r"一定|完全|永远|绝不会|必然|始终|任何情况下|全部"),
        15,
    ),
)


@dataclass(frozen=True)
class ReviewCandidate:
    path: Path
    priority: str
    verified: str | None
    reviewed_at: date | None
    version_scope: tuple[str, ...]
    score: int
    reasons: tuple[str, ...]


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


def frontmatter_value(frontmatter: str, key: str) -> str | None:
    match = re.search(rf"^{re.escape(key)}:\s*(.*?)\s*$", frontmatter, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip() or None


def frontmatter_list(frontmatter: str, key: str) -> tuple[str, ...]:
    lines = frontmatter.splitlines()
    start: int | None = None
    inline_value: str | None = None
    for index, line in enumerate(lines):
        match = re.fullmatch(rf"{re.escape(key)}:\s*(.*?)\s*", line)
        if match:
            start = index + 1
            inline_value = match.group(1).strip() or None
            break

    if start is None:
        return ()
    if inline_value:
        return (inline_value,)

    values: list[str] = []
    for line in lines[start:]:
        if TOP_LEVEL_FIELD_RE.match(line):
            break
        item = re.fullmatch(r"\s+-\s+(.+?)\s*", line)
        if item:
            values.append(item.group(1))
    return tuple(values)


def parse_reviewed_at(
    raw_value: str | None,
    path: Path,
    as_of: date,
) -> tuple[date | None, list[str]]:
    if raw_value is None:
        return None, []
    try:
        reviewed_at = date.fromisoformat(raw_value)
    except ValueError:
        return None, [f"{path.relative_to(ROOT).as_posix()}：reviewed_at 不是 YYYY-MM-DD"]
    if reviewed_at > as_of:
        return reviewed_at, [
            f"{path.relative_to(ROOT).as_posix()}：reviewed_at {reviewed_at} 晚于扫描日期 {as_of}"
        ]
    return reviewed_at, []


def build_candidate(
    path: Path,
    frontmatter: str,
    body: str,
    as_of: date,
) -> tuple[ReviewCandidate, list[str]]:
    errors: list[str] = []
    priority = frontmatter_value(frontmatter, "priority") or ""
    verified = frontmatter_value(frontmatter, "verified")
    reviewed_raw = frontmatter_value(frontmatter, "reviewed_at")
    version_scope = frontmatter_list(frontmatter, "version_scope")

    if priority not in VALID_PRIORITIES:
        errors.append(
            f"{path.relative_to(ROOT).as_posix()}：priority 值无效：{priority!r}"
        )
    if verified is not None and verified not in VALID_VERIFIED:
        errors.append(
            f"{path.relative_to(ROOT).as_posix()}：verified 值无效：{verified!r}"
        )
    reviewed_at, date_errors = parse_reviewed_at(reviewed_raw, path, as_of)
    errors.extend(date_errors)

    score = PRIORITY_WEIGHTS.get(priority, 0)
    reasons: list[str] = []
    if verified is None:
        score += 50
        reasons.append("缺 verified")
    elif verified == "待校验":
        score += 40
        reasons.append("状态待校验")

    if reviewed_at is None:
        score += 50
        reasons.append("缺 reviewed_at")
    else:
        age_days = (as_of - reviewed_at).days
        if age_days >= 365:
            score += 40
            reasons.append("超过 365 天未复核")
        elif age_days >= 180:
            score += 25
            reasons.append("超过 180 天未复核")
        elif age_days >= 90:
            score += 10
            reasons.append("超过 90 天未复核")

    if not version_scope:
        score += 50
        reasons.append("缺 version_scope")

    for label, pattern, weight in RISK_RULES:
        if pattern.search(body):
            score += weight
            reasons.append(label)

    candidate = ReviewCandidate(
        path=path,
        priority=priority or "—",
        verified=verified,
        reviewed_at=reviewed_at,
        version_scope=version_scope,
        score=score,
        reasons=tuple(reasons),
    )
    return candidate, errors


def collect_candidates(as_of: date) -> tuple[list[ReviewCandidate], list[str]]:
    candidates: list[ReviewCandidate] = []
    errors: list[str] = []
    for path in markdown_files():
        if not is_knowledge_note(path):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            errors.append(
                f"{path.relative_to(ROOT).as_posix()}：不是有效的 UTF-8 文件（{exc}）"
            )
            continue
        frontmatter, body = split_frontmatter(text)
        if frontmatter is None:
            errors.append(f"{path.relative_to(ROOT).as_posix()}：缺少或未闭合 Frontmatter")
            continue
        candidate, candidate_errors = build_candidate(path, frontmatter, body, as_of)
        candidates.append(candidate)
        errors.extend(candidate_errors)

    candidates.sort(
        key=lambda item: (
            -item.score,
            PRIORITY_ORDER.get(item.priority, 99),
            item.reviewed_at or date.min,
            item.path.relative_to(ROOT).as_posix(),
        )
    )
    return candidates, errors


def obsidian_link(path: Path) -> str:
    relative_path = path.relative_to(ROOT).as_posix()
    return f"[[{relative_path.removesuffix('.md')}]]"


def render_report(candidates: list[ReviewCandidate], as_of: date, limit: int) -> None:
    complete_count = sum(
        candidate.verified is not None
        and candidate.reviewed_at is not None
        and bool(candidate.version_scope)
        for candidate in candidates
    )
    print(
        f"版本复核扫描：{len(candidates)} 篇知识笔记，"
        f"维护元数据完整 {complete_count} 篇，待补 {len(candidates) - complete_count} 篇；"
        f"扫描日期 {as_of.isoformat()}。"
    )
    print("分数只用于安排复核顺序，不表示内容错误或个人掌握程度。")
    if limit == 0:
        return

    selected = candidates[:limit]
    print()
    print("| 排名 | 笔记 | 优先级 | 校验状态 | 最近复核 | 版本范围 | 分数 | 入队原因 |")
    print("| ---: | --- | --- | --- | --- | --- | ---: | --- |")
    for rank, candidate in enumerate(selected, 1):
        reviewed_at = candidate.reviewed_at.isoformat() if candidate.reviewed_at else "—"
        scope_state = "已记录" if candidate.version_scope else "缺失"
        reasons = "、".join(candidate.reasons) if candidate.reasons else "保持性抽查"
        print(
            f"| {rank} | {obsidian_link(candidate.path)} | {candidate.priority} | "
            f"{candidate.verified or '—'} | {reviewed_at} | {scope_state} | "
            f"{candidate.score} | {reasons} |"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--as-of",
        type=date.fromisoformat,
        default=date.today(),
        metavar="YYYY-MM-DD",
        help="指定扫描基准日期，默认使用今天",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="输出前 N 个候选；0 表示只输出汇总",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="发现非法状态、非法日期或未来日期时返回非零退出码",
    )
    args = parser.parse_args()
    if args.limit < 0:
        parser.error("--limit 不能小于 0")
    return args


def main() -> int:
    args = parse_args()
    candidates, errors = collect_candidates(args.as_of)
    if errors:
        print(f"版本复核元数据检查发现 {len(errors)} 个确定性问题", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        if args.check:
            return 1
    render_report(candidates, args.as_of, args.limit)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
