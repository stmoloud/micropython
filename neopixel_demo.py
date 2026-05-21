"""
NeoPixel LED Controller for MicroPython (Raspberry Pi Pico W)
Improved version with better brightness control and patterns
"""

import neopixel
from machine import Pin
import time

# ===== CONFIGURATION =====
WS_PIN = 1          # GPIO pin for NeoPixel data
LED_COUNT = 5       # Number of NeoPixel LEDs
BRIGHTNESS = 0.5    # 0.0 to 1.0 (50% brightness)
PATTERN_DELAY = 0.5 # Delay between pattern steps (seconds)
# =========================

# Initialize NeoPixel strip
np = neopixel.NeoPixel(Pin(WS_PIN), LED_COUNT)

def set_brightness(color, brightness=BRIGHTNESS):
    """
    Apply brightness to RGB color for MicroPython
    MicroPython doesn't have round(), so we use integer math
    """
    r, g, b = color
    
    # Integer math for brightness (more efficient on MicroPython)
    r = (r * brightness) // 1  # Equivalent to int(r * brightness)
    g = (g * brightness) // 1
    b = (b * brightness) // 1
    
    # Ensure values stay in 0-255 range
    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))
    
    return (int(r), int(g), int(b))

def clear_leds():
    """Turn off all LEDs"""
    np.fill((0, 0, 0))
    np.write()

def set_all(color):
    """Set all LEDs to the same color"""
    color = set_brightness(color)
    np.fill(color)
    np.write()

def set_led(index, color):
    """Set a specific LED to a color"""
    if 0 <= index < LED_COUNT:
        color = set_brightness(color)
        np[index] = color
        np.write()

def rainbow_wheel(pos):
    """Generate rainbow colors across 0-255 positions"""
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)

def color_sequence():
    """Display a sequence of colors on all LEDs"""
    colors = [
        ("White", (255, 255, 255)),
        ("Yellow", (255, 255, 0)),
        ("Purple", (128, 0, 128)),
        ("Red", (255, 0, 0)),
        ("Green", (0, 255, 0)),
        ("Blue", (0, 0, 255)),
        ("Cyan", (0, 255, 255)),
        ("Magenta", (255, 0, 255)),
        ("Orange", (255, 165, 0)),
    ]
    
    for name, color in colors:
        print(f"Showing: {name}")
        set_all(color)
        time.sleep(PATTERN_DELAY * 2)

def knight_rider():
    """Knight Rider scanning pattern"""
    print("Knight Rider pattern")
    for i in range(LED_COUNT):
        clear_leds()
        set_led(i, (255, 0, 0))  # Red
        time.sleep(PATTERN_DELAY / 2)
    
    for i in range(LED_COUNT - 2, 0, -1):
        clear_leds()
        set_led(i, (255, 0, 0))  # Red
        time.sleep(PATTERN_DELAY / 2)

def breathing(color=(255, 255, 255)):
    """Breathing effect with specified color"""
    print(f"Breathing: {color}")
    steps = 20
    for i in range(steps):
        # Calculate brightness from 0.1 to 1.0 and back
        if i < steps / 2:
            brightness = 0.1 + (i / (steps / 2)) * 0.9
        else:
            brightness = 1.0 - ((i - steps / 2) / (steps / 2)) * 0.9
        
        r, g, b = color
        r = int(r * brightness * BRIGHTNESS)
        g = int(g * brightness * BRIGHTNESS)
        b = int(b * brightness * BRIGHTNESS)
        
        np.fill((r, g, b))
        np.write()
        time.sleep(0.05)

def rainbow_cycle():
    """Rainbow cycle animation"""
    print("Rainbow cycle")
    for j in range(256):  # One complete cycle
        for i in range(LED_COUNT):
            # Generate rainbow colors
            rc_index = (i * 256 // LED_COUNT) + j
            color = rainbow_wheel(rc_index & 255)
            color = set_brightness(color)
            np[i] = color
        np.write()
        time.sleep(0.02)

def test_patterns():
    """Run through all available patterns"""
    print("\n" + "="*40)
    print("NeoPixel Pattern Demo")
    print("="*40)
    print(f"LEDs: {LED_COUNT}, Brightness: {BRIGHTNESS}")
    print("="*40)
    
    patterns = [
        ("Color Sequence", color_sequence),
        ("Knight Rider", knight_rider),
        ("Blue Breathing", lambda: breathing((0, 0, 255))),
        ("Rainbow Cycle", rainbow_cycle),
        ("Green Breathing", lambda: breathing((0, 255, 0))),
    ]
    
    for pattern_name, pattern_func in patterns:
        print(f"\nPattern: {pattern_name}")
        pattern_func()
        time.sleep(0.5)  # Brief pause between patterns
    
    # End with all off
    clear_leds()
    print("\nDemo complete. All LEDs off.")

def main():
    """Main program with button control option"""
    print("NeoPixel MicroPython Controller")
    print("Press Ctrl+C to stop")
    
    # Optional: Add button for pattern control
    # button = Pin(0, Pin.IN, Pin.PULL_UP)  # GPIO 0 with pull-up
    
    try:
        # Run demo once
        test_patterns()
        
        # Or run continuous pattern cycle
        print("\nStarting continuous pattern cycle...")
        pattern_index = 0
        patterns = [color_sequence, knight_rider, rainbow_cycle]
        
        while True:
            patterns[pattern_index % len(patterns)]()
            pattern_index += 1
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\nProgram stopped by user")
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        # Always turn off LEDs when exiting
        clear_leds()
        print("LEDs cleared. Goodbye!")

# Configuration helper function
def configure():
    """Interactive configuration (optional)"""
    # This could read from a config file or use buttons
    # For now, just print current config
    print(f"Current configuration:")
    print(f"  Pin: GPIO{WS_PIN}")
    print(f"  LED count: {LED_COUNT}")
    print(f"  Brightness: {BRIGHTNESS}")
    print(f"  Pattern delay: {PATTERN_DELAY}s")

# Run the program
if __name__ == "__main__":
    # Optional: Show configuration
    # configure()
    
    # Run main program
    main()

# Quick test function (call from REPL)
def quick_test():
    """Quick test - run this from REPL to verify hardware"""
    print("Quick NeoPixel test...")
    
    # Test basic colors
    test_colors = [
        (255, 0, 0),    # Red
        (0, 255, 0),    # Green
        (0, 0, 255),    # Blue
        (255, 255, 255) # White
    ]
    
    for color in test_colors:
        print(f"Testing color: {color}")
        set_all(color)
        time.sleep(1)
    
    clear_leds()
    print("Test complete. LEDs off.")

# Individual pattern functions for REPL use
def demo_colors():
    """Just show the color sequence"""
    color_sequence()

def demo_knight():
    """Just show knight rider"""
    knight_rider()

def demo_rainbow():
    """Just show rainbow"""
    rainbow_cycle()

def demo_breathe():
    """Just show breathing effect"""
    breathing()