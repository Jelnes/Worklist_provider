#!/usr/bin/env python3

import unittest
import logging
import logging.handlers
import random
import os

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

    def test_RequireThat_WorklistRequest_ReturnsCleanWorklist_WhenSet(self):
        self._server._config_values.reset()
        self._server._config_values.rateOfCleanExams = 2
        self._server._config_values.rateOfRandomExams = 0

        client = worklist_client.WorklistClient(self._server_config.network_address)

        query_dataset = Dataset()
        query_dataset.PatientName = '*'


        worklist = client.get_worklist(query_dataset)
        worklist_item = worklist[0]

        self.assertEqual((worklist_item.PatientName), 'Clean Exam')

        self._server._config_values.reset()
        self._server._config_values.rateOfCleanExams = 0
        self._server._config_values.rateOfRandomExams = 2

        worklist = client.get_worklist(query_dataset)
        worklist_item = worklist[0]

        self.assertNotEqual((worklist_item.PatientName), 'Clean Exam')
        self._server._config_values.reset()

    def test_RequireThat_WorklistRequest_ReturnsLongStrings_WhenSet(self):
        self._server._config_values.reset()
        self._server._config_values.rateOfCleanExams = 0
        self._server._config_values.rateOfRandomExams = 2

        self._server._config_values.long_enabled = 1
        self._server._config_values.empty_enabled = 0

        self._server._config_values.likelihood_of_long_string = 100.0

        client = worklist_client.WorklistClient(self._server_config.network_address)

        query_dataset = Dataset()
        query_dataset.PatientName = '*'


        worklist = client.get_worklist(query_dataset)
        worklist_item = worklist[0]

        self.assertTrue(len(worklist_item.CurrentPatientLocation) > 64)

        self._server._config_values.long_enabled = 0

        worklist = client.get_worklist(query_dataset)
        worklist_item = worklist[0]

        self.assertTrue(len(worklist_item.CurrentPatientLocation) <= 64)

        self._server._config_values.reset()

    def test_RequireThat_WorklistRequest_ReturnsEmptyStrings_WhenSet(self):
        self._server._config_values.reset()
        self._server._config_values.rateOfCleanExams = 0
        self._server._config_values.rateOfRandomExams = 2

        self._server._config_values.long_enabled = 0
        self._server._config_values.empty_enabled = 1

        self._server._config_values.likelihood_of_long_string = 0.0
        self._server._config_values.likelihood_of_empty_string = 100.0

        client = worklist_client.WorklistClient(self._server_config.network_address)

        query_dataset = Dataset()
        query_dataset.PatientName = '*'

        worklist = client.get_worklist(query_dataset)
        worklist_item = worklist[0]

        self.assertEqual(len(worklist_item.CurrentPatientLocation), 0)

        self._server._config_values.reset()



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

        for i in range(len(worklist_item_one.OtherPatientIDsSequence)):
            self.assertEqual(worklist_item_one.OtherPatientIDsSequence[i].PatientID, worklist_item_two.OtherPatientIDsSequence[i].PatientID)
            self.assertEqual(worklist_item_one.OtherPatientIDsSequence[i].IssuerOfPatientID, worklist_item_two.OtherPatientIDsSequence[i].IssuerOfPatientID)
            self.assertEqual(worklist_item_one.OtherPatientIDsSequence[i].TypeOfPatientID, worklist_item_two.OtherPatientIDsSequence[i].TypeOfPatientID)

        for i in range(len(worklist_item_one.ScheduledProcedureStepSequence)):
            self.assertEqual(worklist_item_one.ScheduledProcedureStepSequence[i].ScheduledPerformingPhysicianName, worklist_item_two.ScheduledProcedureStepSequence[i].ScheduledPerformingPhysicianName)
            self.assertEqual(worklist_item_one.ScheduledProcedureStepSequence[i].ScheduledProcedureStepStartDate, worklist_item_two.ScheduledProcedureStepSequence[i].ScheduledProcedureStepStartDate)
            self.assertEqual(worklist_item_one.ScheduledProcedureStepSequence[i].ScheduledProcedureStepStartTime, worklist_item_two.ScheduledProcedureStepSequence[i].ScheduledProcedureStepStartTime)
            self.assertEqual(worklist_item_one.ScheduledProcedureStepSequence[i].ScheduledProcedureStepDescription, worklist_item_two.ScheduledProcedureStepSequence[i].ScheduledProcedureStepDescription)
            self.assertEqual(worklist_item_one.ScheduledProcedureStepSequence[i].CommentsOnTheScheduledProcedureStep, worklist_item_two.ScheduledProcedureStepSequence[i].CommentsOnTheScheduledProcedureStep)

    def test_RequireThat_Logfile_Returnslogfile_Withcontent(self):
        client = worklist_client.WorklistClient(self._server_config.network_address)

        query_dataset = Dataset()

        query_dataset.PatientName = '*'

        self.assertTrue(os.path.exists("logfile.txt"))
        self.assertTrue(os.path.getsize("logfile.txt") > 0)

    def test_RequireThat_Logfile_Appendsatcall(self):
        client = worklist_client.WorklistClient(self._server_config.network_address)
        query_dataset = Dataset()
        query_dataset.PatientName = '*'

        with open('logfile.txt', 'r') as file:
            data1 = file.read()

        client.get_worklist(query_dataset)

        with open('logfile.txt', 'r') as file:
            data2 = file.read()

        self.assertTrue(data1 != data2)


if __name__ == '__main__':
    _setup_logger_for_test()
    unittest.main()
