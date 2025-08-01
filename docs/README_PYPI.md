# Duck Quest

[![PyPI](https://img.shields.io/pypi/v/duckquest)](https://pypi.org/project/duckquest/)
[![License](https://img.shields.io/github/license/LeoLeman555/Board_Game_DuckQuest)](LICENSE)
[![Status](https://img.shields.io/badge/status-prototype--stable-brightgreen)]()
![Code style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)

Duck Quest is an educational board game designed to teach children algorithmic thinking. Kids help a duck find the shortest path through a graph—mimicking how Dijkstra's algorithm works—via real buttons and LED strips powered by a Raspberry Pi.

## Prerequisites

>⚠️ **Warning:** This project is designed for Raspberry Pi. If you run on another Linux system, some features (like GPIO) may not work.

- [Python 3.11+](https://www.python.org/)

## Features

- Graph-based Gameplay:
    - Kids interact with a real graph made of buttons (nodes) and LED strips (edges).
    - Shortest path challenges using real-world logic and physical interaction.
- Visual Feedback:
    - LED strip colors represent edge weights.
    - Cyan highlights the selected path.
- Modular Architecture:
    - Includes hardware checkers for buttons and LEDs.
    - Rasbberry Pi compatibility checks.
    - Full test suite for simulating the game logic.
- Educational Focus:
    - Develops algorithmic thinking at an early age.
    - Interactive STEM learning.

## Installation

1. To install Duck Quest, simply run:
   ```bash
   pip install duckquest
   ```
2. Once installed, launch the game with:
   ```bash
   duck-quest
   ```

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/LeoLeman555/Board_Game_DuckQuest/blob/main/LICENSE) file for more details.

## Source Code

The source code is available [here](https://github.com/LeoLeman555/Board_Game_DuckQuest/).

## Credits
   - Code: [Léo Leman](https://github.com/LeoLeman555)

## Contact

For any questions or feedback, feel free to contact me:

- GitHub: [LeoLeman555](https://github.com/LeoLeman555)
- Email: leo.leman555@gmail.com
