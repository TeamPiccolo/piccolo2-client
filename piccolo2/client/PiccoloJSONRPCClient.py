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
        self._url = url
        PiccoloBaseClient.__init__(self)

    def connect(self):
        self._http_client = pyjsonrpc.HttpClient(url=self._url)
        PiccoloBaseClient.connect(self)
        
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
        
