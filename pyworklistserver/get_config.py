from pyworklistserver import user_config


class ConfigProvider:
    """ Class that gets and sets values in user_config for current run """
    def __init__(self):
        self.maxAmountOfWorklistExams = user_config.maxAmountOfWorklistExams
        self.minAmountOfWorklistExams = user_config.minAmountOfWorklistExams
        self.rateOfCleanExams = user_config.rateOfCleanExams
        self.rateOfRandomExams = user_config.rateOfRandomExams
        self.seed_Number = user_config.seed_Number
        self.likelihood_of_long_string = user_config.likelihood_of_long_string
        self.likelihood_of_empty_string = user_config.likelihood_of_empty_string
        self.likelihood_of_None_string = user_config.likelihood_of_None_string
        self.likelihood_of_language = user_config.likelihood_of_language
        self.likelihood_of_delay = user_config.likelihood_of_delay
        self.delay_time = user_config.delay_time

        self.oversized_strings_enabled = user_config.oversized_strings_enabled
        self.empty_strings_enabled = user_config.empty_strings_enabled
        self.none_strings_enabled  = user_config.none_strings_enabled
        self.delay_enabled = user_config.delay_enabled

    def reset(self):
        self.maxAmountOfWorklistExams = user_config.maxAmountOfWorklistExams
        self.minAmountOfWorklistExams = user_config.minAmountOfWorklistExams
        self.rateOfCleanExams = user_config.rateOfCleanExams
        self.rateOfRandomExams = user_config.rateOfRandomExams
        self.seed_Number = user_config.seed_Number
        self.likelihood_of_long_string = user_config.likelihood_of_long_string
        self.likelihood_of_empty_string = user_config.likelihood_of_empty_string
        self.likelihood_of_None_string = user_config.likelihood_of_None_string
        self.likelihood_of_delay = user_config.likelihood_of_delay
        self.likelihood_of_language = user_config.likelihood_of_language

        self.oversized_strings_enabled = user_config.oversized_strings_enabled
        self.empty_strings_enabled = user_config.empty_strings_enabled
        self.none_strings_enabled  = user_config.none_strings_enabled
        self.delay_enabled = user_config.delay_enabled
