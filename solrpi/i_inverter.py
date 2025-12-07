# Copyright 2023 Gérard Plangger
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.

# interface for inverters
class Inverter:
    # get_watt() returns array with two values: grid, pv (unit [Watt])
    # pv is always positive
    # grid<0 == pv into grid; grid>0 == grid consumption
    # raises an exception in case of error
    def get_watt(self):
        pass