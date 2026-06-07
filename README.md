# stmoloud/micropython

Collection of MicroPython scripts for Raspberry Pi Pico / Pico W.
Tossed together when something needed automating. Use at your own risk.

## Files

| File | What it does |
|---|---|
| `boot.py` | CircuitPython (Ref: Pico Stopwatch v6.md)   Required for any script that writes to flash. Mounts filesystem as writable. |
| `code.py` | CircuitPython (Ref: Pico Stopwatch v6.md)   Stopwatch with button (GP15), LED blink feedback, and log writes. Press to start/stop. |
| `neopixel_demo.py` | MicroPython  WS2812B LED patterns — rainbow, chase, solid colours. Configurable pin, count, brightness. |
| `sleeping_timer_led.py` | MicroPython  Waits N hours, then turns Pico LED on. Stays on until power cycle. |


## Notes

- CircuitPython mounts the filesystem **read-only by default**. Without `boot.py`, file writes silently fail — no crash, no error message, just nothing written.
- Absolutely NOT production code. Just quick utilities that happened to work.
