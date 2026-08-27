# logger.py
import logging
import sys


def getLogger(name: str, level: int = logging.INFO) -> logging.Logger:
    # this is a very simple logger to substitute simple prints, i think it looks better, i always use one, very
    # useful for kubernetes and containers and also i find it looks cool
    logger = logging.getLogger(name)
    if logger.handlers:  # avoid duplicate handlers on re-import
        return logger

    logger.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    logger.addHandler(handler)
    return logger
