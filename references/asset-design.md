# Asset Design and Generation

When `creative_style` is `animation_explainer`, first apply [animation-profiles.md](animation-profiles.md): use the selected material/graphic language, one complete image per character, and an abstract canvas rather than a three-angle location board for MG. The documentary scene and human skin guidance below applies to live action; stylized scenes preserve actual spatial/use facts without requiring photographic rendering. Real product/App evidence remains mandatory.

Create product, character, and scene references independently. Combining different subjects into one initial image makes reference responsibilities ambiguous and increases visual contamination.

Apply the selected profile from [style-profiles.md](style-profiles.md) to camera-facing character styling, shot treatment, and realism. Keep identity boards neutral enough for reuse, but make scene reference images documentary and location-faithful. A later premium video treatment may refine the shot lighting; it must not rewrite the scene reference as a studio set or cinematic backdrop.

## Product Evidence Asset: `PROD-01`

Route by product kind. The visual references recorded during product research are the truth source for both routes.

### Physical Product Board

Lock product geometry before storytelling. Include:

- front, 3/4 hero, exact side, and back views
- two or three identifying detail close-ups
- stable proportions, materials, colors, seams, openings, controls, and accessory relationships
- neutral studio background and consistent light direction

Describe what each authentic reference controls and avoid conflicting reinvention. If the research images do not reveal a required side, control, material, or configuration, request another official image instead of inventing it. Image generation may normalize the background or build a planning board, but it must preserve the observed product geometry.

Do not rely on image models for exact logos, packaging copy, legal text, prices, or small UI labels. Reserve those for post-production unless the user explicitly accepts generation risk.

### App UI Reference Pack

For an app, do not generate a fictional multi-view product board. Build `PROD-01` from authentic UI screenshots for the identified platform and version. Include only screens needed by the proposed user journey:

- navigation shell or home screen
- entry state for the featured workflow
- one or more key interaction states
- visible result or completion state
- official app icon or wordmark when relevant

Record each screen's source URL, platform, version or access date, state, and intended shot use. Preserve layout, labels, icons, data hierarchy, and navigation. Do not redesign, modernize, translate, or fabricate UI and present it as the product.

Keep this detailed UI inventory in the research and asset records, not in the final video prompt. In the prompt, cite the approved screenshot and name only the current screen or workflow state plus the person's interaction, for example `手机保持图片3中的订单确认页，她用拇指轻触确认`. Do not enumerate navigation bars, card layouts, labels, button colors, typography, icons, or individual UI copy.

When a shot shows the app inside a phone or computer, use the authentic screenshot as a screen-replacement or compositing asset. A generated image may supply the hand, device, lighting, reflections, or surrounding scene, but the final UI surface must come from the approved screenshot when visual accuracy matters.

## Character Reference: `CHAR-01`

For each featured person, generate exactly one image containing exactly one complete person. Use a natural standing or seated three-quarter pose that clearly shows the face and the full outfit, including shoes where visible. Keep the face legible at the intended resolution and show natural body proportions, hairstyle, clothing, accessories, and any carried product in the same frame. Use a simple, credible background and even light. Do not make a face-only image, a separate body image, a triptych, an inset, or a multi-view collage. Each additional featured person gets their own single image and asset ID.

Preserve natural facial asymmetry, skin texture, relaxed eyelids, believable eye focus, and a relaxed jaw. Avoid beauty-filter skin, permanently widened eyes, frozen smiles, theatrical brows, or an expression sheet with extreme emotions. Keep the identity reference neutral; design shot-specific micro-expression and body performance later through [performance-and-atmosphere.md](performance-and-atmosphere.md).

Use this same single image for both human approval and Seedance 2.0 runtime identity binding. Do not create extra face, body, or alternate-angle references for the same person. A multi-view collage can be misread as multiple people by the video model.

If only hands or a silhouette appear once, a character reference may be unnecessary. Record a fixed performer description instead. If the same hands, clothing, or body recur across shots, keep one character reference for that performer.

## Scene Board: `SCENE-01`

Scenes do not have a literal anatomical turnaround. Use a spatially consistent three-angle coverage board:

- master view looking into the scene
- reverse view looking back from the action area
- 90-degree side view; use an overhead plan instead when geography would otherwise be ambiguous

Build the scene image as a realistic location record, not a film set. Show concrete details that prove the place is real: wall and floor wear, seams and joints, ordinary fixtures, signage or route boards when genuinely present, cable runs, handles, shelves, bags, cups, dishes, parked vehicles, passenger spacing, and other context-appropriate objects. Preserve plausible perspective, scale, occlusion, and navigable paths.

