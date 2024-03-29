#!/usr/bin/env python3
""" Application entry point. The functions and classes in this
module are responsible for handling command line arguments logging
and keyboard interrupts """

import argparse
import signal
import string
import time
import logging
import logging.handlers
import json
import os
from pyworklistserver import server_config
from pyworklistserver import default_config
from pyworklistserver import worklist_server

def _configure_logger(filename, pynetdicom_verbosity: int):
    formatter = logging.Formatter('PyWorklistServer: %(levelname).1s: %(message)s')

    # Setup pynetdicom library's logging
    pynd_logger = logging.getLogger('pynetdicom')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    pynd_logger.addHandler(handler)
    pynd_logger.setLevel(pynetdicom_verbosity)

    # Setup application's logging
    app_logger = logging.Logger('PyWorklistServer')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    app_logger.addHandler(handler)
    app_logger.setLevel(logging.DEBUG)

    if filename is not None:
        # Attach file logging
        fileHandler = logging.handlers.RotatingFileHandler(filename, maxBytes=1024 * 1024 * 50, backupCount=3)
        fileFormatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fileHandler.setFormatter(fileFormatter)
        app_logger.addHandler(fileHandler)
        pynd_logger.addHandler(fileHandler)
    return app_logger

def _get_userconfig_from_commandline(file):
    inputDictionary = {}

    try:
        with open(file, 'r') as json_file:
            inputDictionary = json.load(json_file)
            return inputDictionary
    except Exception as e:
        with open(file, 'w') as outfile:
            json.dump(default_config.default_config, outfile, separators=(",\n", ": "))
            return default_config.default_config

def _get_serverconfig_from_commandline():
    parser = argparse.ArgumentParser(description='Launch dicom worklist server')
    parser.add_argument(
        '--ip',
        default='127.0.0.1',
        help='Ip address that this server runs under'
    )

    parser.add_argument(
        '--port',
        type=int,
        default=104,
        help='port that this server will listen to'
    )

    parser.add_argument(
        '--aetitle',
        default='PyWorklistServer',
        help='DICOM Application Entity title that identifies the server (Max 16 characters)'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Extra logging'
    )

    parser.add_argument(
        '--logfile',
        help='Path to log file where server activity is logged'
    )

    parser.add_argument(
        '--seedfile',
        default='seed.txt',
        help='Path to seed file where last seed is stored for Reproduction'
    )

    parser.add_argument(
        '--reproduce',
        action='store_true',
        help='Reproduction with last seed.'
    )

    parser.add_argument(
        '--worklistconfigfile',
        default='worklistconfigfile.json',
        help='J-son file with configurable values. See user-config.py for available keys.'
    )

    args = parser.parse_args()
    network_address = server_config.NetworkAddress(args.ip, args.port)
    return (server_config.ServerConfig(network_address, args.aetitle, args.verbose), args.logfile, args.seedfile, args.reproduce, args.worklistconfigfile)

class PyDicomServer:
    """ Wrapper server implementation that supports stopping through Ctrl+C.

    This is just delegating to the core Worklist server implementation
    """

    def __init__(self, server_config, app_logger, seedfile, reproduce, worklist_config):
        self._running = True
        self._logger = app_logger
        self._server = worklist_server.WorklistServer(server_config, app_logger, seedfile, reproduce, worklist_config, blocking=False)
        signal.signal(signal.SIGINT, self._handle_signal)

    def run_until_stopped(self):
        """ Start server and run it until stopped by Ctrl-C """
        self._server.start()
        while self._running:
            time.sleep(0.1)
        self._server.stop()

    def _handle_signal(self, sig, frame):
        ''' Handle shutdown through Ctrl+C '''
        self._logger.info('Received CTRL-C signal')
        self._running = False


if __name__ == '__main__':
    server_config, logfile, seedfile, reproduce, worklist_config_file = _get_serverconfig_from_commandline()
    logger = _configure_logger(logfile, logging.DEBUG if server_config.verbose else logging.WARN)
    worklist_config = _get_userconfig_from_commandline(worklist_config_file)

    server = PyDicomServer(server_config, logger, seedfile, reproduce, worklist_config)
    server.run_until_stopped()
