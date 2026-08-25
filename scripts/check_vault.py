#!/usr/bin/env python3
"""对 Obsidian Vault 做只读完整性检查，不修改任何文件。"""

from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAINTENANCE_ROADMAP = ROOT / "00-V1.3维护路线图.md"
VERSION_REVIEW_QUEUE = ROOT / "00-版本敏感内容复核队列.md"
LEARNING_QUEUE = ROOT / "00-第一轮学习队列.md"
DAILY_REVIEW_TEMPLATE = ROOT / "00-每日学习与闭卷考核模板.md"
SECOND_ROUND_REVIEW_TEMPLATE = ROOT / "00-第二轮诊断与复习模板.md"
MOCK_INTERVIEW_TEMPLATE = ROOT / "00-模拟面试记录模板.md"
PROJECT_EVIDENCE_TEMPLATE = ROOT / "00-项目证据卡模板.md"
FOLLOWUP_TRAINING_TEMPLATE = ROOT / "00-追问链训练模板.md"
FOLLOWUP_ANSWER_CARD = ROOT / "00-第一组追问链答案核对卡.md"
P0_MOTHER_MAP = ROOT / "00-P0母题与追问链地图.md"
P0_ANSWER_INDEX = ROOT / "00-P0母题答案核对入口.md"
P0_BASIC_ANSWER_CARD = ROOT / "00-P0基础主干答案核对卡.md"
P0_EXTENDED_ANSWER_CARD = ROOT / "00-P0扩展主干答案核对卡.md"
P0_CLOSING_ANSWER_CARD = ROOT / "00-P0收口主干答案核对卡.md"
P0_ANSWER_CARDS = (
    FOLLOWUP_ANSWER_CARD,
    P0_BASIC_ANSWER_CARD,
    P0_EXTENDED_ANSWER_CARD,
    P0_CLOSING_ANSWER_CARD,
)
RESUME_EVIDENCE_DOCS = {
    ROOT / "00-简历证据与追问地图.md",
    ROOT / "00-苍穹外卖项目证据卡.md",
    PROJECT_EVIDENCE_TEMPLATE,
}
EXCLUDED_PARTS = {".git", ".github", ".obsidian", ".idea", ".claude"}
REQUIRED_FIELDS = {"category", "priority", "status", "tags"}
VALID_PRIORITIES = {"P0", "P1", "P2"}
VALID_STATUSES = {"未学习", "看过", "能回答", "需复习"}

