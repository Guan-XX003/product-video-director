# Completeness Audit and Delivery Folder

Use this reference twice: once before the user confirms the video prompts, and once after the storyboard is generated.

## Pre-confirmation audit

Create a checklist from the actual brief, selected style, research evidence, approved assets, storyboard plan, and target model. For every proposed prompt, ask:

1. Does it have a clear commercial job and either a useful approved image or a usable Chinese image-generation prompt for a still-unrendered image?
2. Is that reference image useful for identity, geometry, scene geography, UI state, or storyboard composition rather than merely decorative?
3. Is any required prompt missing an image, or any image present without a prompt or downstream use?
4. Does each featured person have exactly one complete reference image showing face and body together, or one usable image-generation prompt when the image is unavailable?
5. Is there an approved master scene image, or a scene image-generation prompt preserving normal occupancy and lived-in traces?
6. If the product is an app, are authentic App Store description and UI screenshots present and mapped to the relevant product/UI prompt?

Run the audit against the current delta. If the user changed only dialogue, timing, or one scene detail, reuse unchanged research and asset evidence and inspect only the affected downstream files plus the final package manifest.

If a generatable image is missing, unusable, contradictory, or orphaned, generate it when the current image capability and authorization allow it; otherwise write the exact Simplified Chinese image-generation prompt and mark the image `unavailable` with a reason such as `当前没有生图工具`. Do not stop to propose CLI setup, an API key, or a paid provider unless the user explicitly asks for that alternative. A prompt-ready image may proceed to video-prompt confirmation, but the video prompt remains conditional on the missing runtime reference. Authentic product photos, app UI, and App Store screenshots cannot be replaced by generated images or image-generation prompts; obtain the real evidence before declaring an app delivery ready.

Record `audit_status: complete` only when every required prompt exists and every required image is present or, for generatable images only, marked unavailable with a usable prompt and reason.

### User-visible audit summary

Before requesting video-prompt confirmation, show a compact Chinese checklist with actual findings (not prefilled green ticks):

- 主卖点与功能边界：primary claim and whether every spoken/visual claim stays in the verified whitelist.
- 人物与场景：featured actor count, distinct locations, camera operator, and consistency with approved assets; do not count background people or reverse angles as new cast/locations.
- 产品展示：named hardware policy, proof shot, and credible installation/handling; App UI remains authentic and minimally described.
- 场景真实性：真实地点细节、正常占用和生活痕迹是否齐全；场景参考图是否误用了电影光效或棚拍布景。
- 对白与动作：normal-pace duration estimate, unexplained silent gaps, action/speech overlap, natural product introduction, and restrained reactions.
- 输出规范：Chinese prompts, default Seedance 2.0 unless explicitly changed, no added subtitles/music.
- 动画风格：若选择动画，子风格、角色/材质一致性和 MG 是否有人物已记录，并与参考图和提示词一致。
- 资产完整性：present references versus prompt-ready missing images, their actual downstream uses, and whether the video prompt is conditional.

Label unresolved checks as needing repair or user choice. A validator pass confirms structural fields, not speech delivery, image fidelity, or generated-video quality. Repair only affected layers and rerun their checks. For text-only revisions, do not regenerate approved images or re-research the product.

## Confirmation and storyboard gate

The user confirms the video prompts only after the pre-confirmation audit passes. That confirmation authorizes storyboard generation from the approved references; it does not approve unreviewed or missing assets.

Asset confirmation and video-prompt confirmation are both required before any generation job is submitted — including a draft or trial render. A request to "make the video" is a workflow directive, not the confirmation itself; ask for the two confirmations and keep the project gates false until they arrive. If generation ran early, mark the output as an unconfirmed process artifact, reset the confirmation gates, and rename any premature delivery folder so it cannot be mistaken for a release.

After confirmation, generate the storyboard contact sheet or storyboard images from the approved assets and the final shot plan. If image generation is unavailable, keep the storyboard prompt in the folder and mark the storyboard image unavailable. Set delivery `render_status` to `partial` whenever any generatable image is unavailable; otherwise set it to `complete`.

## Final folder layout

Use a stable folder name such as `product-video-delivery/`:

```text
product-video-delivery/
├── manifest.json
├── research.md
├── prompts/
│   ├── product-asset.md
│   ├── character-asset.md          # omit only when no people
│   ├── scene-asset.md
│   ├── storyboard.md
│   └── video-prompts.md
├── images/
│   ├── product/
│   ├── character/                  # omit only when no people
│   ├── scene/
│   ├── storyboard/
│   └── app-store/                  # required for app evidence when applicable
└── project/
    └── product-video-project.json
```

When a required image is unavailable, keep its corresponding prompt file in `prompts/` and record the unavailable image entry in `manifest.json`; the assembler copies present files and preserves unavailable entries with their reasons.

The manifest records each file's `path`, `kind`, `purpose`, `status`, `approved` boolean, and `source_asset_id` or `source_url`. `status` is `present`, `unavailable`, or `not_applicable`; unavailable and not-applicable entries require a `reason`. Only generatable images may be unavailable, and each must have a corresponding present prompt. Every prompt, including the video prompt, must be a present file. App Store screenshots for app deliveries must be authentic present files with a source URL.

Deliver `render_status: complete` as a package with all reference images. Deliver `render_status: partial` as a prompt-ready package and tell the user which images still need rendering or collection. Do not describe a partial package or a video prompt that references missing images as ready to submit to a video model.

Do not silently substitute a generic mockup for an official product image, authentic App UI, or App Store screenshot. Preserve original screenshot text when it is part of the evidence; do not add generated captions or music to storyboard images or prompts.
