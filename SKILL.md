---
name: product-video-director
description: Research a real product and turn the resulting brief into approved product, character, and scene assets, then a timed storyboard and production-ready AI video prompts. Use for product ads, TVCs, ecommerce videos, launch films, or branded shorts; verify official product visuals or app UI, usage scenarios, and selling points before designing assets.
---

# Product Video Director

Create a product-ad workflow whose visual decisions remain stable from the first asset board through the final video prompt.

## Intake And Research Gate

First inspect the current conversation and any existing project files for a completed product research record. If the exact product identity, research sources, visual references, usage scenarios, and selling points are already present and the user has confirmed or accepted them, reuse that context as the active source of truth. Do not search the product again or ask the user to repeat the information. Start new research only when the context is missing a required fact, contains a conflict, the user changes the model/region/app version, the user asks for an update or recheck, or the previous research is clearly stale for the requested claim. Read [references/product-research.md](references/product-research.md) for source priorities, evidence rules, and the research output.

When no reusable research record exists and the user's description identifies a recognizable product, start research immediately. Do not wait for the full campaign brief. Verify the exact product, official product imagery or current app UI, real usage scenarios, and supportable selling points before creative randomization or asset design.

Build the working brief from the user's message, attachments, and verified research:

- product name
- main selling points
- a `primary_claim` for this video, selected from the verified `core_function_whitelist`; supporting claims must stay inside this whitelist
- people appearing in the video; `no people` is a valid explicit answer
- scene or environment
- exact duration in seconds
- actor count and scene count when the user specifies them; otherwise infer a duration-appropriate count and record the assumption
- whether a physical product or device must be visibly shown; use `auto`, `required`, or `not_required`

For `ugc_native_vlog` with people, default to a continuous spoken track: a first-person experience, direct-to-camera explanation, or natural companion exchange should carry most of the human-led footage. Only use sparse or visual-only UGC when the user explicitly asks for it; record that choice as `brief.dialogue_mode`.

Research may supply candidate selling points and realistic scene options, but campaign emphasis, cast, and duration remain user choices. After using existing context or completing research, ask for all unresolved choices together in one short message and include concise research-backed options where useful. If search results do not uniquely identify the exact product, model, region, or app version, ask for that identity detail or an official URL before asset design. Do not ask again for information already supplied, verified, or confirmed in the current conversation.

## Precision And Speed Rules

Use a bounded research pass. For a clearly identified product, the minimum evidence pack is one authoritative identity source, one authentic product or App UI visual source, one real usage source, and evidence for each selected selling point. Stop researching once those requirements are satisfied and no conflict remains. Search independent source types in parallel when the available tools support it; do not browse broadly for background that will not affect the asset, dialogue, or shot plan.

Freeze confirmed layers. Once the user confirms product identity, selected claims, creative style, or approved assets, reuse them in later steps. A change to duration, platform, dialogue wording, or one scene detail should trigger a delta update to the affected storyboard or prompt layer rather than a full research or asset restart. Keep stable IDs and preserve unaffected files.

## Style Preference Gate

After the product identity, selling points, people, scene, and duration are known, ask which of these four built-in styles the user prefers unless they already selected one explicitly:

1. `ugc_native_vlog` — UGC 原生 vlog 风格
2. `premium_commercial` — 高规格质感商业片风格
3. `dialogue_drama` — 剧情对话短剧风格
4. `animation_explainer` — 动画介绍风格：皮克斯式三维角色 / 定格动画 / MG 图形动画

For animation, also record `brief.animation_style` as `stylized_3d`, `stop_motion`, or `motion_graphics`. A user's explicit subtype selects both levels without another question; if only animation was requested, resolve the subtype before designing assets. Read [references/animation-profiles.md](references/animation-profiles.md) for asset, scene, performance, and sound adaptations. Do not randomize between subtypes. Omit `animation_style` for the other three styles.

This is a required campaign choice, not an optional visual-style suggestion. Give one concise sentence explaining each option, record the selected enum in `brief.creative_style`, and do not randomize the creative direction or design assets until it is confirmed. If `dialogue_drama` conflicts with a no-people or otherwise dialogue-incompatible brief, ask the user to change either the cast choice or the style instead of silently weakening the preset. Read [references/style-profiles.md](references/style-profiles.md) after selection and apply only the chosen profile.

Treat aspect ratio, target audience, platform, voiceover, and user-supplied reference images as optional; recommend defaults instead of blocking unless one materially changes the requested result.

## Target Model Default

Unless the user names another video model, set `brief.target_model` to `doubao-seedance-2.0` at intake and design the asset and video-prompt path for Doubao Seedance 2.0. Do not ask the user to choose a model merely because they omitted it. If they explicitly select another model, use that target and its supported instructions; do not apply Seedance-specific slot syntax or claim its limits apply to the other model. The default selects a prompt format, not permission to submit a paid generation job.

For intake, project state, and controlled randomization, read [references/intake-and-state.md](references/intake-and-state.md). Read [references/hook-library.md](references/hook-library.md) when proposing or selecting an opening Hook.

## Workflow

1. Resolve the product identity through the context-reuse gate and complete only the bounded product research pass that is still needed.
2. Complete the campaign brief, clearly separating researched facts from user choices and assumptions.
3. Apply the target-model default or the user's explicit model choice, then complete the style preference gate and load the selected built-in profile.
4. Unless the user already supplied a direction or asked you to choose directly, offer three short creative candidates within the selected style (two if only two meaningfully different approaches fit). Use [references/hook-library.md](references/hook-library.md) to show concrete Chinese openings: default to controlled random Hooks, or keep the user's chosen Hook fixed. Include Hook selection in this existing candidate choice, without adding a mandatory question. Keep verified claims, cast, scene constraints, and duration fixed; vary eligible Hooks and demonstrations, not product facts. Ask the user to select one before designing assets. Preserve each seed and the selected direction; do not reopen an approved concept. See [references/intake-and-state.md](references/intake-and-state.md).
5. Produce three separate asset specifications:
   - product multi-view board
   - one complete reference image per featured person, unless the user explicitly chose no people
   - scene coverage board
6. Route by actual tool capability and render only the assets required by the selected shot plan:
   - With a callable image-generation tool, write each prompt first, then generate the boards when the current request authorizes generation.
   - Without one, immediately deliver copy-ready Simplified Chinese image-generation prompts for the required generatable assets. Do not make CLI setup, an API key, or a paid image provider a prerequisite. For an app, obtain authentic UI and App Store screenshots rather than asking an image model to invent them. Mark unrendered generated images `unavailable` with a reason in the delivery manifest.
   - Explore a CLI/API or paid image-generation route only if the user explicitly requests that alternative. Before any paid provider call, credential use, or external submission, show the exact job and obtain confirmation.
7. Present the prompts or rendered assets for explicit approval. Approval of prompts is sufficient to continue to the storyboard even when no image was rendered; keep later video prompts conditional on missing runtime images. Do not interpret silence or unrelated feedback as approval.
8. Only after asset approval, create the timed storyboard and shot plan from the approved asset IDs. For UGC with people, draft the complete spoken passage before assigning shots and ensure every featured-person shot has dialogue unless it has an explicit silent-beat reason. Before presenting it for confirmation, run the project validator and fix structural errors locally.
9. Review spoken lines for natural Chinese using the dialogue-only pass in [references/performance-and-atmosphere.md](references/performance-and-atmosphere.md), then compile the video prompts. Apply it to character dialogue and user-requested spoken copy, not to technical prompt instructions or verified product facts.
10. When the target is Doubao Seedance 2.0, compile the final prompt through [references/seedance-2.0.md](references/seedance-2.0.md) before asking for confirmation. Keep internal asset IDs in project files, but translate available references into ordered runtime slots such as `图片1`, `视频1`, and `音频1`. If a required runtime image has not been rendered, label the prompt as conditional on that image and do not claim it is ready to submit.
11. Before asking the user to confirm the video prompts, run the pre-confirmation completeness audit in [references/delivery-package.md](references/delivery-package.md). Check that each generatable image has either a useful approved reference or a usable Chinese image-generation prompt; verify authentic product/App evidence separately.
   Show the short audit summary defined in that reference, including claim boundaries, cast/scenes, physical feasibility, speech pacing, and missing references. Structural validation is not proof of natural dialogue or generated-video quality.
12. Ask the user to confirm the video prompts only after the completeness audit passes. Do not treat a draft or silence as confirmation.
13. After the user confirms the video prompts, generate the storyboard contact sheet from the approved assets and shot plan when image generation is available; otherwise provide the storyboard image prompt and mark the storyboard as not rendered.
14. Run the post-storyboard completeness audit, then assemble the final delivery folder using [references/delivery-package.md](references/delivery-package.md). Include all present prompts, approved references, generated storyboard images, and authentic App Store description screenshots for an app; record missing generatable images as prompt-ready in the manifest.
15. Run the quality checks and applicable validators before claiming completion. If a later revision changes only one layer, rerun the checks for that layer and its downstream dependencies instead of restarting the full workflow.

## Default Output Policy

- Write all generated asset prompts, storyboard prompts, video prompts, and copy-ready model prompts in Simplified Chinese. Do not deliver an English prompt or an English translation unless the user explicitly requests it.
- Keep only necessary original text unchanged: brand names, product/model names, URLs, proper nouns, voice/language requirements, and authentic text already visible inside an approved App UI screenshot. Do not use English for ordinary scene, action, camera, performance, sound, or constraint descriptions.
- Spoken copy uses everyday, connected sentences: keep the concrete situation, response, and product action understandable when read as one passage. Short acknowledgements may punctuate the conversation, but must not replace its substance. Apply the spoken-line naturalness pass before splitting or compiling dialogue.
- Add no generated subtitles, captions, titles, stickers, or explanatory text. When an approved real app UI is visible, preserve its existing interface text rather than erasing or rewriting it.
- Add no music. The only audio layers are diegetic environment sound and spoken character dialogue.
- Describe an app UI only by its approved screenshot reference, current screen or workflow state, and the person's interaction. Do not narrate its layout, controls, labels, colors, or hierarchy in detail.
- Keep environment, product, and UI wording concise. Reserve granular description for character expression, gaze, body action, speaking tone, and the other person's immediate dialogue reaction.
- Make asset environments feel normally occupied and used. Streets, public transport, and homes should contain context-appropriate people, background activity, and everyday traces unless the user explicitly requests an empty or controlled scene and the exception is recorded.
- Scene reference images must document a believable real location with concrete everyday details, available or ordinary practical light, and normal spatial clutter. Do not turn a scene reference into a cinematic set: no studio backdrops, staged prop dressing, dramatic movie lighting, artificial fog, decorative bokeh, or an unnaturally empty location unless the user explicitly requests that exception.

