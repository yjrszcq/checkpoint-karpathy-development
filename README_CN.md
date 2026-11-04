# Checkpoint Karpathy Agent Workflow

[English](README.md) | 简体中文

这是一个同时支持 Codex 和 Claude Code 的工作流：路线图驱动、阶段 checkpoint、每个小阶段提交一次 Git commit，并结合 Karpathy 风格的工程护栏。

它适用于从零开发、中途接手、功能开发、Bug 修复、重构、后期维护，以及任何需要在额度耗尽、session 中断、上下文丢失或多人接力时保持可恢复的开发任务。

## 核心思路

每次使用先读取 `config.md`，仅在缺失时创建。配置记录可见性模式、提交风格和文档布局，每项都注明当前值、可填值的作用和默认值。用户指定的设置按要求填，其余默认协作模式、Conventional Commits 和 `auto` 布局；已有值持续沿用，用户要求时修改。

初始化时创建所选模式下固定的 `roadmap/` 和两种模式共用的 `private/work/`。目标文档全部放在 `roadmap/` 中：精简布局适合集中、简单的目标；拆分布局适合多里程碑、复杂依赖和持续演变的计划。初次规划均须完整覆盖全部目标。

目标未完成时，技能跨对话持续使用，恢复当前下一行动。完成或经用户明确要求取消后，技能停用，文档留在原位；下次明确启用技能开展新目标时，将旧文档内容归档，再在原 `roadmap/` 中创建新文档。`config.md` 和 `private/work/` 持续保留。

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

**协作模式：**
```text
.checkpoint-karpathy/
  config.md
  roadmap/
  private/
    work/
  archive/
```

**隐私模式：**
```text
.checkpoint-karpathy/
  private/
    config.md
    roadmap/
    work/
    archive/
```

初始化即创建 `roadmap/` 和 `private/work/`，已有目录继续使用。`archive/` 及 work 分类子目录按需创建。协作模式提交配置、目标文档和归档；隐私模式将它们放在被 Git 忽略的 `private/` 下。

### 配置

生成的 `config.md` 自带逐项说明，用户修改对应的 `Value`：

```md
# Checkpoint Karpathy Configuration

## Mode
- Value: collaborative
- 作用：选择规划文档的可见性和存放位置。
- 可填值：
  - collaborative：协作模式，配置、目标文档和归档纳入 Git。
  - privacy：隐私模式，配置、目标文档和归档放在 Git 忽略的 private/ 下。
- 默认值：collaborative

## Commit message style
- Value: conventional
- 作用：选择提交信息格式。
- 可填值：
  - conventional：约定式提交，例如 feat(auth): add login。
  - phase：阶段式提交，例如 Phase 1.1: add login。
- 默认值：conventional

## Roadmap layout
- Value: auto
- 作用：选择当前目标的文档组织方式。
- 可填值：
  - auto：Agent 根据整个目标选择并评估是否切换布局。
  - compact：固定精简布局，仅在用户要求时切换。
  - structured：固定拆分布局，仅在用户要求时切换。
- 默认值：auto
```

切换协作／隐私模式时，在目标位置创建或复用 `roadmap/`，先检查冲突，再将活动目标内容迁入该目录、将 `config.md` 迁入其上一级状态目录。保留源目录，保全文档内容及内部链接。已有归档、隐私笔记和 work 保留原位。切到隐私模式时，在下次相关提交中移除旧路径的跟踪；已有 Git 历史仍然存在。

### 两种布局

```text
精简布局 roadmap/
  roadmap.md
  progress.md

拆分布局 roadmap/
  README.md
  status.md
  context.md
  milestones.md
  changelog.md
  progress.md
```

| 内容 | 精简布局 | 拆分布局 |
|---|---|---|
| 目标、整体验收、范围、工作类型、初始状态、导航 | roadmap.md | README.md |
| 完成状态、当前状态、当前阶段、下一行动 | roadmap.md | status.md |
| 约束、假设、风险、阻塞及其证据和状态 | roadmap.md | context.md |
| 完整里程碑、子阶段、依赖、验收、验证、提交目标、复核及完成状态 | roadmap.md | milestones.md |
| 实质性计划变更的原因、内容和影响 | roadmap.md 中的变更记录 | changelog.md |
| 实际改动、验证结果、提交、执行决策及问题处理 | progress.md | progress.md |

