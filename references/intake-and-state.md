# Intake, State, and Creative Randomization

## Intake Contract

Before product research, inspect the current conversation and existing project artifacts. If the same product research was already completed and the user confirmed it, reuse the recorded identity, sources, visual references, scenarios, and claims. Do not repeat the search or ask for those details again. Research only missing, conflicting, changed, or explicitly requested current information. Research supplies evidence-backed candidate selling points and real usage scenarios; it does not replace campaign choices. The final brief still requires product name, selected selling points, people, selected scene, duration, and one confirmed built-in creative style. Accept natural-language answers; do not force a questionnaire format.

After research, ask only for unresolved identity or campaign information. Offer researched selling points and scene options instead of asking the user to recall facts the agent can verify. A suitable combined question is:

```text
我查到了两项有依据的产品卖点和三个常见使用场景。你希望突出哪些卖点、选择哪个场景、由谁出镜（可以回答“无人物”），视频要多少秒？
```

Once those prerequisite fields are known, ask a separate concise style question unless the user already chose one explicitly:

```text
你更偏向哪种成片风格：1）UGC 原生 vlog；2）高规格质感商业片；3）剧情对话短剧；4）动画介绍（皮克斯式三维角色、定格或 MG 图形动画）？
```

Store exactly one of `ugc_native_vlog`, `premium_commercial`, `dialogue_drama`, or `animation_explainer`. Animation also requires `brief.animation_style`: `stylized_3d`, `stop_motion`, or `motion_graphics`; omit it otherwise. Copy both values into the selected creative and Seedance package. Do not choose on the user's behalf or proceed to creative randomization before the selection is confirmed. A directly named animation subtype resolves both choices. Count animated performers as actors; MG defaults to no actors if none were requested, and its scene may be an abstract canvas.

Useful optional fields include aspect ratio, audience, channel, voiceover, CTA, slogan, and reference media. Default them conservatively and surface the assumptions. If the user does not name a video model, record `brief.target_model` as `doubao-seedance-2.0`; this is the default prompt target, not a question for the user or authorization to generate a video. Preserve a different model when explicitly requested.

For UGC with people, use `brief.dialogue_mode: "continuous_spoken"` unless the user explicitly requests sparse dialogue or silent visual moments. The other values are `mixed` and `visual_only`. Do not ask a new question for this field by default; infer `continuous_spoken` for ordinary UGC and record an explicit user exception when needed.

Do not invent quantitative product performance, certifications, prices, medical effects, endorsements, or legal claims. Preserve uncertain claims as unresolved rather than converting them into advertising facts.

## Project State

### Production controls

For new work record these controls alongside the existing brief; infer them from confirmed context instead of adding a mandatory questionnaire. They are additive to version 8, so older projects remain readable; fill only the controls needed for the current revision without resetting approvals or redoing research.

- `core_function_whitelist`: non-empty list of exact verified research claim strings permitted in this campaign. A whitelist limits claims; it does not itself verify them. `selling_points` is the subset actually demonstrated in this video.
- `primary_claim`: exactly one selected selling point for a short ad. If several were supplied without priority, recommend one in the candidate summaries for user selection; do not quietly discard the others or fabricate adjacent capabilities. Supporting claims must serve the same story rather than become separate demonstrations.
- `actor_count`: non-negative integer for featured cast, not background passengers or pedestrians. Infer from `people`; zero means no featured people. Lock identities and roles (e.g. main selfie speaker and companion), and identify who holds the camera. A lone selfie speaker cannot hold a phone, operate another device with both hands, and film an external view simultaneously.
- `scene_count`: positive integer counting distinct physical locations, not cuts, reverse angles, or three views of one space. Recommend one location for a 15-second conversation, optionally two when a transition is justified; 30 seconds may suit two or three. These are planning suggestions, not model limits. Preserve an explicit user count or flag a timing conflict.
- `hardware_display_required`: `auto`, `required`, or `not_required`. Applies to the named `hardware_device` (physical product, host device, or phone), not to all props. `not_required` means optional, not forbidden. For `auto`, resolve necessity from the selected demonstration and record it in `hardware_display_reason`; if required, identify a shot showing the device in its real installation/use position. An App does not need a UI close-up merely to say its name; exact UI demonstrations still require authentic references.
- `creative_candidate_count`: normally 3; 1 when a direction is already supplied or the user asks for direct selection. This counts short proposals, not full scripts or separately generated asset sets. Record the actual number offered, which may be 2 if only two distinct directions fit.

