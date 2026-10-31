# Sega Channel 42 launcher for FieldStation42

A community launcher that connects a Raspberry Pi RetroArch setup to a FieldStation42 executable channel. It launches full-screen, selects a different Sega Channel Revival ROM by calendar month, and prevents duplicate launches. Unofficial; not affiliated with Sega.

## Release status

Draft prepared from the working node1 backup dated 2026-10-31T02:36Z. Live SSH authentication was unavailable during packaging. The launcher syntax and installer are checked locally; a fresh Raspberry Pi installation and channel-switching test are still required. This package does not implement the Revival game menu itself: that comes from the user-supplied ROM. It does not contain all of FieldStation42 or modify its player.

## Requirements

- Raspberry Pi with a working graphical desktop and audio. The source setup used an X11 display at :0; other display sessions may need configuration.
- RetroArch installed and working with your controller; `flock` (normally provided by util-linux).
- A compatible Genesis Plus GX expanded-ROM libretro core for your Pi architecture. Large Revival images require an appropriate expanded-ROM core; do not assume a standard Genesis core supports them.
- Your own compatible ROM files.
- For channel integration, a FieldStation42 build supporting `network_type: executable` and `executable_command`. Check your installed build first. Channel number 42 must be free, or choose another number.

## Install

Unpack this project, then run as the same desktop user who runs FieldStation42:

```bash
python3 install.py --fs42 "$HOME/FieldStation42" --channel 42
```

For standalone installation omit `--fs42`. Default destination: `~/sega-channel42`. The installer preserves existing launcher/config files and refuses to replace an existing station file or occupied channel. It does not install system packages, download games/cores, restart services, or change controller settings.

Put the architecture-compatible core at:

```
~/sega-channel42/cores/genesis_plus_gx_ex_libretro.so
```

Place your own monthly ROMs in `~/sega-channel42/roms/`. Exact expected names are listed in `bin/sega-channel42` in January–December order; names are case-sensitive. Alternatively test a single ROM with:

```bash
SEGA_CHANNEL42_ROM="/absolute/path/to/your-game.md" "$HOME/sega-channel42/bin/sega-channel42"
```

Run that command from a terminal in your desktop session first. Once it works, reload/restart FieldStation42 using your normal procedure and tune the configured channel. Test switching away and back; executable cleanup depends on your FieldStation42 version. No automatic service restart is performed.

## Configuration and troubleshooting

- `SEGA_CHANNEL42_HOME`: launcher data directory (default `~/sega-channel42`).
- `SEGA_CHANNEL42_CORE`: override the libretro core path.
- `SEGA_CHANNEL42_ROM`: override calendar selection with a single game.
- Logs: `~/sega-channel42/logs/channel42.log` (not automatically rotated).
- The launcher honors existing DISPLAY, XAUTHORITY and XDG_RUNTIME_DIR variables. Run as the logged-in desktop user. Defaults target X11; Wayland is not verified.
- If nothing starts, read the log, verify the monthly filename/core, then test RetroArch independently. A missing current-month ROM causes a clear failure, not a fallback to another game.
- Configure your gamepad in RetroArch. This package does not remap the TV remote or GPIO keypad.
- To remove: delete the generated `confs/sega_channel42.json` after reviewing it, then remove the launcher folder only after preserving your games/saves. No system services are installed.

## What is shared

Only the launcher, installer, and example RetroArch settings are included. No ROMs, BIOS files, emulator binaries, artwork, music, personal settings, credentials, or node backups are included.

See THIRD_PARTY.md for dependency sources and license boundaries. The MIT license in this package covers these launcher/installer files only.
