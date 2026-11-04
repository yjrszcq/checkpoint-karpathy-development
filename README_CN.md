# Checkpoint Karpathy Agent Workflow

[English](README.md) | 简体中文

一个以线路图推进开发、遵循 Karpathy 工程原则的技能。Agent 先规划完整目标，再逐步实现、验证、提交并记录进展，让工作能够跨会话、跨上下文恢复。

支持 Codex、Claude Code、Pi、Oh My Pi、Antigravity、Cursor、DeepSeek Harness 等兼容 agent。

## 快速安装

项目状态脚本需要 **Python 3.9+** 和 **PyYAML >= 6.0**，用于初始化项目、生成线路图及归档。依赖安装见[项目状态脚本](docs/guide_CN.md#项目状态脚本)。

运行安装脚本，交互选择 harness 和安装范围：

```bash
curl -fsSL https://raw.githubusercontent.com/yjrszcq/checkpoint-karpathy-development/main/install.sh | bash
```

也可以直接指定：

```bash
curl -fsSL https://raw.githubusercontent.com/yjrszcq/checkpoint-karpathy-development/main/install.sh | bash -s -- --harness codex --scope user
```

自定义路径、项目级安装和其他 harness 见[安装选项](docs/guide_CN.md#安装)。

### 让 agent 帮你安装

将下面这段话发给 agent：

```text
请按照仓库中的 INSTALL.md，为我当前使用的 harness 安装这个技能：
https://github.com/yjrszcq/checkpoint-karpathy-development
```

也可以在请求中指定 harness、项目级安装或自定义安装路径。详细流程见 [Agent 安装说明](INSTALL.md)。

## 使用

安装后重启或重新加载 harness，然后提出目标：

```text
使用 checkpoint-karpathy-development，帮我完成：<目标>
```

默认使用协作模式和 Conventional Commits，设置保存在 `config.yaml` 中。隐私模式下，规划文档不会进入 Git。目标文档统一放在固定的 `roadmap/` 目录中，分别记录总览、状态、上下文、里程碑、计划变更和执行历史。

## 文档

- [使用指南](docs/guide_CN.md)：配置、项目状态命令、线路图生命周期和临时文件管理。
- [Agent 安装说明](INSTALL.md)：安装路径、更新、备份和验证。
- [技能指令](SKILL.md)：agent 的工作流程及配套参考文档。
