# Copyright 2023 Gérard Plangger
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.

# interface for inverters
class Inverter:
    # get_watt() returns array with three values: grid, pv, battery (unit [Watt])
    # pv is always positive
    # grid<0 == pv into grid; grid>0 == grid consumption
    # battery<0 == battery charging; battery>0 == battery discharging; 0 if no battery
    # (implementations returning only grid, pv are treated as having no battery)
    # raises an exception in case of error
    def get_watt(self):
        pass