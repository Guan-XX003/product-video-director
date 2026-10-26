# Doubao Seedance 2.0 Adapter

Use this adapter only when the selected target is Doubao Seedance 2.0. It compiles approved project assets and the exact timed storyboard into a concise model-facing prompt. The external storyboard remains the timing authority; the submitted prompt emphasizes event order because the official guide states that precise time ranges can behave unpredictably.

## Choose the Task Type

- `full_modal_reference`: create a new video while reusing selected subjects, scene, action, camera, style, or sound from reference media. This is the normal product-ad route.
- `edit`: modify an existing video. Address `视频N` directly, for example `严格编辑视频1`; do not say `参考视频1`, which may route the task as reference generation.
- `extend`: continue an existing video forward or backward. Address `视频N` directly.
- `combined`: reference one asset while editing another, such as `参考图片1中的产品外观，严格编辑视频1...`.

Do not mix these task forms accidentally.

## Compile the Runtime Manifest

Internal IDs organize the project but are not valid Seedance references. Translate them into ordered runtime slots and show the upload order separately from the prompt.

Each manifest item contains:

- `slot`: `图片1`, `图片2`, `视频1`, or `音频1`
- `asset_id`: internal source ID, kept outside the submitted prompt
- `role`: one responsibility such as `product_identity`, `person_identity`, `scene`, `storyboard_composition`, `motion`, `camera`, `effect`, `environment_sound`, or `voice`
- `format`: `product_multiview`, `app_ui`, `single_person`, `single_scene`, `storyboard`, `video`, or `audio`
- `priority`: positive integer; smaller numbers are introduced earlier

The delivery package also records:

- `creative_style`: the confirmed `ugc_native_vlog`, `premium_commercial`, `dialogue_drama`, or `animation_explainer` profile for product-ad generation tasks
- `animation_style`: required only for `animation_explainer`: `stylized_3d`, `stop_motion`, or `motion_graphics`
- `dialogue_mode`: `continuous_spoken` by default for UGC with people; use `mixed` or `visual_only` only when the brief explicitly allows sparse or silent visual beats
- `prompt_language`: `zh-CN`; the submitted prompt is Simplified Chinese except necessary original product, brand, proper-noun, URL, voice/language, or authentic App UI text
- `person_reference_mode`: `none` or `single_image`
- `audio_policy`: no music, no generated subtitles, and only `ambient_sound` plus `dialogue`
- `app_ui_prompt_detail`: `state_only`
- `app_ui_references`: for each `app_ui` slot, only `slot`, `screen_state`, and `interaction`; do not add layout-detail fields
- `subjects`: stable labels with their bound runtime slots
- `shots`: ordered `镜头N` records, each with at most one `camera_movements` entry, one concrete `action`, a `completion_state`, `environment_atmosphere`, and conditional restrained-person performance fields

Carry each speaking shot's `action_speech_relation` from the project into the structured package and actual Chinese prompt. State that action and speech happen together when physically feasible; a list of action followed by dialogue can otherwise be interpreted as sequential. Preserve the verified claim whitelist and chosen primary claim during compilation; do not add adjacent functions to make dialogue longer. Cast count, location count, and hardware choices stay in the production state and audit; do not dump internal parameter fields into the model prompt.

For `full_modal_reference` and `combined` product-ad tasks, include either a physical-product `product_multiview` reference or an `app_ui` reference. A pure `edit` or `extend` task may legitimately use only `视频N`, so do not invent a product image requirement for those routes. Structured `shots` are required for `full_modal_reference`; they are optional for direct edit or extension instructions.

Use the smallest functional set. Three or four total references is a practical target, not a quota. Too many references create priority conflicts.

For animation, include the chosen `animation_style` in the package and use its material/canvas rules from [animation-profiles.md](animation-profiles.md). A stylized character still uses one `single_person` image per character; MG may use `person_reference_mode: none` and an abstract scene canvas when no character is requested.

Typical 15-second configurations:

```text
Product-only:
图片1 product multiview
图片2 scene master
图片3 storyboard contact sheet
optional 视频1 for a critical motion/camera/effect OR 音频1 for a critical environment sound

Product with a recurring visible person:
图片1 single image of the complete person, with face and outfit visible together
图片2 product multiview
图片3 scene master or storyboard contact sheet
optional 视频1 for motion/effect or 音频1 for a dialogue voice reference only when it adds essential control
```

