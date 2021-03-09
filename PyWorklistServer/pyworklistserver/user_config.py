""" Sets variables for use of the worklist-generators"""
import random

#Maximall number of total patient-objects delivered from generator.
maxAmountOfPatientObjects = 500     

#Rate of clean patient-objects (in percentage) delivered from generator.
rateOfCleanObjects = 20

#Generator seed value, if command line argument not set. Set to 0 for seed to be set to a random number.
seed_Number = 0











"""Return Function for seed-value"""
def get_seedNumber():
    if seed_Number == 0:
        return random.randrange(1, 1000000)
    
    return seed_Number


        
        
    



