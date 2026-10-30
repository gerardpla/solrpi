# Copyright 2023 Gérard Plangger
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.

import logging
from dataclasses import dataclass

WIDTH = 4
HEIGHT = 8
NUM_PIXELS = WIDTH * HEIGHT
MAX_WATT = 6400
WATT_PER_PIXEL = MAX_WATT / NUM_PIXELS

PIX_EMPTY = 0
PIX_GRID = 1
PIX_CONSUME = 2 # PV self-consumption
PIX_PV = 3
PIX_DISCHARGE = 4 # battery discharge
PIX_CHARGE = 5 # battery charge

# brightness values according to rpi_ws281x
BRIGHTNESS_DAY = 5
BRIGHTNESS_SUN = 10

logger = logging.getLogger(__name__)

# Class for index positions.
# Note that comparing objects compares all individual attributes, see test_solrpi_ledmatrix.test_idxs_comparison
@dataclass
class Idxs:
    # Note that the values are relative indexes, not absolute consumption values!
    # Each value is the end index of its layer, layers are stacked bottom to top in this order,
    # so consume <= discharge <= charge <= grid <= pv
    consume: int
    discharge: int
    charge: int
    grid: int
    pv: int

    def __init__(self, consume: int=0, discharge: int=0, charge: int=0, grid: int=0, pv: int=0):
        self.consume = consume
        self.discharge = discharge
        self.charge = charge
        self.grid = grid
        self.pv = pv


def compute_brightness(idxs: Idxs):
	if (idxs.consume > 3) or (idxs.pv - idxs.grid > 3) or (idxs.charge - idxs.discharge > 3): # at least three pixels PV (self-consumption, export or battery charge)
		return BRIGHTNESS_SUN
	return BRIGHTNESS_DAY

# We build from bottom to top, snake-wise to cluster equally-colored pixels,
# this prevents orphaned color-pixels.
# So instead of:
#
#  Y . . .
#  B B Y Y
#
# We rather do:
#
#  . . . Y
#  B B Y Y
def _set_matrix_color(matrix, startidx: int, endidx: int, color):
    logger.debug(f"_set_matrix_color(matrix={matrix}, startidx={startidx}, endix={endidx}, color={color})")
    for i in range(startidx, endidx):
        # matrix[row (max=HEIGHT)][col (max=WIDTH)]
        # for the width index, we go left to right on even length index
        # and right to left on uneven length index
        row = i // WIDTH
        col = i % WIDTH
        if row % 2 == 1: # uneven row -> inverse column index
            col = (WIDTH-1) - col
        matrix[row][col] = color

def _watt_to_idx(watt: float) -> int:
    return min(round(watt / WATT_PER_PIXEL), NUM_PIXELS)

# input parameters grid, pv, battery; represented Watt, grid and battery can be negative
# (grid<0: Rückspeisung ins Netz, battery<0: Laden der Batterie, see i_inverter.py)
# returns the end indexes of the layers, see Idxs
def compute_idxs(grid: float, pv: float, battery: float = 0) -> Idxs:
    logger.info("grid={}, pv={}, battery={}".format(grid, pv, battery))

    netzbezug = max(grid, 0)
    rueckspeisung = max(-grid, 0)
    entladen = max(battery, 0)
    laden = max(-battery, 0)

    # Gesamthöhe = alle Quellen: PV + Netzbezug + Batterie-Entladung
    gesamt = pv + netzbezug + entladen

    # Nur der Anteil Laden aus PV wird als Laden angezeigt, Laden aus dem Netz bleibt Netzbezug
    laden_pv = min(laden, max(pv - rueckspeisung, 0))

    # Layer 1) Eigenverbrauch = PV abzüglich Laden und Rückspeisung
    eigenverbrauch = max(pv - laden_pv - rueckspeisung, 0)
    # Layer 2) Batterie-Entladung, Layer 3) Batterie-Laden, Layer 4) Netzbezug, Layer 5) Rückspeisung
    # Entladen/Laden und Netzbezug/Rückspeisung schliessen sich jeweils gegenseitig aus.
    # Grenzen werden auf die Gesamthöhe begrenzt (z.B. Rückspeisung aus der Batterie).
    grenzen = []
    summe = 0
    for watt in [eigenverbrauch, entladen, laden_pv, netzbezug, rueckspeisung]:
        summe += watt
        grenzen.append(_watt_to_idx(min(summe, gesamt)))

    result = Idxs(*grenzen)
    logger.info(f"Watt per pixel = {WATT_PER_PIXEL}, Pixel-Grenzen = {result}")
    return result

# from and to are each return values of compute_idx, see above
def transition_step(from_idxs: Idxs, to_idxs: Idxs) -> Idxs:
    transition_idxs = Idxs(from_idxs.consume, from_idxs.discharge, from_idxs.charge, from_idxs.grid, from_idxs.pv)

    if transition_idxs.consume < to_idxs.consume: transition_idxs.consume += 1
    elif transition_idxs.consume> to_idxs.consume: transition_idxs.consume -= 1

    if transition_idxs.discharge < to_idxs.discharge: transition_idxs.discharge += 1
    elif transition_idxs.discharge > to_idxs.discharge: transition_idxs.discharge -= 1

    if transition_idxs.charge < to_idxs.charge: transition_idxs.charge += 1
    elif transition_idxs.charge > to_idxs.charge: transition_idxs.charge -= 1

    if transition_idxs.grid < to_idxs.grid: transition_idxs.grid += 1
    elif transition_idxs.grid > to_idxs.grid: transition_idxs.grid -= 1

    if transition_idxs.pv < to_idxs.pv: transition_idxs.pv += 1
    elif transition_idxs.pv > to_idxs.pv: transition_idxs.pv -= 1

    return transition_idxs

# parameters is array of 3 values, see above
def render(pixel_idxs: Idxs):
    pixel_matrix = [[PIX_EMPTY for x in range(WIDTH)] for y in range(HEIGHT)]

    _set_matrix_color(pixel_matrix, 0, pixel_idxs.consume, PIX_CONSUME)
    _set_matrix_color(pixel_matrix, pixel_idxs.consume, pixel_idxs.discharge, PIX_DISCHARGE)
    _set_matrix_color(pixel_matrix, pixel_idxs.discharge, pixel_idxs.charge, PIX_CHARGE)
    _set_matrix_color(pixel_matrix, pixel_idxs.charge, pixel_idxs.grid, PIX_GRID)
    _set_matrix_color(pixel_matrix, pixel_idxs.grid, pixel_idxs.pv, PIX_PV)

    return pixel_matrix
