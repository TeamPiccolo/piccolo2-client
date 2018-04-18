#!/usr/bin/env python

# This script should be run on the Raspberry Pi. Might need to start it with
# nohup (no hangup).

# Import required Piccolo Client modules.
from piccolo2.client import PiccoloJSONRPCClient

# Import the Raspberry Pi General Purpose Input-Output (GPIO) library
import RPi.GPIO as gpio
# Import Python modules.
import datetime
import argparse
import logging
import time
import sys

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',default=False,help="enable debugging output")
    parser.add_argument('-u','--piccolo-url',metavar='URL',default='http://localhost:8080',help='set the URL of the piccolo server, default http://localhost:8080')
    parser.add_argument('--list-spectrometers','-l',action='store_true',default=False,help="list connected spectormeters and exist")
    parser.add_argument('--auto-integration','-a',type=int,help="determine autointegration time automatically. set to 0 to do so once at the beginning of each batch or to n to rerun after each n sequences.")
    parser.add_argument('--downwelling-integration-time','-D',dest="downwelling",default=[],nargs='*',metavar="NAME:TIME",help="set the downwelling integration time of spectrometer NAME to TIME (in ms)")
    parser.add_argument('--upwelling-integration-time','-U',dest="upwelling",default=[],nargs='*',metavar="NAME:TIME",help="set the upwelling integration time of spectrometer NAME to TIME (in ms)")
    parser.add_argument('-r','--current-run',metavar='RUN',help="set the name of the current run")
    parser.add_argument('-n','--number-sequences',metavar='N',type=int,help="set the number of sequences, default=1")
    parser.add_argument('-d','--delay',type=float,metavar='D',help="delay between measurements in ms, default=0")
    parser.add_argument('-v','--version',action='store_true',default=False,help="print version and exit")

    args = parser.parse_args()

    if args.version:
        from client import __version__
        print __version__
        sys.exit(0)
    
    # Which port is the Pixhawk trigger signal connected to? It should be on GPIO
    # port 12, but can be moved if necessary, Avoid ports 5, 17, 18, 22, 23, 24, 25
    # and 27 as these are used by the Piccolo's shutters and LEDs.
    trigger_port = 12 # Should be on GPIO 12.
    reset_port = 20 # used to reset signal
    

    # Set up logging.
    log = logging.getLogger("piccolo")
    if args.debug:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(name)s: %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)

    # Connect.
    log.info('Running Piccolo Client')
    log.info('Connecting to Piccolo Server %s'%args.piccolo_url)
    piccolo = PiccoloJSONRPCClient(args.piccolo_url)

    # Now need a list of spectrometers. Note that spectrometer "names" are slightly
    # different to their serial numberrs. They generall start with "S_". Example:
    # "S_USB2H16355".
    spectrometers = piccolo.piccolo.getSpectrometerList()
    log.info('Spectrometer names are: {}'.format(', '.join(spectrometers)))
    if args.list_spectrometers:
        for s in spectrometers:
            print s
        sys.exit(0)    

    clock = piccolo.piccolo.getClock()
    log.info('The Piccolo clock is set to: {}'.format(clock))

    if piccolo.piccolo.isMountedDataDir():
        log.info('The data directory is mounted.')
    else:
        log.info('The data directory is not mounted.')


    integrationTimes = {}
    for d in ['downwelling','upwelling']:
        integrationTimes[d] = {}
        for iTime in getattr(args,d):
            tmp = iTime.split(':')
            try:
                s = tmp[0]
                t = float(tmp[1])
            except:
                parser.error("Cannot parse downwelling time %s"%iTime)
            if s not in spectrometers:
                parser.error("Spectrometer %s not in list of spectormeters"%s)
            integrationTimes[d][s] = t
    if len(integrationTimes['downwelling'])>0 or len(integrationTimes['upwelling'])>0:
        log.info('Setting integration times manually...')
        for d in integrationTimes:
            for s in integrationTimes[d]:
                piccolo.piccolo.setIntegrationTimeManual(
                    shutter=d,spectrometer=s,milliseconds=integrationTimes[d][s])

    if args.current_run is not None:
        piccolo.piccolo.setCurrentRun(cr=args.current_run)                
    if args.auto_integration is not None:
        piccolo.piccolo.setAuto(auto=args.auto_integration)
    if args.delay is not None:
        piccolo.piccolo.setDelay(delay=args.delay)
    if args.number_sequences is not None:
        piccolo.piccolo.setNCycles(ncycles=args.number_sequences)

    # log current settings
    for s in spectrometers:
        up = piccolo.piccolo.getIntegrationTime(shutter='upwelling', spectrometer=s)
        down = piccolo.piccolo.getIntegrationTime(shutter='downwelling', spectrometer=s)
        log.info('Spectrometer {}, upwelling {} ms, downwelling {} ms'.format(s, up, down))
    log.info('Autointegration: %d'%piccolo.piccolo.getAuto())
    log.info('Number of Sequences: %d'%piccolo.piccolo.getNCycles())
    log.info('Delay: %f'%piccolo.piccolo.getDelay())
    log.info('Batch Name: %s'%piccolo.piccolo.getCurrentRun())
        
    # Configure the GPIO port to receive a trigger signal from a Pixhawk autopilot.
    log.info('Setting port GPIO %d to receive the trigger...'%trigger_port)
    gpio.setmode(gpio.BCM)
    gpio.setup(trigger_port, gpio.IN)
    gpio.setup(reset_port, gpio.OUT)
    
    if gpio.input(trigger_port):
        # If the trigger signal is high initially this probably indicates an electronics problem. Check the connections. The LED
        log.error('Cannot start Piccolo Client because the Pixhawk trigger signal is active (high). Check that the trigger signal from the Pixhawk is connected and that it is low. The Pixhawk trigger LED should be off.')
        log.info('waiting to reset trigger')
    while gpio.input(trigger_port):
        pass
    log.debug('Finished setting up port ')


    while True: # This is an infinite loop!
        log.info('waiting for trigger')
        try:
            while not gpio.input(trigger_port):
                pass
        except KeyboardInterrupt:
            break
        log.debug('got trigger')

        try:
           status = piccolo.piccolo.status()
        except:
            log.warn('could not get status, trying again')
            continue

        if not status.busy:
            log.info('start recording')
            piccolo.piccolo.record()
           
        time.sleep(0.1)
        # reset trigger board
        gpio.output(reset_port, 1)
        sleep(0.01)
        gpio.output(reset_port, 0)

    log.info('done')
if __name__ == '__main__':
    main()
