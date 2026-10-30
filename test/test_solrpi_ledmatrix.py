# Copyright 2023 Gérard Plangger
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.

from solrpi import ledmatrix

# 
def test_idxs_comparison():
    idxs1 = ledmatrix.compute_idxs(200, 400)
    idxs2 = ledmatrix.compute_idxs(200, 400)
    idxs3 = ledmatrix.compute_idxs(200, 1000)
    assert idxs1 == idxs2
    assert idxs1 != idxs3
    idxs2.pv += 1
    assert idxs1 != idxs2

def test_compute_idxs_grid_only():
    idxs = ledmatrix.compute_idxs(1800, 0)
    assert idxs.consume == 0
    assert idxs.grid == round(1800 / ledmatrix.WATT_PER_PIXEL)
    assert idxs.pv == idxs.grid

def test_compute_idxs_self_consumption_only():
    idxs = ledmatrix.compute_idxs(0, 1800)
    assert idxs.consume == round(1800 / ledmatrix.WATT_PER_PIXEL)
    assert idxs.grid == idxs.consume
    assert idxs.pv == idxs.grid

def test_compute_idxs_pv_only():
    idxs = ledmatrix.compute_idxs(-1800, 1800)
    assert idxs.consume == 0
    assert idxs.grid == 0
    assert idxs.pv == round(1800 / ledmatrix.WATT_PER_PIXEL)

def test_compute_idxs_zero():
    idxs = ledmatrix.compute_idxs(0, 0)
    assert idxs.consume == 0
    assert idxs.grid == 0
    assert idxs.pv == 0

def test_compute_idxs_max():
    idxs = ledmatrix.compute_idxs(30000, 0)
    assert idxs.consume == 0
    assert idxs.grid == ledmatrix.NUM_PIXELS
    assert idxs.pv == idxs.pv

def test_transition_pv_down():
    from_idxs = ledmatrix.compute_idxs(2000, 0)
    to_idxs = ledmatrix.compute_idxs(0, 0)
    transition_idxs = ledmatrix.transition_step(from_idxs, to_idxs)
    assert transition_idxs.grid == from_idxs.grid-1

def test_transition_pv_up():
    from_idxs = ledmatrix.compute_idxs(0, 0)
    to_idxs = ledmatrix.compute_idxs(2000, 0)
    transition_idxs = ledmatrix.transition_step(from_idxs, to_idxs)
    assert transition_idxs.grid == from_idxs.grid+1

def test_transition_combined():
    from_idxs = ledmatrix.compute_idxs(-2000, 2000) # pv only
    to_idxs = ledmatrix.compute_idxs(0, 1000) # self consumption only
    transition_idxs = ledmatrix.transition_step(from_idxs, to_idxs)
    assert transition_idxs.consume == from_idxs.consume+1
    assert transition_idxs.grid == from_idxs.grid+1
    assert transition_idxs.pv == from_idxs.pv-1

def test_render_grid_only():
    idxs = ledmatrix.compute_idxs(1800, 0)
    matrix = ledmatrix.render(idxs)
    print(matrix)

    assert matrix[0][0] == ledmatrix.PIX_GRID
    assert matrix[3][0] == ledmatrix.PIX_EMPTY

def test_render_snake():
    idxs = ledmatrix.compute_idxs(-500, 1800)
    matrix = ledmatrix.render(idxs)
    print(matrix)

    assert matrix[0][0] == ledmatrix.PIX_CONSUME
    assert matrix[1][0] == ledmatrix.PIX_PV
    assert matrix[1][3] == ledmatrix.PIX_CONSUME
    assert matrix[2][0] == ledmatrix.PIX_PV
    assert matrix[2][3] == ledmatrix.PIX_EMPTY

def test_render_grid_with_pv():
    idxs = ledmatrix.compute_idxs(1800, 500)
    matrix = ledmatrix.render(idxs)
    print(matrix)

    assert matrix[0][0] == ledmatrix.PIX_CONSUME
    assert matrix[2][3] == ledmatrix.PIX_GRID
    assert matrix[3][0] == ledmatrix.PIX_EMPTY

