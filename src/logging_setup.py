import os
from pathlib import Path
import sys

from loguru import logger


def setup_logging() -> None:
    env = os.getenv("APP_ENV", "dev")  # dev или prod
    level = os.getenv("LOG_LEVEL", "INFO")

    logger.remove()  # убираем дефолтный sink

    BASE_DIR = Path(__file__).resolve().parent.parent
    LOG_DIR = BASE_DIR / "logs"
    LOG_DIR.mkdir(exist_ok=True)

    if env == "prod":
        logger.add(sys.stdout, level=level, serialize=True, enqueue=True)
    else:
        fmt = "<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <cyan>{message}</cyan>"
        logger.add(sys.stdout, level=level, format=fmt)

    logger.add(
        LOG_DIR / "app.log",
        level=level,
        rotation="1 MB",
        retention="7 days",
        compression="zip",
        enqueue=True,
        serialize=(env == "prod"),
    )
