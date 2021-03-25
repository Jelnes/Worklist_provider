""" Class for generation of faulty input """

import random
import time
from pyworklistserver import user_config


class FaultProvider:
    """ Gives faulty input to exam-objects """
    def __init__(self):
        self.long_enabled = user_config.long_enabled
        self.empty_enabled = user_config.empty_enabled
        self.delay_enabled = user_config.delay_enabled
        self.None_enabled = user_config.None_enabled
        self.likelyhood_of_long_string = user_config.likelyhood_of_long_string
        self.likelyhood_of_empty_string = user_config.likelyhood_of_empty_string
        self.likelyhood_of_None_string = user_config.likelyhood_of_None_string
        self.likelyhood_of_delay = user_config.likelyhood_of_delay
        self.delay_time = 5

    def _get_random_length(self, max_len):
        """ Return an int with size, either equal to defaultmax, or greater."""
        r = random.uniform(0.0, 100.0)
        long = self.likelyhood_of_long_string
        if self.long_enabled == 1:
            if (r <= long):
                return random.randrange(max_len+1, max_len+10)
        if self.empty_enabled == 1:
            if (r > long and r <= (long + self.likelyhood_of_empty_string)):
                return 0
        return max_len

    def _return_None_string(self):
        if (self.None_enabled == 1):
            r = random.uniform(0.0, 100.0)
            if (r <= self.likelyhood_of_None_string):
                return 1
        return 0

    def _delay(self):
        """Possibility of delaying the runtime"""
        if self.delay_enabled == 0:
            return 0
        r = random.uniform(0.0, 100.0)
        if (r <= self.likelyhood_of_delay):
            time.sleep(self.delay_time)
        return 0
