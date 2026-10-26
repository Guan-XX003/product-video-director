#!/usr/bin/env python3
"""Choose a reproducible product-video creative direction."""

from __future__ import annotations

import argparse
import json
import math
import random
import secrets

from style_contract import VALID_CREATIVE_STYLES, VALID_ANIMATION_STYLES, validate_style


SHORT_PATTERNS = (
    "product_first_proof",
    "problem_to_proof",
    "sensory_reveal",
)

LONG_PATTERNS = SHORT_PATTERNS + (
    "ritual_to_result",
    "contrast_transformation",
    "micro_story_payoff",
)

HOOKS = {
    "interrupted_routine": ("日常小困扰", 1),
    "result_before_cause": ("结果先行", 0),
    "rapid_physical_proof": ("现场演示", 0),
    "friend_question": ("同伴提问", 2),
    "in_use_observation": ("边用边聊", 1),
    "comparison_moment": ("使用对比", 1),
    "macro_texture_reveal": ("真实细节切入", 0),
    "silent_result_then_context": ("画面结果先行", 0),
    "tactile_trigger": ("操作触发", 1),
    "visual_contradiction": ("可见反差", 0),
    "environment_to_product": ("场景带出产品", 0),
    "direct_question": ("直接提问", 2),
    "misunderstanding": ("轻微误会", 2),
    "companion_notice": ("同伴发现", 2),
    "visible_payoff_first": ("先看到效果", 2),
}

STYLE_POOLS = {
    "ugc_native_vlog": {
        "patterns": ("product_first_proof", "problem_to_proof", "ritual_to_result", "micro_story_payoff"),
        "hooks": ("interrupted_routine", "result_before_cause", "rapid_physical_proof", "friend_question", "in_use_observation", "comparison_moment"),
        "camera_languages": ("phone_handheld_observational", "companion_pov", "intimate_over_shoulder"),
        "scene_progressions": ("single_space_escalation", "foreground_to_world_reveal"),
        "endings": ("human_payoff_then_product", "loopback_to_hook", "result_tableau"),
        "dialogue_strategies": ("continuous_first_person_demo", "connected_companion_exchange"),
    },
    "premium_commercial": {
        "patterns": ("product_first_proof", "sensory_reveal", "contrast_transformation", "ritual_to_result"),
        "hooks": ("macro_texture_reveal", "visual_contradiction", "result_before_cause", "silent_result_then_context", "tactile_trigger", "environment_to_product"),
        "camera_languages": ("precise_studio", "controlled_kinetic", "graphic_match_cut", "macro_to_environment"),
        "scene_progressions": ("single_space_escalation", "foreground_to_world_reveal", "product_triggered_transformation"),
        "endings": ("hero_packshot", "human_payoff_then_product", "result_tableau"),
        "dialogue_strategies": ("sparse_spoken_line", "no_dialogue_product_proof"),
    },
    "dialogue_drama": {
        "patterns": ("problem_to_proof", "micro_story_payoff", "contrast_transformation"),
        "hooks": ("interrupted_routine", "visual_contradiction", "result_before_cause", "direct_question", "misunderstanding", "companion_notice", "visible_payoff_first"),
        "camera_languages": ("motivated_two_shot", "restrained_shot_reverse_shot", "intimate_observational"),
        "scene_progressions": ("single_space_escalation", "foreground_to_world_reveal"),
        "endings": ("human_payoff_then_product", "loopback_to_hook", "result_tableau"),
        "dialogue_strategies": ("responsive_two_person_exchange", "connected_cause_and_payoff"),
    },
}


ANIMATION_POOLS = {
    "stylized_3d": {
        "patterns": ("problem_to_proof", "product_first_proof", "micro_story_payoff"),
        "hooks": ("interrupted_routine", "result_before_cause", "environment_to_product", "friend_question"),
        "camera_languages": ("restrained_character_tracking", "clear_action_medium_shot"),
        "scene_progressions": ("single_space_escalation", "foreground_to_world_reveal"),
        "endings": ("human_payoff_then_product", "result_tableau"),
        "dialogue_strategies": ("character_explanation", "connected_companion_exchange"),
    },
    "stop_motion": {
        "patterns": ("product_first_proof", "sensory_reveal", "ritual_to_result"),
        "hooks": ("macro_texture_reveal", "tactile_trigger", "result_before_cause", "rapid_physical_proof"),
        "camera_languages": ("locked_miniature_camera", "measured_tabletop_reframe"),
        "scene_progressions": ("single_space_escalation", "foreground_to_world_reveal"),
        "endings": ("result_tableau", "loopback_to_hook"),
        "dialogue_strategies": ("character_explanation",),
    },
    "motion_graphics": {
        "patterns": ("product_first_proof", "problem_to_proof", "contrast_transformation"),
        "hooks": ("result_before_cause", "visual_contradiction", "rapid_physical_proof"),
        "camera_languages": ("fixed_graphic_canvas", "clear_layer_transition"),
        "scene_progressions": ("single_canvas_cause_and_effect",),
        "endings": ("result_tableau", "loopback_to_hook"),
        "dialogue_strategies": ("character_explanation",),
    },
}


