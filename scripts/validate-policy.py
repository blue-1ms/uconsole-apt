#!/usr/bin/env python3
"""Validate the static uConsole APT release policy."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    policy = json.loads((ROOT / "release-policy.json").read_text(encoding="utf-8"))
    if policy.get("schema") != "uconsole-apt-release-policy-v2":
        raise SystemExit("unsupported release policy schema")
    if policy.get("repository") != "blue-1ms/uconsole-apt":
        raise SystemExit("release policy repository mismatch")
    if policy.get("immutable") is not True:
        raise SystemExit("release immutability policy is disabled")
    if policy.get("resume_requires_exact_assets") is not True:
        raise SystemExit("draft resume must require the exact validated asset set")
    direct = policy.get("direct_repository")
    if not isinstance(direct, dict):
        raise SystemExit("direct repository policy is missing")
    if direct.get("branch") != "gh-pages":
        raise SystemExit("direct repository branch mismatch")
    if direct.get("url") != "https://blue-1ms.github.io/uconsole-apt":
        raise SystemExit("direct repository URL mismatch")
    if direct.get("suites") != ["stable", "candidate"]:
        raise SystemExit("direct repository suites mismatch")
    if direct.get("candidate_enabled_by_default") is not False:
        raise SystemExit("candidate suite must be disabled by default")
    if direct.get("signed_inrelease_required") is not True:
        raise SystemExit("signed InRelease policy is disabled")
    assets = policy.get("required_channel_assets")
    expected = {
        "CHANNEL-RECEIPT.json",
        "SHA256SUMS",
        "uconsole-archive-keyring.asc",
        "dists/stable/InRelease",
        "dists/candidate/InRelease",
    }
    if not isinstance(assets, list) or set(assets) != expected or len(assets) != len(expected):
        raise SystemExit("required channel asset set is incomplete or duplicated")
    if policy.get("release_tag_patterns") != [
        "<upstream>-candidate.<NN>",
        "<upstream>-stable",
        "platform-<version>-stable",
    ]:
        raise SystemExit("release tag patterns are incomplete")
    if set(policy.get("forbidden_publish_options", [])) != {
        "--clobber",
        "floating-latest-tag",
    }:
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
