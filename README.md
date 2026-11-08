# Product Video Director · 产品视频创作 Skill

把“为一个产品做条视频”的需求，整理成有依据的产品研究、创意方向、人物与场景资产、分镜和可复制的中文 AI 视频提示词。

适合广告创意、产品介绍、电商短片和 App 推广的策划人员。它是给 Codex 等支持 `SKILL.md` 的 AI 助手使用的工作流，实际图片、视频生成能力由你使用的工具提供。

## 能做什么

- 先核实产品功能、官网图片或真实 App 界面，区分事实和创意假设。
- 支持 UGC 原生 vlog、商业广告、剧情对话、动画介绍四类方向；动画包含三维角色、定格和 MG 图形。
- 规划产品、人物和场景参考，保持资产与分镜的一致性。
- 编排时长、动作、自然对白、镜头和声音，默认输出简体中文提示词。
- 默认提供 Seedance 2.0 提示词适配，也可以按用户指定的模型组织内容。
- 用 Python 脚本检查项目结构、资产引用、对白与交付包。

## 安装到 Codex

需要 Git、支持 Skills 的 Codex。只有运行校验脚本才需要 Python 3.10+；Skill 本身无需安装 Python 包。

```bash
git clone https://github.com/Guan-XX003/product-video-director.git
mkdir -p "$HOME/.codex/skills/product-video-director"
cp -R product-video-director/SKILL.md product-video-director/references product-video-director/agents product-video-director/scripts "$HOME/.codex/skills/product-video-director/"
```

已有同名 Skill 时，请先备份已有版本。也可把同样的文件放到 `~/.agents/skills/product-video-director/`，按你的助手支持的发现目录选择一处安装。重新打开任务，使助手发现新 Skill。

## 第一次使用

在 Codex 中输入以下示例，并换成真实产品链接：

```text
$product-video-director
为【产品名称，官网链接】策划一条 15 秒的竖屏产品介绍视频。
目标人群是【目标用户】，主卖点是【已确认的功能】。
使用 UGC 原生 vlog 风格，1 人出镜，在家中自然演示。
先给我创意和资产提示词，实际生成图片或视频前等我确认。
```

建议提供：产品名称或官网、目标用户、主卖点、时长、是否有人出镜、风格偏好。没有搜索能力时，请提供可核实的官方资料和图片。

工作流程：产品核实 → 简报与风格 → 创意候选 → 资产方案确认 → 分镜与视频提示词 → 用户确认 → 按工具能力生成或交付提示词。

生成图片、视频前须按 [Skill 确认规则](SKILL.md#generation-confirmation-gate)取得用户确认；选择了视频模型并不代表已购买或开通该模型。

## 会得到哪些文件

| 文件 | 内容 |
|---|---|
| `research.md` | 产品事实与来源 |
| `assets.md` | 产品、人物和场景的资产说明与提示词 |
| `storyboard.md` | 按时长编排的镜头、动作和对白 |
| `video-prompts.md` | 可复制的视频提示词 |
| `product-video-project.json` | 供校验器读取的项目状态 |

具体字段与交付结构见 [完整工作流](SKILL.md)、[项目状态规范](references/intake-and-state.md)、[交付包说明](references/delivery-package.md)和 [Seedance 适配](references/seedance-2.0.md)。

## 校验与开发

从克隆的仓库目录执行：

```bash
cd product-video-director
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 scripts/validate_project.py --self-test
python3 scripts/validate_seedance_package.py --self-test
# 检查你自己的项目；路径需要替换
python3 scripts/validate_project.py /path/to/product-video-project.json
```

项目校验通过后，可以按 [交付规范](references/delivery-package.md)运行 `assemble_delivery.py`。脚本验证结构与引用，生成视频的真实观感仍需人工检查。

## 使用边界

默认不生成字幕、标题或背景音乐，保留环境声与人物对白；如果需要不同成片风格，请在简报中明确。产品、App UI 与营销主张须有真实依据。

仓库不包含模型权重、生成服务、API Key 或成片素材。没有可用生成工具时，可以先完成提示词与分镜，实际生成需另行配置工具。

遇到问题可提交 [Issue](https://github.com/Guan-XX003/product-video-director/issues)，说明助手版本、任务输入、预期与实际结果，并移除私密产品资料。

[变更记录](CHANGELOG.md) · [维护说明](MANAGEMENT.md)
