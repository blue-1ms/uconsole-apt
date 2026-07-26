# Release policy

## Publication surfaces

The public package channel has two coordinated surfaces:

- `gh-pages` publishes signed `stable` and disabled-by-default `candidate` APT suites;
- GitHub Releases publish individual `.deb` files and, when applicable, the original signed
  offline repository bundle and its evidence.

Every Pages publication includes `CHANNEL-RECEIPT.json`, `SHA256SUMS`, the public keyring,
signed `InRelease` files, package indices, and the exact package pool. A normal kernel stable
transaction includes the image, modules, headers, buildinfo and meta-package `.deb` files, the
exact tested platform package, and Plymouth when applicable. These remain separate Debian
packages. A platform-only release includes the changed platform package and optional Plymouth
without republishing or revalidating unchanged kernel payloads.

## Immutability

- A release tag is never overwritten or reused.
- Remote asset sizes and GitHub SHA-256 digests must match the local receipt.
- `--clobber`, moving floating `latest` tags, and replacement assets are forbidden.
- A failed or incomplete upload remains a draft; clients never use drafts. A complete draft may
  be resumed only when its tag, prerelease state and exact asset name/size/digest set match the
  locally revalidated export. Resume never uploads, replaces or adds an asset.
- A Pages update is a new immutable `gh-pages` commit. It is generated and signed atomically;
  manual edits to `dists/` or `pool/` are forbidden.
- A release already identified by a receipt or SHA is never rebuilt under the same version.
- Stable channel composition must reuse every already-versioned kernel, platform, and Plymouth
  package byte from the hardware-tested candidate. Rebuilding an auxiliary package under the
  same Debian version is forbidden even when its source tree is unchanged.

## Naming and retention

- Kernel candidate: `<upstream>-candidate.<NN>`.
- Kernel promotion: `<upstream>-stable`, pointing to the exact candidate bytes.
- Same-upstream ABI update: `<upstream>-<abi-sequence>-candidate.<NN>` and matching stable tag.
- Platform-only release: `platform-<semver>-stable`, only when kernel bytes are unchanged.

`uconsole-platform` uses independent monotonic SemVer: MAJOR is an incompatible boot/A-B/control
change, MINOR is a compatible feature or migration, and PATCH is a compatible bug fix. Kernel
metadata records the exact tested platform package SHA and a minimum compatible platform. The
meta package uses `uconsole-platform (>= minimum)`; APT must preserve a newer compatible platform
and must never downgrade it to the tested version.

The repository retains the latest hardware-passed kernel and the adjacent N-1 package set during
rollout. N-2 is removed only after promote, controlled fallback, and restoration succeed.

That adjacent-version rule applies only to a kernel rollout. An ordinary Ubuntu, firmware,
initramfs or platform boot-asset update stages a new deployment of the current kernel and retains
the complete pre-update deployment as its fallback. Candidate and fallback may use the same ABI;
receipt identity, boot assets and known-good state determine safety, not version inequality.

## Client trust boundary

GitHub transports bytes but is not the package-signing trust root. Clients must verify:

1. Direct APT `InRelease` with the package-owned keyring.
2. Release asset digests against the immutable channel or release receipt.
3. For offline bundles, `SHA256SUMS.asc` and the extracted APT `InRelease`.
4. Safe archive paths and regular-file/directory member types before extraction.

The active repository directory and its one-generation rollback directory must carry the
uConsole managed marker. Unmanaged paths are never replaced or deleted.

## First-install bootstrap

Public instructions must assume that no uConsole key, source, helper command, or package is
already installed. A short HTTPS-based quick setup may be offered, but it must disclose that its
initial key trust comes from HTTPS. A separate verified setup must:

1. require Ubuntu 26.04 arm64 on the supported uConsole CM4 Lite target;
2. download the public key without executing downloaded content;
3. compare the complete signing-key fingerprint before installation;
4. store the key outside the global APT trusted-key store;
5. use a Deb822 source with an explicit `Signed-By`;
6. enable `stable` and explicitly disable `candidate`;
7. install `uconsole-platform` before the kernel so package-owned policy and A/B validation are
   active;
8. run `uconsole-kernel-policy-validate` before installing a kernel update.

Both setup paths must use a repository-scoped key and the exact source content later owned by
`uconsole-platform`, so the package can adopt them without duplication or a configuration-file
prompt. Neither path may execute downloaded content or use the global APT trusted-key store.

All user-facing repository documentation and GitHub Release notes are maintained in English.
Release notes are stored under `docs/releases/` and used as the source for GitHub Release bodies.

## Promotion

Hardware validation and candidate promotion are controlled by the source repository. Promotion
reuses the exact package bytes and checksums; it does not rebuild or replace this release. Kernel
boot assets are always installed through initramfs, `flash-kernel`, and `piboot-try`.

The current promotion is `7.1.4-candidate.04` to `7.1.4-stable`; its offline bundle SHA-256 is
`b12738c7c0ae49c625598adf7e62b961b966d59d085f0c90c05cdef40525eb43`.

Kernel closeout is incomplete until all release-repository README files identify the new kernel,
runtime ABI, tested/minimum platform and fallback. Those README commits, all Release URLs, exact
package SHA set and signed validation receipts are part of the cross-repository publication
receipt. A second platform tag/Release is not a normal kernel closeout requirement. It is required
only for a platform-only release with unchanged kernel bytes.

## Validation layers

Fast CI covers manifest/hash/documentation/package metadata/static policy. Artifact validation
checks immutable bytes once: kernel identity/ownership, modules/depmod/vermagic, headers, DT,
initramfs and signed APT; platform payload validation covers ownership and maintainer/A-B hooks.
An identical package set may reuse only its signed content-addressed receipt.

The hardware stable gate separately covers A/B try/promote, FAT mailbox, display/backlight/DRM,
input/audio/PMIC, Wi-Fi/BT/basic USB and the release-typed fallback. Kernel rollouts require the
sole adjacent N-1 kernel; ordinary boot-asset updates require the previous known-good deployment
and allow the same ABI. README, Release, tag, retention and publication checks run only during
stable closeout. Kernel-only publication never runs image compose, mounted-image, GNOME or
first-boot validation.
