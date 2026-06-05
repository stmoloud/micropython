# stmoloud/micropython

Collection of MicroPython scripts for Raspberry Pi Pico / Pico W.
Tossed together when something needed automating. Use at your own risk.

## Files

| File | What it does |
|---|---|
| `boot.py` | Required for any script that writes to flash. Mounts filesystem as writable. |
| `code.py` | Stopwatch with button (GP15), LED blink feedback, and log writes. Press to start/stop. |
| `neopixel_demo.py` | WS2812B LED patterns — rainbow, chase, solid colours. Configurable pin, count, brightness. |
| `sleeping_timer_led.py` | Waits N hours, then turns Pico LED on. Stays on until power cycle. |
| `sleeping_timer_led_test.py` | Same timer logic but with serial output + faster cycles for testing. |

## Quick start

1. Copy whichever `.py` files you need onto your Pico's CIRCUITPY drive
2. Always include `boot.py` if the script writes to filesystem
3. Rename the script to `code.py` (or `main.py`) for autorun on power-up

## Pin assignments

- **GP15** — Stopwatch button (code.py only)
- **GP1** — NeoPixel data (neopixel_demo.py only)
- **GP25 / onboard LED** — status indicator (all scripts)

## Notes

- CircuitPython mounts the filesystem **read-only by default**. Without `boot.py`, file writes silently fail — no crash, no error message, just nothing written.
- These aren't production code. They're quick utilities that happened to work.
- PRs welcome but no promises on response time.
