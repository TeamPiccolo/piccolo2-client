__all__ = ["PiccoloBaseClient"]

class PiccoloClientError(RuntimeError):
    pass

class PiccoloComponentClient(object):
    def __init__(self,name,client):
        assert isinstance(client,PiccoloBaseClient)
        self._name = name
        self._client = client

    def __getattr__(self,attr):
        def func(**keywords):
            return self._client.call(attr,component=self._name,keywords=keywords)
        return func

class PiccoloBaseClient(object):
    def __init__(self):
        self._components = {}
        for c in self.call('components'):
            self._components[c] = PiccoloComponentClient(c,self)

    @property
    def components(self):
        return self._components.keys()

    def invoke(self,command,component=None,keywords={}):
        raise NotImplementedError

    def call(self,command,component=None,keywords={}):
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
