import sys
import logging
from enum import IntEnum
from loguru import logger

from utils import states


class LogLevel(IntEnum):
    TRACE = 5
    DEBUG = 10
    INFO = 20
    SUCCESS = 25
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists.
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def set_log_to_console(log_level: str = "INFO") -> None:
    try:
        logger.remove()
        logger.add(sys.stderr, level=LogLevel[log_level])
    except KeyError:
        logger.add(sys.stderr, level="DEBUG")
        logger.critical("Wrong logger level!")
        exit()


def set_log_to_files(log_level: str = "INFO") -> None:
    logger.add(
        states.config.log_dir / "info.log",
        filter=lambda record: LogLevel[log_level]
        <= record["level"].no
        <= LogLevel.SUCCESS,
    )
    logger.add(
        states.config.log_dir / "warning.log",
        filter=lambda record: record["level"].no == LogLevel.WARNING,
    )
    logger.add(
        states.config.log_dir / "error.log",
        filter=lambda record: record["level"].no >= LogLevel.ERROR,
    )
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    logger.debug("Loaded logger's settings")
