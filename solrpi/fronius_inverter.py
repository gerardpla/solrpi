# Copyright 2023 Gérard Plangger
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Fronius inverter class

import requests
import json
import logging
from solrpi.i_inverter import Inverter

FRONIUS_URL = 'http://192.168.50.90/solar_api/v1/GetPowerFlowRealtimeData.fcgi'

logger = logging.getLogger(__name__)

# Returns array with two values: grid, pv (unit [Watt]). 
# See i_inverter.py
class FroniusInverter(Inverter):

    def __init__(self, url: str = FRONIUS_URL):
        self.url = url

    def get_watt(self):
        try:
            response = requests.get(self.url)
            content = json.loads(response.text)
            grid = (content["Body"]["Data"]["Site"]["P_Grid"])
            pv = (content["Body"]["Data"]["Site"]["P_PV"])
            #battery = (content["Body"]["Data"]["Site"]["P_Akku"])
            logger.debug("grid={}, pv={}".format(grid, pv))
            return [grid, pv]
        except requests.exceptions.RequestException as err:
            logger.error("An error occurred reading Fronius at URL '{}'. Will keep trying. Error: '{}'", self.url, err)
            return [0, 0]