Create and submit exactly one image per featured person. Never split a person's face and body across images or submit a character turnaround or multi-view board. If several people appear, keep one stable label and one image slot per person; prioritize the references actually used by the shot plan.

## Define Subjects

Define each subject with two or three stable visual features and bind its single person image:

```text
将图片1中黑色短发、灰色运动外套的年轻女性定义为跑者。
将图片2中的银色圆柱形保温杯定义为产品。
```

Use the same label every time afterward: `跑者`, `产品`. If a simple subject is not defined in advance, mention it as `产品@图片2`. Do not replace `图片N` with an internal Asset ID.

Place the references that need the highest identity fidelity early in the subject-definition block. Keep descriptions concise and non-conflicting. Prefer reference images to long prose for complex spatial relations.

When a scene reference is used, preserve its approved normal state and real-location details in the prompt with one concise phrase, for example `图片3中的真实通勤街景，能看到路面磨损、站牌、自然经过的行人和低强度车流，使用现场普通日光，不要电影光效或摄影棚布景`. Keep background people generic and subordinate. Do not turn them into named subjects or remove ordinary lived-in traces from homes, transit, workplaces, cafes, or public streets.

## Structured Package Example

```json
{
  "target": "doubao-seedance-2.0",
  "task_type": "full_modal_reference",
  "duration_seconds": 15,
  "creative_style": "ugc_native_vlog",
  "prompt_language": "zh-CN",
  "person_reference_mode": "single_image",
  "audio_policy": {
    "music": "none",
    "subtitles": "none",
    "allowed_audio": ["ambient_sound", "dialogue"]
  },
  "app_ui_prompt_detail": "state_only",
  "manifest": [
    {"slot": "图片1", "asset_id": "CHAR-01", "role": "person_identity", "format": "single_person", "priority": 1},
    {"slot": "图片2", "asset_id": "PROD-01", "role": "product_identity", "format": "product_multiview", "priority": 2},
    {"slot": "图片3", "asset_id": "SCENE-01", "role": "scene", "format": "single_scene", "priority": 3}
  ],
  "subjects": [
    {"label": "跑者", "kind": "person", "slots": ["图片1"]},
    {"label": "产品", "kind": "product", "slots": ["图片2"]}
  ],
  "shots": [
    {
      "label": "镜头1",
      "featured_person": true,
      "camera_movements": ["中景平稳推近"],
      "performance": {
        "expression": "眼神放松，嘴角轻微上扬",
        "gaze": "视线先落在产品上",
        "micro_movement": "自然眨眼一次，呼吸带动肩部轻微起伏",
        "body_language": "肩膀放松，手腕保持自然",
        "intensity": "subtle"
      },
      "action": "跑者右手手指缓慢收拢握住产品",
      "completion_state": "产品稳定停在胸前",
      "environment_atmosphere": {
        "summary": "清晨安静的窗边场景",
        "ambient_sound": "低弱城市底噪和衣料摩擦声"
      },
      "action_speech_relation": "跑者拿起杯子时同步以正常聊天语速说话",
      "dialogue": [{"speaker": "跑者", "line": "我先把这杯水放在这里，等会儿回来再喝。", "tone": "正常聊天语速、放松", "reaction": "无听者，面向镜头"}]
    },
    {
      "label": "镜头2",
      "featured_person": false,
      "camera_movements": ["镜头切至产品特写"],
      "action": "产品表面缓慢凝结细小水珠",
      "completion_state": "水珠稳定挂在产品表面",
      "environment_atmosphere": {
        "summary": "安静克制的产品特写",
        "ambient_sound": "克制的环境底噪"
      },
      "dialogue": []
    }
  ],
  "prompt": "将图片1中的女性定义为跑者，将图片2中的保温杯定义为产品，场景参考图片3……"
}
```

## Compile the 15-Second Prompt

Use this order:

```text
[Reference and subject definitions]

镜头1：[one camera or cut instruction] + [subject action/expression] + [position or scene change] + [audio]
镜头2：...
镜头3：...
...

[Global quality and visual style]
[Global audio direction]
[Relevant constraints]
```

Do not copy the full production brief into the prompt. Usually four to seven ordered shots are enough for a 15-second product ad. Do not include per-shot forms such as `0-3秒` or `00:00-00:03`; keep those in `storyboard.md`.

Compile the selected built-in profile into concrete global and per-shot instructions from [style-profiles.md](style-profiles.md). Do not submit only `UGC`, `商业片`, `短剧`, or the internal enum as a style label.

For every shot:

