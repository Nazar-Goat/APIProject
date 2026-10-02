import logging
import sys

from loguru import logger

from src.config import settings


class InterceptHandler(logging.Handler):
    """
    Logging handler that intercepts standard logging messages
    and redirects them to loguru.
    """
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging():
    logger.remove()

    dev_format = (
        "<green>{time:HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
    )

    if settings.ENVIRONMENT == "DEV":
        logger.add(
            sys.stdout,
            level="DEBUG",
            format=dev_format,
            colorize=True,
        )

    elif settings.ENVIRONMENT == "PROD":
        logger.add(
            sys.stdout,
            level="INFO",
            serialize=True,
            colorize=False,
        )

    else:
        logger.add(sys.stdout, level="DEBUG", format=dev_format, colorize=True)
        logger.warning(f"Unknown ENVIRONMENT='{settings.ENVIRONMENT}', falling back to DEV config")

    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    for name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        uvicorn_logger = logging.getLogger(name)
        uvicorn_logger.handlers = [InterceptHandler()]
        uvicorn_logger.propagate = False