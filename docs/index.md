# DuckQuest — Technical Documentation

DuckQuest is an educational board game powered by Python and Raspberry Pi.
It teaches children algorithmic thinking by interacting with a physical graph interface.

This documentation is intended for contributors and maintainers.

## Project Goals

- Teach the concept of shortest paths using real-world physical interaction
- Combine software (graph logic, UI) with hardware (LEDs, buttons, Raspberry Pi)
- Provide a cross-platform application: mock mode on desktop, hardware mode on Pi

## Codebase Overview

```plaintext
duckquest/
├── graph/         # Graph logic, UI components, and Matplotlib rendering
├── hardware/      # GPIO control for buttons and LED strips (with mocks)
├── audio/         # Background music and sound effects manager
├── utils/         # Helper functions and centralized logging system
├── main.py        # Main entry point to launch the game
docs/              # Technical documentation
logs/              # Generated logs (console + file logging system)
scripts/           # Manual testing tools for hardware (GPIO, LEDs)
tests/             # Unit and manual tests using Pytest
```

## Where to Start

- Start with [`architecture.md`](architecture.md) for a modular overview
- Use [`logging.md`](logging.md) to understand how logs are structured
- See [`tests.md`](tests.md) for test instructions and hardware test notes