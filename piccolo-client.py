#!/bin/env python

from piccolo_client import PiccoloJSONRPCClient
import datetime

if __name__ == '__main__':
    
    #piccolo = PiccoloJSONRPCClient("http://localhost:8080")
    piccolo = PiccoloJSONRPCClient("http://129.215.6.10:8080")
    
    #if not piccolo.piccolo.isMountedDataDir():
    #    piccolo.piccolo.mountDatadir()

    print piccolo.components
    print piccolo.piccolo.info()
    print piccolo.piccolo.ping()

    at = datetime.datetime.now()+datetime.timedelta(seconds=5)
    end = at+datetime.timedelta(seconds=30)
    print piccolo.piccolo.ping(at_time=at.isoformat(),interval=5.,end_time=end.isoformat())

    print piccolo.piccolo.isMountedDataDir()

    if piccolo.piccolo.isMountedDataDir():
        piccolo.piccolo.umountDatadir()
