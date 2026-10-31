# Copyright 2023 Gérard Plangger
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.

from solrpi.i_inverter import Inverter

# grid, pv, battery
# comments describe the display from left to right: 
#   import, battery discharge, self-consumption, battery charge, export
watt_demo = [
    [-4000, 4400, 0], # self-consumption, mostly export (px: 2, 20)
    [-1200, 4400, -2400], # self-consumption, battery charge, export (px: 4, 12, 6)
    [0, 4400, -4400], # battery charge only (px: 22)
    [1000, 0, 1600], # import, battery discharge (px: 5, 8)
    [0, 400, 1200], # battery discharge, self-consumption (px: 6, 2)
    [0, 1200, -400], # self-consumption, battery charge (px: 4, 2)
    [1500, 2000, 2000], # high load: import, battery discharge, self-consumption (px: 8, 10, 10)
    [1500, 500, -2000], # import, battery charge; only the PV share of charging is shown as charge (px: 8, 2)
    [1200, 2600, 400], # import, small battery discharge, mostly self-consumption (px: 6, 2, 13)
    [1200, 2600, -400], # (unrealistic) import, mostly self-consumption, small battery charge (px: 6, 11, 2)
    [1200, 600, 400], # mostly import, battery discharge, self-consumption (px: 6, 2, 3)
    [1200, 600, -400], # (unrealistic) mostly import, little self-consumption, battery charge (px: 6, 1, 2)
    [-1200, 2600, 400], # (unrealistic) battery discharge, self-consumption, export (px: 2, 7, 6)
    [-400, 2600, -1000], # self-consumption, battery charge, small export (px: 6, 5, 2)
    [-200, 600, 400], # (unrealistic) battery discharge, self-consumption, small export (px: 2, 2, 1)
    [-200, 1200, -1000], # mostly battery charge, small export (px: 5, 1)
    [-600, 4400, 0], # mostly self-consumption, small export (px: 19, 3)
    [1200, 2600, 0], # import, mostly self-consumption (px: 6, 13)
    [2800, 1000, 0], # mostly import, some self-consumption (px: 14, 5)
    [-1400, 4400, 0], # self-consumption, export (px: 15, 7)
    [-3400, 4400, 0], # little self-consumption, mostly export (px: 5, 17)
    [-700, 1300, 0], # low PV: self-consumption, export (px: 3, 3)
    [5000, 1300, 0], # mostly import, some self-consumption (px: 25, 7)
    [8000, 1300, 0], # import exceeding display (all red) (px: 32)
    [8000, 8000, 0], # import and PV exceeding display (all red) (px: 32)
    [3400, 1300, 0], # import, self-consumption (px: 17, 7)
    [1300, 4400, 0] # import, mostly self-consumption (px: 6, 22)
]

class InverterMock(Inverter):

    def __init__(self):
        self.counter = 0
        self.delay_count = 0

    def get_watt(self):
        if self.counter >= len(watt_demo):
            self.counter = 0

        # display the same entry 3 times before proceeding to the next one
        if self.delay_count < 2:
            self.delay_count += 1
            return watt_demo[self.counter]        
        self.delay_count = 0

        retval = watt_demo[self.counter]
        self.counter += 1
        return retval
    