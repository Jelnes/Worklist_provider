""" Structs/tuples used across the package """
from collections import namedtuple

NetworkAddress = namedtuple('NetworkAddress', ['address', 'port'])
ServerConfig = namedtuple('ServerConfig', ['network_address', 'ae_title', 'verbose'])
