import configparser

class Settings:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('settings.cfg')

    def get_setting(self, section, setting):
            value = self.config.get(section, setting)
            if value is None:
                return None
            return value