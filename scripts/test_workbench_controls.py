#!/usr/bin/env python3
"""Regression tests for production controls and deterministic candidates."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

from validate_project import sample_project, validate


class ProductionControlsTests(unittest.TestCase):
    def setUp(self):
        self.project = sample_project()

    def assert_issue(self, fragment):
        errors = validate(self.project)
        self.assertTrue(any(fragment in error for error in errors), errors)

    def test_current_and_legacy_projects(self):
        self.assertEqual(validate(self.project), [])
        for key in ("core_function_whitelist", "primary_claim", "actor_count",
                    "scene_count", "hardware_device", "hardware_display_required",
                    "hardware_display_reason", "creative_candidate_count"):
            self.project["brief"].pop(key)
        for shot in self.project["shots"]:
            shot.pop("hardware_visible", None)
            shot.pop("action_speech_relation", None)
        self.assertEqual(validate(self.project), [])

    def test_whitelist_does_not_verify_a_claim(self):
        self.project["brief"]["core_function_whitelist"].append("Purifies water")
        self.assert_issue("not a verified research claim")

    def test_selected_claim_outside_whitelist(self):
        self.project["brief"]["core_function_whitelist"] = ["Different claim"]
        self.assert_issue("must be a subset")

    def test_primary_claim_must_be_selected(self):
        self.project["brief"]["primary_claim"] = "Different claim"
        self.assert_issue("primary_claim must be one of")

    def test_shot_cannot_expand_claims(self):
        self.project["shots"][1]["selling_points"] = ["Purifies water"]
        self.assert_issue("outside brief.selling_points")

    def test_malformed_controls_return_errors(self):
        for field, value in (("actor_count", True), ("actor_count", -1),
                             ("scene_count", 0), ("scene_count", 1.5),
                             ("hardware_display_required", {}),
                             ("core_function_whitelist", [7]),
                             ("creative_candidate_count", 0)):
            with self.subTest(field=field, value=value):
                self.project = sample_project()
                self.project["brief"][field] = value
                self.assert_issue(field)

    def test_no_people_count_conflict(self):
        self.project["brief"]["people"] = "no people"
        self.assert_issue("actor_count must be 0")

    def test_required_hardware_must_be_named_and_visible(self):
        self.project["brief"].pop("hardware_device")
        self.assert_issue("hardware_device is required")
        self.project = sample_project()
        for shot in self.project["shots"]:
            shot["hardware_visible"] = False
        self.assert_issue("at least one shot with hardware_visible true")

    def test_optional_hardware_is_not_forbidden(self):
        self.project["brief"]["hardware_display_required"] = "not_required"
        self.assertEqual(validate(self.project), [])
        for shot in self.project["shots"]:
            shot["hardware_visible"] = False
        self.assertEqual(validate(self.project), [])

    def test_speech_requires_action_relation_for_new_work(self):
        self.project["shots"][0].pop("action_speech_relation")
        self.assert_issue("action_speech_relation is required")
        self.project["shots"][0]["action_speech_relation"] = "先吞咽再说话，保留短暂自然呼吸"
        self.assertEqual(validate(self.project), [])

    def add_candidates(self):
        self.project["brief"]["creative_candidate_count"] = 2
        self.project["creative_candidates"] = [
            {"concept_id": key, "seed": index, "summary": summary,
             "primary_claim": self.project["brief"]["primary_claim"]}
            for index, (key, summary) in enumerate((("PVC-A", "从跑步后喝水的动作切入"),
                                                   ("PVC-B", "从出门装水的日常切入")))
        ]

    def test_candidate_selection_gate(self):
        self.add_candidates()
        self.assert_issue("selected_candidate_id before asset design")
        self.project["creative"] = {"selected_candidate_id": "PVC-B"}
        self.assertEqual(validate(self.project), [])

    def test_candidate_identity_and_count(self):
        self.add_candidates()
        self.project["creative_candidates"][1]["concept_id"] = "PVC-A"
        self.assert_issue("duplicate creative candidate id")
        self.project["brief"]["creative_candidate_count"] = 3
        self.assert_issue("must match stored candidates")

    def test_missing_candidates_cannot_skip_selection(self):
        self.project["brief"]["creative_candidate_count"] = 3
        self.assert_issue("creative_candidates are required")

    def test_unknown_selected_candidate_is_rejected(self):
        self.add_candidates()
        self.project["creative"] = {"selected_candidate_id": "PVC-MISSING"}
        self.assert_issue("must identify a stored candidate")


class CandidateGenerationTests(unittest.TestCase):
    def run_helper(self, *extra):
        return subprocess.run(
            [sys.executable, str(Path(__file__).with_name("randomize_concept.py")),
             "--product", "测试产品", "--duration", "15",
             "--style", "ugc_native_vlog", "--seed", "12345", *extra],
            capture_output=True, text=True, timeout=5, check=False,
        )

    def test_reproducible_distinct_batch_and_individual_replay(self):
        result = self.run_helper("--count", "3", "--actor-count", "1")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, self.run_helper("--count", "3", "--actor-count", "1").stdout)
        candidates = json.loads(result.stdout)["candidates"]
        self.assertEqual(len({(c["narrative_pattern"], c["hook"]) for c in candidates}), 3)
        self.assertEqual(len({c["hook"] for c in candidates}), 3)
        for candidate in candidates:
            self.assertEqual(candidate["dialogue_strategy"], "continuous_first_person_demo")
            replay = self.run_helper("--seed", str(candidate["seed"]), "--actor-count", "1")
            self.assertEqual(json.loads(replay.stdout), candidate)

    def test_no_people_and_multiple_locations(self):
        result = self.run_helper("--actor-count", "0", "--scene-count", "2")
        self.assertEqual(result.returncode, 0, result.stderr)
        candidate = json.loads(result.stdout)
        self.assertEqual(candidate["dialogue_strategy"], "no_dialogue_product_proof")
        self.assertNotEqual(candidate["ending"], "human_payoff_then_product")
        self.assertEqual(candidate["scene_progression"], "coherent_multi_location_sequence")

    def test_selected_hook_is_fixed_and_replayable(self):
        result = self.run_helper("--hook", "result_before_cause", "--count", "3")
        self.assertEqual(result.returncode, 0, result.stderr)
        for candidate in json.loads(result.stdout)["candidates"]:
            self.assertEqual(candidate["hook"], "result_before_cause")
            self.assertEqual(candidate["hook_mode"], "user_selected")
            replay = self.run_helper("--hook", "result_before_cause", "--seed", str(candidate["seed"]))
            self.assertEqual(json.loads(replay.stdout), candidate)

    def test_evidence_shortlist_is_respected(self):
        result = self.run_helper("--eligible-hooks", "result_before_cause", "rapid_physical_proof", "--count", "5", "--actor-count", "0")
        self.assertEqual(result.returncode, 0, result.stderr)
        candidates = json.loads(result.stdout)["candidates"]
        self.assertEqual({c["hook"] for c in candidates}, {"result_before_cause", "rapid_physical_proof"})
        self.assertTrue(all(c["hook_mode"] == "random" for c in candidates))

    def test_hook_conflicts_fail_cleanly(self):
        for args in (("--hook", "friend_question", "--actor-count", "1"),
                     ("--hook", "macro_texture_reveal"),
                     ("--hook", "result_before_cause", "--eligible-hooks", "in_use_observation"),
                     ("--eligible-hooks", "friend_question", "--actor-count", "0")):
            with self.subTest(args=args):
                result = self.run_helper(*args)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn("Traceback", result.stderr)

    def test_two_actor_question_hook_is_available(self):
        for seed in (0, 1, 12345):
            result = self.run_helper("--hook", "friend_question", "--actor-count", "2", "--seed", str(seed))
            self.assertEqual(result.returncode, 0, result.stderr)
            candidate = json.loads(result.stdout)
            self.assertEqual(candidate["hook"], "friend_question")
            self.assertEqual(candidate["dialogue_strategy"], "connected_companion_exchange")

    def test_invalid_inputs_fail_cleanly(self):
        for args in (("--duration", "nan"), ("--duration", "inf"),
                     ("--count", "11"), ("--count", "0"),
                     ("--actor-count", "-1"), ("--scene-count", "0"),
                     ("--style", "dialogue_drama", "--actor-count", "1")):
            with self.subTest(args=args):
                result = self.run_helper(*args)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
