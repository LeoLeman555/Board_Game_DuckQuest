# Architecture Overview

This project is modular and cleanly separated into responsibilities:

## Core Modules

- **`GameManager`**  
  Main controller of the application. Connects logic, UI, audio, and hardware.

- **`graph/`**
  - `logic.py`: manages the user's selected path and path validation
  - `manager.py`: graph data structure and edge weights
  - `renderer.py`: matplotlib visualization
  - `ui.py`: Tkinter interface for user interaction

- **`hardware/`**
  - `button_manager.py`: handles physical GPIO button inputs
  - `led_strip_manager.py`: drives WS2812 LED strip
  - `mock.py`: software-only fallback for non-Raspberry Pi systems

- **`audio/manager.py`**
  Plays background music and sound effects

## Modes of Operation

- **Mock mode** (Windows, Linux, macOS) — no GPIO or hardware required
- **Raspberry Pi mode** — uses actual GPIO pins for buttons and LEDs

## Execution Flow

1. `main.py` starts the app
2. `GameManager` initializes graph, UI, logic, and hardware
3. User interacts with nodes via buttons or UI
4. LEDs respond in real time
5. The game evaluates the path against Dijkstra's shortest path
