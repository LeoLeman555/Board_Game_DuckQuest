# Logging System

DuckQuest uses a centralized and structured logging system to trace application behavior, hardware interaction, and test execution.

## Configuration

The logger is defined in `duckquest/utils/logger.py`.

It logs:
- To the console: level `INFO` and above
- To a rotating log file: `logs/duck_quest.log`, level `DEBUG` and above

### Format

```plaintext
YYYY-MM-DD HH:MM:SS | module | level | message
```

## Usage in Modules

To log from any module:

```python
from duckquest.utils.logger import setup_logger

logger = setup_logger(__name__)
logger.info("My message")
logger.warning("Something might be wrong")
logger.error("An error occurred")
```

## Log Levels Used

|       Level      |       Purpose                      |
|------------------|------------------------------------|
|       DEBUG      |Internal state, edge cases          |
|       INFO       |Normal operations and flow          |
|      WARNING     |Unexpected conditions (non-critical)|
|       ERROR      |Failures, recoverable               |
|      CRITICAL    |Irrecoverable failures (rare)       |