For an explicitly selected animation style, apply the material and abstract-canvas adaptations in [references/animation-profiles.md](references/animation-profiles.md). Real product evidence, one reference per character, and the no-subtitles/no-music policy still apply.

Read [references/asset-design.md](references/asset-design.md) when creating, generating, revising, or approving assets. Read [references/storyboard-and-video.md](references/storyboard-and-video.md) only after the asset gate is satisfied. When people appear, also read [references/performance-and-atmosphere.md](references/performance-and-atmosphere.md) and compile restrained micro-expressions, gaze, body mechanics, and environmental atmosphere into each relevant shot. Read [references/quality-control.md](references/quality-control.md) before final delivery or after any material revision.
Read [references/delivery-package.md](references/delivery-package.md) before video-prompt confirmation and again before packaging the final folder.

## Asset Gate

Asset states are `draft`, `rendered`, and `approved`.

- A prompt being written does not make an asset approved.
- A generated image being technically successful does not make it approved.
- Record approval only after the user explicitly accepts the asset prompts or generated boards.
- Formal storyboard and video prompts require the product, required character, and scene assets to be approved.
- A user may explicitly request a provisional storyboard; label it `draft` and do not call it production-ready.

If an approved identity, product geometry, costume, scene geometry, or lighting baseline changes, invalidate affected storyboard frames and video prompts instead of patching around the conflict.

## Generation Confirmation Gate

Never submit a generation job — image or video, including a draft, trial, or "quick test" run — until the user has explicitly confirmed both layers for that project:

- the **assets** (product, character, scene), and
- the **video prompts** (shot plan and compiled runtime prompt).

Record the intent in the project file as `workflow_policy.render_requires_user_confirmation: true` alongside the confirmed layers. Until both confirmations exist, keep `assets_approved`, `pre_confirmation_audit`, `video_prompts_confirmed`, `storyboard_rendered`, and `delivery_ready` false, do not assemble a release delivery folder, and label any earlier output as an unconfirmed process artifact rather than a deliverable.

A general request such as "make the video for this product" authorizes the workflow, not the render step. Ask for the two confirmations instead of inferring them, and never treat silence, unrelated feedback, or your own earlier approval of a layer as the user's confirmation.

## Capability Rules

Determine capabilities from tools actually exposed in the current environment. Never claim that image or video generation is available from model knowledge alone.

- Browser or search tool available: perform product research directly and preserve source URLs. Prefer official sources and inspect visuals rather than relying only on search snippets.
- No browser or search tool: ask for the official product URL and official images or current UI screenshots. Mark research as blocked and do not invent product facts or proceed to asset design.
- Native image tool available: generate asset boards or storyboard images as part of an authorized full workflow.
- No callable image-generation tool exposed: output usable Chinese image-generation prompts, clearly state that no image was rendered, and continue the prompt-first workflow after the user approves those prompts. Shell or CLI availability alone is not image-generation capability. Do not ask the user to configure a CLI, supply an API key, or authorize charges as a condition of continuing.
- Video tool available: do not submit video generation unless the user explicitly requests actual video generation and the Generation Confirmation Gate above is satisfied.
- For an explicitly selected alternate model whose limits are unknown, create model-agnostic shot prompts and avoid inventing duration, reference-count, resolution, or audio limits. The default target is Seedance 2.0; use its adapter without assuming access to its generation service.

## Deliverables

When filesystem access is available, maintain these artifacts in a project directory:

```text
product-video-project.json
research.md
assets.md
storyboard.md
video-prompts.md
```

Use stable IDs: `PROD-01`, `CHAR-01`, `SCENE-01`, `SHOT-001`, and `VID-001`. Keep prompts in the artifacts even when images are generated so the work is reproducible.

Run:

```bash
python3 scripts/validate_project.py path/to/product-video-project.json
```

After the user confirms the video prompts and the final audit passes, assemble the full image package or the clearly labeled partial prompt package with:

```bash
python3 scripts/assemble_delivery.py path/to/product-video-project.json path/to/prompt-and-image-files path/to/product-video-delivery
```

For a Seedance 2.0 delivery package, also run:

```bash
python3 scripts/validate_seedance_package.py path/to/seedance-package.json
```

Resolve validation errors before describing the package as production-ready.
