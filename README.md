# Duck Quest - Board Game

![Logo](./assets/images/logo.png)

*"Embark on a journey to teach children algorithmic thinking through a fun and interactive board game!"*

DuckQuest is an educational game created within a school project. It is aimed at young children and allows them to learn to think like an algorithm in order to understand how these work. We achieve this by asking them to find the shortest route through a graph, just as a Dijkstra algorithm would.

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
- [Installation](#installation)
- [Usage](#usage)
- [Tests](#tests)
- [License](#license)
- [Contact](#contact)

## Overview

### Game Concept
In DuckQuest, the graph is represented as a network of routes around a pond. Children guide a duck along the shortest path using physical buttons for graph nodes and LED strips for graph edges. A Raspberry Pi powers and controls the setup. 

### Example Visualization
Below is a sample graph with nodes and edges:

![Sample graph](./assets/images/sample_graph.png)

## Setup

### Graph Edge Colors
The LED strips light up in different colors to represent edge weights:

| Weight         | Color         |
|----------------|---------------|
| 1              | Green         |
| 2              | Bright-Green  |
| 3              | Yellow        |
| 4              | Orange        |
| 5              | Red           |
| Selected Path  | Cyan          |

### Hardware Requirements
To build the DuckQuest board game, you need the following components:

- Complete Raspberry Pi kit
- Push buttons for nodes
- Jumper wires

*Not yet implemented :*\
*- Addressable RGB strips (like WS2812).*\
*- Breadboard.*

## Installation

### Prerequisites

>⚠️ **Warning:** This project is designed for Raspberry Pi. If you run on another Linux system, some features (like GPIO) may not work.

Ensure you have the following software installed on your raspberry:

- [Python 3.6+](https://www.python.org/)
- [Git](https://git-scm.com/)
- An active graphical interface (like X11) – **required for running the game UI**

### Steps for Installation

1. Clone the repository on your Raspberry Pi:
   ```bash
   git clone https://github.com/LeoLeman555/Board_Game_DuckQuest.git
   ```

2. Navigate to the project directory:
   ```bash
   cd ./Board_Game_DuckQuest/
   ```

3. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:
   - **Linux**:
   ```bash
   source venv/bin/activate
   ```
   - **Windows**:
   ```powershell
   venv\Scripts\activate
   ```

5. Installing dependencies with a Python script:
   ```bash
   python install.py
   ```

> **Why use `install.py` instead of `requirements.txt`?**  
> The `RPi.GPIO` module is specifically designed for Raspberry Pi and does not work on Windows or non-Raspberry Pi Linux systems.  
> If included directly in `requirements.txt`, installation would fail on unsupported platforms.  
>  
> The `install.py` script ensures that `RPi.GPIO` is installed only if the script detects a Raspberry Pi.   

6. You are fine !

## Tests
### Computer Game Modeling
1. Start the test suite:
   ```bash
   python ./tests/launch_game.py
   ```
2. Interact with the GUI:
   - Press nodes to select the path.
   - Validate your selection to see if it matches the shortest path.
3. Example:

![Duck Quest Graph](./assets/images/game_interface.png)

### Raspberry Pi Readiness Checker
Use this script to verify if the Raspberry Pi setup is functional:
   ```bash
   python ./tests/raspberry_pi_checker.py
   ```

- **Features**:
  - Tests internet connectivity.
  - Displays essential system details (CPU, memory, disk usage).

### Button Checker

The Button Checker script tests the functionality of a button connected to the Raspberry Pi GPIO pins. It logs each button press, release, and calculates the duration of presses.

#### How to Use

1. Connect the button to the Raspberry Pi GPIO pin configured in the script (default is GPIO **17**).
2. Run the script:
   ```bash
   python ./button_checker.py
   ```
   The script will:
   - Detect button presses and releases.
   - Log events in a file named `button_test.txt` inside the `logs` directory.
3. Press the button

#### Example Output

During execution, you will see output like this in the terminal:

```plaintext
GPIO port used: 17
Configuration: Button set with internal pull-up.
Events will be logged in the file: logs/button_test.txt
Press the button to start.
Button pressed!
Button released! Duration: 0.324 seconds
Total presses: 1
```

#### Logs

- A `logs` directory is automatically created (if it doesn't exist).
- Button press events are logged in `logs/button_test.txt`. Example log entry:
  ```plaintext
  2025-01-01 00:00:00 - Button pressed and released. Duration: 0.050 s. Count: 1
  ```

#### Stopping the Test

- Use `CTRL + C` to stop the test. Final statistics (total duration and total presses) will be displayed in the terminal and written to the log file.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any questions or feedback, feel free to contact me:
- **Léo Leman** : [My GitHub Profile](https://github.com/LeoLeman555)