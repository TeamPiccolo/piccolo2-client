__all__ = ['PiccoloJSONRPCClient']

from PiccoloBaseClient import PiccoloBaseClient

import pyjsonrpc

class PiccoloJSONRPCClient(PiccoloBaseClient):
    def __init__(self,url):
        self._http_client = pyjsonrpc.HttpClient(url=url)
        PiccoloBaseClient.__init__(self)

    def invoke(self,command,component=None,keywords={}):
        return self._http_client.call('invoke',command,component=component,keywords=keywords)
        
