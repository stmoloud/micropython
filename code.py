"""
Pico Stopwatch v5 - flush writes
CircuitPython (Pico / Pico W)

GP15 button start/stop, writes laps to /log.txt.
Requires boot.py with: storage.remount("/", False)
Without it, write() calls silently fail (read-only FS).
"""
import board
import digitalio
import time
import os

led = digitalio.DigitalInOut(board.LED)
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
