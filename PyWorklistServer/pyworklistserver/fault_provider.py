""" Class for generation of faulty input """

import random
import time
from pyworklistserver import user_config


class FaultProvider:
    """ Gives faulty input to exam-objects """
    def __init__(self):
        self.is_long = 1
        self.is_empty = 1
        self.is_delay = 1
        self.likelyhood_of_long_string = user_config.likelyhood_of_long_string
        self.likelyhood_of_delay = user_config.likelyhood_of_delay
        self.delay_time = 5
        self.likelyhood_of_empty_string = user_config.likelyhood_of_empty_string
        self.likelyhood_of_None_string = user_config.likelyhood_of_None_string


    def _get_random_length(self, max_len):
        """ Return an int with size, either equal to defaultmax, or greater."""
        r = random.uniform(0.0, 100.0)
        long = self.likelyhood_of_long_string
        if self.is_long == 1:
            if (r <= long):
                return random.randrange(max_len+1, max_len+10)
        if self.is_empty == 1:
            if (r > long && r <= (long + self.likelyhood_of_empty_string)):
                return 0
        return max_len

    def _return_None_string(self):
        r = random.uniform(0.0, 100.0)
        if (r <= self.likelyhood_of_None_string):
            return 0
        return 1

    def _delay(self):
        """Possibility of delaying the runtime"""
        if self.is_delay == 0:
            return 0
        r = random.uniform(0.0, 100.0)
        if (r <= self.likelyhood_of_delay):
            time.sleep(self.delay_time)
        return 0
