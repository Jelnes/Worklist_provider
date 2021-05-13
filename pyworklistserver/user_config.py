""" Sets variables for use of the worklist-generators"""

default_config = {
  "maxAmountOfWorklistExams":   70,         #Maximall number of total patient-objects delivered from generator.  
  "minAmountOfWorklistExams":   20,         #Minimum number of total patient-objects delivered from generator.
  "rateOfCleanExams":           0.5,        #Rate of clean patient-objects delivered from generator.
  "likelihoodOfLongString":     2.0,        #likelihood of returning long string, per line in exam, percentage 
  "likelihoodOfEmptyString":    1.0,        #likelihood of returning empty string, per line in exam, percentage
  "likelihoodOfNoneString":     1.0,        #likelihood of returning None instead of string. In percentage
  "likelihoodOfDelay":          2.0,        #likelihood of a delay per exam. in percent 
  "delayTime":                  5,          #Seconds of delay when delay is called 
  "likelihoodOfLanguage":       0,          #likelihood of using one of the unsupported languages, per line in exam, in percentage

  #Enablers / Disablers of the fault_provider:
  "oversizedStringsEnabled":    True,             
  "emptyStringsEnabled":        True,
  "noneStringsEnabled":         True,
  "delayEnabled":               True,
  "chineseEnabled":             True,
  "russianEnabled":             True,
  "greekEnabled":               True,
  "japaneseEnabled":            True,
  "koreanEnabled":              True
}