# Copyright 2014-2016 The Piccolo Team
#
# This file is part of piccolo2-client.
#
# piccolo2-client is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# piccolo2-client is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with piccolo2-client.  If not, see <http://www.gnu.org/licenses/>.

__all__ = ['PiccoloXbeeClient']

from PiccoloBaseClient import PiccoloBaseClient

from piccolo2.hardware import radio
from piccolo2.PiccoloWorkerThread import PiccoloWorkerThread
from piccolo2.PiccoloSpectra import PiccoloSpectraList
import threading
from Queue import Queue, Empty
import logging

import json
import time
import zlib
import sys

class XbeeClientThread(PiccoloWorkerThread):
    """xbee client thread"""

    LOGNAME = 'xbeeClient'

    def __init__(self,address,panid,spectraCache,busy,tasks,results):
        PiccoloWorkerThread.__init__(self,'xbee',busy,tasks,results)

        self._rd = radio.APIModeRadio(panId=panid)
        self._snr = self._rd.getSerialNumber()
        self._address = address
        self._spectraCache = spectraCache
        self._spectraName = None
        self._spectraChunk = -1
        
    def run(self):
        while True:
            # check if we should be downloading data
            if self._spectraChunk > -1:
                self.log.debug('check if new command is available - otherwise continue downloding data')
                block = False
            else:
                self.log.debug('waiting for new command')
                block = True

            try:
                task = self.tasks.get(block)
            except Empty:
                # no new task so get on with downloading the next chunk
                task = ('getSpectra','piccolo',{'fname':self._spectraName,'chunk':self._spectraChunk})
                
            # see if we got poison pill
            if task == None:
                self.log.info('shutting down')
                return

            command,component,keywords = task

            if command == 'status' and component == 'piccolo' and self._spectraChunk > -1:
                # intercept status query during download
                self.results.put(['ok','downloading data'])
                continue                
            
            if command == 'getSpectra' and keywords['fname'] != self._spectraName:
                self._spectraName = keywords['fname']
                self._spectraChunk = 0
                keywords['chunk'] = 0

            cmd = json.dumps((self._snr,command,component,keywords))

            # send command
            self.busy.acquire()
            self._rd.writeBlock(cmd,self._address)

            # get results
            try:
                result = json.loads(self._rd.readBlock(timeoutInSeconds=10))
            except:
                self.log.error('{0} {1}: {2}'.format(task[1],task[0],sys.exc_info()[1].message))
                result = 'nok',sys.exc_info()[1].message
                self.results.put(result)
                continue


            if command == 'getSpectra':
                if result[0]!='ok':
                    raise RuntimeError, result[1]
                self._spectraCache.setChunk(self._spectraChunk,result[1])
                if self._spectraChunk == 0:
                    # got the first chunk
                    self.results.put(('ok',self._spectraCache))

                self._spectraChunk += 1
                if self._spectraChunk >= self._spectraCache.NCHUNKS:
                    # got the entire file, reset
                    self._spectraChunk = -1
            else:
                # normal command
                self.results.put(result)
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
        self._spectraCache = PiccoloSpectraList()
        self._xbeeWorker = XbeeClientThread(address,panid,self._spectraCache,
                                            self._busy,self._tQ,self._rQ)

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
                return ['ok','communicating']

        self._tQ.put((command,component,keywords))

        return self._rQ.get()
                
