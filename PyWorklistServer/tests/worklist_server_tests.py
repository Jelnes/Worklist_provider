#!/usr/bin/env python3

import unittest
import logging
import logging.handlers
import random

from context import pyworklistserver
from pydicom.dataset import Dataset

import worklist_client
from pyworklistserver import worklist_server
from pyworklistserver import server_config
from pyworklistserver import user_config

def _setup_logger_for_test():
    formatter = logging.Formatter('%(levelname).1s: %(message)s')

    # Setup pynetdicom library's logging
    pynd_logger = logging.getLogger('pynetdicom')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    pynd_logger.addHandler(handler)
    pynd_logger.setLevel(logging.WARN)

    # Setup application's logging
    app_logger = logging.Logger('pyworklistserver')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    app_logger.addHandler(handler)
    app_logger.setLevel(logging.WARN)

    return app_logger


class WorklistServerTests(unittest.TestCase):

    def setUp(self):
        network_address = server_config.NetworkAddress('127.0.0.1', 104)
        test_logger = _setup_logger_for_test()
        self._server_config = server_config.ServerConfig(network_address=network_address, ae_title='WorklistServerTests', verbose=True)
        self._server = worklist_server.WorklistServer(self._server_config, test_logger, blocking=False)
        self._server.start()

    def tearDown(self):
        self._server.stop()

    def test_RequireThat_WorklistRequest_ReturnsNonEmptyWorklist_WhenQueryingAllPatients(self):
        client = worklist_client.WorklistClient(self._server_config.network_address)

        query_dataset = Dataset()
        query_dataset.PatientName = '*'
        worklist = client.get_worklist(query_dataset)
        self.assertTrue(len(worklist) > 0)

    def test_RequireThat_WorklistRequest_ReturnsWorklistWithAllExpectedFieldsPopulated(self):
        client = worklist_client.WorklistClient(self._server_config.network_address)

        query_dataset = Dataset()
        query_dataset.PatientName = '*'
        worklist = client.get_worklist(query_dataset)
        worklist_item = worklist[0]

        self.assertTrue(len(worklist_item.StudyInstanceUID) > 0)
        self.assertTrue(len(worklist_item.StudyInstanceUID) > 0)
        self.assertTrue(len(worklist_item.Modality) > 0)
        self.assertTrue(len(worklist_item.SpecificCharacterSet) > 0)
        self.assertTrue(len(worklist_item.AccessionNumber) > 0)
        self.assertTrue(len(worklist_item.PatientBirthDate) > 0)
        self.assertTrue(len(worklist_item.PatientName) > 0)
        self.assertTrue(len(worklist_item.PatientID) > 0)
        self.assertTrue(len(worklist_item.IssuerOfPatientID) > 0)
        self.assertTrue(len(worklist_item.RequestedProcedureID) > 0)
        self.assertTrue(len(worklist_item.RequestedProcedureDescription) > 0)
        self.assertTrue(len(worklist_item.AdmissionID) > 0)
        self.assertTrue(len(str(worklist_item.PatientSize)) > 0)
        self.assertTrue(len(str(worklist_item.PatientWeight)) > 0)

        scheduled_step = worklist_item.ScheduledProcedureStepSequence[0]
        self.assertTrue(len(scheduled_step.ScheduledPerformingPhysicianName) > 0)
        self.assertTrue(len(scheduled_step.ScheduledProcedureStepStartDate) > 0)
        self.assertTrue(len(scheduled_step.ScheduledProcedureStepStartTime) > 0)
        self.assertTrue(len(scheduled_step.ScheduledProcedureStepDescription) > 0)
        self.assertTrue(len(scheduled_step.CommentsOnTheScheduledProcedureStep) > 0)

        otherPatientIdsSq = worklist_item.OtherPatientIDsSequence
        for otherPatientId in otherPatientIdsSq:
            self.assertTrue(len(otherPatientId.PatientID) > 0)
            self.assertTrue(len(otherPatientId.IssuerOfPatientID) > 0)
            self.assertEqual(otherPatientId.TypeOfPatientID, 'TEXT')


    def test_RequireThat_WorklistRequest_ReturnsWorklistSize_BetweenMinMax(self):
        client = worklist_client.WorklistClient(self._server_config.network_address)

        query_dataset = Dataset()
        query_dataset.PatientName = '*'
        worklist = client.get_worklist(query_dataset)
        self.assertTrue(len(worklist) >= user_config.minAmountOfWorklistExams and len(worklist) <= user_config.maxAmountOfWorklistExams)

    def test_RequireThat_MulipleWorklistRequests_ReturnsWorklistWithSameLength_ByUseOfSeed(self):
        client = worklist_client.WorklistClient(self._server_config.network_address)

        query_dataset = Dataset()
        query_dataset.PatientName = '*'

        seed = random.randrange(1000)

        random.seed(seed)
        worklist_one = client.get_worklist(query_dataset)

        random.seed(seed)
        worklist_two = client.get_worklist(query_dataset)

        self.assertEqual(len(worklist_one), len(worklist_two))

    def test_RequireThat_MultipleWorklistRequests_ReturnsIdenticalWorklists_ByUseOfSeed(self):
        client = worklist_client.WorklistClient(self._server_config.network_address)

        query_dataset = Dataset()
        query_dataset.PatientName = '*'

        seed = random.randrange(1000)

        random.seed(seed)
        worklist_one = client.get_worklist(query_dataset)

        random.seed(seed)
        worklist_two = client.get_worklist(query_dataset)

        exam = random.randrange(len(worklist_one))

        worklist_item_one = worklist_one[exam]
        worklist_item_two = worklist_two[exam]

        self.assertEqual(worklist_item_one.StudyInstanceUID, worklist_item_two.StudyInstanceUID)
        self.assertEqual(worklist_item_one.Modality, worklist_item_two.Modality)
        self.assertEqual(worklist_item_one.SpecificCharacterSet, worklist_item_two.SpecificCharacterSet)
        self.assertEqual(worklist_item_one.AccessionNumber, worklist_item_two.AccessionNumber)
        self.assertEqual(worklist_item_one.PatientBirthDate, worklist_item_two.PatientBirthDate)
        self.assertEqual(worklist_item_one.PatientName, worklist_item_two.PatientName)
        self.assertEqual(worklist_item_one.PatientID, worklist_item_two.PatientID)
        self.assertEqual(worklist_item_one.IssuerOfPatientID, worklist_item_two.IssuerOfPatientID)
        self.assertEqual(worklist_item_one.PatientWeight, worklist_item_two.PatientWeight)
        self.assertEqual(worklist_item_one.PatientSize, worklist_item_two.PatientSize)
        self.assertEqual(worklist_item_one.AdmissionID, worklist_item_two.AdmissionID)
        self.assertEqual(worklist_item_one.RequestedProcedureID, worklist_item_two.RequestedProcedureID)
        self.assertEqual(worklist_item_one.RequestedProcedureDescription, worklist_item_two.RequestedProcedureDescription)
        


if __name__ == '__main__':
    _setup_logger_for_test()
    unittest.main()
