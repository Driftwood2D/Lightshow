####################################
# Driftwood 2D Stageshow Engine    #
# lighting.py                      #
# Copyright 2017 Michael D. Reiley #
# & Paul Merrill                   #
####################################

# **********
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
# **********

# Stageshow Lighting Manager

import copy
import random


class LightingFX:
    """Lighting Effects Handler

    Manages special effects involving the viewport."""

    def __init__(self):
        self.__light_flickers = None
        self.__light_flicker_originals = {}

    def flicker(self, lid, rx, ry, ralpha, rate, duration=None):
        """Shake a light around randomly while changing its alpha.
        Args:
            lid: Light ID of the light to shimmer.
            rx: Absolute value range for x offset.
            ry: Absolute value range for y offset.
            ralpha: Absolute value range for alpha offset.
            rate: Rate to update the light offset in hertz.
            duration: If set, how long in seconds before stopping.

        Returns:
            True
        """
        ox = Driftwood.light.light(lid).x
        oy = Driftwood.light.light(lid).y
        oalpha = Driftwood.light.light(lid).alpha

        fc = fncopy(self._flicker_callback)
        fc.active = True
        fc.lid = lid

        if not self.__light_flickers:
            self.__light_flickers = set()
        self.__light_flickers.add(fc)

        self.__light_flicker_originals[lid] = [ox, oy, oalpha]

        Driftwood.tick.register(fc, delay=1.0 / rate, message=[lid, rx, ry, ralpha, fc, self])

        if duration:
            Driftwood.tick.register(self._end_flicker, delay=duration, once=True, message=fc)

        return True

    def reset_flickers(self):
        if self.__light_flickers:
            fcs = self.__light_flickers
            while len(fcs) > 0:
                fc = fcs.pop()
                self._end_flicker(None, fc)

    def _flicker_callback(seconds_past, msg):
        lid, rx, ry, ralpha, fc, self = msg
        if not Driftwood.light.light(lid):
            fc.active = False
            self.__remove_flicker(fc)
            return
        ox, oy, oalpha = copy.deepcopy(self.__light_flicker_originals[lid])
        ox += random.randint(rx * -1, rx)
        oy += random.randint(ry * -1, ry)
        oalpha += random.randint(ralpha * -1, ralpha)
        if oalpha > 255:
            oalpha = 255
        if oalpha < 0:
            oalpha = 0
        Driftwood.light.light(lid).x = ox
        Driftwood.light.light(lid).y = oy
        Driftwood.light.light(lid).alpha = oalpha
        Driftwood.area.changed = True

    def _end_flicker(self, seconds_past, msg):
        fc = msg
        lid = fc.lid

        self.__remove_flicker(fc)

        if fc.active:
            fc.active = False

            Driftwood.light.light(lid).x = self.__light_flicker_originals[lid][0]
            Driftwood.light.light(lid).y = self.__light_flicker_originals[lid][1]
            Driftwood.light.light(lid).alpha = self.__light_flicker_originals[lid][2]
            Driftwood.area.changed = True

    def __remove_flicker(self, fc):
        Driftwood.tick.unregister(fc)
        self.__light_flickers.discard(fc)
