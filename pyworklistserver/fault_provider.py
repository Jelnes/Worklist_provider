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
        if self._config_values.oversized_strings_enabled:
            if (r < self._config_values.likelihood_of_long_string):
                return random.randrange(max_len+1, max_len+10)
        if self._config_values.empty_strings_enabled:
            if (r > self._config_values.likelihood_of_long_string and r < (self._config_values.likelihood_of_long_string + self._config_values.likelihood_of_empty_string)):
                return 0
        return max_len

    def _return_None_string(self):
        if (self._config_values.none_strings_enabled ):
            r = random.uniform(0.0, 100.0)
            if (r <= self._config_values.likelihood_of_None_string):
                return 1
        return 0

    def _sleep_random(self):
        """Possibility of delaying the runtime"""
        if self._config_values.delay_enabled:
            r = random.uniform(0.0, 100.0)
            if (r <= self._config_values.likelihood_of_delay):
                time.sleep(self._config_values.delay_time)
        return 0



