#!/bin/env python

from piccolo2.client import PiccoloJSONRPCClient, PiccoloXbeeClient
import datetime
import argparse
import logging
import time

if __name__ == '__main__':

    log = logging.getLogger("piccolo")
    log.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(name)s: %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)

    parser = argparse.ArgumentParser()
    parser.add_argument('-u','--piccolo-url',metavar='URL',default='http://localhost:8080',help='set the URL of the piccolo server, default http://localhost:8080')
    parser.add_argument('-x','--xbee-address',metavar='ADR',help="xbee address")
    parser.add_argument('-d','--download-spectra',type=int,metavar='ID',help="download set of spectra with ID")
    args = parser.parse_args()

    if args.xbee_address!=None:
        piccolo = PiccoloXbeeClient(args.xbee_address)
    else:    
        piccolo = PiccoloJSONRPCClient(args.piccolo_url)
    
    #if not piccolo.piccolo.isMountedDataDir():
    #    piccolo.piccolo.mountDatadir()

    if args.download_spectra != None:
        spectraList = piccolo.piccolo.getSpectraList()
        spectra = piccolo.piccolo.getSpectra(fname=spectraList[0])
        n = -1
        while not spectra.complete:
            if n!=spectra.chunk:
                n = spectra.chunk
                print spectra.chunk,spectra.NCHUNKS
        print 'done'
        print len(spectra)
    else:
    
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
