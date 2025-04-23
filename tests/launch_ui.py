"""Entry point to manually launch the DuckQuest UI."""

from duckquest.game_manager import GameManager

def launch_ui():
    """Launch the DuckQuest user interface."""
    # Instantiate the game without Raspberry Pi hardware dependencies
    game = GameManager(is_rpi=False)

    # Start the main UI loop
    game.root.mainloop()

if __name__ == "__main__":
    launch_ui()
