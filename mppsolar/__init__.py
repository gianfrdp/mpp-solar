# -*- coding: utf-8 -*-
# !/usr/bin/python
import logging
from argparse import ArgumentParser

# import mppcommands
import mpputils

logger = logging.getLogger()


def main():
    parser = ArgumentParser(description='MPP Solar Command Utility')
    parser.add_argument('-c', '--command', help='Command to run', default='QID')
    parser.add_argument('-ll', '--loglevel',
                        type=str,
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help='Set the logging level')
    parser.add_argument('-d', '--device', type=str, help='Serial device to communicate with', default='/dev/ttyUSB0')
    parser.add_argument('-b', '--baud', type=int, help='Baud rate for serial communications', default=2400)
    parser.add_argument('-l', '--listknown', action='store_true', help='List known commands')
    parser.add_argument('-s', '--getStatus', action='store_true', help='Get Inverter Status')
    parser.add_argument('-t', '--getSettings', action='store_true', help='Get Inverter Settings')
    parser.add_argument('-H', '--makepretty', action='store_true', help='Display result with descriptions etc if possible')
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)

    logging.debug('command %s', args.command)
    logging.debug('Serial device used: %s, baud rate: %d', args.device, args.baud)

    # mp = mppcommands.mppCommands(args.device, args.baud)
    mp = mpputils.mppUtils(args.device, args.baud)

    if(args.listknown):
        for line in mp.getKnownCommands():
            print line
    elif(args.getStatus):
        fullStatus = mp.getFullStatus()
        for key in fullStatus:
            print "{:<30}\t{:<15} {}".format(key, fullStatus[key]['value'], fullStatus[key]['unit'])
    elif(args.getSettings):
        settings = mp.getSettings()
        for key in settings:
            print "{:<30}\t{:<10}\t{:<10} {}".format(key, settings[key]['default'],
                                                     settings[key]['value'],
                                                     settings[key]['unit'])
    else:
        # TODO: check if command is valid
        # maybe check if query or setter and ...
        if(args.makepretty):
            for line in mp.getResponsePretty(args.command):
                print line
        else:
            print mp.getResponse(args.command)
