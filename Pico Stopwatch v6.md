# Pico Stopwatch v6 - Pico / Pico W LED fix
  Circuit Python (Pico / Pico W)

1. Download [Circuit Python](https://circuitpython.org/downloads)
2. Flash to Pico / Pico W 
3. Copy over code.py

GP15 button start/stop, writes laps to /log.txt.
Requires boot.py 

--> CAUTION: [read this first](https://learn.adafruit.com/cpu-temperature-logging-with-circuit-python/writing-to-the-filesystem)

Without boot.py, write() calls silently fail (read-only FS).

LED:
- Pico (non-W): uses onboard LED (board.LED)
- Pico W: onboard LED is unreliable (goes via CYW43 wifi chip),
  so set LED_PIN to an external GPIO (e.g. GP16) and wire an LED
  with a 330Ω resistor to ground.