def pool_for_actor_count(style: str, actor_count: int, animation_style=None) -> dict[str, tuple[str, ...]]:
    source = ANIMATION_POOLS[animation_style] if style == "animation_explainer" else STYLE_POOLS[style]
    pool = {key: tuple(values) for key, values in source.items()}
    pool["hooks"] = tuple(hook for hook in pool["hooks"] if HOOKS[hook][1] <= actor_count)
    if actor_count <= 1:
        pool["camera_languages"] = tuple(camera for camera in pool["camera_languages"] if camera not in {"motivated_two_shot", "restrained_shot_reverse_shot"})
        pool["dialogue_strategies"] = tuple(
            strategy
            for strategy in pool["dialogue_strategies"]
            if strategy not in {"connected_companion_exchange", "responsive_two_person_exchange"}
        )
    if actor_count == 0:
        pool["dialogue_strategies"] = ("no_dialogue_product_proof",)
        pool["camera_languages"] = ("observational_product_closeup",) if style == "ugc_native_vlog" else pool["camera_languages"]
        pool["endings"] = tuple(ending for ending in pool["endings"] if ending != "human_payoff_then_product")
    return pool

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--product", required=True)
    parser.add_argument("--duration", required=True, type=float)
    parser.add_argument("--style", required=True, choices=sorted(VALID_CREATIVE_STYLES))
    parser.add_argument("--animation-style", choices=sorted(VALID_ANIMATION_STYLES))
    parser.add_argument("--seed", type=int)
    parser.add_argument("--count", type=int, default=1, help="number of candidate directions to return")
    parser.add_argument("--actor-count", type=int, help="featured actor count; default 2 for drama and 1 otherwise")
    parser.add_argument("--scene-count", type=int, default=1, help="distinct physical location count")
    parser.add_argument("--hook", default="random", choices=("random", *HOOKS), help="random or a style-compatible opening mechanism")
    parser.add_argument("--eligible-hooks", nargs="+", choices=tuple(HOOKS), help="optional shortlist checked against product evidence and the brief")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    style_errors = validate_style(args.style, args.animation_style)
    if style_errors:
        raise SystemExit("; ".join(style_errors))
    if not math.isfinite(args.duration) or args.duration <= 0:
        raise SystemExit("duration must be greater than zero")
    if not 1 <= args.count <= 10:
        raise SystemExit("count must be between 1 and 10 (local candidate budget, not a model limit)")
    if args.actor_count is None:
        args.actor_count = 0 if args.animation_style == "motion_graphics" else (2 if args.style == "dialogue_drama" else 1)
    if args.actor_count < 0:
        raise SystemExit("actor-count must be non-negative")
    if args.scene_count <= 0:
        raise SystemExit("scene-count must be greater than zero")
    if args.style == "dialogue_drama" and args.actor_count < 2:
        raise SystemExit("dialogue_drama helper requires two actors for a visible exchange; reconcile cast/style first")

    seed = args.seed if args.seed is not None else secrets.randbits(63)
    duration_patterns = set(SHORT_PATTERNS if args.duration <= 6 else LONG_PATTERNS)
    candidates = []
    seen_story_hooks = set()
    pool = pool_for_actor_count(args.style, args.actor_count, args.animation_style)
    if args.eligible_hooks is not None:
        invalid_hooks = set(args.eligible_hooks) - set(pool["hooks"])
        if invalid_hooks:
            raise SystemExit("eligible-hooks incompatible with style or actor count: " + ", ".join(sorted(invalid_hooks)))
        pool["hooks"] = tuple(hook for hook in pool["hooks"] if hook in args.eligible_hooks)
    if args.hook != "random":
        if args.hook not in pool["hooks"]:
            raise SystemExit("selected hook is incompatible with style, actor count, or eligible-hooks")
        pool["hooks"] = (args.hook,)
    seen_hooks = set()
    patterns = tuple(pattern for pattern in pool["patterns"] if pattern in duration_patterns)
    if args.count > len(patterns) * len(pool["hooks"]):
        raise SystemExit("too many distinct story/hook candidates for this style and duration")
    for index in range(1000):
        candidate_seed = seed + index
        rng = random.Random(candidate_seed)
        candidate = {
            "product": args.product,
            "duration_seconds": args.duration,
            "creative_style": args.style,
            "actor_count": args.actor_count,
            "scene_count": args.scene_count,
            "seed": candidate_seed,
            "concept_id": f"PVC-{candidate_seed & 0xFFFFFFFF:08x}",
            "narrative_pattern": rng.choice(patterns),
            "hook": rng.choice(pool["hooks"]),
            "camera_language": rng.choice(pool["camera_languages"]),
            "scene_progression": rng.choice(pool["scene_progressions"]),
            "ending": rng.choice(pool["endings"]),
            "dialogue_strategy": rng.choice(pool["dialogue_strategies"]),
        }
        story_hook = (candidate["narrative_pattern"], candidate["hook"])
        if len(seen_hooks) < len(pool["hooks"]) and candidate["hook"] in seen_hooks:
            continue
        if story_hook in seen_story_hooks:
            continue
        candidate["hook_mode"] = "random" if args.hook == "random" else "user_selected"
        candidate["hook_label"] = HOOKS[candidate["hook"]][0]
        if args.style == "animation_explainer":
            candidate["animation_style"] = args.animation_style
        if candidate["hook"] == "friend_question":
            candidate["dialogue_strategy"] = "connected_companion_exchange"
        if args.scene_count > 1:
            candidate["scene_progression"] = "coherent_multi_canvas_sequence" if args.animation_style == "motion_graphics" else "coherent_multi_location_sequence"
        seen_story_hooks.add(story_hook)
        seen_hooks.add(candidate["hook"])
        candidates.append(candidate)
        if len(candidates) == args.count:
            break
    if len(candidates) != args.count:
        raise SystemExit("could not create distinct candidates within the bounded attempt budget")
    result = candidates[0] if args.count == 1 else {"candidates": candidates}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
