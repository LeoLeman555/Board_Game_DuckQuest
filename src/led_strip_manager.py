import time
from rpi_ws281x import PixelStrip, Color

LED_COUNT = 144  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 10  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53


class LEDStripManager:
    """Manage an LED strip with various lighting effects."""

    def __init__(self):
        """Initialize the LED strip."""
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

    def set_pixel_color(self, pixel: int, color: tuple[int, int, int]):
        """Set a specific pixel to the given color and updates the strip."""
        self.strip.setPixelColor(pixel, Color(*color))
        self.strip.show()

    def set_all_pixels(self, color: tuple[int, int, int]):
        """Set all pixels to the specified color and updates the strip."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(*color))
        self.strip.show()

    def score_effect(self, percentage: float = 1) -> tuple[int, int, int]:
        """Create a progress effect, changing the strip's color gradually."""
        pause = 60  # Initial delay in milliseconds
        color = (0, 0, 0)
        progress = 0.0
        steps = int(self.strip.numPixels() * percentage)

        for i in range(steps):
            color = (
                int(255 * (1 - progress)),
                int(255 * progress),
                0,
            )  # Gradient from red to green
            self.strip.setPixelColor(i, Color(*color))
            self.strip.show()
            progress += percentage / steps
            pause = max(
                10, pause - (i * percentage / 200)
            )  # Reduce pause over time but ensure a minimum
            time.sleep(pause / 1000.0)  # Convert ms to seconds

        time.sleep(0.1)
        return color

    def blink(self, color: tuple[int, int, int], repetitions: int, wait_ms: float):
        """Make the strip blink with the given color for a set number of repetitions."""
        for _ in range(repetitions):
            self.set_all_pixels(color)
            time.sleep(wait_ms / 1000.0)
            self.set_all_pixels((0, 0, 0))  # Turn off LEDs between blinks
            time.sleep(wait_ms / 1000.0)

    def clear(self):
        """Turn off all LEDs."""
        self.set_all_pixels((0, 0, 0))
