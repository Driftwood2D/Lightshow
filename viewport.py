####################################
# Driftwood 2D Stageshow Engine    #
# viewport.py                      #
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

# Stageshow Viewport Manager

import random


class ViewportFX:
    """Viewport Effects Handler

    Manages special effects involving the viewport."""
    def __init__(self):
        self.rumbling = False
        self.__will_end_rumble = False

    def rumble(self, rate, intensity, duration=None):
        """Rumble the viewport.

        Args:
            rate: Rate to update the viewport offset in hertz.
            intensity: Maximum viewport offset.
            duration: If set, how long in seconds before stopping.

        Returns:
            Function to end the rumble.
        """
        self.end_rumble()
        self.__cancel_end_rumble_tick()
        Driftwood.tick.register(self._rumble_callback, delay=1.0 / rate, message=intensity)
        self.rumbling = True
        if duration:
            Driftwood.tick.register(self._end_rumble_tick, delay=duration, once=True)
            self.__will_end_rumble = True

    def end_rumble(self):
        """Stop rumbling right away.

        Returns:
            True
        """
        if self.rumbling:
            Driftwood.tick.unregister(self._rumble_callback)
            Driftwood.area.offset = [0, 0]
            Driftwood.area.changed = True
            self.rumbling = False

        return True

    def _rumble_callback(self, seconds_past, intensity):
        Driftwood.area.offset = [
            random.randint(intensity * -1, intensity),
            random.randint(intensity * -1, intensity)
        ]
        Driftwood.area.changed = True

    def _end_rumble_tick(self):
        self.end_rumble()
        self.__will_end_rumble = False

    def __cancel_end_rumble_tick(self):
        if self.__will_end_rumble:
            Driftwood.tick.unregister(self._end_rumble_tick)
            self.__will_end_rumble = False
