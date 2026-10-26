"""Shared checks for everyday, connected spoken dialogue."""

from __future__ import annotations

import re
from typing import Any


_PUNCTUATION = re.compile(r"[\s\u3000，。！？；：、,.!?;:…‘’“”\"'（）()【】\[\]{}<>《》]+")
_SHORT_ACKNOWLEDGEMENTS = {
    "嗯", "嗯嗯", "哦", "哦哦", "啊", "好", "好的", "对", "对的", "可以", "行", "没问题",
    "不错", "真好", "是吗", "真的吗", "我看看", "你试试", "试试看", "就这个", "太方便了",
    "很方便", "真不错", "好用", "喜欢", "确实", "没错",
}


def _clean(line: Any) -> str:
    return _PUNCTUATION.sub("", str(line or "")).strip()


def _is_fragment(line: Any) -> bool:
    clean = _clean(line)
    if not clean:
        return True
    return clean in _SHORT_ACKNOWLEDGEMENTS or (
        bool(re.fullmatch(r"[\u4e00-\u9fff]{1,3}", clean))
    )


def validate_dialogue_quality(
    dialogue: Any,
    *,
    dialogue_mode: str | None = None,
    creative_style: str | None = None,
    path: str = "dialogue",
) -> list[str]:
    """Reject dialogue made entirely from short fragments without banning natural brief replies."""
    if not isinstance(dialogue, list) or not dialogue:
        return []
    lines = [turn.get("line") for turn in dialogue if isinstance(turn, dict)]
    if not lines or len(lines) != len(dialogue):
        return []
    fragments = [_is_fragment(line) for line in lines]
    errors: list[str] = []
    if len(lines) >= 2 and all(fragments):
        errors.append(
            f"{path} must use connected everyday sentences; do not make the whole exchange only short acknowledgements or slogans"
        )
    if (
        len(lines) == 1
        and fragments[0]
        and (dialogue_mode == "continuous_spoken" or creative_style == "dialogue_drama")
    ):
        errors.append(
            f"{path} needs a complete conversational line for continuous speech; expand the short phrase with a concrete situation, action, or result"
        )
    return errors


def validate_shot_dialogue(shots: list, **kwargs: Any) -> list[str]:
    """Audit the whole spoken passage, so a cut does not invalidate a short reply."""
    dialogue = [
        turn for shot in shots if isinstance(shot, dict)
        and isinstance(shot.get("dialogue"), list)
        for turn in shot["dialogue"]
    ]
    return validate_dialogue_quality(dialogue, path="shots dialogue", **kwargs)
