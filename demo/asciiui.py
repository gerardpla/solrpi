# Copyright 2023 Gérard Plangger
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.

from solrpi.i_uidevice import UIDevice

COLOR_BLACK = '-'
COLOR_RED = '\033[91m' + 'R' + '\033[0m'
COLOR_GREEN = '\033[92m' + 'G' + '\033[0m'
COLOR_YELLOW = '\033[93m' + 'Y' + '\033[0m'
COLOR_BLINK = '\033[94m' + '*' + '\033[0m'

# LED strip configuration:
LED_COUNT      = 32      # Number of LED pixels.
LED_BRIGHTNESS = 5       # Set to 0 for darkest and 255 for brightest

LINE_UP = '\033[1A'

class AsciiUI(UIDevice):

    def __init__(self):
        self.brightness = LED_BRIGHTNESS
        self.strip = None
        self.clear()

    def numPixels(self):
        return LED_COUNT

    def setBrightness(self, brightness: int):
        self.brightness

    def setPixelColor(self, index: int, color: int):
        self.strip[index] = color

    def getPixelColor(self, index: int):
        return self.strip[index]
    
    def draw(self):
        for i in range(LED_COUNT):
            if i % 8 == 0:
                print("") # newline
            print(self.strip[i] + "  ", end='')
        print(LINE_UP, end='\r')
        print(LINE_UP, end='\r')
        print(LINE_UP, end='\r')
        print(LINE_UP, end='\r')
        
    def clear(self):
        self.strip = [' ' for x in range(LED_COUNT)]

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
