# uConsole signed APT repository

This repository is the public, immutable package-release channel for
[`blue-1ms/uconsole-ubuntu-lts`](https://github.com/blue-1ms/uconsole-ubuntu-lts).

The `main` branch contains policy and verification code. The `gh-pages` branch contains the
signed binary APT repository published at
`https://blue-1ms.github.io/uconsole-apt`. GitHub Releases also expose the exact `.deb` files and
offline repository bundles for auditing and manual recovery.

## Normal updates

`uconsole-platform >= 0.1.17` installs the stable source and its package-owned keyring. On a
supported uConsole:

```bash
sudo apt update
sudo apt install uconsole-kernel uconsole-platform uconsole-plymouth-theme
sudo reboot
```

The `candidate` suite is installed but disabled by default. Both suites use the package-owned
keyring and signed `InRelease` metadata. Kernel installation remains under initramfs,
`flash-kernel`, and `piboot-try` A/B control.

The platform package pins Ubuntu-origin `linux-*-raspi` kernel packages below installable
priority, so a normal Ubuntu `apt upgrade` cannot replace the uConsole boot kernel. Raspberry Pi
firmware packages remain eligible for updates. Run `sudo uconsole-kernel-policy-validate` after
changing APT sources or preferences.

## Exact releases

- Kernel candidates use `<upstream>-candidate.<NN>`.
- A hardware-passed promotion uses `<upstream>-stable` and reuses the candidate bytes.
- Userspace releases use `platform-<version>-stable`.

The current stable kernel is
[`7.1.3-stable`](https://github.com/blue-1ms/uconsole-apt/releases/tag/7.1.3-stable).
Its individual `.deb` assets are byte-identical to the signed stable APT channel. The historical
`0.1.0-candidate.16` release keeps the original offline bundle and receipt unchanged.

## Release status

- `candidate`: signed immutable bytes awaiting the complete CM4 hardware checklist.
- `stable`: the exact candidate bytes after hardware, A/B promote, controlled fallback, and FAT
  diagnostic validation.
- Promotion never rebuilds, renames, or replaces an existing package.

See [the release policy](docs/release-policy.md) before publishing or installing packages.

## Security

Do not add the repository with `trusted=yes` and never pipe a release asset into a shell. For
offline bundles, verify both `SHA256SUMS.asc` and the APT `InRelease` against the keyring already
trusted by the uConsole image. Report security issues using [SECURITY.md](SECURITY.md).
