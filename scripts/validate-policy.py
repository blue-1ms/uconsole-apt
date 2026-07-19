#!/usr/bin/env python3
"""Validate the static uConsole APT release policy."""

from __future__ import annotations

import json
import re
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
    bootstrap = policy.get("bootstrap")
    expected_bootstrap = {
        "assumes_existing_repository": False,
        "supported_system": "Ubuntu 26.04 arm64 uConsole CM4 Lite",
        "key_url": (
            "https://blue-1ms.github.io/uconsole-apt/"
            "uconsole-archive-keyring.asc"
        ),
        "key_fingerprint": "79C0DBFA56EDF5B9E0F807CE8E817BEBC6F4DA87",
        "keyring_path": "/usr/share/keyrings/uconsole-archive-keyring.asc",
        "source_path": "/etc/apt/sources.list.d/uconsole.sources",
        "quick_setup_allowed": True,
        "quick_setup_https_trust_disclosed": True,
        "verified_setup_required": True,
        "global_trust_forbidden": True,
        "downloaded_shell_forbidden": True,
        "platform_installed_before_kernel": True,
    }
    if bootstrap != expected_bootstrap:
        raise SystemExit("first-install bootstrap policy is incomplete")
    if policy.get("documentation_language") != "en":
        raise SystemExit("documentation language must be English")
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
    required_docs = (
        ROOT / "README.md",
        ROOT / "docs/bootstrap.md",
        ROOT / "docs/release-policy.md",
        ROOT / "SECURITY.md",
        ROOT / "LICENSE",
        ROOT / "LICENSE-DOCS",
        ROOT / "NOTICE",
    )
    for path in required_docs:
        if not path.is_file() or not path.read_text(encoding="utf-8").strip():
            raise SystemExit(f"required documentation is missing: {path.relative_to(ROOT)}")
    release_notes = sorted((ROOT / "docs/releases").glob("*.md"))
    if not release_notes:
        raise SystemExit("tracked GitHub Release notes are missing")
    cjk = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
    for path in sorted(ROOT.rglob("*.md")):
        if ".git" in path.parts:
            continue
        if cjk.search(path.read_text(encoding="utf-8")):
            raise SystemExit(
                f"user-facing documentation must be English: {path.relative_to(ROOT)}"
            )
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for required_text in (
        "## First installation",
        "### Quick setup",
        "### Verified setup",
        "trusts the repository key downloaded over HTTPS",
        "set -eu",
        expected_bootstrap["key_fingerprint"],
        expected_bootstrap["keyring_path"],
        expected_bootstrap["source_path"],
        "Signing-key fingerprint mismatch",
        "Signed-By:",
        "Enabled: no",
        "sudo apt-get install --yes uconsole-platform",
        "sudo uconsole-kernel-policy-validate",
    ):
        if required_text not in readme:
            raise SystemExit(f"README bootstrap is missing: {required_text}")
    source_marker = "cat >\"${bootstrap_dir}/uconsole.sources\" <<'EOF'\n"
    if source_marker not in readme:
        raise SystemExit("README Deb822 bootstrap block is missing")
    source_block = readme.split(source_marker, 1)[1].split("\nEOF", 1)[0]
    expected_source = """Types: deb
URIs: https://blue-1ms.github.io/uconsole-apt
Suites: stable
Components: main
Architectures: arm64
Signed-By: /usr/share/keyrings/uconsole-archive-keyring.asc
Enabled: yes

Types: deb
URIs: https://blue-1ms.github.io/uconsole-apt
Suites: candidate
Components: main
Architectures: arm64
Signed-By: /usr/share/keyrings/uconsole-archive-keyring.asc
Enabled: no"""
    if source_block != expected_source:
        raise SystemExit("README Deb822 source differs from the package-owned source")
    quick_section = readme.split("### Quick setup", 1)[1].split(
        "### Verified setup", 1
    )[0]
    quick_source_lines = re.findall(
        r"^\s*'([^']*)'\s*\\?$", quick_section, flags=re.MULTILINE
    )
    if "\n".join(quick_source_lines) != expected_source:
        raise SystemExit(
            "README quick-setup source differs from the package-owned source"
        )
    if (
        "wget -qO- " + expected_bootstrap["key_url"]
    ) not in quick_section:
        raise SystemExit("README quick setup does not download the pinned key URL")
    print("uConsole APT release policy validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
