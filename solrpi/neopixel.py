# Copyright 2023 Gérard Plangger
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.

from rpi_ws281x import Adafruit_NeoPixel, Color
from solrpi.i_uidevice import UIDevice

COLOR_BLACK = Color(0,0,0)
COLOR_RED = Color(255,0,0)
COLOR_GREEN = Color(0,255,0)
COLOR_YELLOW = Color(255,255,0)
COLOR_BLINK = Color(0,0,50)

# LED strip configuration:
LED_COUNT      = 32      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 5       # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

class NeoPixel(UIDevice):

    def __init__(self):
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
        self.strip.begin()

    def numPixels(self):
        return LED_COUNT

    def setBrightness(self, brightness: int):
        self.strip.setBrightness(brightness)

    def setPixelColor(self, index: int, color: int):
        self.strip.setPixelColor(index, color)

    def getPixelColor(self, index: int):
        return self.strip.getPixelColor(index)
    
    def draw(self):
        self.strip.show()

    def clear(self):
        for i in range(self.strip.numPixels()):
            self.setPixelColor(i, COLOR_BLACK)
        self.draw()

    def getColorBlink(self):
        return COLOR_BLINK

    def getColorRed(self):
        return COLOR_RED

    def getColorGreen(self):
        return COLOR_GREEN

    def getColorYellow(self):
        return COLOR_YELLOW

    def getColorBlack(self):
        return COLOR_BLACK
