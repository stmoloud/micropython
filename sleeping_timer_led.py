"""
Raspberry Pi Pico W - Sleeping Timer Then Led
1. Waits a user defined duration
2. Turns LED ON continuously
3. Stays ON until user powers-off
"""

import machine
import utime

# ===== CONFIGURATION =====
LED_PIN = 25           # Onboard LED (GPIO 25)
WAIT_HOURS = 1         # Wait 1 hour
TEST_MODE = True       # Set to False for real 1-hour wait
# =========================

# Calculate wait time
if TEST_MODE:
    WAIT_SECONDS = 10      # Test: 10 seconds
else:
    WAIT_SECONDS = WAIT_HOURS * 3600  # Real: time duration

def main():
    """Main program - waits duration, then LED on continuously"""
    
    # Setup LED
    led = machine.Pin(LED_PIN, machine.Pin.OUT)
    led.off()
    
    # ===== PHASE 1: WAIT DURATION =====
    start_time = utime.time()
    end_time = start_time + WAIT_SECONDS
    
    try:
        # Simple countdown
        while utime.time() < end_time:
            current = utime.time()
            remaining = end_time - current
            utime.sleep(1)
        
        # ===== PHASE 2: LED ON CONTINUOUSLY =====
        led.on()
        led_start = utime.time()
        
        # Keep LED on forever (until stopped)
        while True:
            # Just keep LED on - do nothing else
            utime.sleep(1)


def quick_test():
    led = machine.Pin(LED_PIN, machine.Pin.OUT)
    
    for i in range(6):  # 3 blinks
        led.toggle()
        utime.sleep_ms(500)
    
    led.off()
    # Wait a moment
    utime.sleep(2)
    
    # Run main program
    main()

# ===== RUN THE PROGRAM =====
if __name__ == "__main__":
    # Uncomment to run quick test first:
    # quick_test()
    
    # Or run directly:
    main()




