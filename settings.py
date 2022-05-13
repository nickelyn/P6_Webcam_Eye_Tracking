import configparser
from definitions import *


class Settings:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(CONFIG_DIR)

    def get_setting(self, section, setting):
        value = self.config.get(section, setting)
        if value is None:
            return None
        return value
