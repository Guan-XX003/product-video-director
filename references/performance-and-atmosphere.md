# Performance and Atmosphere

Use this when a person appears in the video. The goal is observable, restrained behavior that feels captured rather than performed for a stage.

For animation, also read [animation-profiles.md](animation-profiles.md). Apply these performance fields to animated characters using only expressions and movements their design supports. Do not require human skin texture or physiological movement from graphic or craft characters. No-character MG shots omit performance and dialogue; do not invent a speaker to satisfy these fields.

## Performance Record

For every shot whose featured subject is a person, record:

- `expression`: small visible facial changes, including eyes, brows, mouth, and jaw where relevant
- `gaze`: what the person looks at, when the gaze shifts, and where it settles
- `micro_movement`: blinking, breathing, swallowing, finger adjustment, weight shift, or another subtle involuntary detail
- `body_language`: posture, shoulders, hands, head angle, balance, and the physical transition into the primary action
- `intensity`: `subtle`, `restrained`, or `moderate`

Do not use emotional labels by themselves. Translate them into visible behavior:

```text
Weak: she looks happy
Usable: her eyes soften, the corners of her mouth rise slightly, and her shoulders release as she looks down at the product

Weak: he is surprised
Usable: his brows lift slightly, his gaze pauses on the result, and he takes one short breath before leaning a little closer
```

Keep expression and body motion consistent with the shot scale. A close-up can show a tiny eye or mouth change; a wider shot needs readable posture and hand behavior without theatrical gestures.

## Motion Restraint

Default to low-amplitude actions with normal acceleration and deceleration. Name the acting body part, direction, speed or force, physical contact, and visible completion state. Preserve inertia between actions instead of snapping from pose to pose.

Prefer:

- `右手手指依次收拢，缓慢握住杯身，手腕在接触后自然停稳`
- `视线从屏幕移到同伴脸上，轻轻点头一次，肩膀保持放松`
- `嘴角轻微上扬，短暂眨眼，呼吸带动胸口和衣料细微起伏`

Avoid unless the user explicitly requires a heightened style:

- exaggerated smiles or grimaces
- repeated nodding, large waving, abrupt head turns, or full-body bouncing
- several emotional beats inside one short shot
- simultaneous face, hand, body, prop, and camera actions competing for attention
- abstract directions such as `非常开心`, `无比震惊`, or `情绪爆发`

For ordinary product advertising, do not use `exaggerated`, `extreme`, or equivalent performance intensity. If the creative concept genuinely needs heightened acting, surface it as a deliberate exception before asset approval.

## Dialogue Performance

Record dialogue as ordered turns. Each turn contains:

- `speaker`: the stable character label
- `line`: the exact spoken words
- `tone`: pace, volume, breath, emotional restraint, and any deliberate pause
- `reaction`: the other person's immediate visible response; use a concise `none - monologue` value only when there is no listener

Plan the exchange before splitting it into shots. Dialogue is a short conversation with a reason to begin, a response, and a change caused by the product. Do not force one sentence into each shot. Ordinary people-led UGC carries continuous speech; other styles and explicit silent exceptions need not make every shot speak. A single shot may contain two or three connected turns when the people remain in the same conversational space; preserve eye-line, turn-taking, and the physical action while they speak.

For a typical 15-second dialogue-led ad, start with a complete exchange rather than a slogan list: a concrete situation or problem, a question or observation from the other person, a natural introduction or use of the product, and a response that confirms what was just seen. Roughly two to four turns can work, but do not impose a character count on each turn. UGC can use one connected first-person passage or a short exchange. Budget the whole passage at its actual speaking pace; fewer complete thoughts are preferable to many clipped phrases.

### Everyday, connected wording

Write what someone would actually say in this situation, using complete everyday thoughts and natural Chinese omission where the referent is clear. Preserve useful connections such as “刚才”“所以”“你看”“那我” when they link the situation, action, or response; do not mechanically insert a connector into every sentence. The listener answers the actual question or reacts to the action just seen. A short “嗯”“好，你试试” may occur between substantive turns, including in its own reaction shot, but a whole exchange must not consist of acknowledgements, feature keywords, or repeated praise.

Before making shots, read only the spoken words as one passage: can the viewer understand what is happening, why the product comes up, and what changes? Replace disconnected fragments such as “找不到。用这个。好快。真方便。” with a connected exchange, only if the lookup feature and demonstration are verified: “我刚才存的那条记录怎么找不到了？” / “你在这里搜一下名字，看看是不是这条。” / “对，就是它，那我接着往下看。” Use the real product name where the conversation needs it; do not force a brand mention into every turn. A UGC passage can be “我刚才还在翻那条记录，后来在这里搜了一下名字，就找到了。你看，就是这一条，我接着往下看就行。” These are wording examples, not facts to invent or a fixed template to reuse.

When copy exceeds the time budget, remove a secondary idea or shorten repeated explanation; retain the verbs, references, and causal links that make it understandable. Do not chop sentences into keywords, accelerate unnaturally, pad with filler, or fabricate a personal history to meet a length target. Explicitly sparse commercial speech may stay concise while expressing a clear thought.

The product should enter the conversation because someone notices a problem, asks a question, recognizes the product, or reacts to its visible result. Avoid inserting a brand claim between unrelated lines. The listener's response must address the previous line or visible action, such as asking how it works, noticing the result, or changing their next action. Do not make both people recite separate feature slogans.

