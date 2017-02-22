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

"""
.. moduleauthor:: Magnus Hagdorn <magnus.hagdorn@ed.ac.uk>

"""

__all__ = ["PiccoloClientError","PiccoloComponentClient","PiccoloBaseClient"]
from piccolo2.PiccoloSpectra import PiccoloSpectraList
from piccolo2.PiccoloStatus import PiccoloStatus

class PiccoloClientError(RuntimeError):
    """
    Piccolo Client Exception
    """
    pass

class PiccoloComponentClient(object):
    """
    piccolo client class used to provide a wrapper for remote piccolo components
    """
    def __init__(self,name,client):
        """initialise component client        

        :param name: the name of the component.
        :param client: PiccoloBaseClient instance used to communicate with the remote piccolo server.
        :type client: PiccoloBaseClient
        """
        assert isinstance(client,PiccoloBaseClient)
        self._name = name
        self._client = client

    def __getattr__(self,attr):
        def func(**keywords):
            return self._client.call(attr,component=self._name,keywords=keywords)
        return func

class PiccoloBaseClient(object):
    """base piccolo client

    queries piccolo server to get a list of components and provides proxy access
    to remote components
    """
    def __init__(self):
        self._components = {}
        self._listenerID = self.call('getListenerID','piccolo')
        for c in self.call('components'):
            self._components[c] = PiccoloComponentClient(c,self)

    def __del__(self):
        self.call('removeListener','piccolo',keywords={"listener":self._listenerID})

    @property
    def listenerID(self):
        return self._listenerID
        
    @property
    def components(self):
        """get list of piccolo remote components"""
        return self._components.keys()

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
        raise NotImplementedError

    def call(self,command,component=None,keywords={}):
        """call a remote procedure and handle status

        :param command: name of remote command
        :type command: str
        :param component: name of remote component
        :type component: str or None
        :param keywords: any keywords to be passed to remote call
        :type keywords: dict

        :return: returns result or raises a PiccoloClientError if the status is *nok*
        
        """
        status,result = self.invoke(command,component,keywords)
        if status!='ok':
            raise PiccoloClientError, result
        if command == 'getSpectra':
            if not isinstance(result,PiccoloSpectraList):
                result = PiccoloSpectraList(data=result)
        elif command == 'status':
            if not isinstance(result,PiccoloStatus):
                result = PiccoloStatus(result)
        return result

    def __getattr__(self,attr):
        if attr in self._components:
            return self._components[attr]
        def func(**keywords):
            return self.call(attr,keywords=keywords)
        return func
