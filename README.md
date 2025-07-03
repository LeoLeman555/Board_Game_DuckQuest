# Duck Quest - Board Game

![Logo](./duckquest/assets/images/logo.png)

*"Embark on a journey to teach children algorithmic thinking through a fun and interactive board game!"*

DuckQuest is an educational game created within a school project. It is aimed at young children and allows them to learn to think like an algorithm in order to understand how these work. We achieve this by asking them to find the shortest route through a graph, just as a Dijkstra algorithm would.

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
- [Installation](#installation)
- [Run](#run)
- [Tests](#tests)
- [License](#license)
- [Contact](#contact)

## Overview

### Game Concept
In DuckQuest, the graph is represented as a network of routes around a pond. Children guide a duck along the shortest path using physical buttons for graph nodes and LED strips for graph edges. A Raspberry Pi powers and controls the setup. 

### Example Visualization
Below is a sample graph with nodes and edges:

![Sample graph](./duckquest/assets/images/sample_graph.png)

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
- Addressable RGB strips for edges (like WS2812)
- 5V Power Supply for powering the LED strip
- Jumper wires

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
> Additionally, the `rpi_ws281x` module, which is used to control the WS281x LED strips, is also Raspberry Pi-specific. Just like `RPi.GPIO`, it doesn't function on other platforms.
>  
> The `install.py` script ensures that both `RPi.GPIO` and `rpi_ws281x` are installed only if the script detects a Raspberry Pi. This makes the installation process more flexible and prevents errors on unsupported platforms.

6. You are fine !

## Run
To launch the game, use the following command:
```bash
sudo -E $(which python) -m src.main
```

## Tests

Detailed test instructions are available in [docs/tests.md](docs/tests.md).


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any questions or feedback, feel free to contact me:
- **Léo Leman** : [My GitHub Profile](https://github.com/LeoLeman555)