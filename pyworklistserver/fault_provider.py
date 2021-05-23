""" Class for generation of faulty input """

import random
import time

class FaultProvider:
    """ Gives faulty input to exam-objects """
    def __init__(self, worklist_values):
        self._worklist_values = worklist_values

        available_languages = {
            "chineseEnabled": '也池馳弛水马弓土人女',               # An excempt of chinese characters
            "russianEnabled": 'ДРЛИПЦЗГБЖ',                       # An excempt of russian characters
            "greekEnabled": 'ΑαΒβΓγΔδΕεΖζΗηΘθΙιψΩω',            # An excempt of Greek characters
            "japaneseEnabled": '日一大二目五後.女かたまやたば',       # An excempt of Japanese characters (Kanji, Hiragana and Katakana)
            "koreanEnabled": 'ㄱㄴㄷㄹㅇㅈㅑㅓㅕㅗㅛㅔㅖㅚㅿㆆㆍ'   # An excempt of Korean characters (Hangul)
        }

        self.allowedlanguages = [
            'æÆøØåÅßäöüÄÖÜ'                    # just an arbitrarily selected list of non ascii characters
        ]

        for key in available_languages.keys():
            if self._worklist_values[key]:
                self.allowedlanguages.append(available_languages[key])



    def _get_random_string_length(self, max_len):
        """ Return an int with size, either equal to maximum string length (based on DICOM tag), or greater."""
        r = random.uniform(0.0, 100.0)
        if self._worklist_values["oversizedStringsEnabled"]:
            if (r < self._worklist_values["likelihoodOfLongString"]):
                return random.randrange(max_len+1, max_len+10)
        if self._worklist_values["emptyStringsEnabled"]:
            if (r > self._worklist_values["likelihoodOfLongString"] and r < (self._worklist_values["likelihoodOfLongString"] + self._worklist_values["likelihoodOfEmptyString"])):
                return 0
        return max_len

    def _return_None_string(self):
        if (self._worklist_values["noneStringsEnabled"]):
            r = random.uniform(0.0, 100.0)
            if (r <= self._worklist_values["likelihoodOfNoneString"]):
                return True
        return False

    def _sleep_random(self):
        """Possibility of delaying the runtime"""
        if self._worklist_values["delayEnabled"]:
            r = random.uniform(0.0, 100.0)
            if (r <= self._worklist_values["likelihoodOfDelay"]):
                time.sleep(self._worklist_values["delayTime"])
        return 0

    def _get_random_language_string(self):
        r = random.uniform(0.0, 100.0)
        if (r <= self._worklist_values["likelihoodOfLanguage"]):
            return self.allowedlanguages[random.randint(0, (len(self.allowedlanguages) - 1))]
        else:
            return self.allowedlanguages[0]

