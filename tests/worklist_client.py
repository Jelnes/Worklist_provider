from pynetdicom import AE
from pynetdicom.sop_class import ModalityWorklistInformationFind

class WorklistClient:
    """ Worklist client used to test the server"""

    def __init__(self, serveraddress):
        self._ae = AE()
        self._ae.add_requested_context(ModalityWorklistInformationFind)
        self._ae.acse_timeout = 3600
        self._serveraddress = serveraddress

    def get_worklist(self, query_dataset):
        """ Fetch worklist from server, and return as PyDicom dataset """
        assoc = self._ae.associate(self._serveraddress.address, self._serveraddress.port)
        if not assoc.is_established:
            raise Exception('Association rejected, aborted or never connected')

        worklist = []
        for (status, item) in assoc.send_c_find(query_dataset, ModalityWorklistInformationFind):
            if not status:
                print('Connection timed out, was aborted or received invalid response')
            elif status.Status == 0xFF00: # Matches are continuing
                worklist.append(item)
            elif status.Status != 0x0000: # Anything except Success
                raise Exception("Got unexpected status from worklist server")
        assoc.release()
        return worklist
