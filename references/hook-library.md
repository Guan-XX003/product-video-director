# Hook Library

Use a Hook to decide how the first one to three seconds enter the story. A Hook is an opening mechanism, not a slogan, a new product claim, or a replacement for the complete dialogue. It must be physically possible in the chosen scene, fit the confirmed actor count and duration, and stay inside the verified claim whitelist.

Record `creative.hook_mode` as `random` or `user_selected` and keep the selected `creative.hook` ID in project state. If the user has no preference, use `random` with a reproducible seed. Include the choice within the existing creative candidates; do not add a mandatory question or delay generation waiting for a Hook preference. If the user chooses by natural language, map it to a style-compatible Hook ID without changing their intent. If no preset fits, preserve their custom opening in `creative.hook_description` with `hook: custom`, and compose it directly instead of forcing it through the helper. A selected Hook stays fixed through candidate comparison and later prompt revisions.

Before randomizing, filter by verified product proof, scene, duration, actor count, and dialogue mode. For example, a material close-up must not pretend an App has physical texture; a companion question needs two actors; a comparison needs evidence; a silent opening must not override continuous UGC speech. The helper filters style and actor count; the agent must supply a semantically checked `--eligible-hooks` shortlist when other constraints exclude options. If nothing fits, design a truthful custom opening rather than inventing a claim or extra cast.

When presenting candidates, show the Hook in Chinese: the opening situation, the first visible action, and the first spoken or observational beat. If the user requests several candidates, they may share a user-selected Hook while varying the demonstration or narrative pattern; random mode should prefer distinct Hook IDs until the available pool is exhausted.

## UGC 原生 vlog

- `interrupted_routine`: ordinary activity is interrupted by a small, believable problem; the person keeps handling the situation while speaking.
- `result_before_cause`: show a visible result first, then let the person naturally explain or answer how it happened.
- `rapid_physical_proof`: 现场演示，直接从真实可见的操作或结果切入；不能把慢速过程伪装成即时见效。
- `friend_question`: a nearby person asks a concrete question while the featured person is already using the product.
- `in_use_observation`: begin during a real routine with a short observation that leads into the product's verified primary claim.
- `comparison_moment`: the person notices a difference from a familiar alternative, without inventing superiority beyond the verified claim.

## 高规格质感商业片

- `macro_texture_reveal`: begin with a truthful material, texture, mechanism, or surface detail that leads into the product proof.
- `silent_result_then_context`: open on the result, then reveal the real location and action that produced it.
- `tactile_trigger`: a hand contact, click, opening, pouring, or other real interaction starts the visual chain.
- `visual_contradiction`: place an ordinary expectation beside the product's verified observable result without using an unsupported comparison claim.
- `environment_to_product`: begin with a concrete location detail, then connect it to the product in use.

`result_before_cause` is also available here for an opening with speech. Scene reference images still use real details and ordinary location light.

## 剧情对话短剧

- `interrupted_routine`: one character interrupts an ordinary action with a concrete problem or observation.
- `direct_question`: one character asks a specific question that the product use can answer naturally.
- `misunderstanding`: a small, realistic misunderstanding creates the opening, then the product use resolves it.
- `companion_notice`: the second character notices a visible result before the product is explained.
- `visible_payoff_first`: begin with the consequence of the product use, then let the dialogue trace back to the cause.

`visual_contradiction` and `result_before_cause` are also available for a verified visible contrast or result. Do not use exaggerated conflict to create artificial suspense.

## Chinese Opening Examples

For `animation_explainer`, use the subtype's Hook pool in [animation-profiles.md](animation-profiles.md) and the helper's `--animation-style`. Three-dimensional characters favor routine/result/question Hooks; stop motion favors material/action/result Hooks; MG favors result, verified contrast, or process demonstrations. Keep abstract transformations tied to verified functionality; do not give an App imaginary physical materials or add an actor to make a Hook fit.

These are construction examples, not product claims or fixed copy. Replace them using the confirmed product and scenario:

- 日常小困扰：人物正在处理眼前的事情，边操作边说“等一下，这一步我又卡住了。”接着通过实际操作带出产品。
- 同伴提问：同伴看向已经完成的东西，随口问“你这就弄好了？”使用者接话并继续操作，不停下来念卖点。
- 边用边聊：从进行中的日常任务开始，“我现在做到这一步，就直接用这个。”随后给出可验证的具体用途。
- 结果先行：先给真实可见的结果，再接“刚才我是这样做的。”镜头或对白立即解释因果。

For each proposal store `hook_opening` (visible opening action), `hook_first_line` (exact Chinese first line when someone speaks), and `hook_payoff` (how the primary claim answers the opening). Keep the final video prompt free of internal Hook IDs. UGC dialogue continues through the opening action at normal pace; do not spend several seconds on a silent prelude or an isolated slogan. Audit that the payoff is actually shown or explained within the requested duration.

Avoid Hooks that rely on fake emergencies, unsupported before/after promises, exaggerated shock, invented statistics, or a product reveal unrelated to the researched use case. The opening must connect to the selected primary claim within the first three seconds.
