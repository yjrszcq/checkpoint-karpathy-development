"""Validate structured goal content and fill the bundled Markdown templates."""

from datetime import date
from pathlib import Path
import re
from string import Template


WORK_MODES = ("greenfield", "continuation", "feature", "bugfix", "refactor", "maintenance")


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def fields(value, required, path, optional=()):
    if not isinstance(value, dict):
        raise ValueError(f"{path} must be an object.")
    missing = set(required) - value.keys()
    extra = value.keys() - set(required) - set(optional)
    if missing or extra:
        raise ValueError(f"{path}: missing fields {sorted(missing)}; unknown fields {sorted(extra)}.")


def text(value, path):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{path} must be a nonempty string.")
    return value.strip()


def strings(value, path, nonempty=False):
    if not isinstance(value, list) or (nonempty and not value):
        raise ValueError(f"{path} must be {'a nonempty' if nonempty else 'an'} array of strings.")
    return [text(item, f"{path}[{index}]") for index, item in enumerate(value)]


def bullets(items):
    return "\n".join("- " + item.replace("\n", "\n  ") for item in items) or "None."


def indent(value):
    return value.replace("\n", "\n    ")


def render_goal(payload, style, package):
    fields(payload, ("goal", "acceptance", "included", "non_goals", "work_mode",
                     "initial_state", "current_state", "next_action", "context", "milestones"),
           "goal", ("language",))
    language = payload.get("language", "en")
    if language not in ("en", "zh"):
        raise ValueError("language must be en or zh (generated record language).")
    values = {key: text(payload[key], key) for key in
              ("goal", "work_mode", "initial_state", "current_state", "next_action")}
    if values["work_mode"] not in WORK_MODES:
        raise ValueError(f"work_mode must be one of {WORK_MODES}.")
    for key in ("acceptance", "included", "non_goals"):
        values[key] = bullets(strings(payload[key], key, nonempty=key in ("acceptance", "included")))
    context = payload["context"]
    fields(context, ("constraints", "assumptions", "risks", "blockers"), "context")
    for key, prefix in (("constraints", "C"), ("assumptions", "A"), ("risks", "R"), ("blockers", "B")):
        items = strings(context[key], "context." + key)
        values[key] = bullets([f"{prefix}-{i:02}: {item}" for i, item in enumerate(items, 1)])
    values["related_blockers"] = "[See current blockers](context.md#blockers)" if context["blockers"] else "None."

    milestones = payload["milestones"]
    if not isinstance(milestones, list) or not milestones:
        raise ValueError("milestones must be a nonempty array.")
    identifiers, dependencies, rendered = set(), {}, []
    finish_order, start_order = {}, {}

    def identifier(value, path):
        value = text(value, path)
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", value) or value in identifiers:
            raise ValueError(f"{path} must be a unique stable ID using letters, numbers, dots, hyphens or underscores.")
        identifiers.add(value)
        return value

    def subject(value, phase, review=False):
        value = text(value, "commit")
        prefix = f"Phase {phase}{' Milestone Review' if review else ''}: "
        if "\n" in value or (style == "phase" and not value.startswith(prefix)) or (
                style == "conventional" and not re.fullmatch(r"[a-z]+(?:\([^()\n]+\))?!?: .+", value)):
            raise ValueError(f"Commit target must use the configured {style} style" + (f" ({prefix}...)." if style == "phase" else "."))
        return value

    folder = Path(package) / "assets/roadmap"

    def fill(name, data):
        return Template((folder / name).read_text(encoding="utf-8")).substitute(data)

    for index, milestone in enumerate(milestones):
        path = f"milestones[{index}]"
        fields(milestone, ("id", "title", "purpose", "dependencies", "phases", "review"), path)
        mid = identifier(milestone["id"], path + ".id")
        mvalues = {key: text(milestone[key], path + "." + key) for key in ("title", "purpose")}
        if "\n" in mvalues["title"]:
            raise ValueError(f"{path}.title must fit on one line.")
        dependencies[mid] = strings(milestone["dependencies"], path + ".dependencies")
        start_order[mid] = len(finish_order)
        mvalues.update(id=mid, dependencies=", ".join(dependencies[mid]) or "None.")
        phases = milestone["phases"]
        if not isinstance(phases, list) or not phases:
            raise ValueError(f"{path}.phases must be a nonempty array.")
        entries = []
        for pindex, phase in enumerate(phases):
            ppath = f"{path}.phases[{pindex}]"
            fields(phase, ("id", "title", "dependencies", "scope", "success_criteria", "verification", "commit"), ppath)
            pid = identifier(phase["id"], ppath + ".id")
            pvalues = {key: indent(text(phase[key], ppath + "." + key)) for key in
                       ("title", "scope", "success_criteria", "verification")}
            if "\n" in pvalues["title"]:
                raise ValueError(f"{ppath}.title must fit on one line.")
            dependencies[pid] = strings(phase["dependencies"], ppath + ".dependencies")
            start_order[pid] = len(finish_order)
            pvalues.update(id=pid, dependencies=", ".join(dependencies[pid]) or "None.", commit=subject(phase["commit"], pid))
            entries.append(fill("phase.md", pvalues))
            finish_order[pid] = len(finish_order)
            if index == pindex == 0:
                values["current_phase"] = f"[{pid} — {phase['title']}](milestones.md#milestone-{mid})"
        review = milestone["review"]
        fields(review, ("verification", "commit"), path + ".review")
        mvalues.update(phases="\n".join(entries).rstrip(), last_phase=pid,
                       review_verification=indent(text(review["verification"], path + ".review.verification")),
                       review_commit=subject(review["commit"], pid, review=True))
        rendered.append(fill("milestone.md", mvalues))
        finish_order[mid] = len(finish_order)
    # Dependency IDs must refer to the actual plan, not silently dropped input.
    for item, refs in dependencies.items():
        if item in refs or any(ref not in identifiers for ref in refs):
            raise ValueError(f"Unknown or self dependency in {item}: {refs}")
        if any(finish_order[ref] >= start_order[item] for ref in refs):
            raise ValueError(f"Dependencies of {item} must finish before it starts: {refs}. Supply milestones and phases in executable order.")
    values["milestones"] = "\n".join(rendered).rstrip()
    values["date"] = f"{date.today():%Y-%m-%d}"
    if language == "zh":
        values.update(generation_title="生成线路图", baseline_title="建立初始计划",
                      generation_completed="根据 agent 提供的结构化内容，按模板生成六份目标文档及完整里程碑计划。",
                      generation_verification="输入字段、非空必填内容、计划引用、提交目标格式和模板渲染校验通过；未执行项目测试或目标验收。",
                      generation_remaining="开发子阶段、里程碑复审和整体目标验收均未完成；计划项保持未勾选。",
                      baseline_reason="为当前目标建立初始规划基线。",
                      baseline_change="建立目标、验收条件、背景、完整里程碑计划和初始状态。",
                      baseline_impact="本计划作为后续开发与验收的基线；完成状态为 incomplete。")
    else:
        values.update(generation_title="Generate roadmap", baseline_title="Establish initial plan",
                      generation_completed="Rendered six goal documents and the full milestone plan from agent-supplied structured content.",
                      generation_verification="Validated fields, required content, plan references, commit target formats, and template rendering; no project tests or goal acceptance performed.",
                      generation_remaining="Development subphases, milestone reviews, and full-goal acceptance remain unfinished; all plan items are unchecked.",
                      baseline_reason="Establish the initial planning baseline for this goal.",
                      baseline_change="Created the goal, acceptance criteria, context, complete milestone plan, and initial status.",
                      baseline_impact="This plan is the baseline for development and acceptance; completion is incomplete.")
    values["affected_items"] = ", ".join(m["id"] for m in milestones)
    return {name: fill(name, values) for name in
            ("README.md", "status.md", "context.md", "milestones.md", "changelog.md", "progress.md")}
