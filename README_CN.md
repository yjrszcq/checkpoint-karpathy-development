# Checkpoint Karpathy Agent Workflow

[English](README.md) | 简体中文

一个同时适用于 **Codex** 和 **Claude Code** 的可复用 Agent 工作流。

它把两类能力合在一起：

1. **Checkpoint-driven development（检查点驱动开发）**  
   把开发拆成小阶段；每完成一个阶段就更新 `docs/progress.md`，把临时/中间产物放进 `.agent-artifacts/`，运行项目适用的验证命令，并执行一次 Git commit。

2. **Karpathy-inspired engineering guardrails（Karpathy 风格工程护栏）**  
   先思考再编码，优先简单方案，避免臆想式抽象，在已有代码库中做外科手术式修改，并围绕明确目标验证结果。

推荐 GitHub 仓库名：

```text
codex-claude-checkpoint-karpathy-workflow
```

较短备选：

```text
checkpoint-karpathy-agent-workflow
checkpoint-karpathy-dev-skill
```

## 包含内容

```text
checkpoint-karpathy-agent-workflow/
  README.md
  README.zh-CN.md
  SKILL.md                                      # 通用 Skill 源文件
  AGENTS.md                                    # Codex 项目级指令
  CLAUDE.md                                    # Claude Code 项目级记忆/指令
  .gitignore                                   # 忽略 .agent-artifacts/
  codex/
    skills/
      checkpoint-karpathy-development/
        SKILL.md                               # Codex 安装布局
  .claude/
    skills/
      checkpoint-karpathy-development/
        SKILL.md                               # Claude Code Skill 布局
    commands/
      checkpoint-karpathy.md                   # 兼容旧式/自定义 slash command 的包装命令
```

## 适合什么时候用

适合用于：

- 从零开发新项目；
- 中途接手已有项目；
- 继续未完成工作；
- 新功能开发；
- Bug 修复；
- 重构；
- 后期维护；
- 发布前保守修改；
- 会影响开发流程的文档/配置修改；
- 任何多步骤、丢失未提交进度代价较高的 coding 任务。

不建议用于极小的一行修改，除非你明确希望每次改动都 checkpoint。

## 核心行为

每个完成的阶段都必须以这些结果收尾：

- 仓库处于一致、可继续的状态；
- `docs/progress.md` 已更新；
- 临时/中间产物统一放在 `.agent-artifacts/`；
- `.agent-artifacts/` 已被 Git 忽略；
- 已运行项目适用的最小验证；
- 已创建 Git commit。

**一个阶段没有 commit，就不算完成。**

## 工作模式

Agent 开始前应先判断当前任务属于哪种模式：

| 模式 | 使用场景 |
| --- | --- |
| Greenfield Development | 从零开始开发新项目 |
| Mid-Project Continuation | 中途接手已有代码库或继续未完成工作 |
| Feature Development | 增加新功能 |
| Bug Fixing | 复现、定位并修复 bug |
| Refactoring | 在保持行为不变的前提下改善结构 |
| Late-Stage Maintenance | 发布前或生产环境附近的保守修改 |

## Codex 安装

### 全局安装 Skill

把 Skill 复制到 Codex skills 目录：

```bash
mkdir -p ~/.codex/skills/checkpoint-karpathy-development
cp SKILL.md ~/.codex/skills/checkpoint-karpathy-development/SKILL.md
```

或者使用本仓库里的 Codex 布局：

```bash
mkdir -p ~/.codex/skills/checkpoint-karpathy-development
cp .codex/skills/checkpoint-karpathy-development/SKILL.md ~/.codex/skills/checkpoint-karpathy-development/SKILL.md
```

### 项目级指令

把 `AGENTS.md` 复制到目标项目根目录：

```bash
cp AGENTS.md /path/to/your/project/AGENTS.md
```

然后在该项目目录启动 Codex，并这样调用：

```text
$checkpoint-karpathy-development

阅读并遵守项目根目录的 AGENTS.md。按 checkpoint 阶段工作：更新 docs/progress.md，把临时文件放进 .agent-artifacts/，运行项目适用的验证命令，并在每个完成阶段后 git commit。
```

## Claude Code 安装

