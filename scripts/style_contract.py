"""Shared style/substyle contract for generation and validation."""

VALID_CREATIVE_STYLES = {"ugc_native_vlog", "premium_commercial", "dialogue_drama", "animation_explainer"}
VALID_ANIMATION_STYLES = {"stylized_3d", "stop_motion", "motion_graphics"}


def validate_style(style, animation_style, prefix=""):
    errors = []
    if not isinstance(style, str) or style not in VALID_CREATIVE_STYLES:
        errors.append(f"{prefix}creative_style must be " + ", ".join(sorted(VALID_CREATIVE_STYLES)))
    if style == "animation_explainer":
        if not isinstance(animation_style, str) or animation_style not in VALID_ANIMATION_STYLES:
            errors.append(f"{prefix}animation_style must be stylized_3d, stop_motion, or motion_graphics for animation_explainer")
    elif animation_style is not None:
        errors.append(f"{prefix}animation_style is only applicable to animation_explainer")
    return errors
