# Checkpoint Karpathy Agent Workflow

[English](README.md) | 简体中文

这是一个同时支持 Codex 和 Claude Code 的工作流：路线图驱动、阶段 checkpoint、每个小阶段提交一次 Git commit，并结合 Karpathy 风格的工程护栏。

它适用于从零开发、中途接手、功能开发、Bug 修复、重构、后期维护，以及任何需要在额度耗尽、session 中断、上下文丢失或多人接力时保持可恢复的开发任务。

## 核心思路

正式开发前，agent 先创建或更新路线图。之后每次只完成一个适合 commit 的小阶段。

每个正常小阶段结束时必须有：

- 已完成的 roadmap 项；
- 项目适用的验证；
- 更新后的 progress 日志；
- 一个 Git commit；
- 明确的下一步。

工程护栏是：

- 先思考再写代码；
- 保持方案简单；
- 在已有代码库里做小范围、精确修改；
- 围绕具体目标验证结果。

## 仓库状态文件

工作流使用一个命名空间目录：

```text
.checkpoint-karpathy/
  roadmap.md
  progress.md
  private/
```

默认协作模式：

- 提交 `.checkpoint-karpathy/roadmap.md`；
- 提交 `.checkpoint-karpathy/progress.md`；
- 忽略 `.checkpoint-karpathy/private/`。

隐私模式：

- 忽略 `.checkpoint-karpathy/roadmap.md`；
- 忽略 `.checkpoint-karpathy/progress.md`；
- 忽略 `.checkpoint-karpathy/private/`。

公开仓库或不想暴露开发规划时，使用隐私模式。

## 临时文件和项目产物规则

这个工作流不创建专用的 `tmp/` 目录。

agent 自己的临时文件应使用 agent 或工具原生的临时存储位置。不要把项目文件、构建输出、运行时临时文件、缓存、生成文件、覆盖率、日志、依赖 manifest、lockfile、源码、测试、配置、迁移或项目必需输出移动到 workflow 目录里。

项目文件应该留在真实项目树中。

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

默认协作模式：

```gitignore
.checkpoint-karpathy/private/
```

隐私模式：

```gitignore
.checkpoint-karpathy/roadmap.md
.checkpoint-karpathy/progress.md
.checkpoint-karpathy/private/
```

不要直接忽略整个 `.checkpoint-karpathy/`，除非你有意隐藏全部工作流状态。

## 推荐仓库名

```text
codex-claude-checkpoint-karpathy-workflow
```