Use natural conversational timing: normal speaking pace, brief clause-level pauses and breathing, occasional overlap or quick handoff when appropriate, and no long silent gap after every line. Never describe the exchange as one person saying one short sentence and then waiting for a long time before the next person speaks. Spoken lines may continue across a cut when the meaning and eyeline remain clear.

For UGC with people, treat speech as part of the capture rather than an optional decoration. Draft one continuous first-person passage or connected exchange before dividing it across shots. Every featured-person shot should carry a line or a continuing sentence by default. A featured-person shot may be silent only when the brief explicitly allows sparse or visual-only dialogue and the shot records a `silent_beat_reason`; product-only inserts can remain silent when the visible proof is doing the communication.

### Parallel action and speech

When an action permits speaking, perform it during the line rather than finishing the demonstration, pausing, and then delivering a slogan. Record `action_speech_relation` on speaking shots: what the hands/body are doing during which words and how the listener responds without waiting for a cut. For swallowing, strenuous exertion, safety-critical handling, or a sound that must be heard, record a short sequential beat and its reason instead; never force physically impossible simultaneous speech.

For a 15-second Mandarin UGC starting draft, roughly 45–65 spoken Chinese characters often fit a connected passage at a conversational pace. This is an editing heuristic, not a hard minimum or a Seedance guarantee: read it at the intended pace with brand pronunciation, breaths, reactions, and essential silent actions included. Preserve meaningful content rather than filling a quota. Shorten overloaded copy, or add a concrete observation/use/result when sparse copy leaves unexplained silence. Do not solve overcrowding with unnatural speed. Inspect every human-led silent gap; do not count a whole shot as spoken just because it contains one short line.

Keep speaking speed separate from gesture amplitude: restrained expressions and small movements do not imply slow speech. Compile the overlap into the actual prompt, for example `她一边将杯子递给同伴，一边以正常聊天语速说{……}，同伴接过杯子时立即回应{……}`. No voice-over is added by default; if a product close-up would hide the speaker, stay in a composition that includes them or use a justified short silent insert.

Describe the reaction as a physical beat rather than an interpretation. Example of a restrained listener reaction:

```text
跑者用正常聊天语速、放松的语气说{这杯水先帮我拿一下，我把外套穿上。}，同伴看向杯子，伸手接住时自然回应{好，你慢慢来。}，两人肩膀保持放松。
```

Do not add subtitles for spoken lines. Do not add narration, voice-over, or off-screen speech unless the user later requests it; default dialogue is spoken by visible characters.

### Spoken-line naturalness pass

After the shot plan establishes who speaks and why, but before video-prompt confirmation, review only the spoken `line` fields and any spoken copy the user explicitly requested. Read the whole exchange aloud at its intended pace and include natural pauses in the shot's time budget. Remove formulaic AI phrasing, filler, unsupported superlatives, and feature-list recitals, but preserve connective words and complete thoughts needed for a real conversation. Keep the selected style: UGC can sound informal and continuous, dialogue drama should sound responsive to the other person, and premium commercial may be spare rather than chatty. Do not add slang, jokes, personal anecdotes, or manufactured hesitation merely to sound human.

Protect the rest of the production specification. Do not rewrite asset IDs, reference slots, shot order, timing, camera/action constraints, app UI text, brand/product names, or the no-subtitles/no-music policy. Do not change the meaning or strength of a verified selling point, or introduce an experience, result, number, or endorsement without evidence. If natural wording would weaken or alter a required claim, preserve the claim and adjust only its spoken framing. Keep `tone` and `reaction` aligned with the final words and the existing restrained performance. If a line changes after prompt compilation, update its structured shot and compiled prompt together, then recheck duration and claim mapping.

Example, only when the feature is verified and the scene shows it: replace a slogan exchange such as `这款产品带来了颠覆性的便捷体验。` / `确实非常方便。` with a connected exchange such as `你刚才不是还在找开瓶器吗？` / `对，我换成这个以后，单手就能打开。你试试。` / `还真是，拿着东西也能开。` Do not add the single-hand claim if it has not been verified or visibly demonstrated.

The shared `scripts/dialogue_quality.py` check inspects the complete passage across shots and catches obvious all-fragment exchanges. It allows a brief reply after a substantive turn and does not impose a per-line minimum. Passing it does not establish semantic coherence, truthful claims, or good pacing; the read-aloud and claim checks still apply.

## Environmental Atmosphere

Every shot, including product-only shots, records only:

- `summary`: one concise visual atmosphere phrase covering only the context needed to situate the action
- `ambient_sound`: room tone, traffic bed, fabric movement, appliance hum, wind, birds, or intentional silence

Atmosphere must support the product and performance without receiving the same descriptive density as a person. Do not enumerate lighting diagrams, weather mechanics, background props, or decorative adjectives unless one directly affects the action. Background people and props remain subordinate.

Example:

```text
清晨安静的窗边场景，<低弱城市底噪与衣料摩擦声>。人物目光先停在杯盖上，轻眨一次眼，右手手指缓慢收拢握住杯身，嘴角只轻微上扬，肩膀随呼气逐渐放松，最终将杯子稳定停在胸前。
```

## Prompt Compilation

Compile details in this order when it reads naturally:

1. concise atmosphere and ambient sound
2. gaze and expression
3. micro-movement and body language
4. primary product interaction
5. completion state
6. dialogue line, speaking tone, and listener reaction when present
7. one camera instruction

This order is a readability default. A target adapter may place the camera instruction first when that model benefits from it, as Seedance 2.0 does. Do not turn the checklist into robotic prose. Combine compatible details into one continuous physical beat and omit irrelevant anatomy. The final prompt must still contain the actual observable details recorded in the structured shot.
