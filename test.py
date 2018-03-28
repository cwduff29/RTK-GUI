# Copyright (C) 2015 Swift Navigation Inc.
# Contact: Fergus Noble <fergus@swiftnav.com>
#
# This source is subject to the license found in the file 'LICENSE' which must
# be be distributed together with this source. All other rights reserved.
#
# THIS CODE AND INFORMATION IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND,
# EITHER EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND/OR FITNESS FOR A PARTICULAR PURPOSE.
"""
the :mod:`sbp.client.examples.simple` module contains a basic example of
reading SBP messages from a serial port, decoding BASELINE_NED messages and
printing them out.
"""

from sbp.client.drivers.pyserial_driver import PySerialDriver
from sbp.client import Handler, Framer
from sbp.client.loggers.json_logger import JSONLogger
from sbp.system import SBP_MSG_STARTUP, MsgStartup
from sbp.navigation import *
from sbp.observation import *
import argparse
import time
import csv

DEFAULT_LOG_FILENAME=time.strftime("sbp-%Y%m%d-%H%M%S.log")

def main():
    parser = argparse.ArgumentParser(
        description="Swift Navigation SBP Example.")
    parser.add_argument(
        "-p",
        "--port",
        default=['/dev/ttyUSB0'],
        nargs=1,
        help="specify the serial port to use.")
    parser.add_argument(
	"-b",
	"--baud",
	default=[115200],
	nargs=1,
	help="specify the baud rate")
    parser.add_argument(
	"-f",
	"--filename",
	default=[DEFAULT_LOG_FILENAME],
	nargs=1,
	help="specify the name of the log file")
    args = parser.parse_args()

    # Open a connection to Piksi using the default baud rate (1Mbaud)
    with PySerialDriver(args.port[0], args.baud[0]) as driver:
        with Handler(Framer(driver.read, None, verbose=True)) as source:
          try:
	        for msg, metadata in source.filter(SBP_MSG_POS_LLH):
              # Print out the N, E, D coordinates of the baseline
                  print "%.4f,%.4f,%.4f" % (msg.lat, msg.lon, msg.height)
		  # data = msg.lat
		  # print data
          except KeyboardInterrupt:
             pass


if __name__ == "__main__":
    main()

