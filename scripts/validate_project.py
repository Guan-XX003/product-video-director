#!/usr/bin/env python3
"""Validate Product Video Director project state."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from style_contract import validate_style
from dialogue_quality import validate_shot_dialogue


REQUIRED_BRIEF_FIELDS = (
    "product_name",
    "selling_points",
    "people",
    "scene",
    "duration_seconds",
    "creative_style",
)

PROJECT_VERSION = 8
VALID_ASSET_STATES = {"draft", "rendered", "approved"}
VALID_PRODUCT_KINDS = {"physical_product", "app", "service", "other"}
VALID_VISUAL_KINDS = {"product_photo", "app_ui", "official_visual"}
VALID_CLAIM_STATES = {"verified", "user_claim", "inference"}
VALID_PERFORMANCE_INTENSITIES = {"subtle", "restrained", "moderate"}
VALID_DIALOGUE_MODES = {"continuous_spoken", "mixed", "visual_only"}
VALID_HARDWARE_DISPLAY_POLICIES = {"auto", "required", "not_required"}
VALID_DELIVERY_RENDER_STATES = {"complete", "partial"}
DELIVERY_PROMPT_KINDS = {
    "product_prompt",
    "character_prompt",
    "scene_prompt",
    "storyboard_prompt",
    "video_prompt",
}
GENERATABLE_IMAGE_PROMPTS = {
    "product_reference_image": "product_prompt",
    "character_reference_image": "character_prompt",
    "scene_reference_image": "scene_prompt",
    "storyboard_image": "storyboard_prompt",
}
PERFORMANCE_FIELDS = ("expression", "gaze", "micro_movement", "body_language")
ATMOSPHERE_FIELDS = ("summary", "ambient_sound")
NORMAL_STATE_FIELDS = ("contextual_occupancy", "lived_in_traces", "ambient_activity")
FIRST_PARTY_SOURCE_TYPES = {
    "official_product_page",
    "official_store",
    "app_store",
    "official_help_center",
    "official_media",
    "manual",
    "release_notes",
}
URL_PATTERN = re.compile(r"https?://\S+", re.IGNORECASE)


def nonempty(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, tuple, dict)):
        return bool(value)
    return True


def validate_production_controls(brief: dict[str, Any], selling_points: list[Any], no_people: bool) -> list[str]:
    """Validate optional workbench controls when a project records them."""
    errors: list[str] = []

    whitelist = brief.get("core_function_whitelist")
    if whitelist is not None:
        if not isinstance(whitelist, list) or not whitelist or not all(isinstance(item, str) and item.strip() for item in whitelist):
            errors.append("brief.core_function_whitelist must be a non-empty list when provided")
        elif any(str(point) not in {str(item) for item in whitelist} for point in selling_points):
            errors.append("brief.selling_points must be a subset of brief.core_function_whitelist")

    primary_claim = brief.get("primary_claim")
    if primary_claim is not None:
        if not isinstance(primary_claim, str) or not primary_claim.strip():
            errors.append("brief.primary_claim must be non-empty when provided")
        elif str(primary_claim) not in {str(point) for point in selling_points}:
            errors.append("brief.primary_claim must be one of brief.selling_points")

    actor_count = brief.get("actor_count")
    if actor_count is not None:
        if isinstance(actor_count, bool) or not isinstance(actor_count, int) or actor_count < 0:
            errors.append("brief.actor_count must be a non-negative integer when provided")
        elif no_people and actor_count != 0:
            errors.append("brief.actor_count must be 0 when brief.people indicates no people")
        elif not no_people and actor_count == 0:
            errors.append("brief.actor_count must be greater than 0 when people appear")

    scene_count = brief.get("scene_count")
    if scene_count is not None and (
        isinstance(scene_count, bool) or not isinstance(scene_count, int) or scene_count <= 0
    ):
        errors.append("brief.scene_count must be a positive integer when provided")

    hardware_policy = brief.get("hardware_display_required")
    if hardware_policy is not None and (not isinstance(hardware_policy, str) or hardware_policy not in VALID_HARDWARE_DISPLAY_POLICIES):
        errors.append("brief.hardware_display_required must be auto, required, or not_required")
    if hardware_policy == "required" and not nonempty(brief.get("hardware_device")):
        errors.append("brief.hardware_device is required when hardware_display_required is required")
    if "hardware_display_reason" in brief and not nonempty(brief.get("hardware_display_reason")):
        errors.append("brief.hardware_display_reason must be non-empty when provided")

    candidate_count = brief.get("creative_candidate_count")
    if candidate_count is not None and (
        isinstance(candidate_count, bool) or not isinstance(candidate_count, int) or candidate_count <= 0
    ):
        errors.append("brief.creative_candidate_count must be a positive integer when provided")

    return errors


def load_project(source: str) -> dict[str, Any]:
    if source == "-":
        return json.load(sys.stdin)
    return json.loads(Path(source).read_text(encoding="utf-8"))


def valid_url(value: Any) -> bool:
    return isinstance(value, str) and bool(URL_PATTERN.fullmatch(value.strip()))


def validate_output_policy(project: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    policy = project.get("output_policy")
    if not isinstance(policy, dict):
        return ["output_policy must be an object"]
    if policy.get("subtitles") != "none":
        errors.append("output_policy.subtitles must be none")
    if policy.get("music") != "none":
        errors.append("output_policy.music must be none")
    if policy.get("prompt_language") != "zh-CN":
        errors.append("output_policy.prompt_language must be zh-CN")
    allowed_audio = policy.get("allowed_audio")
    if not isinstance(allowed_audio, list) or set(allowed_audio) != {"ambient_sound", "dialogue"}:
        errors.append("output_policy.allowed_audio must contain only ambient_sound and dialogue")
    if policy.get("app_ui_prompt_detail") != "state_only":
        errors.append("output_policy.app_ui_prompt_detail must be state_only")
    return errors


def validate_normal_state(asset: dict[str, Any], index: int) -> list[str]:
    errors: list[str] = []
    normal_state = asset.get("normal_state")
    if not isinstance(normal_state, dict):
        return [f"assets[{index}].normal_state must be an object for scene assets"]
    for field in NORMAL_STATE_FIELDS:
        if not nonempty(normal_state.get(field)):
            errors.append(f"assets[{index}].normal_state.{field} is required")
    exception_reason = normal_state.get("exception_reason")
    if exception_reason is not None and not nonempty(exception_reason):
        errors.append(f"assets[{index}].normal_state.exception_reason must not be empty")
    return errors


def validate_delivery(project: dict[str, Any], no_people: bool, product_kind: Any) -> list[str]:
    errors: list[str] = []
    gates = project.get("gates", {})
    if not isinstance(gates, dict) or not gates.get("delivery_ready"):
        return errors
    delivery = project.get("delivery")
    if not isinstance(delivery, dict):
        return ["delivery must be an object when gates.delivery_ready is true"]
    if delivery.get("audit_status") != "complete":
        errors.append("delivery.audit_status must be complete when delivery is ready")
    render_status = delivery.get("render_status")
    if render_status not in VALID_DELIVERY_RENDER_STATES:
        errors.append("delivery.render_status must be complete or partial when delivery is ready")
    if not nonempty(delivery.get("folder_name")):
        errors.append("delivery.folder_name is required when delivery is ready")
    files = delivery.get("files")
    if not isinstance(files, list):
        return errors + ["delivery.files must be a list when delivery is ready"]
    present_kinds: set[str] = set()
    unavailable_kinds: set[str] = set()
    seen_paths: set[str] = set()
    character_image_counts: dict[str, int] = {}
    for index, item in enumerate(files):
        if not isinstance(item, dict):
            errors.append(f"delivery.files[{index}] must be an object")
            continue
        for field in ("path", "kind", "purpose"):
            if not nonempty(item.get(field)):
                errors.append(f"delivery.files[{index}].{field} is required")
        path = item.get("path")
        if isinstance(path, str) and path.strip():
            if path in seen_paths:
                errors.append(f"delivery.files[{index}].path is duplicated: {path}")
            seen_paths.add(path)
        kind = item.get("kind")
        status = item.get("status")
        if kind == "character_reference_image" and status in {"present", "unavailable"}:
            asset_id = str(item.get("source_asset_id", ""))
            character_image_counts[asset_id] = character_image_counts.get(asset_id, 0) + 1
        if not isinstance(item.get("approved"), bool):
            errors.append(f"delivery.files[{index}].approved must be boolean")
        if status != "not_applicable" and not nonempty(item.get("source_asset_id")) and not valid_url(item.get("source_url")):
            errors.append(f"delivery.files[{index}] requires source_asset_id or source_url")
        if status not in {"present", "not_applicable", "unavailable"}:
            errors.append(f"delivery.files[{index}].status is invalid")
        if status in {"unavailable", "not_applicable"} and not nonempty(item.get("reason")):
            errors.append(f"delivery.files[{index}].reason is required for {status}")
        if status == "unavailable" and kind not in GENERATABLE_IMAGE_PROMPTS:
            errors.append(f"delivery.files[{index}].kind cannot be unavailable: {kind}")
        if kind in DELIVERY_PROMPT_KINDS and status != "present":
            errors.append(f"delivery.files[{index}].kind must be present: {kind}")
        if kind == "app_store_screenshot" and product_kind == "app" and status != "present":
            errors.append("app_store_screenshot must be present for app delivery")
        if kind == "app_store_screenshot" and status == "present" and not valid_url(item.get("source_url")):
            errors.append(f"delivery.files[{index}].source_url must identify the App Store screenshot")
        if status == "present":
            present_kinds.add(str(kind))
        elif status == "unavailable":
            unavailable_kinds.add(str(kind))
    prompt_kinds = {"product_prompt", "scene_prompt", "storyboard_prompt", "video_prompt"}
    image_kinds = {"product_reference_image", "scene_reference_image", "storyboard_image"}
    if not no_people:
        prompt_kinds.add("character_prompt")
        image_kinds.add("character_reference_image")
        for asset in project.get("assets", []):
            if isinstance(asset, dict) and asset.get("type") == "character":
                asset_id = str(asset.get("id", ""))
                if character_image_counts.get(asset_id) != 1:
                    errors.append(f"character {asset_id} requires exactly one reference image entry")
    if product_kind == "app":
        image_kinds.add("app_store_screenshot")
    for kind in sorted(prompt_kinds - present_kinds):
        errors.append(f"delivery is missing present prompt kind: {kind}")
    for kind in sorted(image_kinds - present_kinds - unavailable_kinds):
        errors.append(f"delivery is missing present or unavailable image kind: {kind}")
    if product_kind == "app" and "product_reference_image" not in present_kinds:
        errors.append("app delivery requires an authentic present product_reference_image")
    for image_kind in sorted(unavailable_kinds & set(GENERATABLE_IMAGE_PROMPTS)):
        if GENERATABLE_IMAGE_PROMPTS[image_kind] not in present_kinds:
            errors.append(f"unavailable {image_kind} requires {GENERATABLE_IMAGE_PROMPTS[image_kind]}")
    if unavailable_kinds and render_status != "partial":
        errors.append("unavailable generated images require delivery.render_status partial")
    if render_status == "partial" and not unavailable_kinds:
        errors.append("delivery.render_status partial requires an unavailable generated image")
    if bool(gates.get("storyboard_rendered")) != ("storyboard_image" in present_kinds):
        errors.append("gates.storyboard_rendered must match storyboard_image status")
    if not gates.get("video_prompts_confirmed"):
        errors.append("gates.delivery_ready requires gates.video_prompts_confirmed")
    if not gates.get("storyboard_rendered") and render_status != "partial":
        errors.append("gates.delivery_ready requires gates.storyboard_rendered unless delivery is partial")
    return errors


def validate_research(project: dict[str, Any], selling_points: list[Any]) -> list[str]:
    errors: list[str] = []
    research = project.get("research")
    if not isinstance(research, dict):
        return ["research must be an object"]

    if research.get("status") != "complete":
        errors.append("research.status must be complete before asset design")

    product_kind = research.get("product_kind")
    if product_kind not in VALID_PRODUCT_KINDS:
        errors.append("research.product_kind must be physical_product, app, service, or other")
    for field in ("canonical_name", "model_or_version"):
        if not nonempty(research.get(field)):
            errors.append(f"research.{field} is required")

    sources = research.get("sources")
    if not isinstance(sources, list) or not sources:
        errors.append("research.sources must be a non-empty list")
        sources = []

    source_urls: set[str] = set()
    first_party_count = 0
    for index, source in enumerate(sources):
        if not isinstance(source, dict):
            errors.append(f"research.sources[{index}] must be an object")
            continue
        url = str(source.get("url", "")).strip()
        if not valid_url(url):
            errors.append(f"research.sources[{index}].url must be an http(s) URL")
        elif url in source_urls:
            errors.append(f"duplicate research source URL: {url}")
        else:
            source_urls.add(url)
        for field in ("title", "publisher", "source_type", "accessed_on"):
            if not nonempty(source.get(field)):
                errors.append(f"research.sources[{index}].{field} is required")
        if source.get("source_type") in FIRST_PARTY_SOURCE_TYPES:
            first_party_count += 1
    if sources and first_party_count == 0:
        errors.append("research.sources must include at least one first-party source")

    visuals = research.get("visual_references")
    if not isinstance(visuals, list) or not visuals:
        errors.append("research.visual_references must be a non-empty list")
        visuals = []

    visual_kinds: set[str] = set()
    for index, visual in enumerate(visuals):
        if not isinstance(visual, dict):
            errors.append(f"research.visual_references[{index}] must be an object")
            continue
        if not valid_url(visual.get("url")):
            errors.append(f"research.visual_references[{index}].url must be an http(s) URL")
        source_url = str(visual.get("source_url", "")).strip()
        if source_url not in source_urls:
            errors.append(f"research.visual_references[{index}].source_url must match a research source")
        kind = visual.get("kind")
        if kind not in VALID_VISUAL_KINDS:
            errors.append(
                f"research.visual_references[{index}].kind must be product_photo, app_ui, or official_visual"
            )
        else:
            visual_kinds.add(str(kind))
        if not nonempty(visual.get("view_or_screen")):
            errors.append(f"research.visual_references[{index}].view_or_screen is required")

    if product_kind == "physical_product" and "product_photo" not in visual_kinds:
        errors.append("physical product research requires a product_photo visual reference")
    if product_kind == "app" and "app_ui" not in visual_kinds:
        errors.append("app research requires an app_ui visual reference")

    scenarios = research.get("usage_scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        errors.append("research.usage_scenarios must be a non-empty list")
        scenarios = []
    for index, scenario in enumerate(scenarios):
        if not isinstance(scenario, dict):
            errors.append(f"research.usage_scenarios[{index}] must be an object")
            continue
        if not nonempty(scenario.get("scenario")):
            errors.append(f"research.usage_scenarios[{index}].scenario is required")
        evidence_urls = scenario.get("evidence_source_urls")
        if not isinstance(evidence_urls, list) or not evidence_urls:
            errors.append(f"research.usage_scenarios[{index}].evidence_source_urls must be non-empty")
        else:
            for url in evidence_urls:
                if str(url) not in source_urls:
                    errors.append(f"research.usage_scenarios[{index}] references unknown source URL: {url}")

    claims = research.get("selling_points")
    if not isinstance(claims, list) or not claims:
        errors.append("research.selling_points must be a non-empty list")
        claims = []

    verified_claims: set[str] = set()
    for index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            errors.append(f"research.selling_points[{index}] must be an object")
            continue
        claim_text = str(claim.get("claim", "")).strip()
        if not claim_text:
            errors.append(f"research.selling_points[{index}].claim is required")
        status = claim.get("status")
        if status not in VALID_CLAIM_STATES:
            errors.append(f"research.selling_points[{index}].status is invalid")
        evidence_urls = claim.get("evidence_source_urls")
        if status == "verified":
            if claim_text:
                verified_claims.add(claim_text)
            if not isinstance(evidence_urls, list) or not evidence_urls:
                errors.append(
                    f"research.selling_points[{index}] verified claim requires evidence_source_urls"
                )
            else:
                for url in evidence_urls:
                    if str(url) not in source_urls:
                        errors.append(f"research.selling_points[{index}] references unknown source URL: {url}")

    if claims and not verified_claims:
        errors.append("research.selling_points must include at least one verified claim")
    for point in selling_points:
        if str(point) not in verified_claims:
            errors.append(f"brief selling point is not a verified research claim: {point}")

    unresolved = research.get("unresolved")
    if not isinstance(unresolved, list):
        errors.append("research.unresolved must be a list")
    elif unresolved:
        errors.append("research.unresolved must be empty when research.status is complete")

    return errors


def validate(project: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if project.get("version") != PROJECT_VERSION:
        errors.append(f"version must be {PROJECT_VERSION}")
    errors.extend(validate_output_policy(project))
    brief = project.get("brief")
    if not isinstance(brief, dict):
        return ["brief must be an object"]

    for field in REQUIRED_BRIEF_FIELDS:
        if not nonempty(brief.get(field)):
            errors.append(f"brief.{field} is required")

    selling_points = brief.get("selling_points", [])
    if not isinstance(selling_points, list) or not selling_points or not all(nonempty(x) for x in selling_points):
        errors.append("brief.selling_points must be a non-empty list of non-empty values")
        selling_points = []

    whitelist = brief.get("core_function_whitelist")
    research_claims = list(selling_points)
    if isinstance(whitelist, list):
        research_claims.extend(point for point in whitelist if point not in research_claims)
    errors.extend(validate_research(project, research_claims))

    try:
        duration = float(brief.get("duration_seconds", 0))
        if duration <= 0:
            errors.append("brief.duration_seconds must be greater than zero")
    except (TypeError, ValueError):
        duration = 0.0
        errors.append("brief.duration_seconds must be numeric")

    people = str(brief.get("people", "")).strip().lower()
    no_people = people in {"none", "no people", "product only", "无人物", "纯产品"}
    creative_style = brief.get("creative_style")
    errors.extend(validate_style(creative_style, brief.get("animation_style"), "brief."))
    if creative_style == "dialogue_drama" and no_people:
        errors.append("brief.creative_style dialogue_drama requires people who can participate in dialogue")
    dialogue_mode = brief.get("dialogue_mode")
    if dialogue_mode is not None and dialogue_mode not in VALID_DIALOGUE_MODES:
        errors.append("brief.dialogue_mode must be continuous_spoken, mixed, or visual_only")
    if dialogue_mode is None:
        dialogue_mode = "continuous_spoken" if creative_style == "ugc_native_vlog" and not no_people else "mixed"
    errors.extend(validate_production_controls(brief, selling_points, no_people))

    assets = project.get("assets", [])
    if not isinstance(assets, list):
        errors.append("assets must be a list")
        assets = []

    ids: set[str] = set()
    assets_by_type: dict[str, list[dict[str, Any]]] = {}
    for index, asset in enumerate(assets):
        if not isinstance(asset, dict):
            errors.append(f"assets[{index}] must be an object")
            continue
        asset_id = asset.get("id")
        if not nonempty(asset_id):
            errors.append(f"assets[{index}].id is required")
        elif str(asset_id) in ids:
            errors.append(f"duplicate asset id: {asset_id}")
        else:
            ids.add(str(asset_id))
        asset_type = asset.get("type")
        if not nonempty(asset_type):
            errors.append(f"assets[{index}].type is required")
        else:
            assets_by_type.setdefault(str(asset_type), []).append(asset)
        if asset.get("status") not in VALID_ASSET_STATES:
            errors.append(f"assets[{index}].status must be draft, rendered, or approved")
        if not nonempty(asset.get("prompt")):
            errors.append(f"assets[{index}].prompt is required for reproducibility")
        if asset_type == "character":
            image_refs = asset.get("image_refs", [])
            if not isinstance(image_refs, list) or len(image_refs) > 1:
                errors.append(f"assets[{index}].image_refs must contain at most one image per person")
        if asset_type == "scene":
            errors.extend(validate_normal_state(asset, index))

    for required_type in ("product", "scene"):
        if not assets_by_type.get(required_type):
            errors.append(f"at least one {required_type} asset is required")
    if not no_people and not assets_by_type.get("character"):
        errors.append("at least one character asset is required when people appear")

    gates = project.get("gates", {})
    if not isinstance(gates, dict):
        errors.append("gates must be an object")
        gates = {}
    if gates.get("style_confirmed") is not True:
        errors.append("gates.style_confirmed must be true before asset design")

    candidates = project.get("creative_candidates", [])
    if not isinstance(candidates, list):
        errors.append("creative_candidates must be a list")
    elif not candidates and assets and type(brief.get("creative_candidate_count")) is int and brief["creative_candidate_count"] > 1:
        errors.append("creative_candidates are required before asset design when multiple candidates are planned")
    elif candidates:
        candidate_ids: set[str] = set()
        for index, candidate in enumerate(candidates):
            if not isinstance(candidate, dict):
                errors.append(f"creative_candidates[{index}] must be an object")
                continue
            candidate_id = candidate.get("concept_id")
            if not isinstance(candidate_id, str) or not candidate_id.strip():
                errors.append(f"creative_candidates[{index}].concept_id is required")
            elif candidate_id in candidate_ids:
                errors.append(f"duplicate creative candidate id: {candidate_id}")
            else:
                candidate_ids.add(candidate_id)
            if type(candidate.get("seed")) is not int:
                errors.append(f"creative_candidates[{index}].seed must be an integer")
            if not isinstance(candidate.get("summary"), str) or not candidate["summary"].strip():
                errors.append(f"creative_candidates[{index}].summary is required")
            if candidate.get("primary_claim") not in selling_points:
                errors.append(f"creative_candidates[{index}].primary_claim must be a selected selling point")
        if brief.get("creative_candidate_count", len(candidates)) != len(candidates):
            errors.append("creative_candidate_count must match stored candidates")
        creative = project.get("creative", {})
        selected = creative.get("selected_candidate_id") if isinstance(creative, dict) else None
        if selected is not None and (not isinstance(selected, str) or selected not in candidate_ids):
            errors.append("creative.selected_candidate_id must identify a stored candidate")
        elif assets and len(candidates) > 1 and selected is None:
            errors.append("select a valid creative.selected_candidate_id before asset design")
        elif isinstance(selected, str) and selected in candidate_ids:
            chosen = next(c for c in candidates if isinstance(c, dict) and c.get("concept_id") == selected)
            if chosen.get("primary_claim") != brief.get("primary_claim"):
                errors.append("selected candidate primary_claim must match brief.primary_claim")

    if gates.get("assets_approved"):
        required_types = ["product", "scene"] + ([] if no_people else ["character"])
        for required_type in required_types:
            relevant = assets_by_type.get(required_type, [])
            if not relevant or any(asset.get("status") != "approved" for asset in relevant):
                errors.append(f"gates.assets_approved requires every {required_type} asset to be approved")

    shots = project.get("shots", [])
    if not isinstance(shots, list):
        errors.append("shots must be a list")
        shots = []

    if shots:
        shot_ids: set[str] = set()
        covered_points: set[str] = set()
        previous_end = 0.0
        hardware_visible_count = 0
        for index, shot in enumerate(shots):
            if not isinstance(shot, dict):
                errors.append(f"shots[{index}] must be an object")
                continue
            shot_id = shot.get("id")
            if not nonempty(shot_id):
                errors.append(f"shots[{index}].id is required")
            elif str(shot_id) in shot_ids:
                errors.append(f"duplicate shot id: {shot_id}")
            else:
                shot_ids.add(str(shot_id))
            try:
                start = float(shot.get("start"))
                end = float(shot.get("end"))
            except (TypeError, ValueError):
                errors.append(f"shots[{index}] start and end must be numeric")
                continue
            if end <= start:
                errors.append(f"shots[{index}] end must be greater than start")
            if abs(start - previous_end) > 0.05:
                errors.append(f"shots[{index}] must start at {previous_end:g}, got {start:g}")
            previous_end = end
            if not nonempty(shot.get("action")):
                errors.append(f"shots[{index}].action is required")
            if not nonempty(shot.get("completion_state")):
                errors.append(f"shots[{index}].completion_state is required")

            featured_person = shot.get("featured_person")
            if not isinstance(featured_person, bool):
                errors.append(f"shots[{index}].featured_person must be boolean")
            elif no_people and featured_person:
                errors.append(f"shots[{index}] cannot feature a person when brief.people is no people")

            if "hardware_visible" in shot:
                if not isinstance(shot.get("hardware_visible"), bool):
                    errors.append(f"shots[{index}].hardware_visible must be boolean when provided")
                elif shot.get("hardware_visible"):
                    hardware_visible_count += 1

            atmosphere = shot.get("environment_atmosphere")
            if not isinstance(atmosphere, dict):
                errors.append(f"shots[{index}].environment_atmosphere must be an object")
            else:
                for field in ATMOSPHERE_FIELDS:
                    if not nonempty(atmosphere.get(field)):
                        errors.append(f"shots[{index}].environment_atmosphere.{field} is required")

            performance = shot.get("performance")
            if featured_person:
                if not isinstance(performance, dict):
                    errors.append(f"shots[{index}].performance must be an object for a featured person")
                else:
                    for field in PERFORMANCE_FIELDS:
                        if not nonempty(performance.get(field)):
                            errors.append(f"shots[{index}].performance.{field} is required")
                    if performance.get("intensity") not in VALID_PERFORMANCE_INTENSITIES:
                        errors.append(
                            f"shots[{index}].performance.intensity must be subtle, restrained, or moderate"
                        )
            elif performance is not None and not isinstance(performance, dict):
                errors.append(f"shots[{index}].performance must be an object when provided")

            dialogue = shot.get("dialogue")
            if not isinstance(dialogue, list):
                errors.append(f"shots[{index}].dialogue must be a list")
            else:
                if dialogue and not featured_person:
                    errors.append(f"shots[{index}] with dialogue must feature a person")
                if dialogue and ("core_function_whitelist" in brief or "action_speech_relation" in shot) and not (isinstance(shot.get("action_speech_relation"), str) and shot["action_speech_relation"].strip()):
                    errors.append(f"shots[{index}].action_speech_relation is required when dialogue is present")
                if (
                    creative_style == "ugc_native_vlog"
                    and dialogue_mode == "continuous_spoken"
                    and featured_person
                    and not dialogue
                    and not nonempty(shot.get("silent_beat_reason"))
                ):
                    errors.append(
                        f"shots[{index}] featured-person UGC shot requires dialogue or silent_beat_reason"
                    )
                for turn_index, turn in enumerate(dialogue):
                    if not isinstance(turn, dict):
                        errors.append(f"shots[{index}].dialogue[{turn_index}] must be an object")
                        continue
                    for field in ("speaker", "line", "tone", "reaction"):
                        if not nonempty(turn.get(field)):
                            errors.append(
                                f"shots[{index}].dialogue[{turn_index}].{field} is required"
                            )

            refs = shot.get("asset_refs", [])
            if not isinstance(refs, list) or not refs:
                errors.append(f"shots[{index}].asset_refs must be a non-empty list")
            else:
                for ref in refs:
                    if str(ref) not in ids:
                        errors.append(f"shots[{index}] references unknown asset: {ref}")
            points = shot.get("selling_points", [])
            if not isinstance(points, list):
                errors.append(f"shots[{index}].selling_points must be a list")
            else:
                covered_points.update(str(point) for point in points)
                for point in points:
                    if point not in selling_points:
                        errors.append(f"shots[{index}] uses a selling point outside brief.selling_points: {point}")

        if duration and abs(previous_end - duration) > 0.05:
            errors.append(f"shots end at {previous_end:g}s but brief duration is {duration:g}s")
        if brief.get("hardware_display_required") == "required" and hardware_visible_count == 0:
            errors.append("brief.hardware_display_required required at least one shot with hardware_visible true")
        for point in selling_points:
            if str(point) not in covered_points:
                errors.append(f"selling point is not mapped to any shot: {point}")

    errors.extend(validate_shot_dialogue(shots, dialogue_mode=dialogue_mode, creative_style=creative_style))

    if gates.get("storyboard_ready") and not gates.get("assets_approved"):
        errors.append("gates.storyboard_ready requires gates.assets_approved")
    if gates.get("storyboard_ready") and not shots:
        errors.append("gates.storyboard_ready requires shots")
    if gates.get("video_prompts_ready") and not gates.get("storyboard_ready"):
        errors.append("gates.video_prompts_ready requires gates.storyboard_ready")

    if gates.get("video_prompts_confirmed") and not gates.get("video_prompts_ready"):
        errors.append("gates.video_prompts_confirmed requires gates.video_prompts_ready")
    if gates.get("video_prompts_confirmed") and not gates.get("pre_confirmation_audit"):
        errors.append("gates.video_prompts_confirmed requires gates.pre_confirmation_audit")
    if gates.get("storyboard_rendered") and not gates.get("video_prompts_confirmed"):
        errors.append("gates.storyboard_rendered requires gates.video_prompts_confirmed")
    if gates.get("delivery_ready") and not gates.get("storyboard_rendered"):
        delivery_state = project.get("delivery")
        if not isinstance(delivery_state, dict) or delivery_state.get("render_status") != "partial":
            errors.append("gates.delivery_ready requires gates.storyboard_rendered unless delivery is partial")
    research_state = project.get("research")
    product_kind = research_state.get("product_kind") if isinstance(research_state, dict) else None
    errors.extend(validate_delivery(project, no_people, product_kind))

    return errors


def sample_project() -> dict[str, Any]:
    valid = {
        "version": 8,
        "output_policy": {
            "prompt_language": "zh-CN",
            "subtitles": "none",
            "music": "none",
            "allowed_audio": ["ambient_sound", "dialogue"],
            "app_ui_prompt_detail": "state_only",
        },
        "research": {
            "status": "complete",
            "product_kind": "physical_product",
            "canonical_name": "Bottle Model X",
            "model_or_version": "Model X / CN",
            "sources": [
                {
                    "url": "https://example.com/model-x",
                    "title": "Official Model X page",
                    "publisher": "Example",
                    "source_type": "official_product_page",
                    "accessed_on": "2026-09-21",
                }
            ],
            "visual_references": [
                {
                    "url": "https://example.com/model-x-front.jpg",
                    "source_url": "https://example.com/model-x",
                    "kind": "product_photo",
                    "view_or_screen": "front three-quarter",
                }
            ],
            "usage_scenarios": [
                {
                    "scenario": "Cold drinks during outdoor exercise",
                    "evidence_source_urls": ["https://example.com/model-x"],
                }
            ],
            "selling_points": [
                {
                    "claim": "Keeps water cold",
                    "status": "verified",
                    "evidence_source_urls": ["https://example.com/model-x"],
                }
            ],
            "unresolved": [],
        },
        "brief": {
            "product_name": "Bottle",
            "selling_points": ["Keeps water cold"],
            "core_function_whitelist": ["Keeps water cold"],
            "primary_claim": "Keeps water cold",
            "people": "One runner",
            "actor_count": 1,
            "scene": "City park",
            "scene_count": 1,
            "hardware_device": "Bottle",
            "hardware_display_required": "required",
            "hardware_display_reason": "The bottle is held during the proof",
            "creative_candidate_count": 1,
            "duration_seconds": 6,
            "creative_style": "ugc_native_vlog",
        },
        "assets": [
            {"id": "PROD-01", "type": "product", "status": "approved", "prompt": "Product board"},
            {"id": "CHAR-01", "type": "character", "status": "approved", "prompt": "Character board"},
            {
                "id": "SCENE-01",
                "type": "scene",
                "status": "approved",
                "prompt": "Scene board",
                "normal_state": {
                    "contextual_occupancy": "A few pedestrians pass through the city park",
                    "lived_in_traces": "Used bench, water bottle, and casual bags",
                    "ambient_activity": "Distant runners move slowly out of focus",
                },
            },
        ],
        "gates": {
            "style_confirmed": True,
            "assets_approved": True,
            "storyboard_ready": True,
            "video_prompts_ready": True,
        },
        "shots": [
            {
                "id": "SHOT-001",
                "start": 0,
                "end": 3,
                "featured_person": True,
                "performance": {
                    "expression": "Eyes soften and mouth corners rise slightly",
                    "gaze": "Looks from the path down to the bottle",
                    "micro_movement": "Blinks once and exhales gently",
                    "body_language": "Shoulders release while the wrist stays relaxed",
                    "intensity": "subtle",
                },
                "action": "Right fingers close slowly around the bottle",
                "completion_state": "Bottle rests steadily at chest height",
                "action_speech_relation": "She speaks at a normal conversational pace while lifting the bottle to chest height",
                "hardware_visible": True,
                "environment_atmosphere": {
                    "summary": "Quiet city park in soft morning light",
                    "ambient_sound": "Quiet park tone and soft fabric movement",
                },
                "dialogue": [
                    {
                        "speaker": "Runner",
                        "line": "出门带着这杯水，跑完还能喝口凉的。",
                        "tone": "Soft, relaxed, with a slight breathiness",
                        "reaction": "Companion glances at the bottle and nods once",
                    }
                ],
                "asset_refs": ["PROD-01", "CHAR-01", "SCENE-01"],
                "selling_points": ["Keeps water cold"],
            },
            {
                "id": "SHOT-002",
                "start": 3,
                "end": 6,
                "featured_person": False,
                "action": "Condensation forms slowly on the bottle surface",
                "completion_state": "Fine droplets remain stable on the bottle",
                "environment_atmosphere": {
                    "summary": "Quiet restrained bottle close-up",
                    "ambient_sound": "Restrained park ambience",
                },
                "dialogue": [],
                "asset_refs": ["PROD-01", "CHAR-01", "SCENE-01"],
                "selling_points": [],
                "hardware_visible": True,
            },
        ],
    }
    return valid


def self_test() -> int:
    valid = sample_project()
    errors = validate(valid)
    if errors:
        print("self-test failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    split_character = json.loads(json.dumps(valid))
    split_character["assets"][1]["image_refs"] = ["face.png", "body.png"]
    if not any("at most one image per person" in error for error in validate(split_character)):
        print("self-test failed: split character image_refs were accepted")
        return 1
    invalid = json.loads(json.dumps(valid))
    invalid["shots"][1]["end"] = 5
    if not validate(invalid):
        print("self-test failed: invalid fixture unexpectedly passed")
        return 1
    invalid_research = json.loads(json.dumps(valid))
    invalid_research["research"]["visual_references"][0]["kind"] = "app_ui"
    research_errors = validate(invalid_research)
    if not any("product_photo" in error for error in research_errors):
        print("self-test failed: physical product visual violation was not detected")
        return 1
    invalid_performance = json.loads(json.dumps(valid))
    invalid_performance["shots"][0]["performance"]["intensity"] = "exaggerated"
    performance_errors = validate(invalid_performance)
    if not any("subtle, restrained, or moderate" in error for error in performance_errors):
        print("self-test failed: exaggerated performance intensity was not detected")
        return 1
    invalid_policy = json.loads(json.dumps(valid))
    invalid_policy["output_policy"]["music"] = "background_music"
    policy_errors = validate(invalid_policy)
    if not any("output_policy.music must be none" in error for error in policy_errors):
        print("self-test failed: music policy violation was not detected")
        return 1
    invalid_dialogue = json.loads(json.dumps(valid))
    invalid_dialogue["shots"][0]["dialogue"][0]["tone"] = ""
    dialogue_errors = validate(invalid_dialogue)
    if not any("dialogue[0].tone is required" in error for error in dialogue_errors):
        print("self-test failed: missing dialogue tone was not detected")
        return 1
    invalid_ugc_dialogue = json.loads(json.dumps(valid))
    invalid_ugc_dialogue["shots"][0]["dialogue"] = []
    ugc_dialogue_errors = validate(invalid_ugc_dialogue)
    if not any("featured-person UGC shot requires dialogue" in error for error in ugc_dialogue_errors):
        print("self-test failed: silent featured-person UGC shot was not detected")
        return 1
    invalid_normal_state = json.loads(json.dumps(valid))
    del invalid_normal_state["assets"][2]["normal_state"]
    normal_state_errors = validate(invalid_normal_state)
    if not any("assets[2].normal_state must be an object for scene assets" in error for error in normal_state_errors):
        print("self-test failed: missing scene normal state was not detected")
        return 1
    invalid_style = json.loads(json.dumps(valid))
    invalid_style["brief"]["creative_style"] = "cinematic"
    style_errors = validate(invalid_style)
    if not any("brief.creative_style must be" in error for error in style_errors):
        print("self-test failed: invalid creative style was not detected")
        return 1
    unconfirmed_style = json.loads(json.dumps(valid))
    unconfirmed_style["gates"]["style_confirmed"] = False
    style_gate_errors = validate(unconfirmed_style)
    if not any("gates.style_confirmed must be true" in error for error in style_gate_errors):
        print("self-test failed: unconfirmed style gate was not detected")
        return 1
    invalid_delivery = json.loads(json.dumps(valid))
    invalid_delivery["gates"]["delivery_ready"] = True
    delivery_errors = validate(invalid_delivery)
    if not any("gates.delivery_ready requires gates.storyboard_rendered" in error for error in delivery_errors):
        print("self-test failed: incomplete delivery gate was not detected")
        return 1
    partial_delivery = json.loads(json.dumps(valid))
    partial_delivery["gates"].update(
        {
            "pre_confirmation_audit": True,
            "video_prompts_confirmed": True,
            "storyboard_rendered": False,
            "delivery_ready": True,
        }
    )
    partial_delivery["delivery"] = {
        "audit_status": "complete",
        "render_status": "partial",
        "folder_name": "product-video-delivery",
        "files": [
            {"path": "prompts/product-asset.md", "kind": "product_prompt", "purpose": "产品生图", "status": "present", "source_asset_id": "PROD-01", "approved": True},
            {"path": "prompts/character-asset.md", "kind": "character_prompt", "purpose": "人物生图", "status": "present", "source_asset_id": "CHAR-01", "approved": True},
            {"path": "prompts/scene-asset.md", "kind": "scene_prompt", "purpose": "场景生图", "status": "present", "source_asset_id": "SCENE-01", "approved": True},
            {"path": "prompts/storyboard.md", "kind": "storyboard_prompt", "purpose": "故事版生图", "status": "present", "source_asset_id": "SHOT-001", "approved": False},
            {"path": "prompts/video-prompts.md", "kind": "video_prompt", "purpose": "视频生成", "status": "present", "source_asset_id": "VID-001", "approved": True},
            {"path": "images/product/ref.png", "kind": "product_reference_image", "purpose": "产品参考", "status": "unavailable", "source_asset_id": "PROD-01", "approved": False, "reason": "当前没有生图工具"},
            {"path": "images/character/ref.png", "kind": "character_reference_image", "purpose": "人物参考", "status": "unavailable", "source_asset_id": "CHAR-01", "approved": False, "reason": "当前没有生图工具"},
            {"path": "images/scene/ref.png", "kind": "scene_reference_image", "purpose": "场景参考", "status": "unavailable", "source_asset_id": "SCENE-01", "approved": False, "reason": "当前没有生图工具"},
            {"path": "images/storyboard/contact.png", "kind": "storyboard_image", "purpose": "故事版参考", "status": "unavailable", "source_asset_id": "SHOT-001", "approved": False, "reason": "当前没有生图工具"},
        ],
    }
    partial_errors = validate(partial_delivery)
    if partial_errors:
        print("self-test failed: prompt-ready partial delivery was rejected:")
        for error in partial_errors:
            print(f"- {error}")
        return 1
    duplicate_character_image = json.loads(json.dumps(partial_delivery))
    duplicate_character_image["delivery"]["files"].append({
        "path": "images/character/extra.png", "kind": "character_reference_image",
        "purpose": "重复人物参考", "status": "unavailable", "source_asset_id": "CHAR-01",
        "approved": False, "reason": "当前没有生图工具",
    })
    if not any("requires exactly one reference image entry" in error for error in validate(duplicate_character_image)):
        print("self-test failed: duplicate character delivery image was accepted")
        return 1
    missing_video_prompt = json.loads(json.dumps(partial_delivery))
    missing_video_prompt["delivery"]["files"][4]["status"] = "unavailable"
    missing_video_prompt["delivery"]["files"][4]["reason"] = "错误标记"
    if not any("video_prompt" in error for error in validate(missing_video_prompt)):
        print("self-test failed: unavailable video prompt was not rejected")
        return 1
    missing_reason = json.loads(json.dumps(partial_delivery))
    del missing_reason["delivery"]["files"][5]["reason"]
    if not any("reason is required" in error for error in validate(missing_reason)):
        print("self-test failed: unavailable image without reason was not rejected")
        return 1
    app_delivery = json.loads(json.dumps(partial_delivery))
    app_delivery["research"]["product_kind"] = "app"
    app_delivery["research"]["visual_references"][0]["kind"] = "app_ui"
    app_delivery["delivery"]["files"].append({
        "path": "images/app-store/listing.png", "kind": "app_store_screenshot",
        "purpose": "苹果应用商店介绍", "status": "unavailable", "approved": False,
        "source_url": "https://example.com/app-store", "reason": "未取得截图",
    })
    if not any("app_store_screenshot must be present" in error for error in validate(app_delivery)):
        print("self-test failed: unavailable App Store screenshot was not rejected")
        return 1
    app_delivery["delivery"]["files"][5]["status"] = "present"
    app_delivery["delivery"]["files"][5]["approved"] = True
    del app_delivery["delivery"]["files"][5]["reason"]
    app_delivery["delivery"]["files"][9]["status"] = "present"
    app_delivery["delivery"]["files"][9]["approved"] = True
    app_delivery["delivery"]["files"][9]["source_url"] = "https://apps.apple.com/cn/app/example"
    del app_delivery["delivery"]["files"][9]["reason"]
    if app_errors := validate(app_delivery):
        print("self-test failed: authentic app screenshot delivery was rejected:")
        for error in app_errors:
            print(f"- {error}")
        return 1
    print("self-test passed")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", nargs="?", help="Project JSON path, or - for stdin")
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.self_test:
        return self_test()
    if not args.project:
        raise SystemExit("provide a project JSON path or use --self-test")
    project = load_project(args.project)
    errors = validate(project)
    if errors:
        print("validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
