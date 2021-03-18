from context import pyworklistserver

from pyworklistserver import get_config

if __name__ == '__main__':
    test = get_config.GetConfig()

    print(test.maxAmountOfWorklistExams)

    test.maxAmountOfWorklistExams = 10

    print(test.maxAmountOfWorklistExams)

    test.reset()
    
    print(test.maxAmountOfWorklistExams)
