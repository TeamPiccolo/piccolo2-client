#!/bin/env python

from piccolo_client import PiccoloJSONRPCClient

if __name__ == '__main__':
    
    piccolo = PiccoloJSONRPCClient("http://localhost:8080")
    
    print piccolo.components
    print piccolo.piccolo.info()
    
