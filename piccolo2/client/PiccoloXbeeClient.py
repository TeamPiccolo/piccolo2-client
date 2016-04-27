__all__ = ['PiccoloXbeeClient']

from PiccoloBaseClient import PiccoloBaseClient

from piccolo2.hardware import radio
import json
import time
import zlib

class PiccoloXbeeClient(PiccoloBaseClient):
    """communication via radio link"""

    CHUNK = 100
    
    def __init__(self,address,panid='2525'):
        """
        :param address: the address of the remote server
        :param panid: the panid"""

        self._rd = radio.APIModeRadio(panId=panid)
        self._snr = self._rd.getSerialNumber()
        self._address = address
        PiccoloBaseClient.__init__(self)

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

        cmd = json.dumps((self._snr,command,component,keywords))
        l = len(cmd)
        n = l//self.CHUNK+1
        for i in range(0,n):
            s = i*self.CHUNK
            e = min((i+1)*self.CHUNK,l)
            self._rd.writeline(cmd[s:e],self._address)
            time.sleep(0.1)
        self._rd.writeline('ok',self._address)
            
        result = ''
        res = 'nok'
        while res!='ok':
            res = self._rd.readline()
            time.sleep(0.1)
            if res=='ok':
                break
            result += res
        
        return json.loads(result)