Lock room or landscape geometry, doors, windows, large props, product surfaces, ordinary practical lights, light direction, time of day, weather, materials, and navigable action paths. Use available daylight or the location's normal practical light. Avoid dramatic key lights, colored gels, theatrical rim lights, artificial haze, lens flares, decorative bokeh, showroom staging, studio backdrops, and newly placed props that do not belong in the researched location. The three views must depict the same place, not three stylized variations.

For required hardware, show its authentic installation or normal use position in the contextual scene: support surface, reachable controls, and plausible person/device scale. An installed device must not become a floating prop or a handheld substitute. Keep neutral product identity boards separate from this contextual requirement. Reuse approved cast identities across alternative scripts unless the user requests new casting; background occupants do not consume actor slots.

Also record the atmosphere baseline: ordinary light softness and color temperature, air or weather behavior, plausible low-intensity background motion, and ambient sound sources. These anchors keep later shot prompts specific without making the background compete with the product.

## Normal Environmental State

Scene asset prompts and generated scene boards must depict a believable ordinary state for the selected place. Record a `normal_state` block with:

- `contextual_occupancy`: who normally occupies or passes through the place, such as pedestrians on a street or passengers on public transport
- `lived_in_traces`: ordinary signs of use, such as bags, cups, shoes, folded clothes, mail, chargers, handrails, seat wear, or slightly moved objects
- `ambient_activity`: low-intensity background behavior, such as walking, waiting, reading, looking at a phone, commuting, cooking, or distant traffic
- `exception_reason`: required only when the scene is intentionally empty, pristine, closed, evacuated, or otherwise outside its normal state

Use authentic contextual occupancy and lived-in traces in both the asset prompt and the rendered scene image:

- street, plaza, shopping street: a natural mix of pedestrians, cyclists, storefront activity, and passing traffic where appropriate
- bus, subway, train, station: passengers seated or standing, varied postures, bags, handrails, doors, route displays, and ordinary commuting behavior
- home, bedroom, kitchen, living room: signs of current daily use, such as personal belongings, dishes, textiles, charging cables, groceries, books, or a recently used surface
- office, school, cafe, gym, park: people and objects that match the time and activity implied by the selected use case

Background people must remain generic, varied, naturally distributed, and subordinate to the featured subject. Do not make them named characters, duplicate the hero, or give them elaborate costume and facial direction. Do not add a crowd merely for decoration when it conflicts with the researched use case or the user's explicit empty-scene choice.

For a deliberate empty or highly controlled scene, write the reason explicitly, for example `exception_reason: sterile product tabletop requested by user` or `exception_reason: closed station after hours`. A neutral studio product board is automatically exempt; a scene board is not exempt unless its prompt records the exception.

When compiling for Seedance 2.0, normally submit one approved master scene image rather than the whole scene coverage board. Use the remaining views for planning and consistency review unless a specific view is required by the storyboard.

## Prompt Structure

Each generated asset prompt should contain:

1. asset ID and purpose
2. identity or geometry anchors
3. required views and layout
4. materials, costume, or spatial facts
5. ordinary location lighting and background detail; explicitly exclude cinematic set dressing
6. consistency requirements
7. normal environmental state, when the asset is a scene
8. explicit exclusions

Keep model-specific syntax out of the base prompt. Add a short adapter only when the target image system is known.

For an app UI reference pack, store source and compositing instructions instead of writing a prompt that asks an image model to recreate the interface.

## Rendering Route

Separate approval coverage from runtime coverage where appropriate. Each character has one complete-person image for approval and runtime. The scene coverage board supports spatial consistency; for Seedance 2.0, submit only the approved master scene reference needed by the shot plan. Do not render duplicate character angles.

When an image tool is callable:

1. Save the copy-ready prompt first.
2. Generate product boards, one image per featured person, and scene boards separately.
3. Inspect the results for repeated identity, view completeness, geometry, hands, text artifacts, and contradictions.
4. Retry once only for an obvious technical failure when the generation path is non-billable. Otherwise report the defect and wait for direction.
5. Set state to `rendered`, show the boards, and request explicit approval.

When no image-generation tool is callable, deliver the complete Chinese prompts and set state to `draft`. Do not substitute an imagined CLI/API route or ask for credentials to unlock this stage. The user can take the prompts to an image generator of their choice.

The user may approve prompts instead of images. Record exactly what was approved, continue to the storyboard and conditional video prompt, and do not later treat an unapproved render as the new source of truth. A later rendered image still needs review before becoming a runtime reference.
