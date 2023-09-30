# Copyright 2023 Gérard Plangger
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.

from solrpi import ledmatrix

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
