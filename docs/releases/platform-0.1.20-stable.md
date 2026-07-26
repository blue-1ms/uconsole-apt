# uConsole platform 0.1.20 stable

This is the stable platform package paired with uConsole kernel 7.1.4 on
Ubuntu 26.04 arm64 for the ClockworkPi uConsole CM4 Lite.

## Release identity

- Package: `uconsole-platform`
- Version: `0.1.20`
- SHA-256: `861323a9a285f54efff9c9478e57fef56ee98fcc86defb0d05025b4648aa2eda`
- Matching kernel release: `7.1.4-stable`
- Minimum firmware dependencies are version floors, not permanent exact pins.

## Included

- Receipt-driven kernel and A/B slot identity validation without static ABI
  whitelists.
- Complete Canonical Raspberry Pi overlay seeding for `flash-kernel`.
- Slot-specific, Mac-readable FAT diagnostic mailboxes.
- CWU50 panel, OCP8178 backlight, AXP PMIC/battery, input and audio-routing
  validation.
- Read-only `uconsole-apt-health` reporting for holds, pins, dependency issues,
  repository priority and Ubuntu Pro/ESM restrictions.
- Precise protection against Ubuntu Raspberry Pi boot-owner kernel takeover
  while allowing ordinary Ubuntu and firmware updates.

## Install or update

```bash
sudo apt update
sudo uconsole-apt-health
sudo apt install uconsole-platform
```

The package is also present, with the same SHA-256, in the signed stable APT
channel and the `7.1.4-stable` kernel Release. This tag does not represent a
rebuild or replacement package.
