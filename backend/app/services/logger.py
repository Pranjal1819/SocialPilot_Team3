import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("socialpilot")

logger.setLevel(logging.INFO)


handler = RotatingFileHandler(
    "socialpilot.log", maxBytes=5 * 1024 * 1024, backupCount=3
)

formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

handler.setFormatter(formatter)

logger.addHandler(handler)
