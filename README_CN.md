# Checkpoint Karpathy Agent Workflow

[English](README.md) | 简体中文

这是一个同时支持 Codex 和 Claude Code 的工作流：路线图驱动、阶段 checkpoint、每个小阶段提交一次 Git commit，并结合 Karpathy 风格的工程护栏。

它适用于从零开发、中途接手、功能开发、Bug 修复、重构、后期维护，以及任何需要在额度耗尽、session 中断、上下文丢失或多人接力时保持可恢复的开发任务。

## 核心思路

正式开发前，agent 先创建路线图，从当前状态完整规划到实现所有目标。

skill 激活后，在 roadmap 完成之前会跨对话持续使用。每次新的开发对话自动从下一未完成子阶段恢复——用户无需重复调用。

roadmap 全部完成后，skill 自动停用。如果用户后续要求再次使用，已完成的 roadmap 和 progress 会被归档到 `.checkpoint-karpathy/archive/YYYY-MM-DD-<概括>/`。

每个正常小阶段结束时必须有：

- 已完成的 roadmap 项；
- 项目适用的验证；
- 更新后的 progress 日志；
- 一个默认使用英文 Conventional Commits 风格提交信息的 Git commit，除非用户明确要求中文或其他语言；
- 明确的下一步。

当一个大阶段完成时，agent 必须先单独执行 milestone review checkpoint 再继续。这个 checkpoint 不占用下一个规划 Phase/Subphase 编号；它先确认范围，再精简本大阶段工作，运行最完整且相关的验证，审查回归或集成缺口，debug 并修复范围内的问题，重新验证，记录 progress，并提交这次收尾。

工程护栏是：

- 先思考再写代码；
- 保持方案简单；
- 在已有代码库里做小范围、精确修改；
- 围绕具体目标验证结果。

Commit message 默认使用标准工程风格：

```text
type(scope): English summary
```

例如 `fix(web): update stale button state` 或 `docs(skill): require conventional commit messages`。只有用户明确要求时才使用中文或其他语言。

## 仓库状态文件

工作流使用一个命名空间目录：

**协作模式：**
```text
.checkpoint-karpathy/
  roadmap.md
  progress.md
  private/
  archive/
```

**隐私模式：**
```text
.checkpoint-karpathy/
  private/
    roadmap.md
    progress.md
    archive/
```

默认协作模式：

- 提交 `.checkpoint-karpathy/roadmap.md`；
- 提交 `.checkpoint-karpathy/progress.md`；
- 忽略 `.checkpoint-karpathy/private/`。

隐私模式：

- 将 `roadmap.md` 和 `progress.md` 放在 `.checkpoint-karpathy/private/` 下；
- `.checkpoint-karpathy/private/` 被 gitignore；
- 不提交 roadmap 或 progress。

公开仓库或不想暴露开发规划时，使用隐私模式。

## Codex 安装

把 skill 复制到 Codex 的用户级或项目级 skill 目录：

```bash
mkdir -p ~/.codex/skills/checkpoint-karpathy-development
cp .codex/skills/checkpoint-karpathy-development/SKILL.md ~/.codex/skills/checkpoint-karpathy-development/SKILL.md
```

项目级 Codex 指令：

```bash
cp AGENTS.md /path/to/your/project/AGENTS.md
```

调用示例：

```text
$checkpoint-karpathy-development

阅读 AGENTS.md。为当前任务创建或更新 .checkpoint-karpathy/roadmap.md，完成一个 roadmap 小阶段，更新 .checkpoint-karpathy/progress.md，运行项目适用的验证命令，并 git commit。
```

## Claude Code 安装

项目级 Claude Code 指令：

```bash
cp CLAUDE.md /path/to/your/project/CLAUDE.md
```

复制 Claude Code skill：

```bash
mkdir -p /path/to/your/project/.claude/skills/checkpoint-karpathy-development
cp .claude/skills/checkpoint-karpathy-development/SKILL.md /path/to/your/project/.claude/skills/checkpoint-karpathy-development/SKILL.md
```

可选 slash command：

```bash
mkdir -p /path/to/your/project/.claude/commands
cp .claude/commands/checkpoint-karpathy.md /path/to/your/project/.claude/commands/checkpoint-karpathy.md
```

调用示例：

```text
/checkpoint-karpathy 使用 checkpoint-karpathy development 继续这个项目。先判断工作模式，更新 roadmap，完成一个小阶段，更新 progress，运行验证并 commit。
```

## Gitignore

在 `.gitignore` 中加一行：

```gitignore
.checkpoint-karpathy/private/
```

隐私模式下 `roadmap.md` 和 `progress.md` 放在 `private/` 内，自动被覆盖。协作模式下仅敏感笔记被忽略。

不要直接忽略整个 `.checkpoint-karpathy/`，除非你有意隐藏全部工作流状态。

不要直接忽略整个 `.checkpoint-karpathy/`，除非你有意隐藏全部工作流状态。
