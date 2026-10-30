# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Working agreement

- Do not modify, delete, or rename existing files, and do not commit, push, or create branches, without the owner's explicit consent. Propose changes first.
- Never run `make install`, `make uninstall`, `make run`, `install.sh`, `uninstall.sh`, or `setup_raspberry-zero.sh` on the development machine: they use `sudo`, `apt-get`, and `systemctl` and target a Raspberry Pi.

## Project

solrpi drives a 32-pixel WS281x RGB LED HAT on a Raspberry Pi Zero. It shows current grid consumption and PV production, polled from a Fronius inverter's HTTP API. It's a plain Python 3 project with no framework.

## Commands

- `make` / `make all`: create `.venv` and install `requirements_base.txt` (pytest, requests, responses).
- `make test`: run `pytest -rP` in the venv. This works on macOS/Linux and needs no hardware.
- Single test: `.venv/bin/python3 -m pytest test/test_solrpi_ledmatrix.py::test_compute_idxs_grid_only`
- `make asciidemo`: run the renderer against a mock inverter and an ASCII terminal UI (`solrpi_demo_ascii.py`). It logs DEBUG output to `./solrpi.log`.
- `make run` / `make pkg`: Pi only. They install `rpi_ws281x` (`requirements_runtime.txt`), which doesn't build on macOS.

## Architecture

- `solrpi_main.py`: production entry point. It wires `FroniusInverter` and `NeoPixel` into `Renderer`, handles SIGTERM (clears the display) and SIGQUIT (prints a stack trace), and logs WARN to `/var/log/solrpi.log`.
- `solrpi/i_inverter.py` `Inverter`: interface. `get_watt()` returns `[grid, pv, battery]` in watts. `grid < 0` means feeding into the grid, `pv` is always ≥ 0, and `battery < 0` means charging, `> 0` discharging (Fronius `P_Akku` convention, `null` → 0). The renderer also accepts the legacy two-value form. It raises an exception on error.
- `solrpi/i_uidevice.py` `UIDevice`: display interface (pixels, brightness, draw, clear, named colors).
- `solrpi/fronius_inverter.py`: `Inverter` implementation. The URL is hardcoded in `FRONIUS_URL`, with a 1 s timeout.
- `solrpi/neopixel.py`: `UIDevice` on `rpi_ws281x`. It imports hardware libraries, so it can't be imported on non-Pi machines.
- `solrpi/ledmatrix.py`: pure logic, and the main unit-test target. It converts watts into the `Idxs(consume, discharge, charge, grid, pv)` pixel layers (`MAX_WATT=6400` over 4×8 pixels). Each field is the cumulative end index of its layer. From the bottom up: green self-consumption, magenta battery discharge, orange battery charge, red grid import, yellow grid export. It also handles brightness, step-wise transitions, and `render()` into a HEIGHT×WIDTH matrix filled snake-wise.
- `solrpi/renderer.py` `Renderer.run()`: endless loop that polls the inverter, animates the transition, and sleeps for 2 s (0.4 s after a change). Each cycle blinks one pixel as a heartbeat. Between 00:00 and 05:00 it clears the display (power-save mode) and triple-blinks every 60 s. On a poll error it keeps the previous display.
- `demo/`: `InverterMock` (cycles fixed sample values) and `AsciiUI` (terminal display) for running without hardware.
- `test/`: pytest. Fronius tests mock HTTP with `responses` and sample JSON in `test/`. Tests open fixture files with paths relative to the repo root, so run pytest from the root.

To add support for another inverter, implement `Inverter` and swap the class in `solrpi_main.py`. See README.md.

## Deployment (reference only)

`install.sh` copies `solrpi/` and `solrpi_main.py` to `/usr/local/solrpi`, creates a venv there, and installs and starts `service/solrpi.service` as root.

## Conventions

- Every source file starts with the MPL-2.0 copyright header. Keep it in new files.
- Code uses module-level `logger = logging.getLogger(__name__)` and uppercase module constants for tunables.
- Indentation is mixed: the entry scripts use tabs and the package modules use 4 spaces. Match the file you edit.
- Some comments in `ledmatrix.py` are in German (Eigenverbrauch = self-consumption, Überschuss = surplus, Netzbezug = grid draw).
