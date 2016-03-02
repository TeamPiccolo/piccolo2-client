#!/bin/env python

from piccolo_client import PiccoloJSONRPCClient
import datetime
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-u','--piccolo-url',metavar='URL',default='http://localhost:8080',help='set the URL of the piccolo server, default http://localhost:8080')
    args = parser.parse_args()
    
    piccolo = PiccoloJSONRPCClient(args.piccolo_url)
    
    print piccolo.components
    print piccolo.piccolo.info()
    print piccolo.piccolo.ping()

    at = datetime.datetime.now()+datetime.timedelta(seconds=5)
    end = at+datetime.timedelta(seconds=30)
    print piccolo.piccolo.ping(at_time=at.isoformat(),interval=5.,end_time=end.isoformat())
