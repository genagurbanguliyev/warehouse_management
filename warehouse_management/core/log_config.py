from logging.config import dictConfig

from warehouse_management.core.config import configs

handlers = ["default", "rotating_file"]


# if settings.ENV_STATE == "prod":
#     handlers = ["default", "rotating_file", "logtail"]


def configure_logging() -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "correlation_id": {
                    "()": "asgi_correlation_id.CorrelationIdFilter",
                    "uuid_length": 8 if configs.ENV_STATE == "dev" else 32,
                    "default_value": "-",
                }
            },
            "formatters": {
                "console": {
                    "class": "logging.Formatter",
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                    "format": "(%(correlation_id)s) %(name)s:%(lineno)d - %(message)s",
                },
                "file": {
                    "class": "logging.Formatter",
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                    "format": "%(asctime)s.%(msecs)03dZ | %(levelname)-8s | [%(correlation_id)s] %(name)s:%(lineno)d - %(message)s",
                },
            },
            "handlers": {
                "default": {
                    "class": "rich.logging.RichHandler",
                    "level": "DEBUG",
                    "formatter": "console",
                    "filters": ["correlation_id"],
                },
                "rotating_file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": "DEBUG",
                    "formatter": "file",
                    "filters": ["correlation_id"],
                    "filename": "logs/app.log",
                    "maxBytes": 1024 * 1024 * 2,  # 2 MB
                    "backupCount": 3,
                    "encoding": "utf8",
                },
            },
            "loggers": {
                "uvicorn": {"handlers": ["default", "rotating_file"], "level": "INFO"},
                "gunicorn": {"handlers": ["default", "rotating_file"], "level": "INFO"},
                "app": {
                    "handlers": handlers,
                    "level": "DEBUG" if configs.ENV_STATE == "dev" else "INFO",
                    "propagate": False,
                },
                "databases": {"handlers": ["default"], "level": "WARNING"},
                "aiosqlite": {"handlers": ["default"], "level": "WARNING"},
            },
        }
    )
