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

    def __init__(self, serverConfig, app_logger, blocking):
        self._config = serverConfig
        self._config_values = get_config.GetConfig()
        self._logger = app_logger
        self._blocking = blocking
        self._worklist_factory = worklist.RandomWorklist('ISO_IR 100', self._config_values)
        self._handlers = [
            (evt.EVT_C_FIND, self._on_find, [app_logger]),
        ]
        self._server = None

    def get_seedNumber(self):
        """Return Function for seed-value"""
        if self._config_values.seed_Number == 0:
            return random.randrange(1, 1000000)
        return self._config_values.seed_Number

    def setup_log_seed(self):
        if os.path.exists("logfile.txt"):
            os.remove("logfile.txt")
        f = open("logfile.txt", "w+")
        f.write('User_config:\trateOfRandomExams: %d\t rateOfCleanExams: %d\t minAmountOfWorklistExams: %d\t maxAmountOfWorklistExams: %d\t seed_Number (set): %d\n likelihood_of_long_string: %d\t likelihood_of_empty_string: %d\t likelihood_of_None_string: %d\t likelihood_of_delay: %d\t is_long: %d\t is_empty: %d\t is_None: %d\t is_delay: %d \n\n'
        % (user_config.rateOfRandomExams, user_config.rateOfCleanExams, user_config.minAmountOfWorklistExams, user_config.maxAmountOfWorklistExams, user_config.seed_Number, user_config.likelihood_of_long_string, user_config.likelihood_of_empty_string, user_config.likelihood_of_None_string, user_config.likelihood_of_delay, user_config.long_enabled, user_config.empty_enabled, user_config.none_enabled, user_config.delay_enabled))

        f.close()

    def log_seed (self, seed):
        f = open("logfile.txt", "a+")
        f.write('%s\tSeed: %d\n' % (time.asctime(time.localtime()), seed))
        f.close()

    def start(self):
        """ Start the server and listen to specified address and port """
        ae = AE(self._config.ae_title)
        ae.add_supported_context(ModalityWorklistInformationFind)
        self._logger.info('Running worklist server with AE title {}, ip: {}, listening to port: {}'.format(
            self._config.ae_title,
            self._config.network_address.address,
            self._config.network_address.port)
        )

        self.setup_log_seed()

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
        seed = self.get_seedNumber()
        random.seed(seed)
        self.log_seed(seed)

        totalRate = self._config_values.rateOfRandomExams + self._config_values.rateOfCleanExams
        totalExams = random.randrange(self._config_values.minAmountOfWorklistExams, self._config_values.maxAmountOfWorklistExams)

        for i in range (totalExams):
            r = random.randrange(1, totalRate)
            if r <= self._config_values.rateOfCleanExams:
                worklist = self._worklist_factory.get_clean_worklist()
            else:
                worklist = self._worklist_factory.get_random_worklist()

            if event.is_cancelled:
                app_logger.info('Exams are cancelled')
                yield (0xFE00, None)  # Check if C-CANCEL has been received
                return

            yield (0xFF00, worklist)

        app_logger.info('Created worklist with {} exams'.format(totalExams))
        app_logger.info('The seed used is: {}'.format(seed))

        return
