import copy
import unittest

from dialogue_quality import validate_dialogue_quality, validate_shot_dialogue
from validate_project import sample_project, validate as validate_project
from validate_seedance_package import validate as validate_package


class DialogueQualityTests(unittest.TestCase):
    def test_all_short_fragments_are_rejected(self):
        dialogue = [
            {"speaker": "甲", "line": "嗯", "tone": "自然", "reaction": "看向对方"},
            {"speaker": "乙", "line": "可以", "tone": "自然", "reaction": "点头"},
        ]
        errors = validate_dialogue_quality(dialogue, creative_style="dialogue_drama")
        self.assertTrue(any("connected everyday sentences" in error for error in errors))

    def test_natural_long_turn_with_short_reply_passes(self):
        dialogue = [
            {"speaker": "甲", "line": "我刚才还在找开瓶器，没想到这个拿起来就能直接打开。", "tone": "自然", "reaction": "看向产品"},
            {"speaker": "乙", "line": "你试试", "tone": "自然", "reaction": "把产品递过去"},
        ]
        self.assertEqual(validate_dialogue_quality(dialogue, creative_style="dialogue_drama"), [])

    def test_ugc_single_fragment_is_rejected(self):
        dialogue = [{"speaker": "甲", "line": "太方便了", "tone": "自然", "reaction": "无"}]
        errors = validate_dialogue_quality(dialogue, dialogue_mode="continuous_spoken", creative_style="ugc_native_vlog")
        self.assertTrue(any("complete conversational line" in error for error in errors))

    def test_valid_fixtures_use_complete_lines(self):
        self.assertEqual(validate_project(sample_project()), [])

        project = sample_project()
        shot = copy.deepcopy(project["shots"][0])
        shot["label"] = "镜头1"
        shot["camera_movements"] = []
        shot["dialogue"][0]["line"] = "我先把这杯水放在这里，等会儿回来再喝。"
        values = [shot["action"], shot["completion_state"], shot["action_speech_relation"]]
        values += [v for k, v in shot["performance"].items() if k != "intensity"]
        values += list(shot["environment_atmosphere"].values())
        values += list(shot["dialogue"][0].values())
        package = {
            "target": "doubao-seedance-2.0", "task_type": "full_modal_reference",
            "creative_style": "ugc_native_vlog", "duration_seconds": 15,
            "prompt_language": "zh-CN", "person_reference_mode": "single_image",
            "dialogue_mode": "continuous_spoken",
            "audio_policy": {"music": "none", "subtitles": "none", "allowed_audio": ["ambient_sound", "dialogue"]},
            "app_ui_prompt_detail": "state_only",
            "manifest": [
                {"slot": "图片1", "asset_id": "PROD-01", "role": "product_identity", "format": "product_multiview", "priority": 1},
                {"slot": "图片2", "asset_id": "CHAR-01", "role": "person_identity", "format": "single_person", "priority": 2},
            ],
            "subjects": [{"label": "产品", "kind": "product", "slots": ["图片1"]},
                         {"label": "Runner", "kind": "person", "slots": ["图片2"]}],
            "shots": [shot],
            "prompt": "产品参考图片1，Runner参考图片2。镜头1：" + "。".join(values) + "。不要生成额外字幕、标题、贴纸或说明文字。不要添加背景音乐，仅保留环境音与人物对白。",
        }
        self.assertEqual(validate_package(package), [])
        for line in ("嗯", "太方便了"):
            invalid = copy.deepcopy(package)
            invalid["prompt"] = invalid["prompt"].replace(shot["dialogue"][0]["line"], line)
            invalid["shots"][0]["dialogue"][0]["line"] = line
            self.assertTrue(any("complete conversational line" in e for e in validate_package(invalid)))
        reply = copy.deepcopy(shot)
        reply["label"] = "镜头2"
        reply["dialogue"][0]["line"] = "好"
        package["shots"].append(reply)
        package["prompt"] += "镜头2：" + "。".join(values).replace(shot["dialogue"][0]["line"], "好")
        self.assertEqual(validate_package(package), [])
        package["shots"][0]["dialogue"][0]["line"] = "嗯"
        package["prompt"] = package["prompt"].replace(shot["dialogue"][0]["line"], "嗯")
        self.assertTrue(any("connected everyday sentences" in e for e in validate_package(package)))

    def test_cross_shot_short_reply_passes_project_validator(self):
        project = sample_project()
        reply = copy.deepcopy(project["shots"][0])
        reply.update(id="SHOT-002", start=3, end=6)
        reply["dialogue"][0]["line"] = "好"
        project["shots"][1] = reply
        self.assertEqual(validate_project(project), [])
        project["shots"][0]["dialogue"][0]["line"] = "嗯"
        self.assertTrue(any("connected everyday sentences" in e for e in validate_project(project)))

    def test_connected_ugc_passage_passes(self):
        passage = "出门前我会先把水装好，这样跑完就不用再去买了。你看，放在旁边，歇下来的时候拿起来就能喝。"
        self.assertEqual(validate_dialogue_quality([{"line": passage}], dialogue_mode="continuous_spoken"), [])

    def test_short_complete_exchange_not_rejected_by_length(self):
        self.assertEqual(validate_dialogue_quality([{"line": "你带伞了吗？"}, {"line": "带了，在包里。"}]), [])

    def test_sparse_commercial_and_no_character_animation(self):
        self.assertEqual(validate_shot_dialogue([{"dialogue": [{"line": "嗯"}]}], creative_style="premium_commercial", dialogue_mode="mixed"), [])
        self.assertEqual(validate_shot_dialogue([{"dialogue": []}], creative_style="animation_explainer"), [])


if __name__ == "__main__":
    unittest.main()
