import time
import RPi.GPIO as GPIO
from rpi_ws281x import PixelStrip, Color

# GPIO pin for the button
BUTTON_GPIO = 17  # Change this according to your setup

# LED strip configuration
LED_COUNT = 144  # Number of LEDs in the strip
LED_PIN = 18  # GPIO pin connected to the LED strip (18 uses PWM!)
LED_FREQ_HZ = 800000  # LED signal frequency (typically 800kHz)
LED_DMA = 10  # DMA channel for generating the signal
LED_BRIGHTNESS = 10  # Brightness level (0 = off, 255 = max brightness)
LED_INVERT = (
    False  # Invert signal (set True if using an NPN transistor for level shifting)
)
LED_CHANNEL = 0  # Use channel 1 for GPIOs 13, 19, 41, 45, or 53


class HardwareChecker:
    """Controls the LED strip and monitors a button press."""

    def __init__(self, button_gpio):
        self.button_gpio = button_gpio
        self._setup_gpio()

        # Initialize LED strip
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

    def _setup_gpio(self):
        """Configures the GPIO pin for the button with a pull-up resistor."""
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.button_gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def all_color(self, color):
        """Sets all LEDs to a specified color."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
        self.strip.show()

    def blink(self, color, repetitions, wait_ms):
        """Blinks the LEDs with a given color and duration."""
        for _ in range(repetitions):
            self.all_color(color)
            time.sleep(wait_ms / 1000.0)
            self.all_color(Color(0, 0, 0))  # Turn off LEDs
            time.sleep(wait_ms / 1000.0)

    def clear(self):
        """Turns off all LEDs."""
        self.all_color(Color(0, 0, 0))

    def cleanup(self):
        """Turns off LEDs and resets GPIO settings before exiting."""
        self.clear()
        GPIO.cleanup()
        print("GPIO cleaned up. Program exiting.")

    def run(self):
        """Continuously monitors the button and changes LED color when pressed."""
        print("Press the button to turn the LEDs yellow.")
        try:
            while True:
                if GPIO.input(self.button_gpio) == GPIO.LOW:  # Button is pressed
                    self.all_color(Color(255, 255, 0))  # Set LEDs to yellow
                    time.sleep(0.2)  # Small delay to avoid bouncing issues
                else:
                    self.clear()
                time.sleep(0.01)  # Short delay to reduce CPU usage
        except KeyboardInterrupt:
            print("Program interrupted by user.")
        finally:
            self.cleanup()


# Main execution
if __name__ == "__main__":
    print(f"GPIO port used for the button: {BUTTON_GPIO}")
    print(f"GPIO port used for LEDs: {LED_PIN}")
    print(f"Number of LEDs: {LED_COUNT}")

    signal = HardwareChecker(BUTTON_GPIO)
    signal.run()
