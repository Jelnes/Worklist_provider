""" Class for generation of faulty input """

import random
import time
from pyworklistserver import user_config

__NONASCII = 'æÆøØåÅßäöüÄÖÜ' #just an arbitrarily selected list of non ascii characters

__CHINESE = '也池馳弛水马弓土人女' #An excempt of chinese characters

__RUSSIAN = 'ДРЛИПЦЗГБЖ'   #An excempt of russian characters

__GREEK = 'ΑαΒβΓγΔδΕεΖζΗηΘθΙιψΩω' #An excempt of Greek characters

__JAPANESE = '日一大二目五後.女かたまやたば' #An excempt of Japanese characters (Kanji, Hiragana and Katakana)

__KOREAN = 'ㄱㄴㄷㄹㅇㅈㅑㅓㅕㅗㅛㅔㅖㅚㅿㆆㆍ' #An excempt of Korean characters (Hangul)

class FaultProvider:
    """ Gives faulty input to exam-objects """
    def __init__(self, config_values):
        self._config_values = config_values

        self.delay_time = 5

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
            return 0
        r = random.uniform(0.0, 100.0)
        if (r <= self._config_values.likelihood_of_delay):
            time.sleep(self.delay_time)
        return 0

    def _get_random_language_string(self):
        r = random.uniform(0.0, 100.0)
        if (r <= self._config_values.likelihood_of_language):
            r = random.uniform(0.0, 100.0)
            if (r < 20) and (self._config_values.chinese_enabled):  # CHINESE
                return __CHINESE
            elif (20 <= r < 40) and (self._config_values.russian_enabled): # RUSSIAN
                return __RUSSIAN
            elif (40 <= r < 60) and (self._config_values.greek_enabled): # GREEK
                return __GREEK
            elif (60 <= r < 80) and (self._config_values.japanese_enabled): # JAPANESE
                return __JAPANESE
            elif (80 <= r) and (self._config_values.korean_enabled): # KOREAN
                return __KOREAN
        return __NONASCII
