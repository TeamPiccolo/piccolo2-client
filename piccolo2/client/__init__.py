"""piccolo client module

.. moduleauthor: Magnus Hagdorn <magnus.hagdorn@ed.ac.uk>

Example
-------
connect to piccolo server running on localhost
 >>> piccolo = PiccoloJSONRPCClient("http://localhost:8080")
get the list of components
 >>> print piccolo.components
execute the info method of the piccolo component
 >>> print piccolo.piccolo.info()

"""
from piccolo2.PiccoloSpectra import *
from PiccoloBaseClient import *
from PiccoloJSONRPCClient import *
from PiccoloXbeeClient import *