QUESTION_RE = re.compile(r"^##\s+(\d+)\.\s+(.+?)\s*$", re.MULTILINE)
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)
WIKILINK_RE = re.compile(r"!?\[\[([^\]]+)\]\]")
FIELD_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):", re.MULTILINE)
QUESTION_SECTION_RE = re.compile(
    r"^\*\*(面试回答|原理与理解|成立条件与边界|"
    r"实际场景(?:（[^）\n]+）)?|常见追问|易错点)\*\*\s*$",
    re.MULTILINE,
)
REQUIRED_QUESTION_SECTIONS = (
    "面试回答",
    "原理与理解",
    "成立条件与边界",
    "实际场景",
    "常见追问",
    "易错点",
)
EXPECTED_P0_IDS = tuple(
    f"{prefix}{number}" for prefix in "JSMRWA" for number in range(1, 5)
)
P0_MOTHER_ROW_RE = re.compile(r"^\|\s*([JSMRWA]\d+)\s*\|", re.MULTILINE)
P0_INDEX_MAPPING_RE = re.compile(
    r"\b([JSMRWA]\d+)\s+\[\[([^#\]|]+)#([^\]|]+)(?:\|[^\]]+)?\]\]"
)
P0_ANSWER_HEADING_RE = re.compile(
    r"^##\s+(.+?[：:]\s*([JSMRWA]\d+)(?:\s+.+)?)\s*$",
    re.MULTILINE,
)
P0_ANSWER_SECTION_RE = re.compile(
    r"^###\s+(30 秒参考回答|60 秒扩展要点|120 秒场景闭环)\s*$",
    re.MULTILINE,
)
P0_LEVEL_RE = re.compile(r"^>\s*-\s*(L[0-4])：", re.MULTILINE)
P0_CHECK_CALLOUT_RE = re.compile(
    r"^>\s*\[!check\]-\s*L0～L4 核对\s*$",
    re.MULTILINE,
)
REQUIRED_P0_ANSWER_SECTIONS = (
    "30 秒参考回答",
    "60 秒扩展要点",
    "120 秒场景闭环",
)
REQUIRED_P0_LEVELS = ("L0", "L1", "L2", "L3", "L4")
MAINTENANCE_ROADMAP_HEADINGS = {
    "维护目标",
    "批次顺序",
    "已落地门禁",
    "后续批次边界",
    "V1.3 完成条件",
}
VERSION_REVIEW_QUEUE_HEADINGS = {
    "判定边界",
    "队列输入",
    "排序规则",
    "当前基线",
    "执行流程",
    "验收与回流",
}
DAILY_REVIEW_HEADINGS = {
    "今日计划",
    "白天学习记录",
    "晚间闭卷考核",
    "错题复盘",
    "学习状态变更",
    "当日结果",
    "明日行动",
}
SECOND_ROUND_REVIEW_HEADINGS = {
    "六线输入",
    "白天断点修复",
    "场景复盘",
    "算法与手写",
    "晚间闭卷考核",
    "项目真实性检查",
    "学习状态变更",
    "队列更新",
}
MOCK_INTERVIEW_HEADINGS = {
    "面试信息",
    "面试前",
    "六线面试记录",
    "单题证据",
    "项目真实性检查",
    "算法与手写",
    "面试后复盘",
    "第二轮队列回流",
    "状态变更",
    "下一次面试",
}
PROJECT_EVIDENCE_HEADINGS = {
    "证据元数据",
    "简历主张",
    "知识链",
    "60 秒回答骨架",
    "追问树",
    "证据清单",
    "真实性边界",
    "复测记录",
}
FOLLOWUP_TRAINING_HEADINGS = {
    "训练信息",
    "母题入口",
    "30 秒核心回答",
    "60 秒机制与边界",
    "120 秒场景闭环",
    "连续追问记录",
    "错误断点",
    "六线结果",
    "第二轮回流",
    "复测",
}
FOLLOWUP_ANSWER_CARD_HEADINGS = {
    "使用规则",
    "① Java：J4 线程池过载",
    "② Spring：S1 单例 Bean 与请求状态",
    "③ MySQL：M3 MVCC 与并发扣减",
    "④ Redis：R4 持久化与高可用",
    "⑤ Web/项目：W4 支付回调幂等",
    "⑥ 算法：A2 前缀和 + HashMap",
    "核对结果回流",
}
P0_ANSWER_INDEX_HEADINGS = {
    "使用规则",
    "覆盖进度",
    "使用流程",
    "维护边界",
}
P0_BASIC_ANSWER_CARD_HEADINGS = {
    "使用规则",
    "① Java：J1 对象相等与 HashMap Key",
    "② Spring：S2 MVC 请求与异常响应链",
    "③ MySQL：M2 索引、回表与执行计划",
    "④ Redis：R2 Cache Aside 与一致性",
    "⑤ Web/项目：W1 JWT 认证与请求上下文",
    "⑥ 算法：A1 API、Comparator 与输入契约",
    "核对结果回流",
}
P0_EXTENDED_ANSWER_CARD_HEADINGS = {
    "使用规则",
    "① Java：J2 集合选择、迭代与并发修改",
    "② Spring：S3 AOP 代理与公共字段自动填充",
    "③ MySQL：M1 SQL 结果语义、连接与分页",
    "④ Redis：R1 数据结构、Key、过期与内存",
    "⑤ Web/项目：W2 HTTP 语义、幂等与网络链路",
    "⑥ 算法：A3 栈队列、树图与搜索",
    "核对结果回流",
}
P0_CLOSING_ANSWER_CARD_HEADINGS = {
    "使用规则",
    "① Java：J3 JVM 内存、对象创建与回收",
    "② Spring：S4 声明式事务与 MyBatis 写入链",
    "③ MySQL：M4 锁、超卖与死锁",
    "④ Redis：R3 穿透、击穿与雪崩",
    "⑤ Web/项目：W3 统一异常、订单关联与历史快照",
    "⑥ 算法：A4 堆、动态规划与正确性证明",
    "核对结果回流",
}
PRIVATE_CONTACT_RE = re.compile(
    r"(?:1[3-9]\d{9}|[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,})",
    re.IGNORECASE,
)


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


