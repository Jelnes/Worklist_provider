from pyworklistserver import default_config


class ConfigProvider:
    """ Class that gets and sets values in default_config for current run """
    def __init__(self, worklist_config):
        self._worklist_config = worklist_config
        self.defaultConfig = default_config.default_config.copy()
        self.defaultConfig.update(self._worklist_config)


    def reset(self):
        self.defaultConfig = default_config.default_config.copy()
        self.defaultConfig.update(self._worklist_config)
