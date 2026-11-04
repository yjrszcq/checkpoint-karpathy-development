# 使用指南

[English](guide.md) | [项目首页](../README_CN.md)

## 安装

一键安装，交互选择 harness 和安装范围：

```bash
curl -fsSL https://raw.githubusercontent.com/yjrszcq/checkpoint-karpathy-development-skills/main/install.sh | bash
```

也可以直接指定 harness：

```bash
curl -fsSL https://raw.githubusercontent.com/yjrszcq/checkpoint-karpathy-development-skills/main/install.sh | bash -s -- --harness codex --scope user
```

支持 `claude`、`codex`、`pi`、`ohmypi`、`antigravity`、`cursor`、`deepseek`、`gemini`、`opencode`。多个 harness 可写为 `--harness claude,cursor`；项目级安装使用 `--project /path/to/project`。本地仓库可运行 `bash install.sh --harness codex --source .`。

在交互菜单选择 `custom`，即可手动输入技能目录；也可使用参数 `--harness custom --skills-dir /实际路径/skills`。安装器会在该目录下创建 `checkpoint-karpathy-development/`。

### 让 agent 帮你安装

把仓库链接和安装要求一起发给 agent，例如：

```text
帮我给当前使用的 harness 安装这个技能：
https://github.com/yjrszcq/checkpoint-karpathy-development-skills
请按照仓库里的 INSTALL.md 安装。
```

[INSTALL.md](../INSTALL.md) 提供 agent 安装流程、支持路径、自定义目录、更新、备份和验证说明。安装源统一为根目录的 `SKILL.md` 和完整 `references/`、`scripts/`、`assets/`；已有安装先备份到技能扫描目录之外。

安装后重启 harness 或重新加载技能，再要求它使用 `checkpoint-karpathy-development` 处理你的目标。

## 核心思路

每次使用先读取 `config.yaml`，仅在缺失时创建。配置记录可见性模式和提交风格，每项都注明当前值、可填值的作用和默认值。用户指定的设置按要求填，其余默认协作模式和 Conventional Commits；已有值持续沿用，用户要求时修改。

初始化时创建所选模式下固定的 `roadmap/` 和两种模式共用的 `private/work/`。目标文档全部放在 `roadmap/` 中，分别记录总览、状态、背景、里程碑计划、计划变更历史和执行历史。初次规划须完整覆盖全部目标。

目标未完成时，技能跨对话持续使用，恢复当前下一行动。完成或经用户明确要求取消后，技能停用，文档留在原位；下次明确启用技能开展新目标时，将旧文档内容归档，再在原 `roadmap/` 中创建新文档。`config.yaml` 和 `private/work/` 持续保留。

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

当一个大阶段完成时，agent 必须先单独执行 milestone review checkpoint 再继续。这个 checkpoint 沿用最后一个规划阶段的编号并添加复核后缀，先确认范围，再精简本大阶段工作，运行最完整且相关的验证，审查回归或集成缺口，debug 并修复范围内的问题，重新验证，记录 progress，并提交这次收尾。

工程护栏是：

- 先思考再写代码；
- 保持方案简单；
- 在已有代码库里做小范围、精确修改；
- 围绕具体目标验证结果。

## 仓库状态文件

**协作模式：**
```text
.checkpoint-karpathy/
  config.yaml
  roadmap/
  private/
    work/
  archive/
```

**隐私模式：**
```text
.checkpoint-karpathy/
  private/
    config.yaml
    roadmap/
    work/
    archive/
```

初始化即创建 `roadmap/` 和 `private/work/`，已有目录继续使用。`archive/` 及 work 分类子目录按需创建。协作模式提交配置、目标文档和归档；隐私模式将它们放在被 Git 忽略的 `private/` 下。

### 配置

生成的 `config.yaml` 自带逐项说明，用户修改对应的 YAML 值，注释说明配置项：

```yaml
# 规划文档的可见性和位置，默认 collaborative。
# collaborative：协作模式，配置、目标文档和归档纳入 Git。
# privacy：隐私模式，放在 Git 忽略的 private/ 下。
mode: collaborative

# 提交信息格式，默认 conventional。
# conventional：约定式提交，例如 feat(auth): add login。
# phase：阶段式提交，例如 Phase 1.1: add login。
commit_message_style: conventional
```

切换协作／隐私模式时，在目标位置创建或复用 `roadmap/`，先检查冲突，再将活动目标内容迁入该目录、将 `config.yaml` 迁入其上一级状态目录。保留源目录，保全文档内容及内部链接。已有归档、隐私笔记和 work 保留原位。切到隐私模式时，在下次相关提交中移除旧路径的跟踪；已有 Git 历史仍然存在。

### 项目状态脚本

项目状态脚本需要 **Python 3.9+** 和 **PyYAML >= 6.0**。使用前，在运行脚本的 Python 环境中安装依赖：

```bash
python3 -m pip install -r /技能路径/scripts/requirements.txt
```

使用已安装技能中的脚本，并填写实际项目根目录：

