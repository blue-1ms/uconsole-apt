# Repository bootstrap

This guide covers a clean Ubuntu 26.04 arm64 uConsole CM4 Lite installation that has no existing
uConsole APT source, signing key, or package.

The short installation procedure is in the [repository README](../README.md). This page explains
the trust model, verification steps, and safe recovery behavior.

## Trust model

The repository signing key fingerprint is:

```text
79C0DBFA56EDF5B9E0F807CE8E817BEBC6F4DA87
```

The key is stored at `/usr/share/keyrings/uconsole-archive-keyring.asc` and is referenced only by
`/etc/apt/sources.list.d/uconsole.sources` through `Signed-By`. It is deliberately not installed
in `/etc/apt/trusted.gpg.d`, because a globally trusted key could authenticate unrelated APT
sources.

The initial key is downloaded over HTTPS and its complete fingerprint must match before it is
installed. Package downloads are then authenticated by the signed `InRelease` metadata. The
first `uconsole-platform` installation adopts the same source and key files as package-owned
configuration.

Never use `trusted=yes`, never skip the fingerprint comparison, and never run a downloaded
script through a shell.

## Verify the configured repository

After following the README bootstrap procedure, run:

```bash
apt-cache policy uconsole-platform uconsole-kernel uconsole-plymouth-theme
apt-cache policy linux-image-raspi linux-raspi
sudo uconsole-kernel-policy-validate
```

The stable uConsole packages must have an installable version from
`https://blue-1ms.github.io/uconsole-apt`. Ubuntu `linux-*-raspi` kernel packages must not be
selected as an upgrade candidate. Raspberry Pi firmware packages remain eligible for normal
Ubuntu updates.

The candidate suite is present in the Deb822 file but disabled. Do not enable it on a daily-use
device unless a specific candidate test procedure says to do so.

## Kernel installation behavior

Installing `uconsole-kernel` does not overwrite `kernel8.img` directly. The package uses the
standard initramfs and `flash-kernel` hooks to stage a complete `new` slot, including the kernel,
initramfs, DTB, Raspberry Pi overlay set, and uConsole overlays. `piboot-try` validates the new
slot before promotion.

If validation fails, the device returns to the N-1 known-good kernel. Diagnostic files remain on
the FAT boot partition:

```text
/boot/firmware/uconsole-debug.txt
/boot/firmware/uconsole-debug-new.txt
/boot/firmware/uconsole-debug-current.txt
/boot/firmware/uconsole-debug-previous.txt
```

These files can be read after moving the microSD card to another computer. They intentionally
exclude credentials, Wi-Fi state, Tailscale state, SSH keys, tokens, and user information.

## Removing an incomplete bootstrap

If `apt-get update` has not successfully authenticated the repository and no uConsole package
has been installed, remove only the two bootstrap files:

```bash
sudo rm -f /etc/apt/sources.list.d/uconsole.sources
sudo rm -f /usr/share/keyrings/uconsole-archive-keyring.asc
sudo apt-get update
```

After `uconsole-platform` is installed, those paths are package-owned. Use the Debian package
manager rather than deleting package-owned files manually.
