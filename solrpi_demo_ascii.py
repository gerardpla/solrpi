#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# NeoPixel display for SolarManager, running on a RaspberryPi
# Copyright 2023 Gérard Plangger
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.

import logging

from solrpi.renderer import Renderer
from demo.invertermock import InverterMock
from demo.asciiui import AsciiUI

logging.basicConfig(
	filename='./solrpi.log',
	level=logging.DEBUG,
	format='%(asctime)s - %(threadName)s - %(levelname)s - %(name)s - %(message)s')

def main():
	inverter = InverterMock()
	uidevice = AsciiUI()
	renderer = Renderer(inverter, uidevice)

	try:
		renderer.run()

	finally:
		if renderer: renderer.clear()
		print("END")

# Main
if __name__ == '__main__':
	print("BEGIN")
	main()
