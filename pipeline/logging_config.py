from logging.config import dictConfig


def setup_logging(level: str = "INFO"):
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                },
            },
            "root": {
                "level": level.upper(),
                "handlers": ["console"],
            },
            "loggers": {
                "pikepdf": {
                    "level": "WARNING",  # suppress INFO unless explicitly asked
                    "handlers": ["console"],
                    "propagate": False,
                }
            },
        }
    )
