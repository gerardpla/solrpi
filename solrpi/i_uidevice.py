# Copyright 2023 Gérard Plangger
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.

# interface for UI devices
class UIDevice:

    def numPixels(self):
        pass

    def setBrightness(self, brightness: int):
        pass

    def setPixelColor(self):
        pass

    def getPixelColor(self, index: int):
        pass
    
    def draw(self):
        pass

    def clear(self):
        pass

    def getColorBlink(self):
        pass

    def getColorRed(self):
        pass

    def getColorGreen(self):
        pass

    def getColorYellow(self):
        pass

    def getColorBlack(self):
        pass