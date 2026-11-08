---
name: product-video-director-setup
description: "Guide first-time installation and capability setup for Product Video Director. Use this when the user wants to install this repository, configure available tools, check readiness, or begin their first project."
---

# 产品视频 Skill 配置引导

Guide first-time installation and capability setup for Product Video Director. Use this when the user wants to install this repository, configure available tools, check readiness, or begin their first project.

## Locate the project

The installer writes a local `references/installation.json` containing `repository_path`. Read it when present, then verify that directory contains this project's `onboarding.json`, root `SKILL.md` and `scripts/validate_project.py`. If the clone moved, locate the path supplied by the user or ask for the clone location; do not run project commands from the installed Skill directory. Read the clone's README and relevant references as needed.

## Configure and verify

1. Check that the functional `product-video-director` Skill is installed beside this setup Skill. If missing, use the clone's `python3 scripts/install_skills.py`; it backs up existing Skills. Reopen the task to refresh discovery. Python 3.10+ is used for validators, not a prerequisite for writing prompts.
2. Inspect actually available search/browser, image and video tools. No generation provider or API key is included. Do not require a paid generator to use the prompt-only workflow. If search is unavailable, use the user's official product references and say which facts remain unverified.
3. Reuse supplied preferences. Ask once for the missing product identity/official URL, target audience, duration, style and whether people appear. Keep business facts separate from assumptions. Do not invent an example product's features or collect credentials.
4. In the clone run `python3 scripts/validate_project.py --self-test` and `python3 scripts/validate_seedance_package.py --self-test`. Failures block claiming the validators ready, not unrelated product research.
5. Start a separate user project folder with a researched brief and the artifact structure described in root `SKILL.md`; preserve supplied materials. Follow that Skill for asset and video-prompt approvals. Setup is not authorization to submit image/video generation jobs.

Finish with installed Skill name, actual available capabilities, validator results and one concrete next prompt. Distinguish prompt-ready from generation-ready. Do not claim a finished ad or paid-provider connection from installation alone.
