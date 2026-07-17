# uConsole signed APT releases

This repository is the public, immutable package-release channel for
[`blue-1ms/uconsole-ubuntu-lts`](https://github.com/blue-1ms/uconsole-ubuntu-lts).

Git history contains policy and verification code only. Debian packages are not committed to
Git. Each GitHub prerelease contains one signed offline APT repository bundle bound to an exact
uConsole test-image release.

## Install an exact release

On an image that includes `uconsole-repo-update`:

```bash
sudo uconsole-repo-update 0.1.0-candidate.N
sudo apt update
sudo apt install uconsole-kernel
sudo reboot
```

The updater rejects floating `latest` URLs. It verifies the signed checksum file, the exact
bundle SHA-256 and the repository `InRelease`, then atomically switches a managed local
repository. Kernel installation remains under `flash-kernel` and `piboot-try` A/B control.

## Release status

- `prerelease`: package bytes are bound to a mounted-validated test image but still require the
  remaining CM4 hardware checklist.
- `candidate`: not represented by a new package upload; promotion must reuse identical bytes.
- `stable`: not available yet.

See [the release policy](docs/release-policy.md) before publishing or installing packages.

## Security

Do not install a bundle unless both `SHA256SUMS.asc` and the APT `InRelease` validate against the
keyring already trusted by the uConsole image. Never pipe a release asset into a shell. Report
security issues using the instructions in [SECURITY.md](SECURITY.md).
