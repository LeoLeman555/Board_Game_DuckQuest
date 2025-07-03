"""Script to manually verify button functionality on a Raspberry Pi GPIO pin."""

import time
import RPi.GPIO as GPIO

def setup_gpio(pin: int) -> None:
    """Configure the GPIO pin for input with internal pull-up."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def wait_for_button(pin: int) -> None:
    """
    Continuously monitor the button pin.
    Print press/release events and duration.
    """
    press_count = 0
    is_pressed = False
    press_start_time = None

    print(f"Monitoring GPIO pin {pin} for button input (Ctrl+C to stop)...")

    try:
        while True:
            if GPIO.input(pin) == GPIO.LOW:
                if not is_pressed:
                    is_pressed = True
                    press_start_time = time.time()
                    print("Button pressed.")
            else:
                if is_pressed:
                    is_pressed = False
                    press_duration = time.time() - press_start_time
                    press_count += 1
                    print(f"Button released. Duration: {press_duration:.3f} seconds")
                    print(f"Total presses: {press_count}")
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("\nTest interrupted by user.")
    finally:
        GPIO.cleanup()
        print("GPIO cleanup complete.")
        print(f"Total button presses: {press_count}")


def run_checker(gpio_pin: int = 17) -> None:
    """Main entry point to start button checking."""
    setup_gpio(gpio_pin)
    wait_for_button(gpio_pin)


if __name__ == "__main__":
    run_checker()
