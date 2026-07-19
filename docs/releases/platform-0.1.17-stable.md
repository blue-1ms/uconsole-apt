# uConsole platform 0.1.17 stable

- `uconsole-platform 0.1.17` owns the signed APT source, complete Raspberry Pi overlay seed,
  uConsole hardware validator, audio routing, FAT diagnostics, and the Ubuntu `linux-raspi`
  takeover guard.
- `uconsole-plymouth-theme 0.1.2` provides the icon-free Material-style spinner with Ubuntu Sans
  and dynamic Ubuntu/kernel versions.
- The Plymouth package is reproducible and bound to the manifest `SOURCE_DATE_EPOCH`.
- Controlled fallback to `7.1.3-1001-uconsole` and restoration of
  `7.1.3-1003-uconsole` both passed the full `piboot-try` validator.

The attached `.deb` files are identical to the signed stable APT channel.

For a machine that has never used this repository, start with the
[first-install instructions](https://github.com/blue-1ms/uconsole-apt#first-installation). The
bootstrap verifies the full signing-key fingerprint before installing a repository-scoped key
and Deb822 source.
