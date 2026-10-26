#!/usr/bin/env python3
"""Assemble a validated product-video delivery folder from a project manifest."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

from validate_project import validate


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", help="product-video-project.json")
    parser.add_argument("source_dir", help="directory containing prompt and image files")
    parser.add_argument("output_dir", help="new delivery folder")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_path = Path(args.project).resolve()
    source_dir = Path(args.source_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    project: dict[str, Any] = json.loads(project_path.read_text(encoding="utf-8"))
    validation_errors = validate(project)
    if validation_errors:
        raise SystemExit("project validation failed:\n- " + "\n- ".join(validation_errors))
    gates = project.get("gates", {})
    delivery = project.get("delivery", {})
    if not isinstance(gates, dict) or not gates.get("delivery_ready"):
        raise SystemExit("delivery gate is not ready; complete the audits and storyboard first")
    if not isinstance(delivery, dict) or delivery.get("audit_status") != "complete":
        raise SystemExit("delivery.audit_status must be complete")
    files = delivery.get("files")
    if not isinstance(files, list):
        raise SystemExit("delivery.files must be a list")
    if not source_dir.is_dir():
        raise SystemExit(f"source directory does not exist: {source_dir}")
    if output_dir.exists():
        raise SystemExit(f"output directory already exists: {output_dir}")

    present_files: list[tuple[dict[str, Any], Path, Path]] = []
    manifest_files: list[dict[str, Any]] = []
    for item in files:
        if not isinstance(item, dict):
            raise SystemExit("delivery.files entries must be objects")
        manifest_files.append(item)
        if item.get("status") != "present":
            continue
        relative_path = Path(str(item.get("path", "")))
        if relative_path.is_absolute() or ".." in relative_path.parts:
            raise SystemExit(f"delivery path must stay relative to source_dir: {relative_path}")
        if relative_path.as_posix() in {"manifest.json", "project/product-video-project.json"}:
            raise SystemExit(f"delivery path is reserved: {relative_path}")
        source = (source_dir / relative_path).resolve()
        if not source.is_relative_to(source_dir) or not source.is_file():
            raise SystemExit(f"delivery file is missing or outside source_dir: {source}")
        present_files.append((item, source, relative_path))

    output_dir.mkdir(parents=True)
    try:
        for _, source, relative_path in present_files:
            destination = output_dir / relative_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)

        project_destination = output_dir / "project" / "product-video-project.json"
        project_destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(project_path, project_destination)
        manifest = {
            "folder_name": delivery.get("folder_name", output_dir.name),
            "audit_status": delivery.get("audit_status"),
            "render_status": delivery.get("render_status"),
            "files": manifest_files,
            "project_file": "project/product-video-project.json",
        }
        (output_dir / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    except Exception:
        shutil.rmtree(output_dir, ignore_errors=True)
        raise
    print(output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
