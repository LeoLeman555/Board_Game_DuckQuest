import platform
from duckquest.utils.helpers import is_raspberry_pi


def main():
    OS_NAME = platform.system()
    ON_RASPBERRY_PI = is_raspberry_pi()

    print(f"Starting game on {OS_NAME}")
    if ON_RASPBERRY_PI:
        print("Running on Raspberry Pi hardware.")
    else:
        print("Running in mock mode (Non-Raspberry Pi system).")

    from duckquest.game_manager import GameManager

    game = GameManager(ON_RASPBERRY_PI)
    game.root.mainloop()


if __name__ == "__main__":
    main()
