# Changelog

## 2026-09-30 — 会话规则固化（本次更新）

### SKILL.md

- 新增 `## Generation Confirmation Gate`：**未经用户明确确认「资产」与「视频提示词」，禁止提交任何生成任务（含草稿/试跑）**。
  - 要求项目文件记录 `workflow_policy.render_requires_user_confirmation: true` 及已确认层；
  - 未确认前保持 `assets_approved` / `pre_confirmation_audit` / `video_prompts_confirmed` / `storyboard_rendered` / `delivery_ready` 为 false，且不得组装正式交付包；
  - 明确"用户说『做个视频』只是授权流程，不等于渲染确认"，不得把沉默、无关反馈或自己先前的判断当成用户确认。
- `## Capability Rules` 的 Video 条目补上该门前置条件。

### references/delivery-package.md

- `## Confirmation and storyboard gate` 补充：资产确认 + 提示词确认缺一不可；若提前跑过生成，须把产物标记为未确认过程文件、复位确认门、并改名过早组装的交付目录。

### 本版技能中已包含、与本会话结论一致的既有条款（核对无冲突）

- 人物参考：每个出镜人物**只出一张完整单图**（`single_person` / `person_reference_mode: single_image`），禁止 face-only、body-only、多视图拼版（`references/asset-design.md`）。
- 场景参考：使用空间一致的**三视角覆盖板**，运行时只提交一张主场景图（`references/asset-design.md`、`references/seedance-2.0.md`）。
- 对白：日常、连贯、成句，禁止广告词式短句堆叠；新增 `Everyday, connected wording` 与 `Spoken-line naturalness pass`，并配 `scripts/dialogue_quality.py` 检查器（`references/performance-and-atmosphere.md`）。
- App 类产品：`app_ui` 槽只描述屏幕状态与人物交互，界面必须来自真实截图。

### 下游项目迁移（本机工作区）

- `beebook-overseas-drama` / `beebook-ugc-vlog` / `mycar-vlog` 三套 Seedance 包由旧契约迁移到新契约：
  `person_reference_mode: body_only → single_image`，manifest 人物槽 `format: single_fullbody → single_person`，`role → person_identity`。
- 三个项目的分镜/提示词/素材文档同步改名；已确认的两个交付包（剧情片、vlog）重新组装并复验通过。
