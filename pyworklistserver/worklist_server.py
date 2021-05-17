""" DICOM server implementation that responds to C-FIND requests"""
import random
import os
import time
from pynetdicom import AE
from pynetdicom import evt
from pynetdicom.sop_class import ModalityWorklistInformationFind

from pyworklistserver import worklist
from pyworklistserver import user_config
from pyworklistserver import get_config

class WorklistServer:
    """ Simple worklist server with support for one client. This
    implementation class is responsible for network communication with
    the client. """

<<<<<<< HEAD
    def __init__(self, serverConfig, app_logger, seedfile, reproduce, blocking):
=======
    def __init__(self, serverConfig, app_logger, inserted_config, blocking):
>>>>>>> 76a562a (Added command-line argument for path to json-file with configurable values to allow command-line control over the server-output.)
        self._config = serverConfig
        self._config_provider = get_config.ConfigProvider(inserted_config)
        self._config_values = self._config_provider.defaultConfig
        self._logger = app_logger
        self._blocking = blocking
        self._seedfile = seedfile
        self._reproduce = reproduce
        self._worklist_factory = worklist.RandomWorklist('ISO_IR 100', self._config_values)
        self._handlers = [
            (evt.EVT_C_FIND, self._on_find, [app_logger]),
        ]
        self._server = None

<<<<<<< HEAD
<<<<<<< HEAD
    def get_seedNumber(self):
        """Return Function for seed-value"""
        if self._reproduce:
            with open(self._seedfile, "r") as f:
                seed = int(f.read())
        else:
            seed = random.randrange(1, 1000000)
            with open(self._seedfile, "w") as f:
                f.write(str(seed))
        return seed

=======
>>>>>>> 335d443 (Put content in user-config.py in dictionary, and updated use througout project. Purpose: Cleaner code and opening the possibility to merge with config-input from command-line.)
=======
        self._logger.info(self._config_values)

>>>>>>> 76a562a (Added command-line argument for path to json-file with configurable values to allow command-line control over the server-output.)
    def start(self):
        """ Start the server and listen to specified address and port """
        ae = AE(self._config.ae_title)
        ae.add_supported_context(ModalityWorklistInformationFind)
        self._logger.info('Running worklist server with AE title {}, ip: {}, listening to port: {}'.format(
            self._config.ae_title,
            self._config.network_address.address,
            self._config.network_address.port)
        )

<<<<<<< HEAD

=======
>>>>>>> 335d443 (Put content in user-config.py in dictionary, and updated use througout project. Purpose: Cleaner code and opening the possibility to merge with config-input from command-line.)
        self._server = ae.start_server(
            self._config.network_address,
            evt_handlers=self._handlers,
            block=self._blocking)

    def stop(self):
        """ Stop the server """
        self._logger.info('Shutting down')
        self._server.shutdown()

    def _on_find(self, event, app_logger):
        """ Event handler for C-FIND requests """
        seed = random.randrange(1, 1000000)
        random.seed(seed)

        totalExams = random.randrange(self._config_values["minAmountOfWorklistExams"], self._config_values["maxAmountOfWorklistExams"])

        for i in range (totalExams):
            r = random.uniform(0, 1)
            if r <= self._config_values["rateOfCleanExams"]:
                worklist = self._worklist_factory.get_clean_worklist()
            else:
                worklist = self._worklist_factory.get_random_worklist()

            if event.is_cancelled:
                app_logger.info('Request cancelled by client')
                yield (0xFE00, None)  # Check if C-CANCEL has been received
                return

            yield (0xFF00, worklist)

        app_logger.info('Created worklist with {} exams'.format(totalExams))
        app_logger.info('The seed used is: {}'.format(seed))

        return
