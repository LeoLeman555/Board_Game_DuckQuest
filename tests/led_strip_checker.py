import time
from rpi_ws281x import PixelStrip, Color


LED_COUNT = 144  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53


class LEDStripChecker:
    def __init__(self):
        """Initializes the LED strip."""
        self.strip = PixelStrip(
            LED_COUNT,
            LED_PIN,
            LED_FREQ_HZ,
            LED_DMA,
            LED_INVERT,
            LED_BRIGHTNESS,
            LED_CHANNEL,
        )
        self.strip.begin()

    def color_wipe(self, color, wait_ms=10):
        """Applies a color to all LEDs, one by one."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms / 1000.0)

    def theater_chase(self, color, wait_ms=50, iterations=10):
        """Creates a theater-style chasing effect."""
        for j in range(iterations):
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, color)
                self.strip.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, 0)

    def wheel(self, pos):
        """Generates a rainbow color based on a given position (0-255)."""
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)

    def rainbow(self, wait_ms=20, iterations=1):
        """Displays a rainbow effect across all LEDs."""
        for j in range(256 * iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel((i + j) & 255))
            self.strip.show()
            time.sleep(wait_ms / 1000.0)

    def rainbow_cycle(self, wait_ms=20, iterations=5):
        """Creates a moving rainbow effect across the strip."""
        for j in range(256 * iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(
                    i, self.wheel((int(i * 256 / self.strip.numPixels()) + j) & 255)
                )
            self.strip.show()
            time.sleep(wait_ms / 1000.0)

    def theater_chase_rainbow(self, wait_ms=50):
        """Creates a theater-style chasing effect with rainbow colors."""
        for j in range(256):
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, self.wheel((i + j) % 255))
                self.strip.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, 0)

    def clear(self):
        """Turns off all LEDs."""
        self.color_wipe(Color(0, 0, 0), 10)

    def run_demo(self):
        """Runs a demonstration sequence of the LED animations."""
        try:
            while True:
                print("Color wipe animations.")
                self.color_wipe(Color(255, 0, 0))  # Red
                self.color_wipe(Color(0, 255, 0))  # Green
                self.color_wipe(Color(0, 0, 255))  # Blue
                self.color_wipe(Color(255, 255, 0))  # Yellow
                self.color_wipe(Color(255, 0, 255))  # Magenta
                self.color_wipe(Color(0, 255, 255))  # Cyan
                self.color_wipe(Color(255, 255, 255))  # White

                print("Theater chase animations.")
                self.theater_chase(Color(127, 127, 127))  # White
                self.theater_chase(Color(127, 0, 0))  # Red
                self.theater_chase(Color(0, 0, 127))  # Blue
                self.theater_chase(Color(0, 127, 0))  # Green
                self.theater_chase(Color(127, 127, 0))  # Yellow
                self.theater_chase(Color(127, 0, 127))  # Magenta
                self.theater_chase(Color(0, 127, 127))  # Cyan

                print("Rainbow animations.")
                self.rainbow()
                self.rainbow_cycle()
                self.theater_chase_rainbow()
        except KeyboardInterrupt:
            print("\nProgram stopped, turning off LEDs.")
            self.clear()


# Run if this file is executed directly
if __name__ == "__main__":
    print(f"GPIO port used: {LED_PIN}")
    print(f"Number of LEDs: {LED_COUNT}")
    led_strip = LEDStripChecker()
    led_strip.run_demo()
