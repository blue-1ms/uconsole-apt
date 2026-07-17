# Release policy

## Required assets

Every prerelease must use one exact tag and include:

- `uconsole-apt-repository-<release>.tar.zst`
- `SHA256SUMS`
- `SHA256SUMS.asc`
- `build-manifest.yaml`
- `repository-receipt.json`
- `mounted-image-validation-report.json`
- `TEST-IMAGE.json`
- `package-set.sha256`

The repository bundle contains the signed `dists/` and `pool/` trees. The checksum signature
binds the bundle to the image export; `repository-receipt.json` records package identities and
hashes.

## Immutability

- A release tag is never overwritten or reused.
- Upload starts as a draft and becomes a prerelease only after all remote asset sizes and
  available GitHub SHA-256 digests match the local files.
- `--clobber`, moving `latest` tags and replacement assets are forbidden.
- A failed or incomplete upload remains a draft; clients never use drafts. A complete draft may
  be resumed only when its tag, prerelease state and exact asset name/size/digest set match the
  locally revalidated export. Resume never uploads, replaces or adds an asset.
- A test image with `candidate: false` is never described as stable.

## Client trust boundary

GitHub transports bytes but is not the package-signing trust root. Clients must verify:

1. `SHA256SUMS.asc` with the keyring already installed by a trusted image.
2. The downloaded bundle against its exact signed SHA-256 entry.
3. The extracted APT `InRelease` with the same keyring.
4. Safe archive paths and regular-file/directory member types before extraction.

The active repository directory and its one-generation rollback directory must carry the
uConsole managed marker. Unmanaged paths are never replaced or deleted.

## Promotion

Hardware validation and candidate promotion are controlled by the source repository. Promotion
reuses the exact package bytes and checksums; it does not rebuild or replace this release.
