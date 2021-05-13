""" Class for generation of faulty input """

import random
import time
from pyworklistserver import user_config

class FaultProvider:
    """ Gives faulty input to exam-objects """
    def __init__(self, config_values):
        self._config_values = config_values

    def _get_random_string_length(self, max_len):
        """ Return an int with size, either equal to maximum string length (based on DICOM tag), or greater."""
        r = random.uniform(0.0, 100.0)
        if self._config_values["oversizedStringsEnabled"]:
            if (r < self._config_values["likelihoodOfLongString"]):
                return random.randrange(max_len+1, max_len+10)
        if self._config_values["emptyStringsEnabled"]:
            if (r > self._config_values["likelihoodOfLongString"] and r < (self._config_values["likelihoodOfLongString"] + self._config_values["likelihoodOfEmptyString"])):
                return 0
        return max_len

    def _return_None_string(self):
        if (self._config_values["noneStringsEnabled"]):
            r = random.uniform(0.0, 100.0)
            if (r <= self._config_values["likelihoodOfNoneString"]):
                return True
        return False

    def _sleep_random(self):
        """Possibility of delaying the runtime"""
        if self._config_values["delayEnabled"]:
            r = random.uniform(0.0, 100.0)
            if (r <= self._config_values["likelihoodOfDelay"]):
                time.sleep(self._config_values["delayTime"])
        return 0
