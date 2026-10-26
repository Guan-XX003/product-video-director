# Built-in Style Profiles

Load this reference only after the user selects a style. The selected profile constrains creative randomization, asset styling, storyboard rhythm, camera language, performance, sound, and the final video prompt. It does not override verified product appearance, authentic app UI, the approved normal environmental state, or the default no-subtitles/no-music policy. The three live-action styles use real location details and ordinary available/practical light; any polished commercial lighting belongs to later shot direction, not the location reference.

## UGC 原生 vlog 风格: `ugc_native_vlog`

- Visual point of view: believable phone-camera or compact-camera capture by the user, a friend, or a nearby observer; intimate distance and naturally imperfect framing.
- Camera: handheld but readable, small reframing and body-following drift, mostly eye-level or practical hand-held angles; avoid artificial shake, chaotic whip pans, and polished crane or impossible gimbal moves.
- Light and texture: available light or simple practical light, realistic exposure changes, natural skin texture, ordinary location color, no beauty-filter finish.
- Performance: spontaneous but restrained; conversational gaze, slight hesitation, natural breathing, small hand adjustments, and low-amplitude reactions. Direct-to-camera delivery is allowed when it fits the concept. By default, people-led footage carries a continuous spoken passage or connected companion exchange across most shots. Spoken delivery may be a connected passage with natural sentence length; do not reduce it to one short slogan per shot or leave human-led shots silent. Product-only inserts may be silent when they show a clear visual proof.
- Product proof: show the product being used in a recognizable real routine. Favor tactile, first-person, over-the-shoulder, mirror, desk, commute, or companion-shot evidence over a detached studio montage.
- Environment and sound: preserve normal occupancy and lived-in traces. Use location ambience, handling sounds, footsteps, clothing movement, and natural dialogue only.
- Avoid: influencer caricature, exaggerated surprise, nonstop smiling, fake candid behavior, excessive lens dirt, deliberate low quality, generated captions, and music.

## 高规格质感商业片风格: `premium_commercial`

- Visual point of view: deliberate premium advertising composition with controlled depth, material detail, clear product hierarchy, and consistent color and lighting design.
- Camera: stable dolly, slider, controlled orbit, precise macro, composed static frames, or motivated match cuts; keep one main movement per shot.
- Light and texture: for the final video shot, shaped soft or directional light, controlled highlights, believable reflections, rich but natural contrast, and accurate product materials. The underlying scene reference keeps ordinary location lighting and natural use, without cinema lighting effects or set dressing. Premium does not mean sterile unless the approved scene requires it.
- Performance: minimal and assured; precise gaze, measured hand placement, relaxed posture, and subtle reaction timing. Product handling must feel physically credible rather than posed.
- Product proof: prioritize legible mechanisms, textures, transformations, and results. Use fewer, more intentional shots and finish with a stable product or result tableau.
- Environment and sound: retain believable people and daily traces while controlling clutter and visual priority. Use refined diegetic sound design such as product clicks, material movement, room tone, and restrained dialogue.
- Avoid: generic luxury adjectives without visible evidence, excessive slow motion, implausible floating products, over-clean public or domestic spaces, generated captions, and music.

## 剧情对话短剧风格: `dialogue_drama`

- Visual point of view: a compact cause-and-effect scene driven by a relatable situation, character objective, product intervention, and visible payoff.
- Camera: establish spatial relationships, then use motivated two-shots, over-the-shoulder views, reaction shots, inserts, or restrained push-ins. Maintain eyelines and conversational geography.
- Light and texture: naturalistic narrative lighting appropriate to the researched place and time; polished enough for clarity without losing everyday realism.
- Performance: dialogue-led and restrained. Build a complete exchange with a concrete situation, responsive turn-taking, product intervention, and visible payoff. Every spoken line includes speaking tone, controlled facial and body detail, and the listener's immediate visible reaction. Favor natural handoffs, brief clause pauses, glances, breath, hand occupation, and subtle posture changes over theatrical gestures. Do not make each shot contain only one short line followed by a long pause.
- Product proof: the product must causally resolve, clarify, or improve the situation. Do not interrupt the scene for an unrelated feature recital.
- Environment and sound: preserve normal occupancy and activity without letting background people compete with the exchange. Use environment sound and visible-character dialogue only.
- Avoid: melodrama, shouting by default, exaggerated comedy faces, dense exposition, isolated feature slogans, unnatural one-line turns, long gaps after every sentence, multiple emotional reversals in one shot, voice-over standing in for action, generated captions, and music.

## 动画介绍风格: `animation_explainer`

Select `animation_style: stylized_3d`, `stop_motion`, or `motion_graphics` and read [animation-profiles.md](animation-profiles.md). The three subtypes use different character materials, movement, scene assets, and Hook pools. An explicit animation choice permits stylized locations or an abstract MG canvas; the documentary location rule at the top applies to the three live-action profiles. Preserve product evidence and use one complete reference per character. Do not randomly switch subtype or add music, captions, or unrequested narration.

## Applying a Profile

Translate the profile into concrete visual and behavioral instructions. Do not place only the enum or Chinese style name in an asset or video prompt and assume the generation model will infer the rules.

Random choices must remain inside the selected profile. A reroll may change the hook, narrative pattern, shot order, or ending, but must not drift into another profile. User-provided brand requirements override a profile detail when they do not violate product truth or output policy; record the override.
