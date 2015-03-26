import os
import logging
import logging.handlers
from utils import mkdir


def initialize_logger(log_dir, app_name):
    mkdir(log_dir)
    logger = logging.getLogger()
    logger.setLevel(logging.NOTSET)  # NOTSET to log all levels messages

    details_formatter = logging.Formatter('%(asctime)s %(name)-12s: %(levelname)s %(message)s')
    simple_formatter = logging.Formatter("%(levelname)s: %(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)

    error_handler = logging.handlers.RotatingFileHandler(
        os.path.join(log_dir, app_name + "_error.log"),
        maxBytes=1024 * 1000,
        backupCount=10)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(details_formatter)
    logger.addHandler(error_handler)

    file_handler = logging.handlers.RotatingFileHandler(
        os.path.join(log_dir, app_name + ".log"),
        maxBytes=1024 * 1000,
        backupCount=10)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(details_formatter)
    logger.addHandler(file_handler)
