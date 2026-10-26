# Quality Control

Run these checks before final delivery and after material revisions.

## Style Gate

- The user explicitly selected exactly one built-in style after the prerequisite brief fields were known.
- `brief.creative_style` matches `ugc_native_vlog`, `premium_commercial`, `dialogue_drama`, or `animation_explainer`; animation has a valid `brief.animation_style`.
- Creative randomization, asset treatment, storyboard rhythm, performance, camera language, sound, and final prompts remain inside the selected profile.
- Prompts express concrete profile behavior instead of relying only on a style label.
- `dialogue_drama` is not used with a no-people or dialogue-incompatible brief. Animation subtype rules match the selected `stylized_3d`, `stop_motion`, or `motion_graphics` profile.

## Prompt Language

- `output_policy.prompt_language` is `zh-CN`.
- Asset, storyboard, and video prompts are written in Simplified Chinese.
- English is retained only when it is necessary original text: brand/product/model names, URLs, proper nouns, voice or language requirements, or authentic text visible in an approved App UI screenshot.
- Ordinary scene, action, camera, performance, sound, and constraint descriptions are not written in English.

## Target Model

- If the user did not specify a video model, `brief.target_model` is `doubao-seedance-2.0` and the final prompt uses the Seedance 2.0 adapter.
- An explicitly chosen alternate model is preserved; Seedance slot syntax and model-specific claims do not leak into its prompt.

## Delivery Completeness

- A pre-confirmation audit has checked every generatable image against a useful approved reference or a usable Chinese image-generation prompt.
- When no image-generation tool is exposed, complete Chinese asset prompts are delivered without CLI/API-key or paid-provider setup as a prerequisite; prompt approval permits the conditional storyboard/video-prompt path.
- No required prompt is missing; unavailable generated images have a corresponding present prompt and a reason.
- One complete character reference per featured person, product reference, scene reference, and storyboard image are present or explicitly marked unavailable with prompts when generation is unavailable.
- App projects include authentic App Store description/UI screenshots and a source URL; generated substitutes are not accepted.
- The user confirmed the video prompts before storyboard generation.
- The final delivery manifest lists every prompt, image, source, purpose, and approval state.
- A partial folder names the images still missing and is not described as ready for direct video submission.
- The final folder is assembled only after the post-storyboard audit and project validation pass.

## Brief and Claims

- Existing confirmed product research was reused when the current conversation or project files already contained the same product identity, sources, visual references, scenarios, and claims; repeated searches were limited to missing, conflicting, changed, or explicitly refreshed information.
- Research stops at the minimum evidence pack: authoritative identity, authentic visual evidence, real usage evidence, and traceable support for every selected selling point. Extra sources are added only to resolve a conflict or make a required creative decision.
- Product identity, model or version, and region are unambiguous.
- At least one first-party source and its access date are recorded.
- Physical-product visuals are authentic product photos; app visuals are current authentic UI screenshots for the identified platform/version.
- Usage scenarios have source evidence and are genuine product uses rather than decorative settings.
- All six required fields are explicit, including the confirmed creative style.
- Every selected selling point maps to a `verified` research claim. User claims and creative inferences are not presented as product facts.
- No invented statistics, certification, endorsement, price, efficacy, legal, medical, or financial claim appears.
- Duration and aspect ratio match the current brief.
- `primary_claim` is selected from `selling_points`; every selected and implied claim stays inside the verified `core_function_whitelist`. Unused whitelist entries need not be demonstrated.
- Candidate selection precedes new asset work; user-supplied or already approved directions are not reopened. Alternatives differ in narrative or demonstration, not merely colors.
- Actor count excludes background occupants; scene count excludes cuts and reverse angles. Camera handling and named hardware visibility are physically feasible for the cast and duration.

## Assets

For explicitly selected animation, apply [animation-profiles.md](animation-profiles.md) to these checks: stylized 3D/stop-motion preserve credible location/use details, while abstract MG uses its approved graphic canvas and documented `normal_state` exception. Do not reject MG for lacking real-world pedestrians or require human skin detail on designed characters. Product research evidence remains authentic.

- Runtime references are limited to the approved shot plan; approval boards are not rendered again as duplicate runtime images when standalone references already control the target model.
- Product geometry and UI details are anchored to the recorded visual references.
- App UI is not regenerated or redesigned; authentic screenshots are composited into devices when exact UI is needed.
- Product views show one geometry, not variants.
- Each featured person has exactly one image containing a legible face and complete body/styling in the same frame; no split face/body files, multi-view collage, or second image for the same identity.
- Animated characters follow the same one-character-one-image rule; the image defines the designed character's complete silhouette, face or head treatment, clothing/material, and identifying accessories.
- Scene views preserve geography, concrete real-world details, ordinary prop placement, time, weather, and normal location lighting. They do not become a cinematic set or a staged backdrop.
- Scene assets show a normal state for the place: contextual occupants, believable background activity, and ordinary lived-in traces. Empty or pristine scenes carry an explicit exception reason.
- Background people are generic, varied, naturally distributed, and subordinate; they are not accidental duplicate hero characters.
- Scene prompts name enough fixed fixtures, wear, objects, occupancy, and practical light to make the place inspectably real; they exclude dramatic movie lighting, artificial haze, decorative bokeh, and studio dressing unless an explicit exception is recorded.
- Each prompt remains stored even when an image was generated.
- Required assets are explicitly approved before production-ready downstream output.

