import logging
class CustomLogger:
    def __init__(self, logger_name, level=logging.ERROR):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(level)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def get_logger(self):
        return self.logger