Do not copy website defaults blindly: no mandatory three locations, multi-view character boards, external API dependency, or Seedance 2.5 default.

Use this shape for `product-video-project.json`:

This example uses a single user-supplied direction. For new open-ended work, store two or three candidates and their selection before asset design instead.

```json
{
  "version": 8,
  "output_policy": {
    "prompt_language": "zh-CN",
    "subtitles": "none",
    "music": "none",
    "allowed_audio": ["ambient_sound", "dialogue"],
    "app_ui_prompt_detail": "state_only"
  },
  "research": {
    "status": "complete",
    "product_kind": "physical_product",
    "canonical_name": "Example Bottle Model X",
    "model_or_version": "Model X / CN",
    "sources": [
      {
        "url": "https://example.com/model-x",
        "title": "Official Model X page",
        "publisher": "Example",
        "source_type": "official_product_page",
        "accessed_on": "2026-09-21"
      }
    ],
    "visual_references": [
      {
        "url": "https://example.com/model-x-front.jpg",
        "source_url": "https://example.com/model-x",
        "kind": "product_photo",
        "view_or_screen": "front three-quarter"
      }
    ],
    "usage_scenarios": [
      {
        "scenario": "Cold drinks during outdoor exercise",
        "evidence_source_urls": ["https://example.com/model-x"]
      }
    ],
    "selling_points": [
      {
        "claim": "保持饮品低温",
        "status": "verified",
        "evidence_source_urls": ["https://example.com/model-x"]
      }
    ],
    "unresolved": []
  },
  "brief": {
    "product_name": "Example product",
    "selling_points": ["保持饮品低温"],
    "core_function_whitelist": ["保持饮品低温"],
    "primary_claim": "保持饮品低温",
    "people": "One adult commuter",
    "actor_count": 1,
    "scene": "Rainy evening subway entrance",
    "scene_count": 1,
    "hardware_device": "保温杯",
    "hardware_display_required": "required",
    "hardware_display_reason": "通过拿起杯子饮用后的反应呈现主卖点",
    "creative_candidate_count": 1,
    "duration_seconds": 15,
    "creative_style": "ugc_native_vlog",
    "aspect_ratio": "9:16",
    "target_platform": null,
    "target_model": "doubao-seedance-2.0",
    "dialogue_mode": "continuous_spoken"
  },
  "creative": {
    "style_profile": "ugc_native_vlog",
    "seed": 12345,
    "concept_id": "PVC-00003039",
    "narrative_pattern": "problem_to_proof",
    "hook": "interrupted_routine",
    "hook_mode": "random",
    "hook_opening": null,
    "hook_first_line": null,
    "hook_payoff": null,
    "camera_language": "phone_handheld_observational",
    "scene_progression": "single_space_escalation",
    "ending": "human_payoff_then_product",
    "selected_candidate_id": null
  },
  "creative_candidates": [],
  "capabilities": {
    "image_generation": "available",
    "video_generation": "unknown"
  },
  "assets": [
    {
      "id": "PROD-01",
      "type": "product",
      "status": "draft",
      "prompt": "依据真实产品照片生成产品多视图参考板，保持外形、材质和颜色一致。",
      "image_refs": []
    },
    {
      "id": "CHAR-01",
      "type": "character",
      "status": "draft",
      "prompt": "生成一张只包含该人物的完整参考图，同一画面清晰呈现面部、自然体态、发型和全套服装，不分拆面部与身体，不做多视图拼贴。",
      "image_refs": []
    },
    {
      "id": "SCENE-01",
      "type": "scene",
      "status": "draft",
      "prompt": "生成同一真实场景的主视、反向和侧向参考，呈现墙面、地面、固定设施、日常物件、正常人流和使用痕迹，使用现场自然光或普通实用灯光，保持空间结构与光线一致，不要电影光效、摄影棚布景或刻意摆拍。",
      "image_refs": [],
      "normal_state": {
        "contextual_occupancy": "少量正常通行的乘客与行人",
        "lived_in_traces": "背包、扶手及日常使用痕迹",
        "ambient_activity": "背景人物自然候车或经过",
        "exception_reason": null
      }
    }
  ],
  "gates": {
    "intake_complete": true,
    "style_confirmed": true,
    "assets_approved": false,
    "storyboard_ready": false,
    "video_prompts_ready": false,
    "pre_confirmation_audit": false,
    "video_prompts_confirmed": false,
    "storyboard_rendered": false,
    "delivery_ready": false
  },
  "delivery": {
    "audit_status": "pending",
    "render_status": "partial",
    "folder_name": "product-video-delivery",
    "files": []
  },
  "shots": []
}
```

