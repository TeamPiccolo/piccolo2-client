"""
.. moduleauthor:: Magnus Hagdorn <magnus.hagdorn@ed.ac.uk>

"""

__all__ = ["PiccoloClientError","PiccoloComponentClient","PiccoloBaseClient"]

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
        for c in self.call('components'):
            self._components[c] = PiccoloComponentClient(c,self)

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
        return result

    def __getattr__(self,attr):
        if attr in self._components:
            return self._components[attr]
        def func(**keywords):
            return self.call(attr,keywords=keywords)
        return func
