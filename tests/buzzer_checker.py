import RPi.GPIO as GPIO
import pygame
import time


class BuzzerChecker:
    def __init__(self, button_gpio, sound_file):
        self.button_gpio = button_gpio
        self.sound_file = sound_file

        # Initialize GPIO and pygame mixer
        self._setup_gpio()
        self._setup_pygame()

    def _setup_gpio(self):
        """Sets up the GPIO pin for the button with pull-up resistor."""
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.button_gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def _setup_pygame(self):
        """Initializes the pygame mixer for audio playback."""
        pygame.mixer.init()
        try:
            pygame.mixer.music.load(self.sound_file)
        except pygame.error as e:
            print(f"Error loading sound file: {e}")
            exit(1)

    def play_sound_on_button_press(self):
        """Continuously checks for button press and plays sound when pressed."""
        print("Press the button to play the sound.")
        try:
            while True:
                if GPIO.input(self.button_gpio) == GPIO.LOW:  # Button pressed
                    pygame.mixer.music.play()
                    time.sleep(0.2)  # Delay to prevent repeated sound triggers
                time.sleep(0.01)  # Small delay for debounce
        except KeyboardInterrupt:
            print("Program interrupted by user.")
        finally:
            self.cleanup()

    def cleanup(self):
        """Cleans up GPIO settings before exiting the program."""
        GPIO.cleanup()
        print("GPIO cleaned up. Program exiting.")


if __name__ == "__main__":
    BUTTON_GPIO = 17  # Replace with your button's GPIO pin
    SOUND_FILE = (
        "duckquest/assets/sounds/congratulation.wav"  # Replace with the path to your sound file
    )
    button_sound_player = BuzzerChecker(BUTTON_GPIO, SOUND_FILE)
    button_sound_player.play_sound_on_button_press()