```bash
python3 /技能路径/scripts/init_project.py --project /项目路径 --mode collaborative --language zh
# 通过标准输入传入完整的结构化 JSON，见下方链接中的调用示例。
python3 /技能路径/scripts/create_goal.py --project /项目路径
python3 /技能路径/scripts/archive_goal.py --project /项目路径 --title old-goal-summary
```

初始化创建带注释的 YAML 配置、固定的空目录，并添加 private 的 Git 忽略规则。用户要求隐私模式或阶段式提交时，分别传 `--mode privacy`、`--commit-message-style phase`。已有配置和完整目标文档保持原样，部分缺失的状态先恢复。agent 将结构化 JSON 通过标准输入传给 `create_goal.py`，脚本校验后按模板生成六份实际文档，计划项均未勾选，并在 progress 记录“生成线路图”、在 changelog 记录“建立初始计划”。完整输入格式和调用示例见[结构化目标输入](../references/goal-input.md)。替换已结束目标时，先用 `--check-only` 校验新内容，再归档旧目标，最后用同一份输入创建新文档。归档脚本读取配置，只移动旧目标内容，保留空的固定 roadmap 目录；配置和 work 持续保留。状态字段要求和失败恢复见[脚本说明](../references/project-state.md#helper-commands)。

### 路线图文档

```text
roadmap/
  README.md
  status.md
  context.md
  milestones.md
  changelog.md
  progress.md
```

| 文档 | 内容 |
|---|---|
| README.md | 目标、整体验收、范围、工作类型、初始状态、导航 |
| status.md | 完成状态、当前状态、当前阶段、下一行动 |
| context.md | 约束、假设、风险、阻塞及其证据和状态 |
| milestones.md | 完整里程碑、子阶段、依赖、验收、验证、提交目标、复核及完成状态 |
| changelog.md | 实质性计划变更的原因、内容和影响 |
| progress.md | 实际改动、验证结果、提交、执行决策及问题处理 |

创建这六份文档，内容详略与任务规模相称。详细状态只在一处维护，其他文档通过稳定编号和相对链接引用。最新状态覆盖更新，历史追加；普通勾选和下一行动更新无需写计划变更记录。下一行动也可能是里程碑复核或解除阻塞。

恢复任务时先读 `README.md`、`status.md`、最近进度和当前里程碑，再按需读取相关背景及依赖。需要了解决策原因时读取计划变更历史；变更范围、跨里程碑依赖或进行最终验收时核对完整计划。普通检查点同步更新里程碑勾选、状态和进度，其他文档在对应信息变化时更新。

文档模板见 [roadmap-templates.md](../references/roadmap-templates.md)。文档较长时可继续按里程碑或查阅需要拆分，保持完整规划和导航。正式设计文档留在项目文档位置，由路线图引用。

### 完成状态与归档

完成状态记录在 `roadmap/status.md`：

- `incomplete`（未完成）：目标有效，继续当前任务；进行中、暂停、受阻写入当前状态。
- `completed`（已完成）：所有阶段、里程碑复核、提交和整体验收均完成，有验证记录。
- `cancelled`（已取消）：用户明确要求或确认终止；记录原因及终止经过，未完成项保留原状。

已完成和已取消采用相同归档流程：下次启用技能开展新目标时，将 `roadmap/` 内全部内容直接移入 `archive/YYYYMMDDa-<旧目标概括>/`，含额外文件和子目录。日期后字母递增，避免冲突。

固定 `roadmap/` 目录保留，再在其中创建新目标文档。`config.yaml` 持续保留并复用。

## 临时工作文件

两种模式都在初始化时创建 `.checkpoint-karpathy/private/work/`，由 `.checkpoint-karpathy/private/` 的 gitignore 规则覆盖。切换模式和归档目标时保持原位；不自动归档，也不在新任务开始时自动清空。

根目录不平铺文件。按用途或任务分类，按需创建 `logs/`、`verification/`、`tools/`、`reports/`、`browser/`、`screenshots/`、`configs/`、`fixtures/`、`backups/`、`drafts/`、`bin/`、`artifacts/` 等目录，再按任务或批次细分。

临时内容单独按需保留或清理，遵循项目删除规则。长期结论与验证摘要写入 `roadmap/progress.md`，使归档文档不依赖临时文件也能说明结果。需保留的原始证据可按任务放在 work 中并记录路径；正式源码、长期维护的测试和交付物留在各自项目位置。

## 技能文件组织

[SKILL.md](../SKILL.md) 保留执行流程、强制约束，并在需要细节的操作处提供链接。开始对应操作前，读取相关引用文档：

- [项目状态](../references/project-state.md)：配置、初始化、可见性模式切换和归档。
- [结构化目标输入](../references/goal-input.md)：字段、校验规则和 JSON 调用示例。
- [路线图模板](../references/roadmap-templates.md)：文档职责和目标模板。
- [检查点细节](../references/checkpoint-details.md)：进度模板、里程碑复核和验证方法查找。

## Gitignore

在 `.gitignore` 中加一行：

```gitignore
.checkpoint-karpathy/private/
```

隐私模式下配置、`roadmap/` 和归档都在 `private/` 内。两种模式的 work、备份和敏感笔记均由同一规则覆盖。

不要直接忽略整个 `.checkpoint-karpathy/`，除非你有意隐藏全部工作流状态。
