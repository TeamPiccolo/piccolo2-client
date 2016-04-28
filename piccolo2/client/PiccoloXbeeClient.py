__all__ = ['PiccoloXbeeClient']

from PiccoloBaseClient import PiccoloBaseClient

from piccolo2.hardware import radio
from piccolo2.PiccoloWorkerThread import PiccoloWorkerThread
import threading
from Queue import Queue
import logging

import json
import time
import zlib

class XbeeClientThread(PiccoloWorkerThread):
    """xbee client thread"""

    LOGNAME = 'xbeeClient'

    def __init__(self,address,panid,busy,tasks,results):
        PiccoloWorkerThread.__init__(self,'xbee',busy,tasks,results)

        self._rd = radio.APIModeRadio(panId=panid)
        self._snr = self._rd.getSerialNumber()
        self._address = address
        
    def run(self):
        while True:
            # wait for a new task from the task queue
            task = self.tasks.get()
            if task == None:
                self.log.info('shutting down')
                return
            else:
                command,component,keywords = task
                cmd = json.dumps((self._snr,command,component,keywords))

                self.busy.acquire()
                self._rd.writeBlock(cmd,self._address)

                result = self._rd.readBlock()
                self.results.put(json.loads(result))
                self.busy.release()
                
class PiccoloXbeeClient(PiccoloBaseClient):
    """communication via radio link"""

    def __init__(self,address,panid='2525'):
        """
        :param address: the address of the remote server
        :param panid: the panid"""

        
        self._busy = threading.Lock()
        self._tQ = Queue()
        self._rQ = Queue()
        self._xbeeWorker = XbeeClientThread(address,panid,self._busy,self._tQ,self._rQ)

        self._xbeeWorker.start()
        PiccoloBaseClient.__init__(self)
        

    def __del__(self):
        # send poison pill to worker
        self._tQ.put(None)
        #PiccoloBaseClient.__del__()

    def invoke(self,command,component=None,keywords={}):
        """method used to call remote procedures
        
        :param command: name of remote command
        :type command: str
        :param component: name of remote component
        :type component: str or None
        :param keywords: any keywords to be passed to remote call
        :type keywords: dict

        :return: returns status and result. status is either *ok* or *nok*
        :rtype: (str,obj)
        """

        if command == 'status' and component == 'piccolo':
            # catch the status command and divert if xbee is busy
            if self._busy.locked():
                return 'communicating'

        self._tQ.put((command,component,keywords))

        return self._rQ.get()
                
