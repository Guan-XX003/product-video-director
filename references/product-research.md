# Product Research

Complete this stage before creative randomization or asset design. The goal is not a generic market summary; it is a compact evidence pack that anchors product appearance, real usage, and supportable claims.

## Reuse Research Already Confirmed In Context

Before searching, inspect the current conversation and project files such as `product-video-project.json`, `research.md`, and `assets.md`. Reuse an existing record when it identifies the same product, model or edition, region, and app platform/version, includes its source URLs and visual references, and the user has confirmed or accepted the record. Carry forward the confirmed product identity, source-backed selling points, usage scenarios, and approved visual references without asking the user to repeat them or performing the same search again.

Refresh only the affected fields when the user requests current information, changes the model/region/version, points out a conflict, or the existing record lacks evidence needed for the new creative. Do not discard confirmed research merely because the new campaign has a different style, cast, scene, duration, or selling-point emphasis. If the conversation mentions prior research but does not contain its actual facts or sources, treat it as unavailable and research or request the missing source.

## Search Sequence

Use the smallest sufficient evidence set. The research pass is complete when identity, one authentic visual source, one real usage source, and every selected claim have traceable evidence. Do not collect additional articles, reviews, or lifestyle references unless they resolve a conflict or directly change a creative decision.

1. Resolve the exact identity: canonical product name, model or edition, region, color or configuration when visually relevant, and current app platform/version when applicable. Record `not applicable` explicitly when a model/version dimension genuinely does not exist.
2. In parallel where supported, find first-party visuals and real usage evidence:
   - physical product: official product page, media kit, manual, official store, or authorized retailer when the manufacturer does not expose enough angles
   - app: current App Store or Google Play screenshots, official product pages, release notes, help-center articles, or official demo videos showing the real UI
   - real usage scenarios: official use cases, support documentation, manuals, demonstrations, and credible reviews
3. Verify selling points against first-party wording or independently corroborated evidence.
4. Record conflicts, regional or version differences, and unresolved facts before selecting the campaign direction.

Search exact quoted product names plus model/version identifiers. Open the source pages and inspect the evidence; do not treat search-result snippets, generated summaries, or marketplace titles as verification.

Preserve a compact research snapshot in the project files: identity, source URLs, visual references, usage scenarios, verified claims, unresolved items, and access dates. Later turns should read this snapshot before using search again.

## Source Priority

Use sources in this order:

1. official product page, manual, media kit, official store, app-store listing, help center, or release notes
2. authorized retailer or distributor for missing product angles and configuration details
3. reputable independent review for observed usage context, clearly separated from manufacturer claims

Do not use AI-generated product images, unofficial UI mockups, fan renders, or unsourced reposts as truth references. Social posts are acceptable only when published by the official brand account and still relevant to the identified model/version.

## Visual Evidence

For a physical product, gather enough authentic views to identify silhouette, dimensions and proportions, materials, controls, ports, seams, colors, logo placement, packaging, and any state changes during use. Prefer clean official images but retain real lifestyle photos when they clarify scale or handling.

For an app, gather authentic UI screens for the current platform and version. Capture the navigation shell, core workflow, key controls, important states, typography, color system, icon style, and device framing. Do not redraw or modernize an outdated screenshot and present it as current UI.

Store source URLs and observable facts. A visual URL is a reference, not permission to redistribute it; use it to preserve product accuracy and follow the user's intended production workflow.

## Selling Points And Scenarios

Classify every proposed claim:

- `verified`: explicitly supported by a source
- `user_claim`: supplied by the user but not independently verified
- `inference`: a reasonable creative interpretation, not an advertising fact

Only `verified` claims are default candidates for final advertising copy. Keep exact quantities, prices, certifications, compatibility, health effects, awards, and comparative claims verbatim and source-linked. If a user claim cannot be verified, flag it and ask for supporting material instead of silently upgrading it to fact.

Usage scenarios must connect a real user need, environment, product action, and visible outcome. Use research to propose scene options, then let the user select or override the campaign scene. Do not mistake a visually attractive location for a genuine use case.

For each selected scene option, note the normal environmental state: typical occupants, ordinary background activity, and physical traces of daily use. The asset stage should preserve these observations so a street, vehicle, transit space, or home does not become implausibly empty or sterile.

## Required Research Record

Add this structure to `product-video-project.json` and summarize it in `research.md`:

```json
{
  "research": {
    "status": "complete",
    "product_kind": "physical_product",
    "canonical_name": "Exact product name",
    "model_or_version": "Exact model, region, or app version",
    "sources": [
      {
        "url": "https://official.example/product",
        "title": "Official product page",
        "publisher": "Brand",
        "source_type": "official_product_page",
        "accessed_on": "YYYY-MM-DD"
      }
    ],
    "visual_references": [
      {
        "url": "https://official.example/product-image.jpg",
        "source_url": "https://official.example/product",
        "kind": "product_photo",
        "view_or_screen": "front three-quarter"
      }
    ],
    "usage_scenarios": [
      {
        "scenario": "Concrete real-world use case",
        "evidence_source_urls": ["https://official.example/product"]
      }
    ],
    "selling_points": [
      {
        "claim": "Source-supported product benefit",
        "status": "verified",
        "evidence_source_urls": ["https://official.example/product"]
      }
    ],
    "unresolved": []
  }
}
```

Use `product_kind: app` and `kind: app_ui` for software. Research is complete only when the product identity is unambiguous, at least one first-party source is present, visual evidence matches the product kind, and usage scenarios and selling points have traceable evidence. If public evidence is unavailable, set `status` to `blocked`, explain the missing evidence, request official materials, and stop before asset design.
