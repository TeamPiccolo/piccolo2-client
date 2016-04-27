#!/bin/env python

from piccolo2.client import PiccoloJSONRPCClient, PiccoloXbeeClient
import datetime
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-u','--piccolo-url',metavar='URL',default='http://localhost:8080',help='set the URL of the piccolo server, default http://localhost:8080')
    parser.add_argument('-x','--xbee-address',metavar='ADR',help="xbee address")
    args = parser.parse_args()

    if args.xbee_address!=None:
        piccolo = PiccoloXbeeClient(args.xbee_address)
    else:    
        piccolo = PiccoloJSONRPCClient(args.piccolo_url)
    
    #if not piccolo.piccolo.isMountedDataDir():
    #    piccolo.piccolo.mountDatadir()

    print piccolo.components
    print piccolo.piccolo.info()
    print piccolo.piccolo.ping()

    print 'njobs',piccolo.scheduler.njobs()

    at = datetime.datetime.now()+datetime.timedelta(seconds=5)
    end = at+datetime.timedelta(seconds=30)
    print piccolo.piccolo.ping(at_time=at.isoformat(),interval=5.,end_time=end.isoformat())

    print 'njobs',piccolo.scheduler.njobs()
    print piccolo.scheduler.getJob(jid=0)

    #print piccolo.piccolo.getClock()
    #print piccolo.piccolo.setClock(clock='2017-10-2')

    print piccolo.piccolo.isMountedDataDir()

    #piccolo.upwelling.open_close(milliseconds=3000)
    #piccolo.downwelling.open_close(milliseconds=3000)
    #print piccolo.upwelling.info()

    piccolo.piccolo.setIntegrationTime(shutter='downwelling',spectrometer='test1',milliseconds=2000)
    piccolo.piccolo.setIntegrationTime(shutter='downwelling',spectrometer='test3',milliseconds=3000)

    piccolo.piccolo.record(delay=5,nCycles=5)
    
    at = datetime.datetime.now()+datetime.timedelta(seconds=120)
    piccolo.piccolo.record(delay=5,nCycles=2,at_time=at.isoformat())
    

    #if piccolo.piccolo.isMountedDataDir():
    #    piccolo.piccolo.umountDatadir()