def test_brightness():
    idxs = ledmatrix.compute_idxs(1800, 200)
    brightness = ledmatrix.compute_brightness(idxs)
    assert brightness == ledmatrix.BRIGHTNESS_DAY

    idxs = ledmatrix.compute_idxs(-200, 4000)
    brightness = ledmatrix.compute_brightness(idxs)
    assert brightness == ledmatrix.BRIGHTNESS_SUN

def test_compute_idxs_battery_charge_with_export():
    idxs = ledmatrix.compute_idxs(-1200, 4400, -2400)
    assert idxs.consume == round(800 / ledmatrix.WATT_PER_PIXEL)
    assert idxs.discharge == idxs.consume
    assert idxs.charge == round(3200 / ledmatrix.WATT_PER_PIXEL)
    assert idxs.grid == idxs.charge
    assert idxs.pv == round(4400 / ledmatrix.WATT_PER_PIXEL)

def test_compute_idxs_battery_discharge_with_grid():
    idxs = ledmatrix.compute_idxs(800, 400, 1600)
    assert idxs.consume == round(400 / ledmatrix.WATT_PER_PIXEL)
    assert idxs.discharge == round(2000 / ledmatrix.WATT_PER_PIXEL)
    assert idxs.charge == idxs.discharge
    assert idxs.grid == round(2800 / ledmatrix.WATT_PER_PIXEL)
    assert idxs.pv == idxs.grid

def test_compute_idxs_battery_charge_from_grid():
    # charging from PV and grid: only the PV part is shown as charge, the rest as grid import
    idxs = ledmatrix.compute_idxs(1400, 600, -2000)
    assert idxs.consume == 0
    assert idxs.discharge == 0
    assert idxs.charge == round(600 / ledmatrix.WATT_PER_PIXEL)
    assert idxs.grid == round(2000 / ledmatrix.WATT_PER_PIXEL)
    assert idxs.pv == idxs.grid

def test_compute_idxs_battery_zero_unchanged():
    assert ledmatrix.compute_idxs(-500, 1800, 0) == ledmatrix.compute_idxs(-500, 1800)
    assert ledmatrix.compute_idxs(1800, 500, 0) == ledmatrix.compute_idxs(1800, 500)

def test_transition_battery():
    from_idxs = ledmatrix.compute_idxs(0, 0, 0)
    to_idxs = ledmatrix.compute_idxs(0, 0, 2000) # battery discharge only
    transition_idxs = ledmatrix.transition_step(from_idxs, to_idxs)
    assert transition_idxs.discharge == from_idxs.discharge+1
    assert transition_idxs.charge == from_idxs.charge+1

def test_render_battery_charge():
    idxs = ledmatrix.compute_idxs(-1200, 4400, -2400)
    matrix = ledmatrix.render(idxs)
    print(matrix)

    assert matrix[0][0] == ledmatrix.PIX_CONSUME
    assert matrix[1][0] == ledmatrix.PIX_CHARGE
    assert matrix[3][0] == ledmatrix.PIX_CHARGE
    assert matrix[4][0] == ledmatrix.PIX_PV
    assert matrix[5][3] == ledmatrix.PIX_PV
    assert matrix[5][0] == ledmatrix.PIX_EMPTY

def test_render_battery_discharge():
    idxs = ledmatrix.compute_idxs(800, 400, 1600)
    matrix = ledmatrix.render(idxs)
    print(matrix)

    assert matrix[0][0] == ledmatrix.PIX_CONSUME
    assert matrix[0][3] == ledmatrix.PIX_DISCHARGE
    assert matrix[2][0] == ledmatrix.PIX_DISCHARGE
    assert matrix[2][3] == ledmatrix.PIX_GRID
    assert matrix[3][3] == ledmatrix.PIX_GRID
    assert matrix[3][0] == ledmatrix.PIX_EMPTY

def test_brightness_battery_charge():
    idxs = ledmatrix.compute_idxs(0, 4000, -4000)
    assert ledmatrix.compute_brightness(idxs) == ledmatrix.BRIGHTNESS_SUN
