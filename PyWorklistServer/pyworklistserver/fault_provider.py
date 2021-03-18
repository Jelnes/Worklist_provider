""" Class for generation of faulty input """

import random


class FaultProvider:
    """ Gives faulty input to exam-objects """
    def __init__(self):
        self.isLong = 0
        self.likelyhood_of_long_string = 1


    def _get_random_length(self, max_len):
        """ Return an int with size, either equal to defaultmax, or greater."""
        if self.isLong == 0:
            return max_len

        r = random.randrange(1, 100)
        if (r < self.likelyhood_of_long_string):
            length = random.randrange(max_len+1, max_len+10)
        else:
            length = max_len
        return length
