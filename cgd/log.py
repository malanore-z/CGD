import logging.config
from logging import Filter

import zcommons as zc


class ColorFilter(Filter):

    colors = {
        logging.DEBUG: zc.FORE_CYAN,
        logging.INFO: zc.FORE_GREEN,
        logging.WARNING: zc.FORE_YELLOW,
        logging.ERROR: zc.FORE_RED,
        logging.CRITICAL: zc.FORE_MAGENTA
    }

    def __init__(self):
        super(ColorFilter, self).__init__()

    def filter(self, record) -> bool:
        color = self.colors.get(record.levelno, None)
        if color:
            record.levelname = f"{color}{record.levelname}{' ' * (8 - len(record.levelname))}{zc.FORE_RESET}"
        return True


config = {
    "version": 1,
    "formatters": {
        "common": {
            "format": f"%(asctime)s %(name)20s [%(levelname)-8s] %(message)s"
        }
    },
    "filters": {
        "color": {
            "()": ColorFilter
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "common",
            "stream": "ext://sys.stdout"
        },
        "cgd": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "common",
            "filters": [
                "color"
            ],
            "stream": "ext://sys.stdout"
        },
    },
    "loggers": {
        "cgd": {
            "level": "INFO",
            "handlers": [
                "cgd"
            ],
            "propagate": False
        }
    }
}

logging.config.dictConfig(config)


def set_level(level):
    logger = logging.getLogger("cgd")
    logger.setLevel(level)
