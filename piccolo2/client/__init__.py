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

from pkg_resources import get_distribution, DistributionNotFound
try:
    __version__ = get_distribution('piccolo2-client').version
except DistributionNotFound:
    # package is not installed
    pass

from piccolo2.PiccoloSpectra import *
from PiccoloBaseClient import *
from PiccoloJSONRPCClient import *
from PiccoloXbeeClient import *
