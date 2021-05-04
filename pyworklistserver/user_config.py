""" Sets variables for use of the worklist-generators"""
import random

#Maximall number of total patient-objects delivered from generator.
maxAmountOfWorklistExams = 70

#Minimum number of total patient-objects delivered from generator.
minAmountOfWorklistExams = 20

#Rate of clean patient-objects delivered from generator.
rateOfCleanExams = 2

#Rate of random patient-objects delivered from generator.
rateOfRandomExams = 5

#Generator seed value, if command line argument not set. Set to 0 for seed to be set to a random number.
seed_Number = 0

#likelihood of returning long string, per line in exam, percentage
likelihood_of_long_string = 2.0

#likelihood of returning empty string, per line in exam, percentage
likelihood_of_empty_string = 1.0

#likelihood of returning None instead of string. In percentage
likelihood_of_None_string = 1.0

#likelihood of a delay per exam. in percent
likelihood_of_delay = 2.0

#likelihood of using one of the unsupported languages, per line in exam, in percentage
likelihood_of_language = 0

#Enablers / Disablers of the fault_provider:
long_enabled = 1

empty_enabled = 1

none_enabled = 1

delay_enabled = 1

chinese_enabled = 1

russian_enabled = 1

greek_enabled = 1

japanese_enabled = 1

korean_enabled = 1
