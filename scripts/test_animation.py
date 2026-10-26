"""Check animation routing across candidate, project, and runtime contracts."""

import json
from pathlib import Path
import subprocess
import sys
import unittest

from validate_project import sample_project, validate as validate_project
from validate_seedance_package import validate as validate_package


class AnimationTests(unittest.TestCase):
    subtypes = ("stylized_3d", "stop_motion", "motion_graphics")

    def project(self, subtype):
        project = sample_project()
        project["brief"].update(creative_style="animation_explainer", animation_style=subtype,
                                people="no people", actor_count=0)
        project["assets"] = [asset for asset in project["assets"] if asset["type"] != "character"]
        for shot in project["shots"]:
            shot["featured_person"] = False
            shot["dialogue"] = []
            shot.pop("performance", None)
            shot["asset_refs"] = [ref for ref in shot["asset_refs"] if ref != "CHAR-01"]
        return project

    def package(self, subtype):
        return {
            "target": "doubao-seedance-2.0", "task_type": "full_modal_reference",
            "creative_style": "animation_explainer", "animation_style": subtype,
            "duration_seconds": 15, "prompt_language": "zh-CN", "person_reference_mode": "none",
            "audio_policy": {"music": "none", "subtitles": "none", "allowed_audio": ["ambient_sound", "dialogue"]},
            "app_ui_prompt_detail": "state_only",
            "manifest": [{"slot": "图片1", "asset_id": "PROD-01", "role": "product_identity", "format": "product_multiview", "priority": 1}],
            "subjects": [{"label": "产品", "kind": "product", "slots": ["图片1"]}],
            "shots": [{"label": "镜头1", "featured_person": False, "camera_movements": [],
                       "action": "产品图形平移到中央", "completion_state": "产品图形停稳",
                       "environment_atmosphere": {"summary": "简洁图形画布", "ambient_sound": "无环境音"}, "dialogue": []}],
            "prompt": "产品参考图片1。镜头1：简洁图形画布，产品图形平移到中央，产品图形停稳。无环境音。不要生成额外字幕、标题、贴纸或说明文字。不要添加背景音乐，仅保留环境音与人物对白。",
        }

    def test_all_subtypes_pass_both_validators(self):
        for subtype in self.subtypes:
            with self.subTest(subtype=subtype):
                self.assertEqual(validate_project(self.project(subtype)), [])
                self.assertEqual(validate_package(self.package(subtype)), [])

    def test_missing_and_malformed_subtype_rejected(self):
        for value in (None, "unknown", {}, []):
            project = self.project(value)
            package = self.package(value)
            self.assertTrue(any("animation_style must be" in e for e in validate_project(project)))
            self.assertTrue(any("animation_style must be" in e for e in validate_package(package)))

    def test_live_action_rejects_animation_subtype(self):
        project = self.project("stop_motion")
        project["brief"]["creative_style"] = "premium_commercial"
        package = self.package("stop_motion")
        package["creative_style"] = "premium_commercial"
        self.assertTrue(any("only applicable" in e for e in validate_project(project)))
        self.assertTrue(any("only applicable" in e for e in validate_package(package)))

    def helper(self, *args):
        return subprocess.run([sys.executable, str(Path(__file__).with_name("randomize_concept.py")),
                               "--product", "测试产品", "--duration", "15", "--style", "animation_explainer",
                               "--seed", "12345", *args], capture_output=True, text=True, timeout=5)

    def test_all_subtypes_generate_replayable_candidates(self):
        for subtype in self.subtypes:
            for count in (0, 1, 2):
                args = ("--animation-style", subtype, "--actor-count", str(count))
                result = self.helper(*args, "--count", "2")
                self.assertEqual(result.returncode, 0, result.stderr)
                for candidate in json.loads(result.stdout)["candidates"]:
                    self.assertEqual(candidate["animation_style"], subtype)
                    replay = self.helper(*args, "--seed", str(candidate["seed"]))
                    self.assertEqual(json.loads(replay.stdout), candidate)
                    if count == 0:
                        self.assertEqual(candidate["dialogue_strategy"], "no_dialogue_product_proof")

    def test_mg_default_and_canvas_progression(self):
        result = self.helper("--animation-style", "motion_graphics", "--scene-count", "2")
        self.assertEqual(result.returncode, 0, result.stderr)
        candidate = json.loads(result.stdout)
        self.assertEqual(candidate["actor_count"], 0)
        self.assertEqual(candidate["scene_progression"], "coherent_multi_canvas_sequence")

    def test_helper_rejects_missing_and_cross_style_subtypes(self):
        for args in ((), ("--animation-style", "stop_motion", "--style", "ugc_native_vlog")):
            result = self.helper(*args)
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
