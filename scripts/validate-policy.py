#!/usr/bin/env python3
"""Validate the static uConsole APT release policy."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    policy = json.loads((ROOT / "release-policy.json").read_text(encoding="utf-8"))
    if policy.get("schema") != "uconsole-apt-release-policy-v1":
        raise SystemExit("unsupported release policy schema")
    if policy.get("repository") != "blue-1ms/uconsole-apt":
        raise SystemExit("release policy repository mismatch")
    if policy.get("immutable") is not True or policy.get("test_image_release_type") != "prerelease":
        raise SystemExit("release immutability or prerelease policy is disabled")
    if policy.get("resume_requires_exact_assets") is not True:
        raise SystemExit("draft resume must require the exact validated asset set")
    assets = policy.get("required_assets")
    expected = {
        "uconsole-apt-repository-<release>.tar.zst",
        "SHA256SUMS",
        "SHA256SUMS.asc",
        "build-manifest.yaml",
        "repository-receipt.json",
        "mounted-image-validation-report.json",
        "TEST-IMAGE.json",
        "package-set.sha256",
    }
    if not isinstance(assets, list) or set(assets) != expected or len(assets) != len(expected):
        raise SystemExit("required release asset set is incomplete or duplicated")
    if set(policy.get("forbidden_publish_options", [])) != {"--clobber", "latest"}:
        raise SystemExit("forbidden publish options are incomplete")
    for path in (
        ROOT / "README.md",
        ROOT / "docs/release-policy.md",
        ROOT / "SECURITY.md",
        ROOT / "LICENSE",
        ROOT / "LICENSE-DOCS",
        ROOT / "NOTICE",
    ):
        if not path.is_file() or not path.read_text(encoding="utf-8").strip():
            raise SystemExit(f"required documentation is missing: {path.relative_to(ROOT)}")
    print("uConsole APT release policy validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
