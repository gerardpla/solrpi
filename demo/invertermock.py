# Copyright 2023 Gérard Plangger
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.

from solrpi.i_inverter import Inverter

# grid, pv
watt_demo = [
    [-4000, 4400],
    [-600, 4400],
    [1200, 2600],
    [2800, 1000],
    [-1400, 4400],
    [-3400, 4400],
    [-700, 1300],
    [5000, 1300],
    [8000, 1300],
    [8000, 8000],
    [3400, 1300],
    [1300, 4400]
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
    