def question_structure_errors(question_body: str) -> list[str]:
    """验证单道编号题的六段式标签、顺序和非空正文。"""
    cleaned = remove_code_examples(question_body)
    section_matches = list(QUESTION_SECTION_RE.finditer(cleaned))
    actual_sections = [
        "实际场景" if match.group(1).startswith("实际场景") else match.group(1)
        for match in section_matches
    ]
    expected_sections = list(REQUIRED_QUESTION_SECTIONS)

    if actual_sections != expected_sections:
        expected = " → ".join(expected_sections)
        actual = " → ".join(actual_sections) if actual_sections else "无"
        return [f"六段式结构异常（期望 {expected}；实际 {actual}）"]

    issues: list[str] = []
    for index, match in enumerate(section_matches):
        section_end = (
            section_matches[index + 1].start()
            if index + 1 < len(section_matches)
            else len(cleaned)
        )
        if not cleaned[match.end() : section_end].strip():
            issues.append(f"`{actual_sections[index]}` 正文为空")
    return issues


def p0_id_coverage_errors(
    actual_ids: list[str],
    source_name: str,
    *,
    require_order: bool,
) -> list[str]:
    """验证 P0 ID 是否恰好覆盖 J/S/M/R/W/A 各 1～4。"""
    issues: list[str] = []
    counts = Counter(actual_ids)
    expected_set = set(EXPECTED_P0_IDS)
    missing = [p0_id for p0_id in EXPECTED_P0_IDS if counts[p0_id] == 0]
    duplicates = sorted(p0_id for p0_id, count in counts.items() if count > 1)
    unexpected = sorted(set(actual_ids) - expected_set)

    if missing:
        issues.append(f"{source_name}缺少 P0 ID：{', '.join(missing)}")
    if duplicates:
        issues.append(f"{source_name}存在重复 P0 ID：{', '.join(duplicates)}")
    if unexpected:
        issues.append(f"{source_name}存在未知 P0 ID：{', '.join(unexpected)}")
    if (
        require_order
        and not missing
        and not duplicates
        and not unexpected
        and tuple(actual_ids) != EXPECTED_P0_IDS
    ):
        issues.append(f"{source_name}的 P0 ID 顺序与母题规范不一致")
    return issues


def p0_answer_structure_errors(answer_body: str) -> list[str]:
    """验证一条 P0 答案的 30/60/120 秒层级和 L0～L4 核对项。"""
    cleaned = remove_code_examples(answer_body)
    section_matches = list(P0_ANSWER_SECTION_RE.finditer(cleaned))
    actual_sections = [match.group(1) for match in section_matches]
    issues: list[str] = []

    if tuple(actual_sections) != REQUIRED_P0_ANSWER_SECTIONS:
        expected = " → ".join(REQUIRED_P0_ANSWER_SECTIONS)
        actual = " → ".join(actual_sections) if actual_sections else "无"
        issues.append(f"答案层级异常（期望 {expected}；实际 {actual}）")
    else:
        for index, match in enumerate(section_matches):
            section_end = (
                section_matches[index + 1].start()
                if index + 1 < len(section_matches)
                else len(cleaned)
            )
            if not cleaned[match.end() : section_end].strip():
                issues.append(f"`{actual_sections[index]}` 正文为空")

    callout_count = len(P0_CHECK_CALLOUT_RE.findall(cleaned))
    if callout_count != 1:
        issues.append(f"L0～L4 核对块数量应为 1，实际为 {callout_count}")

    actual_levels = P0_LEVEL_RE.findall(cleaned)
    if tuple(actual_levels) != REQUIRED_P0_LEVELS:
        expected = " → ".join(REQUIRED_P0_LEVELS)
        actual = " → ".join(actual_levels) if actual_levels else "无"
        issues.append(f"核对层级异常（期望 {expected}；实际 {actual}）")
    return issues


