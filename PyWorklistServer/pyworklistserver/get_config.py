from pyworklistserver import user_config


class GetConfig:
    """ Class that gets and sets values in user_config for current run """
    def __init__(self):
        self.maxAmountOfWorklistExams = user_config.maxAmountOfWorklistExams
        self.minAmountOfWorklistExams = user_config.minAmountOfWorklistExams
        self.rateOfCleanExams = user_config.rateOfCleanExams
        self.rateOfRandomExams = user_config.rateOfRandomExams
        self.seed_Number = user_config.seed_Number
        self.likelyhood_of_long_string = user_config.likelyhood_of_long_string
        self.likelyhood_of_empty_string = user_config.likelyhood_of_empty_string
        self.likelyhood_of_None_string = user_config.likelyhood_of_None_string
        self.likelyhood_of_delay = user_config.likelyhood_of_delay

    def reset(self):
        self.maxAmountOfWorklistExams = user_config.maxAmountOfWorklistExams
        self.minAmountOfWorklistExams = user_config.minAmountOfWorklistExams
        self.rateOfCleanExams = user_config.rateOfCleanExams
        self.rateOfRandomExams = user_config.rateOfRandomExams
        self.seed_Number = user_config.seed_Number
        self.likelyhood_of_long_string = user_config.likelyhood_of_long_string
        self.likelyhood_of_empty_string = user_config.likelyhood_of_empty_string
        self.likelyhood_of_None_string = user_config.likelyhood_of_None_string
        self.likelyhood_of_delay = user_config.likelyhood_of_delay
