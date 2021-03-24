""" Class for generation of faulty input """

import random
import time
from pyworklistserver import user_config


class FaultProvider:
    """ Gives faulty input to exam-objects """
    def __init__(self):
        self.is_long = 1
        self.is_delay = 1
        self.likelyhood_of_long_string = user_config.likelyhood_of_long_string
        self.likelyhood_of_delay = user_config.likelyhood_of_delay
        self.delay_time = 5


    def _get_random_length(self, max_len):
        """ Return an int with size, either equal to defaultmax, or greater."""
        if self.is_long == 0:
            return max_len

        r = random.uniform(0.0, 100.0)
        if (r <= self.likelyhood_of_long_string):
            length = random.randrange(max_len+1, max_len+10)
        else:
            length = max_len
        return length


    def _delay(self):
        """Possibility of delaying the runtime"""
        if self.is_delay == 0:
            return 0
        r = random.uniform(0.0, 100.0)
        if (r <= self.likelyhood_of_delay):
            time.sleep(self.delay_time)
        return 0
