""" Worklist generator classes """


""" Worklist generator classes """

import datetime
import random
import string
from pydicom.uid import generate_uid
from pydicom.dataset import Dataset

__NONASCII = 'æÆøØåÅßäöüÄÖÜ' # Just an arbitrarily selected list of non ascii characters

def _random_unicode_string(length):
    """ Create a random string of specified length containing some non-ascii characters """
    return ''.join(random.choices(' ' + string.ascii_uppercase + string.ascii_lowercase + string.digits + __NONASCII, k=length))

def _extend_with_random_to_length(text, length):
    """ Extend a string with random characters up to the given length """
    return text + _random_unicode_string(length - len(text))

def _random_person_name(max_len_per_name):
    """ Create a random person name separated by ^ character """
    return '^'.join([_random_unicode_string(max_len_per_name) for _ in range(1, random.randrange(2, 4))])

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
    def __init__(self, specificCharSet):
        self._specific_charset = specificCharSet

    def get_random_worklist(self):
        """ Generate a random worklist """

        worklist_item = Dataset()
        worklist_item.StudyInstanceUID = generate_uid(prefix='1.2.840.113619.2.391.6789.', entropy_srcs=[_random_unicode_string(10), _random_unicode_string(10)])
        worklist_item.Modality = 'US'
        worklist_item.SpecificCharacterSet = self._specific_charset
        worklist_item.AccessionNumber = _random_unicode_string(16)
        worklist_item.PatientBirthDate = _random_dicom_date_after_1900()
        worklist_item.PatientName = self._get_person_name()
        worklist_item.PatientID = _extend_with_random_to_length('Patient id ', 64)
        worklist_item.IssuerOfPatientID = _extend_with_random_to_length('Issuer of patient id ', 64)
        worklist_item.PatientWeight = str(random.uniform(10.0, 150.0))[:16]
        worklist_item.PatientSize = str(random.uniform(1.0, 2.5))[:16]
        worklist_item.AdmissionID= _extend_with_random_to_length('Admission id ', 64)
        worklist_item.RequestedProcedureID = _extend_with_random_to_length('Step id ', 16)
        worklist_item.RequestedProcedureDescription = _extend_with_random_to_length('Step description ', 64)

        otherPatientIdsSq = [Dataset(), Dataset()]
        for otherPatientId in otherPatientIdsSq:
            otherPatientId.PatientID = _extend_with_random_to_length('Other patient id ', 64)
            otherPatientId.IssuerOfPatientID = _extend_with_random_to_length('Issuer of patient id ', 64)
            otherPatientId.TypeOfPatientID = 'TEXT'

            worklist_item.OtherPatientIDsSequence = otherPatientIdsSq

            step = Dataset()
            step.ScheduledPerformingPhysicianName = self._get_person_name()
            step.ScheduledProcedureStepStartDate = _random_dicom_date_after_1900()
            step.ScheduledProcedureStepStartTime = _random_dicom_time()
            step.ScheduledProcedureStepDescription = _extend_with_random_to_length('Scheduled procedure step desc ', 64)
            step.CommentsOnTheScheduledProcedureStep = _extend_with_random_to_length('Scheduled step comments ', 10240)
            worklist_item.ScheduledProcedureStepSequence = [step]

        yield worklist_item

    def get_clean_worklist(self):
        """ Generates a clean worklist """

        worklist_item = Dataset()
        worklist_item.StudyInstanceUID = generate_uid('1.2.840.113619.2.391.6789.')
        worklist_item.Modality = 'US'
        worklist_item.SpecificCharacterSet = self._specific_charset
        worklist_item.AccessionNumber = _random_unicode_string(16)
        worklist_item.PatientBirthDate = _random_dicom_date_after_1900()
        worklist_item.PatientName = self._get_person_name()
        worklist_item.PatientID = ('Arne ')
        worklist_item.IssuerOfPatientID = _extend_with_random_to_length('Issuer of patient id ', 64)
        worklist_item.PatientWeight = str(random.uniform(10.0, 150.0))[:16]
        worklist_item.PatientSize = str(random.uniform(1.0, 2.5))[:16]
        worklist_item.AdmissionID= _extend_with_random_to_length('Admission id ', 64)
        worklist_item.RequestedProcedureID = _extend_with_random_to_length('Step id ', 16)
        worklist_item.RequestedProcedureDescription = _extend_with_random_to_length('Step description ', 64)

        otherPatientIdsSq = [Dataset(), Dataset()]
        for otherPatientId in otherPatientIdsSq:
            otherPatientId.PatientID = _extend_with_random_to_length('Other patient id ', 64)
            otherPatientId.IssuerOfPatientID = _extend_with_random_to_length('Issuer of patient id ', 64)
            otherPatientId.TypeOfPatientID = 'TEXT'

        worklist_item.OtherPatientIDsSequence = otherPatientIdsSq

        step = Dataset()
        step.ScheduledPerformingPhysicianName = self._get_person_name()
        step.ScheduledProcedureStepStartDate = _random_dicom_date_after_1900()
        step.ScheduledProcedureStepStartTime = _random_dicom_time()
        step.ScheduledProcedureStepDescription = _extend_with_random_to_length('Scheduled procedure step desc ', 64)
        step.CommentsOnTheScheduledProcedureStep = _extend_with_random_to_length('Scheduled step comments ', 10240)
        worklist_item.ScheduledProcedureStepSequence = [step]

        yield worklist_item

    def _get_person_name(self):
        """ Create a random person name and truncate the name components according to Vivid bug """
        return _random_person_name(32)[:_VIVID_HACK_MAX_PERSON_NAME]  # fix for wrong handling in EchoPAC/Scanner
