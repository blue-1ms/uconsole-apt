# uConsole signed APT repository

This repository is the public, immutable package-release channel for
[`blue-1ms/uconsole-ubuntu-lts`](https://github.com/blue-1ms/uconsole-ubuntu-lts).

The `main` branch contains policy and verification code. The `gh-pages` branch contains the
signed binary APT repository published at
`https://blue-1ms.github.io/uconsole-apt`. GitHub Releases also expose the exact `.deb` files and
offline repository bundles for auditing and manual recovery.

## First installation

These instructions assume that the machine has never used this repository. They are supported
only on the Ubuntu 26.04 arm64 uConsole CM4 Lite image.

### Quick setup

This is the shortest supported setup. It trusts the repository key downloaded over HTTPS but
still scopes that key to this repository; it does not add the key to APT's global trust store.

```bash
wget -qO- https://blue-1ms.github.io/uconsole-apt/uconsole-archive-keyring.asc \
  | sudo tee /usr/share/keyrings/uconsole-archive-keyring.asc >/dev/null

printf '%s\n' \
  'Types: deb' \
  'URIs: https://blue-1ms.github.io/uconsole-apt' \
  'Suites: stable' \
  'Components: main' \
  'Architectures: arm64' \
  'Signed-By: /usr/share/keyrings/uconsole-archive-keyring.asc' \
  'Enabled: yes' \
  '' \
  'Types: deb' \
  'URIs: https://blue-1ms.github.io/uconsole-apt' \
  'Suites: candidate' \
  'Components: main' \
  'Architectures: arm64' \
  'Signed-By: /usr/share/keyrings/uconsole-archive-keyring.asc' \
  'Enabled: no' \
  | sudo tee /etc/apt/sources.list.d/uconsole.sources >/dev/null

sudo apt update
sudo apt install uconsole-platform
sudo uconsole-kernel-policy-validate
sudo apt install uconsole-kernel uconsole-plymouth-theme
sudo reboot
```

Allow the one or two automatic restarts required by `piboot-try`. Do not power off the device
while the new slot is being validated.

### Verified setup

Use this procedure when you want to verify the complete signing-key fingerprint before installing
the repository configuration.

Install the bootstrap tools and confirm the architecture:

```bash
sudo apt-get update
sudo apt-get install --yes ca-certificates curl gpg
test "$(dpkg --print-architecture)" = arm64
```

Download the public key, verify its full fingerprint, and install a key and Deb822 source that
are scoped only to this repository. Run the complete block as one operation:

```bash
(
set -eu
repo_url="https://blue-1ms.github.io/uconsole-apt"
expected_fingerprint="79C0DBFA56EDF5B9E0F807CE8E817BEBC6F4DA87"
bootstrap_dir="$(mktemp -d)"
trap 'rm -rf "${bootstrap_dir}"' EXIT
export GNUPGHOME="${bootstrap_dir}/gnupg"
install -d -m 0700 "${GNUPGHOME}"
curl --fail --silent --show-error --location \
  "${repo_url}/uconsole-archive-keyring.asc" \
  --output "${bootstrap_dir}/uconsole-archive-keyring.asc"
actual_fingerprint="$(
  gpg --batch --show-keys --with-colons \
    "${bootstrap_dir}/uconsole-archive-keyring.asc" |
    awk -F: '$1 == "fpr" { print $10; exit }'
)"
if [ "${actual_fingerprint}" != "${expected_fingerprint}" ]; then
  echo "Signing-key fingerprint mismatch; repository was not configured." >&2
  exit 1
fi
sudo install -o root -g root -m 0644 \
  "${bootstrap_dir}/uconsole-archive-keyring.asc" \
  /usr/share/keyrings/uconsole-archive-keyring.asc
cat >"${bootstrap_dir}/uconsole.sources" <<'EOF'
Types: deb
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
Enabled: no
EOF
sudo install -o root -g root -m 0644 \
  "${bootstrap_dir}/uconsole.sources" \
  /etc/apt/sources.list.d/uconsole.sources
sudo apt-get update
)
```

Install the platform policy first. It adopts the exact bootstrap key and source files, protects
the uConsole kernel from Ubuntu `linux-*-raspi` meta-packages, and installs the A/B validator.
Then install the stable kernel and optional Plymouth theme:

```bash
sudo apt-get install --yes uconsole-platform
sudo uconsole-kernel-policy-validate
sudo apt-get install --yes uconsole-kernel uconsole-plymouth-theme
sudo reboot
```

Allow the one or two automatic restarts required by `piboot-try`. Do not power off the device
while the new slot is being validated. See [the bootstrap guide](docs/bootstrap.md) for trust,
verification, and recovery details.

## Updating an existing installation

`uconsole-platform >= 0.1.17` owns the stable source, candidate opt-in, scoped keyring, and kernel
policy. On a supported uConsole:

```bash
sudo apt update
sudo uconsole-kernel-policy-validate
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

Do not add the repository with `trusted=yes`, do not put its key in the global
`/etc/apt/trusted.gpg.d` trust store, and never pipe downloaded content into a shell. For offline
bundles, verify both `SHA256SUMS.asc` and the APT `InRelease` against the scoped keyring. Report
security issues using [SECURITY.md](SECURITY.md).
