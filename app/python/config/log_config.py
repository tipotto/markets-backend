import logging
from constants.util import LOGGER_NAME, DEV_PYTHON_LOG_DIR_PATH, PROD_PYTHON_LOG_DIR_PATH


def get_logger(file_path):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(file_path)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(levelname)-9s %(asctime)s [%(name)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def log_error(data):
    get_logger(PROD_PYTHON_LOG_DIR_PATH + '/error.log').error(data)


def log_info(data):
    get_logger(PROD_PYTHON_LOG_DIR_PATH + '/http.log').info(data)