See [product-research.md](product-research.md) for evidence rules and app UI handling.

If the user explicitly chooses no people, omit `CHAR-01` and store a clear no-people value in `brief.people`.

## Controlled Randomization

Before assets, present each candidate in two or three Chinese sentences: the Hook's opening situation and first action, how the selected primary claim is demonstrated, and the natural dialogue/camera approach. Keep cast identities and product truth fixed; candidates must differ in narrative or demonstration rather than clothing/color alone. Store proposals in `creative_candidates` with unique `concept_id`, `seed`, `primary_claim`, `hook`, `hook_mode`, `hook_opening`, `hook_first_line` when spoken, `hook_payoff`, and `summary`; copy the selected ID and its parameters into `creative`. When multiple candidates exist, wait for selection before generating their assets. A user-supplied direction or explicit permission to choose directly skips this extra question. For revisions, keep the selected direction and Hook unless the user requests alternatives.

Randomize direction, not product facts. Preserve the user's product, selling points, people, scene, duration, references, restrictions, and brand requirements.

When shell execution is available, run:

```bash
python3 scripts/randomize_concept.py --product "PRODUCT" --duration 15 --style ugc_native_vlog
```

Use `--seed` to reproduce or deliberately reroll a direction. Store the returned seed and selections in project state.

Read [hook-library.md](hook-library.md) before preparing openings. `--hook random` is the default; `--hook result_before_cause` fixes an explicit choice. Use `--eligible-hooks result_before_cause in_use_observation` after checking product evidence, location, speech needs, and duration. The helper rejects a fixed Hook outside the allowed pool, filters actor requirements, and favors different Hooks across random candidates. It returns Chinese `hook_label` plus `hook_mode`; the agent writes the actual Chinese opening and payoff. Keep the same arguments, including the shortlist and fixed Hook, when replaying a returned seed.

Store each proposed opening's `hook`, `hook_mode`, `hook_opening`, `hook_first_line` when spoken, and `hook_payoff` alongside its existing candidate fields; copy them into `creative` when selected. An explicit Hook stays fixed across candidates. With no preference, show different eligible openings in the existing candidate choice; do not ask an extra required Hook question. Reuse approved Hooks on revisions unless the user requests a change.

Use `--count 3` for a reproducible candidate batch, `--actor-count 1` to avoid companion-only strategies for a solo cast, or `--actor-count 0` for no featured cast. The helper proposes axes, not finished scripts; translate them into Chinese and reconcile each against the whitelist, scene budget, hardware policy, and confirmed brief before presenting it.

Pass the confirmed cast count explicitly. The helper defaults to two actors for dialogue drama and one otherwise. Its dialogue-drama pool requires two visible speakers; reconcile an incompatible brief instead of silently adding a person. Use `--scene-count` for distinct locations. These are helper rules, not model limits. A returned seed reproduces a candidate with the same arguments; review semantic diversity after writing the Chinese summaries.

The `--style` value is required and limits the random pools to the chosen profile. Read [style-profiles.md](style-profiles.md) and translate the chosen profile into concrete downstream instructions.

For animation use `--style animation_explainer --animation-style stylized_3d` (or `stop_motion` / `motion_graphics`). Subtype is required only for animation. MG defaults to zero actors; other animation subtypes default to one, unless the brief says otherwise. Pass confirmed counts explicitly. Each subtype has its own Hook/camera pools and is preserved on replay. For abstract MG, `scene_count` counts independent canvases.

The random axes are:

- narrative pattern
- Hook mechanism
- camera language
- scene progression
- ending structure

Reject combinations that contradict the brief. For example, do not choose a multi-location journey when the user requires a single tabletop scene. Make the smallest necessary substitution and record it as an override.

Before asset approval, a reroll may replace the creative direction. After approval, explain which assets and downstream work the reroll would invalidate.
