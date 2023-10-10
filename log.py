import logging
from colorlog import ColoredFormatter

logging.addLevelName(logging.WARNING, "WARN")


def setup_logger(name: str):
    formatter = ColoredFormatter(
        "[%(name)s] %(asctime)s.%(msecs)03d %(log_color)s%(levelname)-5s%(reset)s %(white)s%(message)s",
        log_colors={
            "DEBUG": "blue",
            "INFO": "green",
            "WARN": "yellow",
            "ERROR": "red",
        },
        datefmt="%H:%M:%S",
    )
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger
