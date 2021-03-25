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

#Likelyhood of returning long string, per line in exam, percentage
likelyhood_of_long_string = 2.0

#Likelyhood of returning empty string, per line in exam, percentage
likelyhood_of_empty_string = 1.0

#Likelyhood of returning None instead of string. In percentage
likelyhood_of_None_string = 1.0

#likelyhood of a delay per exam. in percent
likelyhood_of_delay = 2.0

#Enablers / Disablers of the fault_provider:
long_enabled = 1

empty_enabled = 1

None_enabled = 1

delay_enabled = 1
