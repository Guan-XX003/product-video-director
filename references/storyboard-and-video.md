# Storyboard and Video Prompt Compilation

Read this only after the required asset gate is satisfied, unless the user explicitly requests a provisional draft.

Load the selected profile from [style-profiles.md](style-profiles.md). Every shot and the master lock must express its concrete camera, lighting, performance, product-proof, environment, and sound behavior; the style enum alone is not a usable prompt.

Write the storyboard and final video prompts in Simplified Chinese. Preserve only necessary original product names, proper nouns, URLs, requested spoken-language text, and authentic App UI text.

## Shot Budget

Use duration as a constraint, not a reason to overload shots:

| Duration | Typical shot count |
|---|---:|
| 1-6 seconds | 2-4 |
| 7-15 seconds | 4-7 |
| 16-30 seconds | 7-12 |
| Over 30 seconds | Divide into coherent modules, then budget each module |

Adjust for dialogue, required demonstrations, and target-model limits. Do not invent provider limits. Each shot should have one primary visible action and one main commercial job. This does not limit the number of spoken turns: a continuous conversation can run through several actions or remain within one shot.

Shot counts are not scene counts. Keep the brief's distinct-location budget and fixed featured cast; background people do not consume cast slots. For UGC and dialogue, use fewer cuts if that preserves a complete natural exchange. Verify who operates the camera, where the hardware sits, and whether the performer can handle it while speaking. A required hardware display must map to at least one `hardware_visible: true` shot and a plausible installation/use position.

Before compiling the final prompt, run the spoken-line naturalness pass in [performance-and-atmosphere.md](performance-and-atmosphere.md) on dialogue and explicitly requested spoken copy only. Recheck speaking time, listener reaction, and verified-claim mapping after any wording change. Leave visual, reference, timing, camera, and audio-policy instructions intact.

For dialogue-led or UGC work, write a small conversation arc before assigning lines to shots: situation or friction → question/observation → product introduced through action → visible result or response. Do not use the shot list as a dialogue template. Avoid one short line per shot, long pauses between turns, and two people reciting isolated features. Keep the spoken exchange long enough to sound like a real interaction while fitting the requested duration; the product should be brought up by the situation or another person's reaction.

For UGC with people, use a continuous first-person voice or connected exchange as the default dialogue plan. Carry the spoken passage across the main human-led shots and attach a line to every featured-person shot. Reserve silent shots for product-only proof or an explicitly recorded `silent_beat_reason`; do not let an arbitrary cut create a silent gap in the middle of a spoken thought.

Keep the approved spoken passage intact when assigning shots: preserve everyday verbs, referents, and connective phrasing. Cuts may divide a sentence or isolate a natural short reply; judge completeness across the full conversation rather than requiring a long sentence per shot. Apply the everyday-wording rules in [performance-and-atmosphere.md](performance-and-atmosphere.md).

## Advertising Structure

Unless the brief demands another structure:

- show the product, its effect, or a directly relevant visual question within the first three seconds
- map every selling point to visible evidence, not adjectives alone
- make the product causal to the story rather than a decorative insert
- end with a stable product or result image and reserve accurate logo, slogan, price, and legal text for post-production when needed

Do not duplicate the same demonstration merely to fill duration.

## Shot Record

Every `SHOT-*` entry includes:

- start and end seconds
- commercial job
- approved asset references
- frame and composition
- subject starting state
- one primary action with body part or subject, direction, speed or force
- explicit completion state
- `featured_person`: whether a person is the featured subject in this shot
- when `featured_person` is true, a performance block containing expression, gaze, micro-movement, body language, and `subtle`, `restrained`, or `moderate` intensity
- camera behavior
- environment atmosphere containing one concise visual summary and ambient sound
- scene atmosphere summaries preserve the approved normal environmental state, including context-appropriate occupancy, background activity, and lived-in traces
- ordered dialogue turns with speaker, exact line, speaking tone, and listener reaction; use an empty list when nobody speaks. Multiple connected turns may appear in one shot.
- for speaking shots, `action_speech_relation`: the action performed during the line, or a justified sequential action such as swallowing before speaking; compile this relation into the prompt
- `hardware_visible` when hardware visibility is planned; only `true` when the named device is actually visible, not merely mentioned
- for UGC with people, `dialogue` is non-empty on every featured-person shot by default; a silent featured-person beat requires `silent_beat_reason`
- transition and next-shot handoff
- selling points proved by the shot

