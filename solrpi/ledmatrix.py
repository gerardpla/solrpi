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

# brightness values according to rpi_ws281x
BRIGHTNESS_DAY = 5
BRIGHTNESS_SUN = 10

logger = logging.getLogger(__name__)

@dataclass
class Idxs:
    # Note that the values are relative indexes, not absolute consumption values!
    consume: int
    grid: int
    pv: int

    def __init__(self, consume: int=0, grid: int=0, pv: int=0):
        self.consume = consume
        self.grid = grid
        self.pv = pv


def compute_brightness(idxs: Idxs):
	if (idxs.consume > 3) or (idxs.pv - idxs.grid > 3): # at least three pixels PV (or self-consumption)
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

# input parameters grid, pv; represented Watt, values can be negative
# returns an array with 3 values: grid index, consume index, pv index
def compute_idxs(grid: float, pv: float) -> Idxs:
    logger.info("grid={}, pv={}".format(grid, pv))
    result = None

    if (grid < 0):
        # PV Produktion mit Anteil Rückspeisung ins Netz (grid negativ!)

        # Layer 1) 0 .. pv+grid = Eigenverbrauch
        eigenverbrauch_idx = min(round((pv+grid) / WATT_PER_PIXEL), NUM_PIXELS)

        # Layer 2) pv+grid .. pv = Überschuss
        ueberschuss_idx = min(round(pv / WATT_PER_PIXEL), NUM_PIXELS)
        logger.info(f"Watt per pixel = {WATT_PER_PIXEL}, Eigenverbrauch Pixels = {eigenverbrauch_idx}, Ueberschuss Pixels = {ueberschuss_idx}")

        result = Idxs(eigenverbrauch_idx, eigenverbrauch_idx, ueberschuss_idx)
    else: # grid >= 0
        # (Eventuell) PV Produktion (Eigenverbrauch) und Bezug aus Netz

        # Layer 1) 0 .. pv = Eigenverbrauch
        eigenverbrauch_idx = min(round(pv / WATT_PER_PIXEL), NUM_PIXELS)

        # Layer 2) pv .. pv+grid = Bezug Netz
        grid_idx = min(round((pv+grid) / WATT_PER_PIXEL), NUM_PIXELS)
        
        logger.info(f"Watt per pixel = {WATT_PER_PIXEL}, Eigenverbrauch Pixels = {eigenverbrauch_idx}, Netzbezug Pixels = {grid_idx}")
        result = Idxs(eigenverbrauch_idx, grid_idx, grid_idx)

    return result

# from and to are each return values of compute_idx (array of 3 values, see above)
def transition_step(from_idxs: Idxs, to_idxs: Idxs) -> Idxs:
    transition_idxs = Idxs(from_idxs.consume, from_idxs.grid, from_idxs.pv)

    if transition_idxs.consume < to_idxs.consume: transition_idxs.consume += 1
    elif transition_idxs.consume> to_idxs.consume: transition_idxs.consume -= 1

    if transition_idxs.grid < to_idxs.grid: transition_idxs.grid += 1
    elif transition_idxs.grid > to_idxs.grid: transition_idxs.grid -= 1

    if transition_idxs.pv < to_idxs.pv: transition_idxs.pv += 1
    elif transition_idxs.pv > to_idxs.pv: transition_idxs.pv -= 1

    return transition_idxs

# parameters is array of 3 values, see above
def render(pixel_idxs: Idxs):
    pixel_matrix = [[PIX_EMPTY for x in range(WIDTH)] for y in range(HEIGHT)]

    _set_matrix_color(pixel_matrix, 0, pixel_idxs.consume, PIX_CONSUME)
    _set_matrix_color(pixel_matrix, pixel_idxs.consume, pixel_idxs.grid, PIX_GRID)
    _set_matrix_color(pixel_matrix, pixel_idxs.grid, pixel_idxs.pv, PIX_PV)

    return pixel_matrix
