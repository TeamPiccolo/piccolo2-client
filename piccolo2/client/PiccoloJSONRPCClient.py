__all__ = ['PiccoloJSONRPCClient']

from PiccoloBaseClient import PiccoloBaseClient

import pyjsonrpc

class PiccoloJSONRPCClient(PiccoloBaseClient):
    """JSON RPC based piccolo client"""
    def __init__(self,url):
        """
        :param url: URL of piccolo server
        :type url: str
        """
        self._http_client = pyjsonrpc.HttpClient(url=url)
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
        return self._http_client.call('invoke',command,component=component,keywords=keywords)
        
