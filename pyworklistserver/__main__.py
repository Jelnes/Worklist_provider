#!/usr/bin/env python3
""" Application entry point. The functions and classes in this 
module are responsible for handling command line arguments logging
and keyboard interrupts """

import argparse
import signal
import time
import logging
import logging.handlers
from pyworklistserver import server_config
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
        '--seed',
        type=int,
        default=0,
        help='Seed to be used to generate patients'
    )

    args = parser.parse_args()
    network_address = server_config.NetworkAddress(args.ip, args.port)
    return (server_config.ServerConfig(network_address, args.aetitle, args.verbose), args.logfile, args.seed)

class PyDicomServer:
    """ Wrapper server implementation that supports stopping through Ctrl+C.

    This is just delegating to the core Worklist server implementation
    """

    def __init__(self, config, app_logger, seed):
        self._running = True
        self._logger = app_logger
        self._server = worklist_server.WorklistServer(config, app_logger, seed, blocking=False)
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
    server_config, logfile, seed = _get_serverconfig_from_commandline()
    logger = _configure_logger(logfile, logging.DEBUG if server_config.verbose else logging.WARN)

    server = PyDicomServer(server_config, logger, seed)
    server.run_until_stopped()
