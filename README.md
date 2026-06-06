# stmoloud/micropython

Collection of MicroPython scripts for Raspberry Pi Pico / Pico W.
Tossed together when something needed automating. Use at your own risk.

## Files

| File | What it does |
|---|---|
| `boot.py` | CIRCUITPYTHON (Ref: Pico Stopwatch v6.md)   Required for any script that writes to flash. Mounts filesystem as writable. |
| `code.py` | CIRCUITPYTHON (Ref: Pico Stopwatch v6.md)   Stopwatch with button (GP15), LED blink feedback, and log writes. Press to start/stop. |
| `neopixel_demo.py` | MICROPYTHON  WS2812B LED patterns — rainbow, chase, solid colours. Configurable pin, count, brightness. |
| `sleeping_timer_led.py` | MICROPYTHON  Waits N hours, then turns Pico LED on. Stays on until power cycle. |
| `sleeping_timer_led_REPL.py` | MICROPYTHON  Same timer logic but with serial output. |


## Notes

- CircuitPython mounts the filesystem **read-only by default**. Without `boot.py`, file writes silently fail — no crash, no error message, just nothing written.
- Absolutely NOT production code. Just quick utilities that happened to work.
