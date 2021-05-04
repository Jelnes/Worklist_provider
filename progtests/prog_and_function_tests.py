from context import pyworklistserver

from pyworklistserver import get_config
from pyworklistserver import fault_provider

if __name__ == '__main__':
    test = get_config.GetConfig()
    test.delay_enabled = 1
    test.likelihood_of_delay = 100
    faultTest = fault_provider.FaultProvider(test)

    print(faultTest._delay())
