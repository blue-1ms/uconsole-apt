# Release policy

## Publication surfaces

The public package channel has two coordinated surfaces:

- `gh-pages` publishes signed `stable` and disabled-by-default `candidate` APT suites;
- GitHub Releases publish individual `.deb` files and, when applicable, the original signed
  offline repository bundle and its evidence.

Every Pages publication includes `CHANNEL-RECEIPT.json`, `SHA256SUMS`, the public keyring,
signed `InRelease` files, package indices, and the exact package pool. A kernel release includes
the image, modules, headers, buildinfo, and meta-package `.deb` files. A platform release includes
the platform and Plymouth `.deb` files.

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

## Naming and retention

- Kernel candidate: `<upstream>-candidate.<NN>`.
- Kernel promotion: `<upstream>-stable`, pointing to the exact candidate bytes.
- Same-upstream ABI update: `<upstream>-<abi-sequence>-candidate.<NN>` and matching stable tag.
- Platform release: `platform-<version>-stable`.

The repository retains the latest hardware-passed kernel and the adjacent N-1 package set during
rollout. N-2 is removed only after promote, controlled fallback, and restoration succeed.

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
