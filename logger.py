import os
import logging


class Diagnostics:

    def __init__(self, name, directory):

        self.directory = directory
        self.name = name
        self.logger = self.setup_logger(name=self.name)
        # create log directory if none exists
        if not os.path.exists('log'):
            os.makedirs('log')

    def setup_logger(self, name, level=logging.INFO):

        handler = logging.FileHandler(self.directory)
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(message)s'))

        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)
        return logger


class NicknameLog(Diagnostics):

    def log_nicknames(self, *items):

        self.logger.info('nicknames captured: {} for {}'.format(items[0], items[1]))


class FilteredLog(Diagnostics):

    def log_final_filtered_list(self, items):

        self.logger.info('possible nicknames: {}'.format(items))