1. Start with one camera movement or a cut, such as `中景平稳推近`, `固定机位`, or `镜头切至产品特写`.
2. Establish the scene with one concise atmosphere phrase and the relevant environment sound. Do not give the environment the same descriptive density as the person.
3. If a person is featured, state gaze, observable micro-expression, one subtle involuntary movement, and body language. Use details such as `视线落在杯盖上`, `嘴角轻微上扬`, `自然眨眼一次`, and `肩膀随呼气逐渐放松`.
4. State the subject action using body parts, direction, speed or force, physical contact, and a visible completion state.
5. When characters speak, include the complete ordered dialogue sequence for that shot, with exact lines, speaking tone, natural turn-taking, and the listener's immediate visible reaction. State the spatial relationship or transition to the next action. Do not force one short line into each `镜头N` section or add a long pause after every line. Keep the exchange conversational and let the product enter through the situation, a question, a visible use, or a response to the result.

Prefer low-amplitude, continuous actions. Show the inertia between actions: `借着转身惯性顺势抬手`. Replace abstract emotions with visible details. Default performance intensity to `subtle` or `restrained`; use `moderate` only when needed for readability. Avoid exaggerated smiles, grimaces, large waving, repeated nodding, abrupt head turns, full-body bouncing, and stacked emotional beats. Give every shot a readable completion state. Use no more than one camera movement in a shot. Read [performance-and-atmosphere.md](performance-and-atmosphere.md) for the shared performance rules.

## Audio, Dialogue, and Text Policy

The default output contains no music and no generated on-screen subtitles. Audio is limited to diegetic environment sound and visible-character dialogue. Encode the allowed layers as follows:

- environment sound: `<杯盖轻响与低弱室内底噪>`
- dialogue with tone and reaction: `跑者用正常聊天语速、放松的语气说{这杯水先帮我拿一下，我把外套穿上。}，同伴看向杯子，伸手接住时自然回应{好，你慢慢来。}`

Keep the generated prompt in Simplified Chinese. Dialogue should be Chinese by default unless the user explicitly requests another spoken language; preserve necessary proper nouns and authentic App UI text as-is. When a reference voice is used, add both the audio slot and a compact Chinese voice-quality description. Do not add narration or voice-over unless the user later requests it.

Spoken delivery uses normal conversational pacing with only natural clause pauses and breathing. For UGC with people, carry a continuous first-person passage or connected exchange through the main human-led shots. Do not make characters speak unnaturally slowly, leave a long silent gap after every short line, or omit dialogue from a featured-person shot unless its `silent_beat_reason` is explicitly recorded.

Compile the approved everyday sentences verbatim into `{...}`; do not summarize them as keywords or slogans to shorten the prompt. Preserve links across cuts and responsive short replies. For speaking videos, add: `台词使用日常、连贯的口语，按正常聊天语速接续，句内只保留自然换气，不逐词停顿，不因切镜头重新起一句。` Exact wording, tone, and listener reaction remain aligned with the structured shots.

Every generated-video prompt must include these instructions:

```text
不要生成额外字幕、标题、贴纸或说明文字。不要添加背景音乐，仅保留环境音与人物对白。
```

If an approved app UI is visible, add `保留参考图中真实 App 界面的原有文字，不新增或改写界面内容`. Describe only the referenced screen or workflow state and the person's interaction. Do not enumerate layout, labels, controls, colors, typography, or icons.

## Constraints

Choose only relevant constraints and state them directly:

```text
画面高清，细节丰富，色彩自然，光影柔和，动作连贯自然。
人物表情和动作幅度克制自然，眼神、呼吸、手指和肩部只做细微连续变化，避免夸张表演。
人物面部和身体比例稳定，不变形，不闪烁，不穿模。
产品轮廓、材质、颜色和结构全程保持一致。
不要生成额外字幕、标题、贴纸或说明文字，不要生成水印。
不要添加背景音乐，仅保留环境音与人物对白。
视频全程禁止出现外形、着装、配饰完全一致的重复人物，禁止同款分身和双胞胎效果。
```

Keep exact logo, slogan, price, disclaimer, and campaign typography in post-production. If an exact effect matters, use a reference video that demonstrates the motion rather than relying only on prose.

## Output Package

Deliver:

1. upload-order manifest
2. subject-definition block
3. one copy-ready Seedance prompt
4. short execution notes for aspect ratio, duration, and post-production text

Validate the structured package with `scripts/validate_seedance_package.py` before delivery.
