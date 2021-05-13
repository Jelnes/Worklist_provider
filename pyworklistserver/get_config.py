from pyworklistserver import user_config


class ConfigProvider:
    """ Class that gets and sets values in user_config for current run """
    def __init__(self):
        self.defaultConfig = user_config.default_config.copy()

    def reset(self):
        self.defaultConfig = user_config.default_config.copy()

