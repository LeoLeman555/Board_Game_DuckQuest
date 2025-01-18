import RPi.GPIO as GPIO
import time
import os

# Ensure the logs directory exists
if not os.path.exists("logs"):
    os.makedirs("logs")


class ButtonTest:
    def __init__(self, button_gpio=17, log_file="logs/button_test.txt"):
        self.button_gpio = button_gpio  # GPIO pin used for the button
        self.log_file = log_file  # File to log events
        self.press_count = 0
        self.is_pressed = False
        self.press_start_time = None
        self.start_time = time.time()

        # GPIO configuration
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.button_gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Write the header with the test start time
        start_timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "w") as f:
            f.write(f"Test started: {start_timestamp}\n")
            f.write("The events will be logged here.\n\n")

    def log_event(self, event):
        """Log the event with timestamp into the log file."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a") as f:
            f.write(f"{timestamp} - {event}\n")

    def handle_button_press(self):
        """Detect button presses and log the events."""
        try:
            while True:
                if GPIO.input(self.button_gpio) == GPIO.LOW:
                    if not self.is_pressed:  # Detect the start of the press
                        self.is_pressed = True
                        self.press_start_time = time.time()
                        print("Button pressed!")
                else:
                    if self.is_pressed:  # Detect the end of the press
                        self.is_pressed = False
                        self.press_count += 1
                        press_duration = time.time() - self.press_start_time
                        print(
                            f"Button released! Duration: {press_duration:.3f} seconds"
                        )
                        print(f"Total presses: {self.press_count}")
                        # Log the events
                        self.log_event(
                            f"Button pressed and released. Duration: {press_duration:.3f} s. Count: {self.press_count}"
                        )

                time.sleep(0.01)  # Small delay to limit CPU usage
        except KeyboardInterrupt:
            print("\nTest stopped by the user.")
        finally:
            self.cleanup()

    def cleanup(self):
        """Perform cleanup and log the test duration and statistics."""
        GPIO.cleanup()

        # Calculate the total test duration
        end_time = time.time()
        total_duration = end_time - self.start_time
        total_duration_minutes = total_duration // 60
        total_duration_seconds = total_duration % 60

        # Write the final stats to the log file
        with open(self.log_file, "a") as f:
            f.write(f"\nTest ended: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(
                f"Total test duration: {int(total_duration_minutes)} minutes and {int(total_duration_seconds)} seconds\n"
            )
            f.write(f"Total presses: {self.press_count}\n")

        print("GPIO cleanup completed.")
        print(
            f"Total test duration: {int(total_duration_minutes)} minutes and {int(total_duration_seconds)} seconds"
        )
        print(f"Total presses: {self.press_count}")


# Main program
if __name__ == "__main__":
    button_test = ButtonTest()
    print(f"GPIO port used: {button_test.button_gpio}")
    print("Configuration: Button set with internal pull-up.")
    print(f"Events will be logged in the file: {button_test.log_file}")
    print("Press the button to start.")
    button_test.handle_button_press()
