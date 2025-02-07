import logging
import logging.config
from pathlib import Path

# Log fayllar uchun katalogni yaratamiz
log_dir = Path("./logs")
log_dir.mkdir(exist_ok=True)

# Log konfiguratsiyasi
LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "DEBUG",
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "standard",
            "filename": log_dir / "app.log",
            "level": "INFO",
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "DEBUG",
    },
}

def setup_logging():
    logging.config.dictConfig(LOG_CONFIG)
