""" Class for generation of faulty input """

import random
import time
from pyworklistserver import user_config


class FaultProvider:
    """ Gives faulty input to exam-objects """
    def __init__(self, config_values):
        self._config_values = config_values

        self.delay_time = 5

    def _get_random_length(self, max_len):
        """ Return an int with size, either equal to maximum string length (based on DICOM tag), or greater."""
        r = random.uniform(0.0, 100.0)
        if self._config_values.long_enabled:
            if (r < self._config_values.likelihood_of_long_string):
                return random.randrange(max_len+1, max_len+10)
        if self._config_values.empty_enabled:
            if (r > self._config_values.likelihood_of_long_string and r < (self._config_values.likelihood_of_long_string + self._config_values.likelihood_of_empty_string)):
                return 0
        return max_len

    def _return_None_string(self):
        if (self._config_values.none_enabled):
            r = random.uniform(0.0, 100.0)
            if (r <= self._config_values.likelihood_of_None_string):
                return 1
        return 0

    def _sleep_random(self):
        """Possibility of delaying the runtime"""
        if self._config_values.delay_enabled:
            return 0
        r = random.uniform(0.0, 100.0)
        if (r <= self._config_values.likelihood_of_delay):
            time.sleep(self.delay_time)
        return 0
