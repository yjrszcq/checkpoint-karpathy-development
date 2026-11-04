# Checkpoint Karpathy Agent Workflow

[English](README.md) | 简体中文

这是一个同时支持 Codex 和 Claude Code 的工作流：路线图驱动、阶段 checkpoint、每个小阶段提交一次 Git commit，并结合 Karpathy 风格的工程护栏。

它适用于从零开发、中途接手、功能开发、Bug 修复、重构、后期维护，以及任何需要在额度耗尽、session 中断、上下文丢失或多人接力时保持可恢复的开发任务。

## 核心思路

项目首次使用时，agent 先创建与 roadmap、progress 同层的 `config.md`，记录用户指定的模式和提交信息风格；未指定的项目填写默认值：协作模式、约定式提交。之后每次使用都读取此文件，用户要求调整时更新相应设置。

正式开发前，agent 先创建路线图，从当前状态完整规划到实现所有目标。

skill 激活后，在 roadmap 完成之前会跨对话持续使用。每次新的开发对话自动从下一未完成子阶段恢复——用户无需重复调用。

roadmap 全部完成后，skill 自动停用。如果用户后续要求再次使用，已完成的 roadmap 和 progress 会被归档到当前配置目录下的 `archive/YYYYMMDDa-<概括>/`，`config.md` 保留供后续任务使用。

每个正常小阶段结束时必须有：

- 已完成的 roadmap 项；
- 项目适用的验证；
- 更新后的 progress 日志；
- 一次 Git commit；
- 明确的下一步。

Commit message 有两种风格可选：

约定式提交（Conventional Commits，默认）：
```text
type(scope): <描述>
```

阶段式提交（Phase-style，可选）：
```text
Phase X.Y: <描述>
```

描述默认英文，只有用户明确要求时才使用中文或其他语言。

当一个大阶段完成时，agent 必须先单独执行 milestone review checkpoint 再继续。这个 checkpoint 不占用下一个规划 Phase/Subphase 编号；它先确认范围，再精简本大阶段工作，运行最完整且相关的验证，审查回归或集成缺口，debug 并修复范围内的问题，重新验证，记录 progress，并提交这次收尾。

工程护栏是：

- 先思考再写代码；
- 保持方案简单；
- 在已有代码库里做小范围、精确修改；
- 围绕具体目标验证结果。

## 仓库状态文件

工作流使用一个命名空间目录：

**协作模式：**
```text
.checkpoint-karpathy/
  config.md
  roadmap.md
  progress.md
  private/
    work/
  archive/
```

**隐私模式：**
```text
.checkpoint-karpathy/
  private/
    work/
    config.md
    roadmap.md
    progress.md
    archive/
```

`config.md` 记录实际采用的设置：

```md
# Checkpoint Karpathy Configuration

- Mode: collaborative
- Commit message style: conventional
```

`Mode` 可填 `collaborative`（协作）或 `privacy`（隐私）；`Commit message style` 可填 `conventional`（约定式提交）或 `phase`（阶段式提交）。用户切换模式时，配置、路线图、进度三个文件一起移动到对应目录，并按该模式决定是否纳入 Git。已有归档和其他隐私笔记保留在原位置。

默认协作模式：

- 提交 `.checkpoint-karpathy/config.md`；
- 提交 `.checkpoint-karpathy/roadmap.md`；
- 提交 `.checkpoint-karpathy/progress.md`；
- 忽略 `.checkpoint-karpathy/private/`。

隐私模式：

- 将 `config.md`、`roadmap.md` 和 `progress.md` 放在 `.checkpoint-karpathy/private/` 下；
- `.checkpoint-karpathy/private/` 被 gitignore；
- 配置、roadmap 和 progress 均不纳入 Git 跟踪。

公开仓库或不想暴露开发规划时，使用隐私模式。

## 临时工作文件

两种模式都使用 `.checkpoint-karpathy/private/work/` 存放项目过程中的临时文件，由 `.checkpoint-karpathy/private/` 的 gitignore 规则覆盖。切换模式或归档任务时，`work` 保持原位置。

`work/` 根目录不放散落文件。按用途或任务分类，需要时才创建子目录，例如：`logs/<任务>/` 放命令日志，`tools/<任务>/` 放临时脚本，`reports/<任务>/` 放分析报告，`browser/<任务>/`、`screenshots/<任务>/` 放浏览器数据和截图，`configs/`、`fixtures/` 放临时配置和测试输入，`backups/`、`drafts/` 放中间副本和草稿，`bin/`、`artifacts/` 放编译产物。也可以用一个任务目录，把相关脚本、日志、报告分组放在一起；分类下文件较多时继续按任务或运行批次细分。

正式源码、长期维护的测试和交付给用户的文件放在各自应在的项目位置。需要长期保留的结论、验证摘要写入 progress。

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

阅读 AGENTS.md，并读取或创建 config.md。按其中的模式和提交风格，为当前任务创建或更新 roadmap，完成一个小阶段，更新 progress，运行项目适用的验证命令，并 git commit。
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

隐私模式下 `config.md`、`roadmap.md` 和 `progress.md` 放在 `private/` 内，自动被覆盖。协作模式下仅敏感笔记被忽略。

不要直接忽略整个 `.checkpoint-karpathy/`，除非你有意隐藏全部工作流状态。
