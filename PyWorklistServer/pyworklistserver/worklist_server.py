""" DICOM server implementation that responds to C-FIND requests"""
import random
from pynetdicom import AE
from pynetdicom import evt
from pynetdicom.sop_class import ModalityWorklistInformationFind

from pyworklistserver import worklist
from pyworklistserver import user_config

class WorklistServer:
    """ Simple worklist server with support for one client. This
    implementation class is responsible for network communication with
    the client. """

    def __init__(self, serverConfig, app_logger, blocking):
        self._config = serverConfig
        self._logger = app_logger
        self._blocking = blocking
        self._worklist_factory = worklist.RandomWorklist('ISO_IR 100')
        self._handlers = [
            (evt.EVT_C_FIND, self._on_find, [app_logger]),
        ]
        self._server = None

    def get_seedNumber(self):
        """Return Function for seed-value"""
        if user_config.seed_Number == 0:
            return random.randrange(1, 1000000)
        return user_config.seed_Number

    def start(self):
        """ Start the server and listen to specified address and port """
        ae = AE(self._config.ae_title)
        ae.add_supported_context(ModalityWorklistInformationFind)
        self._logger.info('Running worklist server with AE title {}, ip: {}, listening to port: {}'.format(
            self._config.ae_title,
            self._config.network_address.address,
            self._config.network_address.port)
        )

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
        random.seed(self.get_seedNumber())
        totalRate = user_config.rateOfRandomExams + user_config.rateOfCleanExams
        totalExams = random.randrange(user_config.minAmountOfWorklistExams, user_config.maxAmountOfWorklistExams)

        i = 0
        while i < totalExams:
            r = random.randrange(1, totalRate)
            if r <= user_config.rateOfCleanExams:
                clean_worklist_items = self._worklist_factory.get_clean_worklist()
                for clean_worklist_item in clean_worklist_items:
                    if event.is_cancelled:
                        app_logger.info('Exams are cancelled')
                        yield (0xFE00, None)  # Check if C-CANCEL has been received
                        return
                    i += 1
                    yield (0xFF00, clean_worklist_item)

            elif r > user_config.rateOfCleanExams:
                random_worklist_items = self._worklist_factory.get_worklist()
                for random_worklist_item in random_worklist_items:
                    if event.is_cancelled:
                        app_logger.info('Exams are cancelled')
                        yield (0xFE00, None)  # Check if C-CANCEL has been received
                        return
                    i += 1
                    yield (0xFF00, random_worklist_item)
        app_logger.info('Created worklist with {} exams'.format(totalExams))
        return