## Storyboard

- Shot times begin at zero, have no gaps or overlaps, and end at the requested duration.
- Each shot has one primary action with direction and speed or force, plus a readable completion state.
- Every shot uses one concise atmosphere summary plus ambient sound; environment, product, and UI do not receive unnecessary granular description.
- Every featured-person shot defines gaze, observable micro-expression, subtle involuntary movement, body language, and `subtle`, `restrained`, or `moderate` intensity.
- Every dialogue turn defines the speaker, exact line, speaking tone, and the other person's immediate visible reaction.
- Read all spoken lines together: they use everyday connected thoughts, clear references, and responsive turn-taking. Short replies can remain, but keywords, praise, and acknowledgements do not constitute the whole passage. Do not fill a word quota or impose a sentence-length minimum per shot; the automated fragment check is only a coarse backstop.
- Spoken lines have passed a read-aloud naturalness check: no formulaic praise or feature recital, no invented first-person experience or unsupported claim, and words plus pauses fit the shot duration. Dialogue-only edits preserve technical instructions, reference slots, product facts, and the selected style; the structured line and compiled prompt agree.
- Dialogue-led and UGC spots contain a coherent exchange or connected spoken passage when speech is requested: the situation leads to a question, product use, observation, or visible result; turns respond to one another; dialogue is not reduced to one short line per shot with long gaps.
- UGC with people uses `continuous_spoken` by default: every featured-person shot has dialogue unless a documented user exception sets `dialogue_mode` to `mixed` or `visual_only`; product-only inserts may be silent when they provide visible proof.
- Human performance avoids exaggerated smiles, grimaces, large repeated gestures, abrupt pose changes, and multiple competing emotional beats.
- Every selling point has at least one shot containing visible proof.
- Speaking shots state how action and speech overlap, or why a short sequential beat is needed. Check normal speech duration rather than treating one short line as coverage of an entire shot; gesture restraint must not become artificially slow delivery.
- Product, performer, and scene references are assigned by responsibility.
- The first three seconds contain product relevance or a directly connected hook.
- The Hook respects the selected style, cast, available product evidence, speech mode, and scene; an explicitly chosen Hook stays fixed. Candidate openings are concrete Chinese actions/lines, and the promised payoff connects to a verified primary claim within the video. No unsupported contrast, fake urgency, exaggerated shock, or silent UGC prelude is introduced by randomization.
- The final shot provides a stable commercial closure.

## Video Prompts

- Static identity facts come from approved assets rather than being redesigned per shot.
- Physical actions have a plausible start, interaction, and end state.
- Person prompts contain the approved observable performance details, not only abstract emotion words.
- Expression, gaze, breathing, hands, posture, and product interaction form one continuous restrained beat.
- App prompts reference the approved UI screenshot and state only the screen/workflow state plus the person's interaction; they do not enumerate layout, controls, labels, colors, typography, or icons.
- Prompts explicitly forbid added subtitles, captions, titles, stickers, and explanatory text while preserving approved app UI text.
- Prompts explicitly forbid music. Audio contains only environment sound and visible-character dialogue.
- Camera movement does not conflict with the main action.
- Adjacent shots can continue from the preceding end state.
- Model capabilities and limits are not invented.
- Exact logos, small packaging text, prices, disclaimers, and dense typography are routed to post-production unless generation risk was explicitly accepted.

## Seedance 2.0 Delivery

- Internal IDs such as `PROD-01`, `CHAR-01`, `SCENE-01`, `SHOT-001`, and `VID-001` do not appear in the submitted prompt.
- Every submitted reference has an ordered runtime slot such as `图片1`, `视频1`, or `音频1`, and every slot has one explicit responsibility.
- Important identity references are introduced first. The material set is the smallest set that can do the job; usually three or four references, not the platform maximum.
- Each featured person has one reference image showing the face and body together, never separate face/body images or a multi-view collage.
- Subjects are defined once with stable labels, and every later mention uses the same label or an explicit label-to-slot binding.
- The submitted prompt uses ordered `镜头N` sections without exact per-shot timecodes. Exact seconds remain in the external storyboard.
- Each shot contains no more than one camera movement and favors a concrete, continuous action with body part, speed or force, transition, and visible completion.
- Featured-person shots preserve the structured gaze, micro-expression, micro-movement, body language, and restrained intensity in the submitted prompt.
- Product-only shots still include a concise atmosphere summary and ambient sound without inventing irrelevant human performance.
- The final prompt includes no music notation and no requested-subtitle notation.
- Dialogue language is consistent. Environment sound uses `<...>` and dialogue uses `{...}`; the prompt contains neither music instructions nor requested-subtitle notation.
- Constraints address unwanted subtitles or text, logos, watermarks, deformation, flicker, identity drift, and duplicate people as relevant to the brief.
- If a precise logo, slogan, or effect must be generated, it is supplied as a dedicated reference instead of described only in prose.

## State and Validation

Run `scripts/validate_project.py` before video-prompt confirmation and again after material revisions. For Seedance 2.0, also run `scripts/validate_seedance_package.py` before delivery. A clean validator result establishes structural consistency, not creative quality. Inspect generated images and use direct judgment for visual quality.

Do not silently repair an approved creative choice. Report the issue, identify the smallest affected layer, and request approval when the repair changes creative intent or consumes external resources.