def p0_mapping_target_errors(
    p0_id: str,
    target_path: Path,
    target_heading: str,
    answer_locations: dict[str, list[tuple[Path, str]]],
    answer_cards: set[Path],
) -> list[str]:
    """验证答案入口中的 ID 是否指向承载同一 ID 的唯一标题。"""
    issues: list[str] = []
    if target_path not in answer_cards:
        issues.append(f"指向非 P0 答案卡 {relative(target_path)}")

    locations = answer_locations.get(p0_id, [])
    if len(locations) != 1:
        return issues

    expected_path, expected_heading = locations[0]
    if target_path != expected_path or target_heading.strip() != expected_heading:
        issues.append(
            "映射不一致，应指向 "
            f"`{relative(expected_path)}#{expected_heading}`"
        )
    return issues


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

    target_path = Path(
        cleaned if cleaned.casefold().endswith(".md") else f"{cleaned}.md"
    )

    candidates = [ROOT / target_path, source.parent / target_path]
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve(), None

    matches = notes_by_stem.get(target_path.stem, [])
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
    structured_question_count = 0

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

        question_matches = list(QUESTION_RE.finditer(text))
        for index, match in enumerate(question_matches):
            number, title = match.groups()
            question_count += 1
            question_ids[int(number)].append((path, title))
            if is_knowledge_note(path):
                question_end = (
                    question_matches[index + 1].start()
                    if index + 1 < len(question_matches)
                    else len(text)
                )
                structure_issues = question_structure_errors(
                    text[match.end() : question_end]
                )
                if structure_issues:
                    for issue in structure_issues:
                        errors.append(
                            f"{relative(path)}：题号 {number} {issue}"
                        )
                else:
                    structured_question_count += 1

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

    queue_path = LEARNING_QUEUE.resolve()
    queue_notes: list[Path] = []
    if queue_path not in texts:
        errors.append(f"{relative(LEARNING_QUEUE)}：第一轮学习队列不存在")
    else:
        for raw_link in WIKILINK_RE.findall(remove_code_examples(texts[queue_path])):
            link = raw_link.split("|", 1)[0].strip()
            target_text = link.partition("#")[0]
            target_path, error = resolve_note(
                LEARNING_QUEUE, target_text, notes_by_stem
            )
            if error is None and target_path is not None and is_knowledge_note(target_path):
                queue_notes.append(target_path.resolve())

        knowledge_notes = {path for path in texts if is_knowledge_note(path)}
        queued_note_set = set(queue_notes)
        for path in sorted(knowledge_notes - queued_note_set):
            errors.append(f"{relative(path)}：未加入第一轮学习队列")
        for path in sorted(queued_note_set - knowledge_notes):
            errors.append(f"{relative(path)}：不是有效的知识笔记")

        queue_counts: dict[Path, int] = defaultdict(int)
        for path in queue_notes:
            queue_counts[path] += 1
        for path, count in sorted(queue_counts.items()):
            if count > 1:
                errors.append(
                    f"{relative(path)}：在第一轮学习队列中重复 {count} 次"
                )

    required_documents = {
        MAINTENANCE_ROADMAP: MAINTENANCE_ROADMAP_HEADINGS,
        VERSION_REVIEW_QUEUE: VERSION_REVIEW_QUEUE_HEADINGS,
        DAILY_REVIEW_TEMPLATE: DAILY_REVIEW_HEADINGS,
        SECOND_ROUND_REVIEW_TEMPLATE: SECOND_ROUND_REVIEW_HEADINGS,
        MOCK_INTERVIEW_TEMPLATE: MOCK_INTERVIEW_HEADINGS,
        PROJECT_EVIDENCE_TEMPLATE: PROJECT_EVIDENCE_HEADINGS,
        FOLLOWUP_TRAINING_TEMPLATE: FOLLOWUP_TRAINING_HEADINGS,
        FOLLOWUP_ANSWER_CARD: FOLLOWUP_ANSWER_CARD_HEADINGS,
        P0_ANSWER_INDEX: P0_ANSWER_INDEX_HEADINGS,
        P0_BASIC_ANSWER_CARD: P0_BASIC_ANSWER_CARD_HEADINGS,
        P0_EXTENDED_ANSWER_CARD: P0_EXTENDED_ANSWER_CARD_HEADINGS,
        P0_CLOSING_ANSWER_CARD: P0_CLOSING_ANSWER_CARD_HEADINGS,
    }
    for document_path, required_headings in required_documents.items():
        resolved_path = document_path.resolve()
        if resolved_path not in texts:
            errors.append(f"{relative(document_path)}：必需维护文件不存在")
            continue
        missing_headings = sorted(required_headings - headings[resolved_path])
        if missing_headings:
            errors.append(
                f"{relative(document_path)}：缺少必需标题 "
                f"{', '.join(missing_headings)}"
            )

    p0_map_path = P0_MOTHER_MAP.resolve()
    p0_map_ids: list[str] = []
    if p0_map_path not in texts:
        errors.append(f"{relative(P0_MOTHER_MAP)}：P0 母题地图不存在")
    else:
        p0_map_ids = P0_MOTHER_ROW_RE.findall(
            remove_code_examples(texts[p0_map_path])
        )
        errors.extend(
            p0_id_coverage_errors(
                p0_map_ids,
                "P0 母题地图",
                require_order=True,
            )
        )

    answer_locations: dict[str, list[tuple[Path, str]]] = defaultdict(list)
    answer_ids: list[str] = []
    for answer_card in P0_ANSWER_CARDS:
        answer_card_path = answer_card.resolve()
        if answer_card_path not in texts:
            continue
        answer_text = remove_code_examples(texts[answer_card_path])
        answer_matches = list(P0_ANSWER_HEADING_RE.finditer(answer_text))
        for index, match in enumerate(answer_matches):
            answer_heading, p0_id = match.groups()
            answer_heading = answer_heading.strip()
            answer_end = (
                answer_matches[index + 1].start()
                if index + 1 < len(answer_matches)
                else len(answer_text)
            )
            answer_ids.append(p0_id)
            answer_locations[p0_id].append((answer_card_path, answer_heading))
            for issue in p0_answer_structure_errors(
                answer_text[match.end() : answer_end]
            ):
                errors.append(
                    f"{relative(answer_card)}：{p0_id} {issue}"
                )

    errors.extend(
        p0_id_coverage_errors(
            answer_ids,
            "P0 答案卡",
            require_order=False,
        )
    )

    index_path = P0_ANSWER_INDEX.resolve()
    index_mappings: list[tuple[str, str, str]] = []
    if index_path not in texts:
        errors.append(f"{relative(P0_ANSWER_INDEX)}：P0 答案入口不存在")
    else:
        index_mappings = P0_INDEX_MAPPING_RE.findall(
            remove_code_examples(texts[index_path])
        )
        errors.extend(
            p0_id_coverage_errors(
                [p0_id for p0_id, _, _ in index_mappings],
                "P0 答案入口",
                require_order=True,
            )
        )

    resolved_answer_cards = {path.resolve() for path in P0_ANSWER_CARDS}
    for p0_id, target_text, target_heading in index_mappings:
        target_path, error = resolve_note(
            P0_ANSWER_INDEX,
            target_text,
            notes_by_stem,
        )
        if error or target_path is None:
            errors.append(
                f"{relative(P0_ANSWER_INDEX)}：{p0_id} 的答案映射无法解析"
            )
            continue

        target_path = target_path.resolve()
        for issue in p0_mapping_target_errors(
            p0_id,
            target_path,
            target_heading,
            answer_locations,
            resolved_answer_cards,
        ):
            errors.append(
                f"{relative(P0_ANSWER_INDEX)}：{p0_id} {issue}"
            )

    for evidence_path in RESUME_EVIDENCE_DOCS:
        resolved_path = evidence_path.resolve()
        if resolved_path not in texts:
            errors.append(f"{relative(evidence_path)}：简历证据文件不存在")
            continue
        if PRIVATE_CONTACT_RE.search(texts[resolved_path]):
            errors.append(
                f"{relative(evidence_path)}：不得保存手机号或邮箱等私人联系方式"
            )

    if errors:
        print(f"Obsidian Vault 检查失败：{len(errors)} 个问题", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "Obsidian Vault 检查通过："
        f"{len(files)} 个 Markdown 文件，{question_count} 道编号题，"
        f"六段式结构覆盖 {structured_question_count} 道编号题，"
        f"P0 母题与答案映射 {len(EXPECTED_P0_IDS)}/24，"
        f"{sum(len(WIKILINK_RE.findall(remove_code_examples(text))) for text in texts.values())} 个 Wikilink，"
        f"学习队列覆盖 {len(queue_notes)} 个知识节点。"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
