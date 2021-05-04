""" Worklist generator classes """

import datetime
import random
import string
from pydicom.uid import generate_uid
from pydicom.dataset import Dataset
from pyworklistserver import fault_provider
from pyworklistserver import user_config

def _random_unicode_string(length, language_string):
    """ Create a random string of specified length containing non-ascii, or characters from unsupported languages """
    return ''.join(random.choices(' ' + string.ascii_uppercase + string.ascii_lowercase + string.digits + language_string, k=length))

def _create_random_ascii_string(length):
    """ Creates an ascii string with characters only in the range [0, 127] """
    return ''.join(random.choices(' ' + string.ascii_uppercase + string.ascii_lowercase + string.digits, k=length))


def _extend_with_random_to_length(text, length, _None_string_func):
    """ Extend a string with random characters up to the given length """
    if _None_string_func() == 1:
        return None
    if length == 0:
        return ''
    return text + _random_unicode_string(length - len(text), self._fault_provider._get_random_language_string())

def _random_person_name(max_len_per_name):
    """ Create a random person name separated by ^ character """
    return '^'.join([_random_unicode_string(max_len_per_name, self._fault_provider._get_random_language_string()) for _ in range(1, random.randrange(2, 4))])

def _random_number_string(max_len):
    """ Create a random string containing numeric values only """
    return ''.join(random.choices(string.digits, k=random.randrange(1, max_len)))

def _random_dicom_date_after_1900():
    """ Return a string containing a random date on DICOM format """
    start = datetime.date(1900, 1, 1)
    now = datetime.date.today()
    maxdays = (now - start)
    randomdays = random.randrange(0, maxdays.days)
    date = start + datetime.timedelta(days=randomdays)
    return date.strftime('%Y%m%d')

def _random_dicom_time():
    """ Return a string containing a random time point on DICOM format """
    hour = random.randrange(0, 24)
    minutes = random.randrange(0, 59)
    seconds = random.randrange(0, 59)
    return '{:02}{:02}{:02}'.format(hour, minutes, seconds)



_VIVID_HACK_MAX_PERSON_NAME = 64

class RandomWorklist:
    """ Generator for random worklists """
    def __init__(self, specificCharSet, config_values):
        self._specific_charset = specificCharSet
        self._config_values = config_values
        self._fault_provider = fault_provider.FaultProvider(config_values)


    def get_random_worklist(self):
        """ Generate a random worklist """

        worklist_item = Dataset()
        worklist_item.StudyInstanceUID = generate_uid(prefix='1.2.840.113619.2.391.6789.', entropy_srcs=[_random_unicode_string(10, self._fault_provider._get_random_language_string()), _random_unicode_string(10, self._fault_provider._get_random_language_string())])
        worklist_item.Modality = 'US'
        worklist_item.SpecificCharacterSet = self._specific_charset
        worklist_item.CurrentPatientLocation = _extend_with_random_to_length('', self._fault_provider. _get_random_string_length(64), self._fault_provider._return_None_string)
        worklist_item.AccessionNumber = _random_unicode_string(16, self._fault_provider._get_random_language_string())
        worklist_item.PatientBirthDate = _random_dicom_date_after_1900()
        worklist_item.PatientName = self._get_person_name()
        worklist_item.PatientID = _extend_with_random_to_length('', self._fault_provider. _get_random_string_length(64), self._fault_provider._return_None_string)

        self._fault_provider._sleep_random() #Possible delay

        worklist_item.IssuerOfPatientID = _extend_with_random_to_length('', self._fault_provider. _get_random_string_length(64), self._fault_provider._return_None_string)
        worklist_item.PatientWeight = str(random.uniform(10.0, 150.0))[:16]
        worklist_item.PatientSize = str(random.uniform(1.0, 2.5))[:16]
        worklist_item.AdmissionID = _extend_with_random_to_length('', self._fault_provider. _get_random_string_length(64), self._fault_provider._return_None_string)
        worklist_item.RequestedProcedureID = _extend_with_random_to_length('', self._fault_provider. _get_random_string_length(16), self._fault_provider._return_None_string)
        worklist_item.RequestedProcedureDescription = _extend_with_random_to_length('', self._fault_provider. _get_random_string_length(64), self._fault_provider._return_None_string)
        worklist_item.ReferringPhysicianName = self._get_person_name()

        otherPatientIdsSq = [Dataset(), Dataset()]
        for otherPatientId in otherPatientIdsSq:
            otherPatientId.PatientID = _extend_with_random_to_length('', self._fault_provider. _get_random_string_length(64), self._fault_provider._return_None_string)
            otherPatientId.IssuerOfPatientID = _extend_with_random_to_length('', self._fault_provider. _get_random_string_length(64), self._fault_provider._return_None_string)
            otherPatientId.TypeOfPatientID = 'TEXT'

        worklist_item.OtherPatientIDsSequence = otherPatientIdsSq

        step = Dataset()
        step.ScheduledPerformingPhysicianName = self._get_person_name()
        step.ScheduledProcedureStepStartDate = _random_dicom_date_after_1900()
        step.ScheduledProcedureStepStartTime = _random_dicom_time()
        step.ScheduledProcedureStepDescription = _extend_with_random_to_length('', self._fault_provider. _get_random_string_length(64), self._fault_provider._return_None_string)
        step.CommentsOnTheScheduledProcedureStep = _extend_with_random_to_length('', self._fault_provider. _get_random_string_length(10240), self._fault_provider._return_None_string)
        worklist_item.ScheduledProcedureStepSequence = [step]

        return worklist_item

    def get_clean_worklist(self):
        """ Generates a clean worklist """

        worklist_item = Dataset()
        worklist_item.StudyInstanceUID = generate_uid(prefix='1.2.840.113619.2.391.6789.', entropy_srcs=[_create_random_ascii_string(10), _create_random_ascii_string(10)])
        worklist_item.Modality = 'US'
        worklist_item.SpecificCharacterSet = self._specific_charset
        worklist_item.AccessionNumber = '123'
        worklist_item.PatientBirthDate = '19901015'
        worklist_item.PatientName = 'Clean^Exam'
        worklist_item.PatientID = _create_random_ascii_string(64)
        worklist_item.IssuerOfPatientID = 'Issuer of patient id: Bob'
        worklist_item.PatientWeight = str(100.0)
        worklist_item.PatientSize = str(2.1)
        worklist_item.AdmissionID = 'Admission id 3'
        worklist_item.RequestedProcedureID = 'Step id 2'
        worklist_item.RequestedProcedureDescription = 'Step description Clean Exam'

        otherPatientIdsSq = [Dataset(), Dataset()]
        for otherPatientId in otherPatientIdsSq:
            otherPatientId.PatientID = 'Bob123'
            otherPatientId.IssuerOfPatientID = 'Issuer of patient id: Arne'
            otherPatientId.TypeOfPatientID = 'TEXT'

        worklist_item.OtherPatientIDsSequence = otherPatientIdsSq

        step = Dataset()
        step.ScheduledPerformingPhysicianName = 'Ola Nordmann'
        step.ScheduledProcedureStepStartDate = '20201224'
        step.ScheduledProcedureStepStartTime = '121212'
        step.ScheduledProcedureStepDescription = 'Scheduled procedure step description '
        step.CommentsOnTheScheduledProcedureStep = 'Scheduled step comments '
        worklist_item.ScheduledProcedureStepSequence = [step]

        return worklist_item

    def _get_person_name(self):
        """ Create a random person name and truncate the name components according to Vivid bug """
        return _random_person_name(32)[:_VIVID_HACK_MAX_PERSON_NAME]  # fix for wrong handling in EchoPAC/Scanner
