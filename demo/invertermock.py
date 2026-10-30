# Copyright 2023 Gérard Plangger
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.

from solrpi.i_inverter import Inverter

# grid, pv, battery
watt_demo = [
    [-4000, 4400, 0],
    [-600, 4400, 0],
    [1200, 2600, 0],
    [2800, 1000, 0],
    [-1400, 4400, 0],
    [-3400, 4400, 0],
    [-700, 1300, 0],
    [5000, 1300, 0],
    [8000, 1300, 0],
    [8000, 8000, 0],
    [3400, 1300, 0],
    [1300, 4400, 0],
    [-1200, 4400, -2400], # charging battery and export to grid
    [0, 4400, -3600], # charging battery only
    [800, 0, 1600], # battery discharge and grid import
    [0, 400, 1200], # battery discharge only
    [0, 1200, -400], # charging battery with small PV surplus
    [1500, 2000, 2000], # high load: PV, battery discharge and grid import
    [1500, 500, -2000] # charging battery from PV and grid
]

class InverterMock(Inverter):

    def __init__(self):
        self.counter = 0

    def get_watt(self):
        if self.counter >= len(watt_demo):
            self.counter = 0
        retval = watt_demo[self.counter]
        self.counter += 1
        return retval
    