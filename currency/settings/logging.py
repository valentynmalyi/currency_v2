import os

from currency.settings.django import BASE_DIR

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "asctime": {
            "format": "%(levelname)s::%(asctime)s\n%(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "history": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs", "history.log"),
            "formatter": "asctime",
        },
        "worker_order": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs", "worker_order.log"),
            "formatter": "asctime",
        },
        "worker_result": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs", "worker_result.log"),
            "formatter": "asctime",
        },
        "worker_first_open": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs", "worker_first_open.log"),
            "formatter": "asctime",
        },
        "worker_first_close": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs", "worker_first_close.log"),
            "formatter": "asctime",
        }
    },
    "loggers": {
        "history": {
            "handlers": ["history"],
            "level": "DEBUG",
            "propagate": True,
        },
        "worker_order": {
            "handlers": ["worker_order"],
            "level": "DEBUG",
            "propagate": True,
        },
        "worker_result": {
            "handlers": ["worker_result"],
            "level": "DEBUG",
            "propagate": True,
        },
        "worker_first_open": {
            "handlers": ["worker_first_open"],
            "level": "DEBUG",
            "propagate": True,
        },
        "worker_first_close": {
            "handlers": ["worker_first_close"],
            "level": "DEBUG",
            "propagate": True,
        }
    }
}
