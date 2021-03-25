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

#how often long string will appear in percent. in an exam, per line
likelyhood_of_long_string = 2.0

#Likelyhood of returning empty string, per line in exam, percentage
likelyhood_of_empty_string = 1.0

#Likelyhood of returning None instead of string. In percentage
likelyhood_of_None_string = 1.0

#likelyhood of a delay per exam. in percent
likelyhood_of_delay = 2.0

#Enablers / Disablers of the fault_provider:
is_long = 1

is_empty = 1

is_None = 1

is_delay = 1
