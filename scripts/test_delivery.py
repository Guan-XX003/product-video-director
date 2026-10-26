#!/usr/bin/env python3
"""Exercise complete and prompt-ready delivery packaging."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from validate_project import sample_project, validate


SCRIPT = Path(__file__).with_name("assemble_delivery.py")
PROMPTS = {
    "product_prompt": ("prompts/product-asset.md", "PROD-01"),
    "character_prompt": ("prompts/character-asset.md", "CHAR-01"),
    "scene_prompt": ("prompts/scene-asset.md", "SCENE-01"),
    "storyboard_prompt": ("prompts/storyboard.md", "SHOT-001"),
    "video_prompt": ("prompts/video-prompts.md", "VID-001"),
}
IMAGES = {
    "product_reference_image": ("images/product/ref.png", "PROD-01"),
    "character_reference_image": ("images/character/ref.png", "CHAR-01"),
    "scene_reference_image": ("images/scene/ref.png", "SCENE-01"),
    "storyboard_image": ("images/storyboard/contact.png", "SHOT-001"),
}


class DeliveryTests(unittest.TestCase):
    def make_project(self, rendered: bool) -> dict:
        project = sample_project()
        project["gates"].update({
            "pre_confirmation_audit": True,
            "video_prompts_confirmed": True,
            "storyboard_rendered": rendered,
            "delivery_ready": True,
        })
        files = [
            {
                "path": path, "kind": kind, "purpose": kind,
                "status": "present", "source_asset_id": asset_id, "approved": True,
            }
            for kind, (path, asset_id) in PROMPTS.items()
        ]
        for kind, (path, asset_id) in IMAGES.items():
            item = {
                "path": path, "kind": kind, "purpose": kind,
                "status": "present" if rendered else "unavailable",
                "source_asset_id": asset_id, "approved": rendered,
            }
            if not rendered:
                item["reason"] = "当前没有生图工具"
            files.append(item)
        project["delivery"] = {
            "audit_status": "complete",
            "render_status": "complete" if rendered else "partial",
            "folder_name": "product-video-delivery",
            "files": files,
        }
        return project

    def run_assembler(self, project: dict, missing_path: str | None = None) -> tuple[subprocess.CompletedProcess[str], Path]:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source"
            source.mkdir()
            for item in project["delivery"]["files"]:
                if item["status"] != "present" or item["path"] == missing_path:
                    continue
                file_path = source / item["path"]
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.write_text("测试内容", encoding="utf-8")
            project_path = root / "project.json"
            project_path.write_text(json.dumps(project, ensure_ascii=False), encoding="utf-8")
            output = root / "delivery"
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(project_path), str(source), str(output)],
                capture_output=True, text=True, check=False,
            )
            if result.returncode == 0:
                manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
                self.assertEqual(manifest["render_status"], project["delivery"]["render_status"])
                self.assertTrue((output / "prompts" / "video-prompts.md").is_file())
                self.assertEqual(len(manifest["files"]), len(project["delivery"]["files"]))
            self.assertEqual(output.exists(), result.returncode == 0)
            return result, output

    def test_partial_package_retains_unavailable_entries(self) -> None:
        project = self.make_project(rendered=False)
        self.assertEqual(validate(project), [])
        result, _ = self.run_assembler(project)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_complete_package(self) -> None:
        project = self.make_project(rendered=True)
        self.assertEqual(validate(project), [])
        result, _ = self.run_assembler(project)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_missing_file_does_not_create_folder(self) -> None:
        result, _ = self.run_assembler(self.make_project(rendered=False), "prompts/video-prompts.md")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("delivery file is missing", result.stderr)

    def test_invalid_manifest_does_not_create_folder(self) -> None:
        project = self.make_project(rendered=False)
        project["delivery"]["files"][4]["status"] = "unavailable"
        project["delivery"]["files"][4]["reason"] = "错误标记"
        result, _ = self.run_assembler(project)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("project validation failed", result.stderr)


if __name__ == "__main__":
    unittest.main()
