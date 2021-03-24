""" Sets variables for use of the worklist-generators"""
import random

#Maximall number of total patient-objects delivered from generator.
maxAmountOfWorklistExams = 70

#Minimum number of total patient-objects delivered from generator.
minAmountOfWorklistExams = 20

#Rate of clean patient-objects (in percentage) delivered from generator.
rateOfCleanExams = 2

#Rate of random patient-objects (in percentage) delivered from generator.
rateOfRandomExams = 5

#Generator seed value, if command line argument not set. Set to 0 for seed to be set to a random number.
seed_Number = 0

#how often long string will appear in percent. in an exam, per line
likelyhood_of_long_string = 2

#likelyhood of a delay per exam. in percent
likelyhood_of_delay = 0.2
