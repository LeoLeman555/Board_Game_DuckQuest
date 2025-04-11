import pygame


class AudioManager:
    """Manages background music and sound effects."""

    def __init__(self):
        pygame.mixer.init()
        self.music_paused = False  # Tracks if the music is paused

    def play_music(self, file_path: str, loop=-1):
        """Play background music."""
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play(loop)
            self.music_paused = False
        except Exception as e:
            print(f"Error playing music: {e}")

    def pause_or_resume_music(self):
        """Pause or resume the currently playing music."""
        if self.music_paused:
            pygame.mixer.music.unpause()
            self.music_paused = False
        else:
            pygame.mixer.music.pause()
            self.music_paused = True

    def stop_music(self):
        """Stop the background music."""
        try:
            pygame.mixer.music.stop()
            self.music_paused = False
        except Exception as e:
            print(f"Error stopping music: {e}")

    def play_sound_effect(self, file_path: str):
        """Play a sound effect."""
        try:
            sound = pygame.mixer.Sound(file_path)
            sound.play()
        except Exception as e:
            print(f"Error playing sound effect: {e}")

    def set_volume(self, volume: float):
        """Set the volume for music."""
        if 0.0 <= volume <= 1.0:
            pygame.mixer.music.set_volume(volume)
        else:
            print("Error: Volume must be between 0.0 and 1.0.")

    def increase_volume(self, increment=0.1):
        """Increase the music volume by a specified increment."""
        current_volume = pygame.mixer.music.get_volume()
        new_volume = min(1.0, current_volume + increment)
        pygame.mixer.music.set_volume(new_volume)

    def decrease_volume(self, decrement=0.1):
        """Decrease the music volume by a specified decrement."""
        current_volume = pygame.mixer.music.get_volume()
        new_volume = max(0.0, current_volume - decrement)
        pygame.mixer.music.set_volume(new_volume)