精简布局无需单独 README。详细状态只在一处维护，其他文档通过稳定编号和相对链接引用。最新状态覆盖更新，历史追加；普通勾选和下一行动更新无需写计划变更记录。下一行动也可能是里程碑复核或解除阻塞。

`auto` 在规划和执行时评估整个目标的计划、依赖、背景、设计演变和累计历史，可双向切换。不能仅凭剩余任务变少就合并文档，也应避免频繁切换。固定布局仅在用户要求时切换；自动切换后配置仍保留 `auto`。

切换前，将完整原文档及子目录备份到 `.checkpoint-karpathy/private/work/backups/roadmap-layout/<时间>-<原布局>-to-<目标布局>/`，核对完整性。按内容含义重组，保留自定义章节、目标、状态、编号、验收和全部历史，检查冲突并更新链接。逐项安置被替代文件，核对新文档与备份；失败时保留部分结果并恢复原内容。在计划变更记录中说明切换原因、布局和备份路径。切换不触发任务归档。

模板和转换指导见 [roadmap-templates.md](references/roadmap-templates.md)。文档较长时可继续按里程碑或查阅需要拆分，保持完整规划和导航。正式设计文档留在项目文档位置，由路线图引用。

### 完成状态与归档

完成状态记录在精简布局的 `roadmap.md` 或拆分布局的 `status.md`：

- `incomplete`（未完成）：目标有效，继续当前任务；进行中、暂停、受阻写入当前状态。
- `completed`（已完成）：所有阶段、里程碑复核、提交和整体验收均完成，有验证记录。
- `cancelled`（已取消）：用户明确要求或确认终止；记录原因及终止经过，未完成项保留原状。

已完成和已取消采用相同归档流程：下次启用技能开展新目标时，将 `roadmap/` 内全部内容直接移入 `archive/YYYYMMDDa-<旧目标概括>/`，含额外文件和子目录。日期后字母递增，避免冲突。归档内直接是目标文档，不再套一层 `roadmap/`。

固定 `roadmap/` 目录保留，再在其中创建新目标文档。`config.md` 不归档、不重建。恢复任务先读配置和当前布局的入口、完成状态，再读相关计划、背景及最近进度；核对完成标记与实际验收记录。

## 临时工作文件

两种模式都在初始化时创建 `.checkpoint-karpathy/private/work/`，由 `.checkpoint-karpathy/private/` 的 gitignore 规则覆盖。切换模式、布局和归档目标时保持原位；不自动归档，也不在新任务开始时自动清空。

根目录不平铺文件。按用途或任务分类，按需创建 `logs/`、`verification/`、`tools/`、`reports/`、`browser/`、`screenshots/`、`configs/`、`fixtures/`、`backups/`、`drafts/`、`bin/`、`artifacts/` 等目录，再按任务或批次细分。

临时内容单独按需保留或清理，遵循项目删除规则。长期结论与验证摘要写入 `roadmap/progress.md`，使归档文档不依赖临时文件也能说明结果。需保留的原始证据可按任务放在 work 中并记录路径；正式源码、长期维护的测试和交付物留在各自项目位置。

## Codex 安装

把 skill 复制到 Codex 的用户级或项目级 skill 目录：

```bash
mkdir -p ~/.codex/skills/checkpoint-karpathy-development
cp -R .codex/skills/checkpoint-karpathy-development/. ~/.codex/skills/checkpoint-karpathy-development/
```

项目级 Codex 指令：

```bash
cp AGENTS.md /path/to/your/project/AGENTS.md
```

调用示例：

```text
$checkpoint-karpathy-development

阅读 AGENTS.md，并读取或创建 config.md。按其中的可见性模式、提交风格和布局策略，在 roadmap/ 内创建或更新当前目标的完整计划，完成一个小阶段，更新 progress，运行项目适用的验证命令，并 git commit。
```

## Claude Code 安装

项目级 Claude Code 指令：

```bash
cp CLAUDE.md /path/to/your/project/CLAUDE.md
```

复制 Claude Code skill：

```bash
mkdir -p /path/to/your/project/.claude/skills/checkpoint-karpathy-development
cp -R .claude/skills/checkpoint-karpathy-development/. /path/to/your/project/.claude/skills/checkpoint-karpathy-development/
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

隐私模式下配置、`roadmap/` 和归档都在 `private/` 内。两种模式的 work、备份和敏感笔记均由同一规则覆盖。

不要直接忽略整个 `.checkpoint-karpathy/`，除非你有意隐藏全部工作流状态。
