#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# NeoPixel display for SolarManager, running on a RaspberryPi
# Copyright 2023 Gérard Plangger
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
import logging
from solrpi.renderer import Renderer
import signal
import sys
from solrpi.fronius_inverter import FroniusInverter
from solrpi.neopixel import NeoPixel

logging.basicConfig(
	filename='/var/log/solrpi.log',
	level=logging.WARN,
	format='%(asctime)s - %(threadName)s - %(levelname)s - %(name)s - %(message)s')

renderer_obj = None

def sigterm_handler(_signo, _stack_frame):
    if renderer_obj: renderer_obj.clear()
    sys.exit(0) # raise SystemExit(0)

def main():
	inverter = FroniusInverter()
	uidevice = NeoPixel()
	renderer = Renderer(inverter, uidevice)
	global renderer_obj
	renderer_obj = renderer
	signal.signal(signal.SIGTERM, sigterm_handler)
	
	try:
		renderer.run()

	finally:
		if renderer: renderer.clear()
		logging.warn("Stopping solrpi")


# Main
if __name__ == '__main__':
	logging.info("Starting up solrpi")
	main()
