from pyworklistserver import user_config


class ConfigProvider:
    """ Class that gets and sets values in user_config for current run """
    def __init__(self, inserted_config):
        self._inserted_config = inserted_config
        self.defaultConfig = user_config.default_config.copy()
        self.defaultConfig.update(self._inserted_config)


    def reset(self):
        self.defaultConfig = user_config.default_config.copy()
        self.defaultConfig.update(self._inserted_config)
