import sys
from loguru import logger
from pathlib import Path

from system import log
from utils import settings, states

LOG_LEVEL = "INFO"


if __name__ == "__main__":
    log.set_log_to_console(LOG_LEVEL)
    states.config = settings.get_config(
        Path(__file__).parent / "settings.json",
    )
    print(states.config)
    log.set_log_to_files(LOG_LEVEL)