Claude Code 可通过 `CLAUDE.md` 使用项目级指令，也可以使用 `.claude/skills/<name>/SKILL.md` 这种 Skill 布局。本仓库同时提供两者。

### 项目级安装

把这些文件/目录复制到目标项目根目录：

```bash
cp CLAUDE.md /path/to/your/project/CLAUDE.md
mkdir -p /path/to/your/project/.claude/skills/checkpoint-karpathy-development
cp .claude/skills/checkpoint-karpathy-development/SKILL.md /path/to/your/project/.claude/skills/checkpoint-karpathy-development/SKILL.md
mkdir -p /path/to/your/project/.claude/commands
cp .claude/commands/checkpoint-karpathy.md /path/to/your/project/.claude/commands/checkpoint-karpathy.md
```

同时确保目标项目忽略 `.agent-artifacts/`：

```bash
grep -qxF '.agent-artifacts/' /path/to/your/project/.gitignore 2>/dev/null || echo '.agent-artifacts/' >> /path/to/your/project/.gitignore
```

### Claude Code 中使用

如果 skill 可用，可以直接调用：

```text
/checkpoint-karpathy-development <你的任务>
```

也可以使用本仓库提供的包装命令：

```text
/checkpoint-karpathy <你的任务>
```

或者用自然语言明确要求：

```text
这个任务使用 checkpoint-karpathy development。遵守 CLAUDE.md。按小阶段工作，更新 docs/progress.md，把临时文件放进 .agent-artifacts/，运行项目适用的验证命令，并在每个完成阶段后 commit。
```

## Claude Code 全局/个人安装

如果希望跨项目使用，可以把 skill 复制到 Claude 用户目录：

```bash
mkdir -p ~/.claude/skills/checkpoint-karpathy-development
cp SKILL.md ~/.claude/skills/checkpoint-karpathy-development/SKILL.md
```

兼容旧式/自定义 slash command：

```bash
mkdir -p ~/.claude/commands
cp .claude/commands/checkpoint-karpathy.md ~/.claude/commands/checkpoint-karpathy.md
```

如果某个项目需要特定行为，仍建议在该仓库根目录保留 `CLAUDE.md`。

## 中间产物

`.agent-artifacts/` 用于存放：

- 临时分析文件；
- 中间输出；
- 草稿计划；
- 临时日志；
- 一次性生成物；
- 不应该 commit 的 agent 工作文件。

持久交接信息应写入：

```text
docs/progress.md
```

如果某个中间产物后来变成正式交付物，必须把它移出 `.agent-artifacts/`，在 `docs/progress.md` 中记录原因，然后再 commit。

## Git 安全规则

除非用户明确要求，否则禁止运行破坏性 Git 命令。

没有明确授权时，不要运行：

```bash
git reset --hard
git clean
git rebase
git commit --amend
git push --force
git checkout -- .
git restore .
git restore --staged .
```

不要提交无关的用户改动。

不要提交密钥、token、`.env` 等敏感信息。

遵守 `.gitignore`。

## 推荐首次提示词

Codex：

```text
$checkpoint-karpathy-development

使用 checkpoint-karpathy development 继续这个项目。先检查仓库并选择工作模式。然后只完成一个小阶段，更新 docs/progress.md，把临时文件放进 .agent-artifacts/，运行项目适用的验证命令，并 git commit。
```

Claude Code：

```text
/checkpoint-karpathy 使用 checkpoint-karpathy development 继续这个项目。先检查仓库并选择工作模式。然后只完成一个小阶段，更新 docs/progress.md，把临时文件放进 .agent-artifacts/，运行项目适用的验证命令，并 git commit。
```

## 设计原则

这个工作流的优先级是：

1. **可恢复**：额度耗尽、会话中断、上下文丢失后，仍能从 Git 历史和 `docs/progress.md` 继续。
2. **小阶段**：每次只完成一个可验证目标。
3. **语言无关**：不要默认 Python、Node、Rust、Go 或任何技术栈；先根据项目文件识别。
4. **项目优先**：优先使用项目已有文档、脚本和约定。
5. **不乱提交**：只提交本阶段相关文件，不提交无关用户改动。
6. **不留脏状态**：完成的阶段必须记录、验证并 commit。