Every shot's `selling_points` must be a subset of `brief.selling_points`, itself inside the verified whitelist. Check words and visuals for implied out-of-whitelist capabilities as well; string validation cannot catch a visual claim or a paraphrase.

The first shot starts at `0`. Shots cover the requested duration without gaps or overlaps. The final shot ends at the requested duration.

Read [performance-and-atmosphere.md](performance-and-atmosphere.md) for the performance block, environmental fields, realistic motion, and low-amplitude acting rules.

```json
{
  "id": "SHOT-001",
  "start": 0,
  "end": 3,
  "featured_person": true,
  "performance": {
    "expression": "眼神放松，嘴角轻微上扬",
    "gaze": "视线从前方落到产品上",
    "micro_movement": "自然眨眼一次，呼吸带动肩部轻微起伏",
    "body_language": "肩膀放松，手腕自然",
    "intensity": "subtle"
  },
  "action": "右手手指依次收拢，缓慢握住产品",
  "completion_state": "产品稳定停在胸前",
  "action_speech_relation": "人物拿起产品时以正常聊天语速说话，不等动作结束才开口",
  "hardware_visible": true,
  "environment_atmosphere": {
    "summary": "清晨安静的窗边场景",
    "ambient_sound": "低弱城市底噪与衣料摩擦声"
  },
  "dialogue": [
    {
      "speaker": "跑者",
      "line": "这杯水先帮我拿一下。",
      "tone": "正常聊天语速、放松",
      "reaction": "同伴先看向她手中的杯子，轻轻点头一次，嘴角略微上扬"
    }
  ],
  "camera": "中景平稳推近",
  "asset_refs": ["PROD-01", "CHAR-01", "SCENE-01"],
  "selling_points": ["已验证卖点"]
}
```

For a product-only shot, set `featured_person` to `false`, omit `performance`, and use `dialogue: []`; keep `action`, `completion_state`, `environment_atmosphere.summary`, and `environment_atmosphere.ambient_sound`.

## Storyboard Contact Sheet

The storyboard image prompt should specify:

- exact panel count and reading order
- one panel for each planned shot or selected keyframe
- approved product, character, and scene references and their responsibilities
- consistent aspect ratio inside panels
- no panel numbers, captions, timecodes, arrows, or layout labels inside generated imagery unless the user explicitly requests them
- stable identity, costume, product geometry, scene geography, and light direction

Keep the shot table outside the generated image. If the image tool is available, generate the contact sheet only from approved assets and inspect it before delivery.

## Video Prompt Package

Create a master lock followed by per-shot prompts.

The master lock contains:

- approved product geometry and material invariants
- approved character identity and costume invariants
- approved scene geometry and lighting invariants
- aspect ratio, duration, selected built-in style, and its concrete overall visual language
- text, logo, anatomy, duplication, and deformation exclusions relevant to the brief
- no added subtitles, captions, titles, stickers, or explanatory text; preserve approved app UI text
- no music; audio contains only environment sound and visible-character dialogue

Each per-shot prompt contains:

1. shot ID and time range
2. asset references and what each controls
3. visible starting frame
4. one concise atmosphere phrase and environment sound
5. for a featured person: gaze, micro-expression, involuntary micro-movement, and body language
6. primary action and physical interaction
7. exact completion state for continuation
8. camera movement
9. the complete dialogue sequence for the shot when present, including exact lines, speaking tone, natural turn-taking, and listener reactions

Default to Doubao Seedance 2.0 when the user has not named a target model, and compile with [seedance-2.0.md](seedance-2.0.md). For an explicitly requested alternate model, adapt the package only from reliable capability information; if its limits are unknown, keep the shot prompts model-agnostic. Do not silently change the requested duration or split strategy.

For Doubao Seedance 2.0, keep this project-level timed shot plan as the production specification, but compile the submitted model prompt with sequential `镜头1`, `镜头2`, and `镜头3` sections rather than per-shot timestamp ranges. The official guidance notes that precise time instructions are unstable. Read [seedance-2.0.md](seedance-2.0.md) for material binding, subject labels, action, camera, audio, and constraint syntax.

## Revision Semantics

- Timing-only changes preserve assets but require storyboard and video-prompt validation.
- A new selling point requires remapping shot evidence.
- Character identity, product geometry, costume, scene geography, or lighting-baseline changes invalidate every affected downstream shot.
- Preserve stable IDs for unchanged assets and shots.
