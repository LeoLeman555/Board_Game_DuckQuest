import RPi.GPIO as GPIO


class ButtonManager:
    """Manage multiple buttons connected to GPIO."""

    def __init__(self, pins: list):
        self.pins = pins
        GPIO.setmode(GPIO.BCM)
        self.setup_buttons()

    def setup_buttons(self):
        """Configure GPIO pins as input with pull-up enabled."""
        for pin in self.pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def get_pressed_button(self) -> int | None:
        """Return the pressed button if any, otherwise None."""
        for pin in self.pins:
            if GPIO.input(pin) == GPIO.LOW:  # Button pressed
                return pin
        return None  # No button pressed

    def cleanup(self):
        """Clean up GPIO."""
        GPIO.cleanup()
