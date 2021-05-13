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
        self._server = worklist_server.WorklistServer(self._server_config, test_logger, "seed.txt", False, blocking=False)
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
        self.assertTrue(len(worklist) >= user_config.default_config["minAmountOfWorklistExams"] and len(worklist) <= user_config.default_config["maxAmountOfWorklistExams"])

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
        self._server._config_provider.reset()
        self._server._config_values["rateOfCleanExams"] = 1

        client = worklist_client.WorklistClient(self._server_config.network_address)

        query_dataset = Dataset()
        query_dataset.PatientName = '*'


        worklist = client.get_worklist(query_dataset)
        worklist_item = worklist[0]

        self.assertEqual((worklist_item.PatientName), 'Clean^Exam')

        self._server._config_provider.reset()
        self._server._config_values["rateOfCleanExams"] = 0

        worklist = client.get_worklist(query_dataset)
        worklist_item = worklist[0]

        self.assertNotEqual((worklist_item.PatientName), 'Clean^Exam')
        self._server._config_provider.reset()

    def test_RequireThat_WorklistRequest_ReturnsLongStrings_WhenSet(self):
        self._server._config_provider.reset()
        self._server._config_values["rateOfCleanExams"] = 0

        self._server._config_values["oversizedStringsEnabled"] = True
        self._server._config_values["emptyStringsEnabled"] = False

        self._server._config_values["likelihoodOfLongString"] = 100.0

        client = worklist_client.WorklistClient(self._server_config.network_address)

        query_dataset = Dataset()
        query_dataset.PatientName = '*'


        worklist = client.get_worklist(query_dataset)
        worklist_item = worklist[0]

        self.assertTrue(len(worklist_item.CurrentPatientLocation) > 64)

        self._server._config_values["oversizedStringsEnabled"] = False

        worklist = client.get_worklist(query_dataset)
        worklist_item = worklist[0]

        self.assertTrue(len(worklist_item.CurrentPatientLocation) <= 64)

        self._server._config_provider.reset()

    def test_RequireThat_WorklistRequest_ReturnsEmptyStrings_WhenSet(self):
        self._server._config_provider.reset()
        self._server._config_values["rateOfCleanExams"] = 0

        self._server._config_values["oversizedStringsEnabled"] = False
        self._server._config_values["EmptyStringsEnabled"] = True

        self._server._config_values["likelihoodOfLongString"] = 0.0
        self._server._config_values["likelihoodOfEmptyString"] = 100.0

        client = worklist_client.WorklistClient(self._server_config.network_address)

        query_dataset = Dataset()
        query_dataset.PatientName = '*'

        worklist = client.get_worklist(query_dataset)
        worklist_item = worklist[0]

        self.assertEqual(len(worklist_item.CurrentPatientLocation), 0)

        self._server._config_provider.reset()



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

        tags = [
            "StudyInstanceUID",
            "Modality",
            "SpecificCharacterSet",
            "AccessionNumber",
            "PatientBirthDate",
            "PatientName",
            "PatientID",
            "IssuerOfPatientID",
            "PatientWeight",
            "PatientSize",
            "AdmissionID",
            "RequestedProcedureID",
            "RequestedProcedureDescription"
        ]

        for tag in tags:
            self.assertEqual(worklist_item_one[tag], worklist_item_two[tag])

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

<<<<<<< HEAD
    def test_RequireThat_Seedfile_UpdatesWhen_ReproduceFalse(self):
        client = worklist_client.WorklistClient(self._server_config.network_address)

        query_dataset = Dataset()
        query_dataset.PatientName = '*'

        worklist = client.get_worklist(query_dataset)
        with open("seed.txt", "r") as f:
            seed1 = f.read()

        self._server._reproduce = False

        worklist_two = client.get_worklist(query_dataset)
        with open("seed.txt", "r") as f:
            seed2 = f.read()

        self.assertTrue(seed1 != seed2)

    def test_RequireThat_Seedfile_IsSameWhen_ReproduceTrue(self):
        client = worklist_client.WorklistClient(self._server_config.network_address)

        query_dataset = Dataset()
        query_dataset.PatientName = '*'

        worklist = client.get_worklist(query_dataset)
        with open("seed.txt", "r") as f:
            seed1 = f.read()

        self._server._reproduce = True

        worklist_two = client.get_worklist(query_dataset)
        with open("seed.txt", "r") as f:
            seed2 = f.read()
=======

>>>>>>> 335d443 (Put content in user-config.py in dictionary, and updated use througout project. Purpose: Cleaner code and opening the possibility to merge with config-input from command-line.)

        self.assertTrue(seed1 == seed2)

if __name__ == '__main__':
    _setup_logger_for_test()
    unittest.main()
