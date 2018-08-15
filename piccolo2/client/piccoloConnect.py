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

__all__ = ["piccoloConnect"]

from PiccoloJSONRPCClient import *
from PiccoloXbeeClient import *
from contextlib import contextmanager

@contextmanager
def piccoloConnect(clientType,address,panid='2525'):

    if clientType == 'xbee':
        piccolo = PiccoloXbeeClient(address,panid=panid)
    elif clientType == 'jsonrpc':
        piccolo = PiccoloJSONRPCClient(address)
    else:
        raise ValueError, 'unkown piccolo client type type %s'%lientType

    piccolo.connect()
    yield piccolo
    piccolo.disconnect()
