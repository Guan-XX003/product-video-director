#!/usr/bin/env python3
"""Validate a Doubao Seedance 2.0 delivery package."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from style_contract import validate_style
from dialogue_quality import validate_shot_dialogue


VALID_TASK_TYPES = {"full_modal_reference", "edit", "extend", "combined"}
VALID_SLOT_TYPES = {"image": "图片", "video": "视频", "audio": "音频"}
VALID_PERSON_REFERENCE_MODES = {"none", "single_image"}
VALID_SUBJECT_KINDS = {"person", "product", "scene", "other"}
VALID_PERFORMANCE_INTENSITIES = {"subtle", "restrained", "moderate"}
VALID_DIALOGUE_MODES = {"continuous_spoken", "mixed", "visual_only"}
PERFORMANCE_FIELDS = ("expression", "gaze", "micro_movement", "body_language")
ATMOSPHERE_FIELDS = ("summary", "ambient_sound")
REQUIRED_PROMPT_POLICIES = (
    "不要生成额外字幕、标题、贴纸或说明文字",
    "不要添加背景音乐",
    "仅保留环境音与人物对白",
)
APP_UI_POLICY_TEXT = "保留参考图中真实 App 界面的原有文字，不新增或改写界面内容"
APP_UI_REFERENCE_FIELDS = {"slot", "screen_state", "interaction"}
PROHIBITED_CHARACTER_FORMATS = {
    "character_turnaround", "character_multiview", "single_face", "single_fullbody"
}
INTERNAL_ID_PATTERN = re.compile(
    r"(?<![A-Z0-9])(?:PROD|CHAR|SCENE|SHOT|VID)-\d+[A-Z-]*(?![A-Z0-9-])",
    re.IGNORECASE,
)
TIMECODE_PATTERN = re.compile(
    r"(?:\b\d{1,2}:\d{2}(?::\d{2})?\b|\b\d+(?:\.\d+)?\s*(?:-|–|—|~|至|到)\s*\d+(?:\.\d+)?\s*秒)"
)
SHOT_PATTERN = re.compile(r"镜头\s*(\d+)")
MUSIC_INSTRUCTION_PATTERN = re.compile(
    r"(?:背景音乐|配乐|\bBGM\b|音乐响起|播放[^\n。；]{0,24}音乐|电子音乐|电子节奏)",
    re.IGNORECASE,
)
SUBTITLE_NOTATION_PATTERN = re.compile(r"【[^】\n]+】")


def nonempty(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, tuple, dict)):
        return bool(value)
    return True


def load_package(source: str) -> dict[str, Any]:
    if source == "-":
        return json.load(sys.stdin)
    return json.loads(Path(source).read_text(encoding="utf-8"))


def slot_kind(slot: str) -> str | None:
    for kind, prefix in VALID_SLOT_TYPES.items():
        if re.fullmatch(rf"{prefix}[1-9]\d*", slot):
            return kind
    return None


def prompt_contains(prompt: str, value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    return re.sub(r"\s+", "", value) in re.sub(r"\s+", "", prompt)


def validate_audio_policy(package: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    policy = package.get("audio_policy")
    if not isinstance(policy, dict):
        return ["audio_policy must be an object"]
    if policy.get("music") != "none":
        errors.append("audio_policy.music must be none")
    if policy.get("subtitles") != "none":
        errors.append("audio_policy.subtitles must be none")
    allowed_audio = policy.get("allowed_audio")
    if not isinstance(allowed_audio, list) or set(allowed_audio) != {"ambient_sound", "dialogue"}:
        errors.append("audio_policy.allowed_audio must contain only ambient_sound and dialogue")
    return errors


def validate_contiguous_slots(slots: set[str]) -> list[str]:
    errors: list[str] = []
    for prefix in VALID_SLOT_TYPES.values():
        numbers = sorted(
            int(match.group(1))
            for slot in slots
            if (match := re.fullmatch(rf"{prefix}([1-9]\d*)", slot))
        )
        if numbers and numbers != list(range(1, len(numbers) + 1)):
            errors.append(f"{prefix} slots must be contiguous starting at {prefix}1")
    return errors


def validate(package: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if package.get("target") != "doubao-seedance-2.0":
        errors.append("target must be doubao-seedance-2.0")
    if package.get("task_type") not in VALID_TASK_TYPES:
        errors.append("task_type must be full_modal_reference, edit, extend, or combined")

    if package.get("task_type") in {"full_modal_reference", "combined"}:
        errors.extend(validate_style(package.get("creative_style"), package.get("animation_style")))
    if package.get("task_type") in {"full_modal_reference", "combined"} and package.get("prompt_language") != "zh-CN":
        errors.append("prompt_language must be zh-CN for generation packages")

    dialogue_mode = package.get("dialogue_mode")
    if dialogue_mode is not None and dialogue_mode not in VALID_DIALOGUE_MODES:
        errors.append("dialogue_mode must be continuous_spoken, mixed, or visual_only")
    if dialogue_mode is None:
        dialogue_mode = "continuous_spoken" if package.get("creative_style") == "ugc_native_vlog" else "mixed"

    person_reference_mode = package.get("person_reference_mode")
    if person_reference_mode not in VALID_PERSON_REFERENCE_MODES:
        errors.append("person_reference_mode must be none or single_image")
    errors.extend(validate_audio_policy(package))
    if package.get("app_ui_prompt_detail") != "state_only":
        errors.append("app_ui_prompt_detail must be state_only")

    try:
        duration = float(package.get("duration_seconds", 0))
        if duration <= 0:
            errors.append("duration_seconds must be greater than zero")
    except (TypeError, ValueError):
        errors.append("duration_seconds must be numeric")

    manifest = package.get("manifest")
    if not isinstance(manifest, list) or not manifest:
        errors.append("manifest must be a non-empty list")
        manifest = []

    slots: set[str] = set()
    priorities: set[int] = set()
    manifest_slots: list[str] = []
    manifest_formats: list[str] = []
    manifest_formats_by_slot: dict[str, str] = {}
    person_asset_ids: set[str] = set()
    for index, item in enumerate(manifest):
        if not isinstance(item, dict):
            errors.append(f"manifest[{index}] must be an object")
            continue
        slot = str(item.get("slot", "")).strip()
        kind = slot_kind(slot)
        if not kind:
            errors.append(f"manifest[{index}].slot must look like 图片1, 视频1, or 音频1")
        elif slot in slots:
            errors.append(f"duplicate runtime slot: {slot}")
        else:
            slots.add(slot)
            manifest_slots.append(slot)
        if not nonempty(item.get("asset_id")):
            errors.append(f"manifest[{index}].asset_id is required")
        if not nonempty(item.get("role")):
            errors.append(f"manifest[{index}].role is required")
        media_format = str(item.get("format", "")).strip()
        if not media_format:
            errors.append(f"manifest[{index}].format is required")
        else:
            manifest_formats.append(media_format)
            if slot_kind(slot):
                manifest_formats_by_slot[slot] = media_format
        if media_format in PROHIBITED_CHARACTER_FORMATS:
            errors.append(f"manifest[{index}] must use one single_person image per person, not split or multiview references")
        if media_format == "single_person":
            asset_id = str(item.get("asset_id", "")).strip()
            if asset_id in person_asset_ids:
                errors.append(f"manifest[{index}] duplicates person asset ID: {asset_id}")
            person_asset_ids.add(asset_id)
        if kind == "image" and media_format == "video":
            errors.append(f"manifest[{index}] image slot cannot use video format")
        if kind == "video" and media_format != "video":
            errors.append(f"manifest[{index}] video slot must use video format")
        if kind == "audio" and media_format != "audio":
            errors.append(f"manifest[{index}] audio slot must use audio format")
        priority = item.get("priority")
        if not isinstance(priority, int) or priority <= 0:
            errors.append(f"manifest[{index}].priority must be a positive integer")
        elif priority in priorities:
            errors.append(f"duplicate manifest priority: {priority}")
        else:
            priorities.add(priority)

    errors.extend(validate_contiguous_slots(slots))

    task_type = package.get("task_type")
    if task_type in {"full_modal_reference", "combined"} and not {
        "product_multiview",
        "app_ui",
    }.intersection(manifest_formats):
        errors.append(f"{task_type} must include a product_multiview or app_ui reference")
    if person_reference_mode == "none" and "single_person" in manifest_formats:
        errors.append("person_reference_mode none must not include person reference images")
    if person_reference_mode == "single_image" and "single_person" not in manifest_formats:
        errors.append("person_reference_mode single_image requires a single_person reference")

    prompt = package.get("prompt")
    if not isinstance(prompt, str) or not prompt.strip():
        errors.append("prompt must be a non-empty string")
        prompt = ""

    internal_ids = sorted(set(INTERNAL_ID_PATTERN.findall(prompt)))
    if internal_ids:
        errors.append(f"prompt contains internal asset IDs: {', '.join(internal_ids)}")

    unknown_slots = sorted(
        slot
        for slot in set(re.findall(r"(?:图片|视频|音频)[1-9]\d*", prompt))
        if slot not in slots
    )
    if unknown_slots:
        errors.append(f"prompt references slots missing from manifest: {', '.join(unknown_slots)}")

    unused_slots = [slot for slot in manifest_slots if slot not in prompt]
    if unused_slots:
        errors.append(f"manifest slots are not referenced in prompt: {', '.join(unused_slots)}")

    if TIMECODE_PATTERN.search(prompt):
        errors.append("prompt contains exact timecodes; keep exact seconds in the external storyboard")
    for policy_text in REQUIRED_PROMPT_POLICIES:
        if not prompt_contains(prompt, policy_text):
            errors.append(f"prompt must include policy: {policy_text}")
    music_scan = prompt.replace("不要添加背景音乐", "")
    if MUSIC_INSTRUCTION_PATTERN.search(music_scan):
        errors.append("prompt contains a music instruction; only ambient sound and dialogue are allowed")
    if SUBTITLE_NOTATION_PATTERN.search(prompt):
        errors.append("prompt contains requested-subtitle notation 【...】")

    app_ui_references = package.get("app_ui_references", [])
    if not isinstance(app_ui_references, list):
        errors.append("app_ui_references must be a list")
        app_ui_references = []
    if "app_ui" in manifest_formats and not app_ui_references:
        errors.append("app_ui manifest requires a non-empty app_ui_references list")
    for index, ui_reference in enumerate(app_ui_references):
        if not isinstance(ui_reference, dict):
            errors.append(f"app_ui_references[{index}] must be an object")
            continue
        extra_fields = sorted(set(ui_reference) - APP_UI_REFERENCE_FIELDS)
        if extra_fields:
            errors.append(
                f"app_ui_references[{index}] contains over-detailed fields: {', '.join(extra_fields)}"
            )
        slot = str(ui_reference.get("slot", "")).strip()
        if manifest_formats_by_slot.get(slot) != "app_ui":
            errors.append(f"app_ui_references[{index}].slot must point to an app_ui manifest item")
        for field in ("screen_state", "interaction"):
            value = ui_reference.get(field)
            if not nonempty(value):
                errors.append(f"app_ui_references[{index}].{field} is required")
            elif not prompt_contains(prompt, value):
                errors.append(f"app_ui_references[{index}].{field} must appear in prompt")
    if "app_ui" in manifest_formats and not prompt_contains(prompt, APP_UI_POLICY_TEXT):
        errors.append(f"app UI prompt must include policy: {APP_UI_POLICY_TEXT}")

    shot_numbers = [int(value) for value in SHOT_PATTERN.findall(prompt)]
    shots = package.get("shots", [])
    require_shots = task_type == "full_modal_reference"
    if require_shots and (not isinstance(shots, list) or not shots):
        errors.append("full_modal_reference requires a non-empty shots list")
        shots = []
    elif not isinstance(shots, list):
        errors.append("shots must be a list")
        shots = []

    structured_shot_numbers: list[int] = []
    for index, shot in enumerate(shots):
        if not isinstance(shot, dict):
            errors.append(f"shots[{index}] must be an object")
            continue
        label = str(shot.get("label", "")).strip()
        expected_label = f"镜头{index + 1}"
        if label != expected_label:
            errors.append(f"shots[{index}].label must be {expected_label}")
        else:
            structured_shot_numbers.append(index + 1)
        camera_movements = shot.get("camera_movements", [])
        if not isinstance(camera_movements, list):
            errors.append(f"shots[{index}].camera_movements must be a list")
        elif len(camera_movements) > 1:
            errors.append(f"shots[{index}] must contain at most one camera movement")
        elif any(not nonempty(movement) for movement in camera_movements):
            errors.append(f"shots[{index}].camera_movements must not contain empty values")
        action = shot.get("action")
        if not nonempty(action):
            errors.append(f"shots[{index}].action is required")
        elif not prompt_contains(prompt, action):
            errors.append(f"shots[{index}].action must appear in prompt")

        completion_state = shot.get("completion_state")
        if not nonempty(completion_state):
            errors.append(f"shots[{index}].completion_state is required")
        elif not prompt_contains(prompt, completion_state):
            errors.append(f"shots[{index}].completion_state must appear in prompt")

        featured_person = shot.get("featured_person")
        if not isinstance(featured_person, bool):
            errors.append(f"shots[{index}].featured_person must be boolean")
        elif person_reference_mode == "none" and featured_person:
            errors.append(f"shots[{index}] cannot feature a person when person_reference_mode is none")

        atmosphere = shot.get("environment_atmosphere")
        if not isinstance(atmosphere, dict):
            errors.append(f"shots[{index}].environment_atmosphere must be an object")
        else:
            for field in ATMOSPHERE_FIELDS:
                value = atmosphere.get(field)
                if not nonempty(value):
                    errors.append(f"shots[{index}].environment_atmosphere.{field} is required")
                elif not prompt_contains(prompt, value):
                    errors.append(
                        f"shots[{index}].environment_atmosphere.{field} must appear in prompt"
                    )

        performance = shot.get("performance")
        if featured_person:
            if not isinstance(performance, dict):
                errors.append(f"shots[{index}].performance must be an object for a featured person")
            else:
                for field in PERFORMANCE_FIELDS:
                    value = performance.get(field)
                    if not nonempty(value):
                        errors.append(f"shots[{index}].performance.{field} is required")
                    elif not prompt_contains(prompt, value):
                        errors.append(f"shots[{index}].performance.{field} must appear in prompt")
                if performance.get("intensity") not in VALID_PERFORMANCE_INTENSITIES:
                    errors.append(
                        f"shots[{index}].performance.intensity must be subtle, restrained, or moderate"
                    )
        elif performance is not None and not isinstance(performance, dict):
            errors.append(f"shots[{index}].performance must be an object when provided")

        dialogue = shot.get("dialogue")
        if "action_speech_relation" in shot:
            relation = shot.get("action_speech_relation")
            if not isinstance(relation, str) or not relation.strip():
                errors.append(f"shots[{index}].action_speech_relation must be non-empty text")
            elif not prompt_contains(prompt, relation):
                errors.append(f"shots[{index}].action_speech_relation must appear in prompt")
        if not isinstance(dialogue, list):
            errors.append(f"shots[{index}].dialogue must be a list")
        else:
            if dialogue and not featured_person:
                errors.append(f"shots[{index}] with dialogue must feature a person")
            if (
                package.get("creative_style") == "ugc_native_vlog"
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
                    value = turn.get(field)
                    if not nonempty(value):
                        errors.append(f"shots[{index}].dialogue[{turn_index}].{field} is required")
                    elif not prompt_contains(prompt, value):
                        errors.append(
                            f"shots[{index}].dialogue[{turn_index}].{field} must appear in prompt"
                        )

    errors.extend(validate_shot_dialogue(shots, dialogue_mode=dialogue_mode, creative_style=package.get("creative_style")))

    if require_shots or shots or shot_numbers:
        if not shot_numbers:
            errors.append("prompt must contain ordered 镜头N sections")
        elif shot_numbers != list(range(1, len(shot_numbers) + 1)):
            errors.append("镜头 sections must be sequential starting at 镜头1")
        if shots and shot_numbers != structured_shot_numbers:
            errors.append("structured shots must match prompt 镜头N sections")

    if task_type in {"edit", "extend"}:
        if not re.search(r"(?:严格编辑|编辑|延长|生成视频\d+之后|向前延长)视频\d+", prompt):
            errors.append(f"{task_type} prompt must address 视频N directly")
        if re.search(r"参考\s*视频\d+", prompt):
            errors.append(f"{task_type} prompt must not say 参考视频N")

    subjects = package.get("subjects", [])
    if not isinstance(subjects, list):
        errors.append("subjects must be a list")
    else:
        labels: set[str] = set()
        person_slots: set[str] = set()
        for index, subject in enumerate(subjects):
            if not isinstance(subject, dict):
                errors.append(f"subjects[{index}] must be an object")
                continue
            label = str(subject.get("label", "")).strip()
            kind = str(subject.get("kind", "")).strip()
            subject_slots = subject.get("slots", [])
            if not label:
                errors.append(f"subjects[{index}].label is required")
            elif label in labels:
                errors.append(f"duplicate subject label: {label}")
            else:
                labels.add(label)
            if kind not in VALID_SUBJECT_KINDS:
                errors.append(
                    f"subjects[{index}].kind must be person, product, scene, or other"
                )
            if not isinstance(subject_slots, list) or not subject_slots:
                errors.append(f"subjects[{index}].slots must be a non-empty list")
            else:
                for slot in subject_slots:
                    if str(slot) not in slots:
                        errors.append(f"subjects[{index}] references unknown slot: {slot}")
                if kind == "person":
                    if len(subject_slots) != 1 or manifest_formats_by_slot.get(str(subject_slots[0])) != "single_person":
                        errors.append(f"subjects[{index}] person must use exactly one single_person slot")
                    else:
                        slot = str(subject_slots[0])
                        if slot in person_slots:
                            errors.append(f"subjects[{index}] person slot is shared: {slot}")
                        person_slots.add(slot)
            if label and label not in prompt:
                errors.append(f"subject label is not used in prompt: {label}")
        unbound_person_slots = {
            slot for slot, media_format in manifest_formats_by_slot.items()
            if media_format == "single_person"
        } - person_slots
        if unbound_person_slots:
            errors.append("single_person slots must each bind one person subject: " + ", ".join(sorted(unbound_person_slots)))

    return errors


def self_test() -> int:
    valid = {
        "target": "doubao-seedance-2.0",
        "task_type": "full_modal_reference",
        "duration_seconds": 15,
        "creative_style": "ugc_native_vlog",
        "prompt_language": "zh-CN",
        "person_reference_mode": "single_image",
        "audio_policy": {
            "music": "none",
            "subtitles": "none",
            "allowed_audio": ["ambient_sound", "dialogue"],
        },
        "app_ui_prompt_detail": "state_only",
        "manifest": [
            {"slot": "图片1", "asset_id": "CHAR-01", "role": "person_identity", "format": "single_person", "priority": 1},
            {"slot": "图片2", "asset_id": "PROD-01", "role": "product_identity", "format": "product_multiview", "priority": 2},
            {"slot": "图片3", "asset_id": "SCENE-01", "role": "scene", "format": "single_scene", "priority": 3},
        ],
        "subjects": [
            {"label": "跑者", "kind": "person", "slots": ["图片1"]},
            {"label": "产品", "kind": "product", "slots": ["图片2"]},
        ],
        "shots": [
            {
                "label": "镜头1",
                "featured_person": True,
                "camera_movements": ["中景平稳推近"],
                "performance": {
                    "expression": "眼神放松，嘴角轻微上扬",
                    "gaze": "视线先落在产品上",
                    "micro_movement": "自然眨眼一次，呼吸带动肩部轻微起伏",
                    "body_language": "肩膀放松，手腕保持自然",
                    "intensity": "subtle",
                },
                "action": "跑者右手手指缓慢收拢握住产品",
                "completion_state": "产品稳定停在胸前",
                "environment_atmosphere": {
                    "summary": "清晨安静的窗边场景",
                    "ambient_sound": "低弱城市底噪和衣料摩擦声",
                },
                "dialogue": [
                    {
                        "speaker": "跑者",
                        "line": "我刚喝了一口，温度正好",
                        "tone": "轻声、放松、略带气音",
                        "reaction": "同伴先看向她手中的杯子，轻轻点头一次，嘴角略微上扬",
                    }
                ],
            },
            {
                "label": "镜头2",
                "featured_person": False,
                "camera_movements": ["镜头切至产品特写"],
                "action": "产品表面缓慢凝结细小水珠",
                "completion_state": "水珠稳定挂在产品表面",
                "environment_atmosphere": {
                    "summary": "安静克制的产品特写",
                    "ambient_sound": "克制的环境底噪",
                },
                "dialogue": [],
            },
        ],
        "prompt": (
            "将图片1中的女性定义为跑者，将图片2中的保温杯定义为产品，场景参考图片3。\n"
            "镜头1：中景平稳推近，清晨安静的窗边场景，"
            "<低弱城市底噪和衣料摩擦声>。跑者视线先落在产品上，眼神放松，嘴角轻微上扬，"
            "自然眨眼一次，呼吸带动肩部轻微起伏，肩膀放松，手腕保持自然；跑者右手手指缓慢收拢握住产品，"
            "产品稳定停在胸前。跑者用轻声、放松、略带气音的语气说{我刚喝了一口，温度正好}，"
            "同伴先看向她手中的杯子，轻轻点头一次，嘴角略微上扬。\n"
            "镜头2：镜头切至产品特写，安静克制的产品特写，<克制的环境底噪>。"
            "产品表面缓慢凝结细小水珠，水珠稳定挂在产品表面。\n"
            "不要生成额外字幕、标题、贴纸或说明文字。不要添加背景音乐，仅保留环境音与人物对白。"
        ),
    }
    errors = validate(valid)
    if errors:
        print("self-test failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    split_person = json.loads(json.dumps(valid))
    split_person["person_reference_mode"] = "face_and_body"
    split_person["manifest"][0]["format"] = "single_face"
    split_person["manifest"].append({
        "slot": "图片4", "asset_id": "CHAR-01-BODY", "role": "body_styling",
        "format": "single_fullbody", "priority": 4,
    })
    split_person["subjects"][0]["slots"].append("图片4")
    split_person["prompt"] += "图片4"
    split_errors = validate(split_person)
    if not any("single_person" in error for error in split_errors):
        print("self-test failed: split face/body references were accepted")
        return 1

    shared_person = json.loads(json.dumps(valid))
    shared_person["subjects"].append({"label": "同伴", "kind": "person", "slots": ["图片1"]})
    shared_person["prompt"] += "同伴"
    if not any("person slot is shared" in error for error in validate(shared_person)):
        print("self-test failed: two people shared one identity image")
        return 1

    parallel_speech = json.loads(json.dumps(valid))
    relation = "拿起杯子时同步以正常聊天语速说话"
    parallel_speech["shots"][0]["action_speech_relation"] = relation
    if not any("action_speech_relation must appear" in e for e in validate(parallel_speech)):
        print("self-test failed: action/speech relation lost during compilation")
        return 1
    parallel_speech["prompt"] += relation
    if validate(parallel_speech):
        print("self-test failed: compiled action/speech relation was rejected")
        return 1
    parallel_speech["shots"][0]["action_speech_relation"] = ""
    if not any("action_speech_relation must be non-empty" in e for e in validate(parallel_speech)):
        print("self-test failed: empty action/speech relation was accepted")
        return 1

    valid_edit = {
        "target": "doubao-seedance-2.0",
        "task_type": "edit",
        "duration_seconds": 15,
        "person_reference_mode": "none",
        "audio_policy": {
            "music": "none",
            "subtitles": "none",
            "allowed_audio": ["ambient_sound", "dialogue"],
        },
        "app_ui_prompt_detail": "state_only",
        "manifest": [
            {"slot": "视频1", "asset_id": "VID-001", "role": "edit_source", "format": "video", "priority": 1}
        ],
        "subjects": [],
        "shots": [],
        "prompt": (
            "严格编辑视频1，移除画面左上角的价格标签，其他内容、动作和运镜保持不变。"
            "不要生成额外字幕、标题、贴纸或说明文字。不要添加背景音乐，仅保留环境音与人物对白。"
        ),
    }
    edit_errors = validate(valid_edit)
    if edit_errors:
        print("self-test failed for pure edit task:")
        for error in edit_errors:
            print(f"- {error}")
        return 1

    invalid = json.loads(json.dumps(valid))
    invalid["manifest"][0]["format"] = "character_multiview"
    invalid["shots"][0]["camera_movements"].append("绕拍")
    invalid["shots"][0]["performance"]["intensity"] = "exaggerated"
    invalid["prompt"] += " 0-3秒使用CHAR-01。"
    invalid_errors = validate(invalid)
    if not any("multiview" in error for error in invalid_errors):
        print("self-test failed: character multiview violation was not detected")
        return 1
    if not any("timecodes" in error for error in invalid_errors):
        print("self-test failed: timecode violation was not detected")
        return 1
    if not any("internal asset IDs" in error for error in invalid_errors):
        print("self-test failed: internal ID violation was not detected")
        return 1
    if not any("at most one camera movement" in error for error in invalid_errors):
        print("self-test failed: multiple camera movements were not detected")
        return 1
    if not any("subtle, restrained, or moderate" in error for error in invalid_errors):
        print("self-test failed: exaggerated performance intensity was not detected")
        return 1
    invalid_ugc_dialogue = json.loads(json.dumps(valid))
    invalid_ugc_dialogue["shots"][0]["dialogue"] = []
    ugc_dialogue_errors = validate(invalid_ugc_dialogue)
    if not any("featured-person UGC shot requires dialogue" in error for error in ugc_dialogue_errors):
        print("self-test failed: silent featured-person UGC shot was not detected")
        return 1
    invalid_style = json.loads(json.dumps(valid))
    invalid_style["creative_style"] = "cinematic"
    style_errors = validate(invalid_style)
    if not any("creative_style must be" in error for error in style_errors):
        print("self-test failed: invalid creative style was not detected")
        return 1
    invalid_language = json.loads(json.dumps(valid))
    invalid_language["prompt_language"] = "en-US"
    language_errors = validate(invalid_language)
    if not any("prompt_language must be zh-CN" in error for error in language_errors):
        print("self-test failed: invalid prompt language was not detected")
        return 1
    missing_detail = json.loads(json.dumps(valid))
    missing_detail["prompt"] = missing_detail["prompt"].replace("眼神放松，嘴角轻微上扬", "神情自然")
    detail_errors = validate(missing_detail)
    if not any("performance.expression must appear in prompt" in error for error in detail_errors):
        print("self-test failed: omitted performance detail was not detected")
        return 1
    missing_policy = json.loads(json.dumps(valid))
    missing_policy["prompt"] = missing_policy["prompt"].replace("不要添加背景音乐", "")
    policy_errors = validate(missing_policy)
    if not any("不要添加背景音乐" in error for error in policy_errors):
        print("self-test failed: missing no-music policy was not detected")
        return 1
    forbidden_audio = json.loads(json.dumps(valid))
    forbidden_audio["prompt"] += "（背景中播放电子音乐）【我刚喝了一口，温度正好】"
    forbidden_audio_errors = validate(forbidden_audio)
    if not any("contains a music instruction" in error for error in forbidden_audio_errors):
        print("self-test failed: music instruction was not detected")
        return 1
    if not any("requested-subtitle notation" in error for error in forbidden_audio_errors):
        print("self-test failed: subtitle notation was not detected")
        return 1

    print("self-test passed")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("package", nargs="?", help="Seedance package JSON path, or - for stdin")
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.self_test:
        return self_test()
    if not args.package:
        raise SystemExit("provide a package JSON path or use --self-test")
    errors = validate(load_package(args.package))
    if errors:
        print("validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
