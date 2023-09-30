# Copyright 2023 Gérard Plangger
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.

import solrpi.ledmatrix as ledmatrix
from solrpi.i_inverter import Inverter
from solrpi.i_uidevice import UIDevice
import time
import datetime
import logging

SLEEP_SEC = 2
SLEEP_TRANSITION_STEP_SEC = 0.04
BLINK_SEC = 0.1
PWR_SAVE_FROM_H = 0
PWR_SAVE_UNTIL_H = 5
PWR_SAVE_SLEEP_SEC = 60

logger = logging.getLogger(__name__)

class Renderer:
    def __init__(self, inverter: Inverter, uidevice: UIDevice):
        self.inverter = inverter
        self.ui = uidevice

        self.color_mapping = [self.ui.getColorBlack(), self.ui.getColorRed(), self.ui.getColorGreen(), self.ui.getColorYellow()] # index must match appropriate solrpi_led_matrix.PIX_*

    
    def get_ui(self):
        return self.ui

    def _do_blink(self, times=1):
        blink_idx = ledmatrix.HEIGHT-1
        current_pixel_color = self.ui.getPixelColor(blink_idx)
        n = 0
        ui = self.ui
        while True: # do..while
            ui.setPixelColor(blink_idx, ui.getColorBlink())
            ui.draw()
            time.sleep(BLINK_SEC)
            ui.setPixelColor(blink_idx, current_pixel_color)
            ui.draw()
            n += 1
            if n >= times:
                break
            time.sleep(BLINK_SEC)

    def map_from_matrix(self, matrix):
        for j in range(len(matrix)):
            for i in range(len(matrix[j])):
                val = matrix[j][i]
                pos = i*ledmatrix.HEIGHT + j
                #logger.debug("i={} j={} val={} pos={}".format(i, j, val, pos))
                self.ui.setPixelColor(pos, self.color_mapping[val])

    def run(self):
        pixel_indexes_prev = ledmatrix.Idxs()
        while True:
            now = datetime.datetime.now()
            watt = self.inverter.get_watt()
			#if not watt or watt.len < 2 TODO ERROR HANDLING logger.error("")
            pixel_indexes_target = ledmatrix.compute_idxs(watt[0], watt[1])
            logger.debug("pixel_indexes_prev = {}".format(pixel_indexes_prev))
            logger.debug("pixel_indexes_target = {}".format(pixel_indexes_target))
            self.ui.setBrightness(ledmatrix.compute_brightness(pixel_indexes_target))
            pixel_indexes_transition = pixel_indexes_prev
            sleep_remain = SLEEP_SEC
            while pixel_indexes_transition != pixel_indexes_target:
                pixel_indexes_transition = ledmatrix.transition_step(pixel_indexes_transition, pixel_indexes_target)
                pixels = ledmatrix.render(pixel_indexes_transition)
                logger.debug(pixels)
                self.map_from_matrix(pixels)
                self.ui.draw()
                time.sleep(SLEEP_TRANSITION_STEP_SEC)
                sleep_remain -= SLEEP_TRANSITION_STEP_SEC
            pixel_indexes_prev = pixel_indexes_target

            if sleep_remain > 0:
                time.sleep(sleep_remain)
            self._do_blink() # blink to show we are up

            # Entering power-save mode?
            if now.hour >= PWR_SAVE_FROM_H and now.hour < PWR_SAVE_UNTIL_H:
                self.ui.clear()
                while True: # do..while
                    time.sleep(PWR_SAVE_SLEEP_SEC)
                    self._do_blink(3) # triple blink
                    if datetime.datetime.now().hour >= PWR_SAVE_UNTIL_H:
                        break

    def clear(self):
        self.ui.clear()
