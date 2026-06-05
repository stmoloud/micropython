"""
Pico Stopwatch v6 - Pico / Pico W LED fix
CircuitPython (Pico / Pico W)

GP15 button start/stop, writes laps to /log.txt.
Requires boot.py with: storage.remount("/", False)
Without it, write() calls silently fail (read-only FS).

LED:
- Pico (non-W): uses onboard LED (board.LED)
- Pico W: onboard LED is unreliable (goes via CYW43 wifi chip),
  so set LED_PIN to an external GPIO (e.g. GP16) and wire an LED
  with a 330Ω resistor to ground.
"""
import board
import digitalio
import time
import os
import rtc
import sys

# --- LED Setup ---
# Change LED_PIN for your board:
#   None          = try board.LED (works on Pico, glitchy on Pico W)
#   board.GP16    = external LED on GP16 + 330Ω resistor to GND
LED_PIN = None          # <-- set to board.GPxx for external LED

if LED_PIN is not None:
    led = digitalio.DigitalInOut(LED_PIN)
else:
    try:
        led = digitalio.DigitalInOut(board.LED)
    except AttributeError:
        print("No onboard LED — set LED_PIN to a GPIO for external LED")
        sys.exit(1)
led.direction = digitalio.Direction.OUTPUT

button = digitalio.DigitalInOut(board.GP15)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# Boot indicator
for _ in range(2):
    led.value = True
    time.sleep(0.15)
    led.value = False
    time.sleep(0.15)

# Set RTC — update before flashing: set_rtc(day, month, year, hour, minute, dst)
def set_rtc(d, m, y, hr, mi, dst=0):
    r = rtc.RTC()
    # struct_time: year, month, day, hour, minute, second, weekday, yearday, dst
    r.datetime = time.struct_time((y, m, d, hr, mi, 0, 0, -1, dst))

set_rtc(6, 6, 2026, 5, 30, 0)

state = "IDLE"
start_time = 0.0

def write_log(text):
    """Write to file with flush and sync."""
    try:
        f = open("/log.txt", "a")
        f.write(text + "\n")
        f.flush()
        os.sync()
        f.close()
        return True
    except:
        return False

while True:
    if not button.value:
        time.sleep(0.02)
        if not button.value:
            if state == "IDLE":
                start_time = time.monotonic()
                led.value = True
                state = "RUNNING"

                t = time.localtime()
                ts = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
                    t.tm_year, t.tm_mon, t.tm_mday,
                    t.tm_hour, t.tm_min, t.tm_sec
                )
                write_log("[START] " + ts)

                while not button.value:
                    time.sleep(0.01)

            elif state == "RUNNING":
                elapsed = time.monotonic() - start_time
                led.value = False

                t = time.localtime()
                end_ts = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
                    t.tm_year, t.tm_mon, t.tm_mday,
                    t.tm_hour, t.tm_min, t.tm_sec
                )

                h = int(elapsed // 3600)
                m = int((elapsed % 3600) // 60)
                s = int(elapsed % 60)
                dur = "{:02d}:{:02d}:{:02d}".format(h, m, s)

                ok = write_log("[STOP]  " + end_ts)
                ok = write_log("[DUR]   " + dur + " (" + "{:.1f}".format(elapsed) + "s)") and ok
                ok = write_log("") and ok

                # 3 blinks = stop + long flash if write failed
                for _ in range(3):
                    led.value = True
                    time.sleep(0.15)
                    led.value = False
                    time.sleep(0.15)

                if not ok:
                    # Long flash = write failed!
                    led.value = True
                    time.sleep(1.5)
                    led.value = False

                state = "IDLE"

                while not button.value:
                    time.sleep(0.01)

    time.sleep(0.01)
