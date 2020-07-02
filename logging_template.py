import logging


def enable_logging(loglevel):
    log_format = "\033[96m%(asctime)s \033[95m[%(levelname)s] [%(name)s] \033[93m%(message)s\033[0m"
    logging.basicConfig(format=log_format, level=loglevel)
    logging.debug("!!! Logging Setup Complete !!!")


enable_logging(logging.DEBUG)
