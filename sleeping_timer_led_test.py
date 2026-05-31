"""
Raspberry Pi Pico W - One Hour Wait then Continuous LED
Exactly what you asked for:
1. Waits one hour
2. Turns LED ON continuously
3. Stays ON until you stop the program

Simple, no-frills version.
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
    print("⚠ TEST MODE: Waiting 10 seconds instead of 1 hour")
else:
    WAIT_SECONDS = WAIT_HOURS * 3600  # Real: 1 hour

def main():
    """Main program - waits 1 hour, then LED on continuously"""
    
    # Setup LED
    led = machine.Pin(LED_PIN, machine.Pin.OUT)
    led.off()
    
    print("\n" + "="*50)
    print("PICO W - 1 HOUR WAIT THEN LED")
    print("="*50)
    print(f"LED: GPIO{LED_PIN}")
    print(f"Wait: {WAIT_HOURS} hour ({WAIT_SECONDS} seconds)")
    print(f"Start: {get_time()}")
    print("="*50)
    
    # ===== PHASE 1: WAIT ONE HOUR =====
    print(f"\n⏳ WAITING {WAIT_HOURS} HOUR...")
    print("   (Press Ctrl+C to stop early)")
    
    start_time = utime.time()
    end_time = start_time + WAIT_SECONDS
    
    try:
        # Simple countdown
        while utime.time() < end_time:
            current = utime.time()
            remaining = end_time - current
            
            # Show progress every minute (or every 10% in test mode)
            if TEST_MODE:
                if remaining % 2 == 0:  # Every 2 seconds in test mode
                    print(f"⏳ {remaining} seconds remaining")
            elif remaining % 60 == 0:  # Every minute in normal mode
                minutes = remaining // 60
                print(f"⏳ {minutes} minutes remaining")
            
            utime.sleep(1)
        
        # ===== PHASE 2: LED ON CONTINUOUSLY =====
        print("\n" + "="*50)
        print("🎯 1 HOUR COMPLETE!")
        print("="*50)
        print("💡 TURNING LED ON CONTINUOUSLY")
        print("   LED will stay ON until you stop the program")
        print("   Press Ctrl+C to stop and turn LED off")
        print("="*50)
        
        led.on()
        led_start = utime.time()
        
        # Keep LED on forever (until stopped)
        while True:
            # Just keep LED on - do nothing else
            utime.sleep(1)
            
            # Optional: Show how long LED has been on
            current = utime.time()
            if current % 60 == 0:  # Every minute
                active_seconds = current - led_start
                minutes = active_seconds // 60
                print(f"💡 LED ON for {minutes} minutes")
    
    except KeyboardInterrupt:
        print("\n\n🛑 PROGRAM STOPPED")
    finally:
        led.off()
        print("   LED turned OFF")
        print("\n" + "="*50)
        print("PROGRAM ENDED")
        print("="*50)

def get_time():
    """Get current time as HH:MM:SS"""
    t = utime.localtime()
    return f"{t[3]:02d}:{t[4]:02d}:{t[5]:02d}"

def quick_test():
    """Quick test - blinks LED 3 times then runs main program"""
    print("\n🔧 QUICK HARDWARE TEST")
    led = machine.Pin(LED_PIN, machine.Pin.OUT)
    
    print("Blinking LED 3 times...")
    for i in range(6):  # 3 blinks
        led.toggle()
        utime.sleep_ms(500)
    
    led.off()
    print("✅ Test complete\n")
    
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


# Ultra-simple version (minimal code)
def ultra_simple():
    """Absolute minimum code version"""
    led = machine.Pin(25, machine.Pin.OUT)
    led.off()
    
    print("Waiting 1 hour...")
    utime.sleep(3600)  # Wait 1 hour
    
    print("1 hour complete. LED ON.")
    led.on()
    
    # LED stays on forever
    while True:
        utime.sleep(1)