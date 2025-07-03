"""Script to test and demonstrate an LED strip connected to a Raspberry Pi."""

import time
from rpi_ws281x import PixelStrip, Color


class LEDStripChecker:
    """Encapsulates LED animations for manual hardware testing."""

    LED_COUNT = 144
    LED_PIN = 18
    LED_FREQ_HZ = 800_000
    LED_DMA = 10
    LED_BRIGHTNESS = 255
    LED_INVERT = False
    LED_CHANNEL = 0

    def __init__(self):
        """Initialize the LED strip."""
        self.strip = PixelStrip(
            self.LED_COUNT,
            self.LED_PIN,
            self.LED_FREQ_HZ,
            self.LED_DMA,
            self.LED_INVERT,
            self.LED_BRIGHTNESS,
            self.LED_CHANNEL,
        )
        self.strip.begin()

    def clear(self):
        """Turn off all LEDs."""
        self.color_wipe(Color(0, 0, 0), 10)

    def color_wipe(self, color, wait_ms=10):
        """Apply a color to all LEDs, one by one."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms / 1000.0)

    def theater_chase(self, color, wait_ms=50, iterations=10):
        """Create a theater-style chasing effect."""
        for j in range(iterations):
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, color)
                self.strip.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, 0)

    def wheel(self, pos):
        """Generate a color based on a position (0-255)."""
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)

    def rainbow(self, wait_ms=20, iterations=1):
        """Display a rainbow effect across all LEDs."""
        for j in range(256 * iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel((i + j) & 255))
            self.strip.show()
            time.sleep(wait_ms / 1000.0)

    def rainbow_cycle(self, wait_ms=20, iterations=5):
        """Create a moving rainbow effect across the strip."""
        for j in range(256 * iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(
                    i, self.wheel((int(i * 256 / self.strip.numPixels()) + j) & 255)
                )
            self.strip.show()
            time.sleep(wait_ms / 1000.0)

    def theater_chase_rainbow(self, wait_ms=50):
        """Theater chase effect with rainbow colors."""
        for j in range(256):
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, self.wheel((i + j) % 255))
                self.strip.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, 0)

    def demo_color_wipe(self):
        """Run various color wipe animations."""
        print("Color wipe animations.")
        for color in [
            Color(255, 0, 0),
            Color(0, 255, 0),
            Color(0, 0, 255),
            Color(255, 255, 0),
            Color(255, 0, 255),
            Color(0, 255, 255),
            Color(255, 255, 255),
        ]:
            self.color_wipe(color)

    def demo_theater_chase(self):
        """Run various theater chase animations."""
        print("Theater chase animations.")
        for color in [
            Color(127, 127, 127),
            Color(127, 0, 0),
            Color(0, 0, 127),
            Color(0, 127, 0),
            Color(127, 127, 0),
            Color(127, 0, 127),
            Color(0, 127, 127),
        ]:
            self.theater_chase(color)

    def demo_rainbows(self):
        """Run all rainbow-based animations."""
        print("Rainbow animations.")
        self.rainbow()
        self.rainbow_cycle()
        self.theater_chase_rainbow()

    def run_all_demos(self):
        """Run all LED animations."""
        self.demo_color_wipe()
        self.demo_theater_chase()
        self.demo_rainbows()


def run_checker():
    """Entry point for running the LED strip checker."""
    print(f"GPIO port used: {LEDStripChecker.LED_PIN}")
    print(f"Number of LEDs: {LEDStripChecker.LED_COUNT}")
    checker = LEDStripChecker()

    try:
        checker.run_all_demos()
    except KeyboardInterrupt:
        print("\nTest interrupted by user.")
    finally:
        checker.clear()
        print("LEDs turned off.")


if __name__ == "__main__":
    run_checker()
