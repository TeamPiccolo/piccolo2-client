# Copyright 2014-2016 The Piccolo Team
#
# This file is part of piccolo2-server.
#
# piccolo2-server is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# piccolo2-server is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with piccolo2-server.  If not, see <http://www.gnu.org/licenses/>.

from client import piccoloConnect
import datetime
import argparse
import logging
import time
import sys

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-u','--piccolo-url',metavar='URL',default='http://localhost:8080',help='set the URL of the piccolo server, default http://localhost:8080')
    group.add_argument('-x','--xbee-address',metavar='ADR',help="the address of the xbee radio")
    parser.add_argument('--debug', action='store_true',default=False,help="enable debugging output")
    parser.add_argument('-n','--number-cycles',metavar='N',type=int,default=1,help="set the number of cycles, default=1")
    parser.add_argument('-d','--delay',type=float,metavar='D',default=0.,help="delay between measurements in ms, default=0")
    parser.add_argument('-v','--version',action='store_true',default=False,help="print version and exit")

    args = parser.parse_args()

    if args.version:
        from client import __version__
        print __version__
        sys.exit(0)
    
    log = logging.getLogger("piccolo")
    if args.debug:
        log.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(name)s: %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)
    
    if args.xbee_address != None:
        ctype = 'xbee'
        pargs = args.xbee_address
    else:
        ctype = 'jsonrpc'
        pargs = args.piccolo_url

    with piccoloConnect(ctype,pargs) as piccolo:
        piccolo.piccolo.record(delay=args.delay,nCycles=args.number_cycles)

if __name__ == '__main__':
    main()
