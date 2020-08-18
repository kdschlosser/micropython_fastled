
from . import *
from .colorutils import *


#  Represents a set of CRGB led objects.  Provides the [] array operator, and works like a normal array in that case.
#  This should be kept in sync with the set of functions provided by CRGB as well as functions in colorutils.  Note
#  that a pixel set is a window into another set of led data, it is not its own set of led data.
class CPixelView(object):

    def __init__(self, leds=None, len_=None, _start=None, _end=None, other=None):
        if isinstance(other, CPixelView):
            self.dir = other.dir
            self.len = other.len
            self.leds = other.leds
            self.end_pos = other.end_pos
        elif isinstance(leds, CPixelView):
            self.dir = leds.dir
            self.len = leds.len
            self.leds = leds.leds
            self.end_pos = leds.end_pos

        elif len_ is not None and _start is not None:
            _end = _start
            _start = len_
            len_ = None

        if _start is not None and _end is not None:
            if _end - _start < 0:
                self.dir = -1
            else:
                self.dir = 1

            self.len = (_end - _start) + self.dir
            self.leds = leds[_start:]
            self.end_pos = _start + self.len

        else:
            self.dir = -1 if len_ < 0 else 1
            self.len = len_
            self.leds = leds
            self.end_pos = len_

    # Get the size of this set
    # @return the size of the set
    def size(self):
        return abs(self.len)

    # Whether or not this set goes backwards
    # @return whether or not the set is backwards
    def reversed(self):
        return self.len < 0

    # do these sets point to the same thing (note, this is different from the contents of the set being the same)
    def __eq__(self, rhs):
        return (
            self.leds == rhs.leds and
            self.len == rhs.len and
            self.dir == rhs.dir
        )

    # do these sets point to the different things (note, this is different from the contents of the set being the same)
    def __ne__(self, rhs):
        return not self.__eq__(rhs)

    # access a single element in this set, just like an array operator
    def __getitem__(self, x):
        if isinstance(x, slice):
            start = x.start
            stop = x.stop

            if start is None:
                start = 0
            if stop is None:
                stop = len(self.leds)

            return CPixelView(self.leds, start, stop)

        if self.dir & 0x80:
            return self.leds[-x]

        return self.leds[x]

    def __neg__(self):
        return CPixelView(self.leds, self.len - self.dir, 0)

    def dump(self):
        pass

    # Add the passed in value to r,g, b for all the pixels in this set
    def addToRGB(self, inc):
        for pixel in self.leds:
            pixel += inc

        return self

    # Add every pixel in the other set to this set
    def __iadd__(self, rhs):
        if isinstance(rhs, CPixelView):
            if rhs.len > self.len:
                for i in range(rhs.len):
                    try:
                        pixel = self[i]
                    except IndexError:
                        break

                    pixel += rhs[i]
            else:
                for i in range(self.len):
                    try:
                        pixel = rhs[i]
                    except IndexError:
                        break

                    self[i] += pixel
        else:
            for pixel in self.leds:
                pixel += rhs

        return self

    # Subtract the passed in value from r,g,b for all pixels in this set
    def subFromRGB(self, inc):
        for pixel in self.leds:
            pixel -= inc

        return self

    # Subtract every pixel in the other set from this set
    def __isub__(self, rhs):
        if isinstance(rhs, CPixelView):
            if rhs.len > self.len:
                for i in range(rhs.len):
                    try:
                        pixel = self[i]
                    except IndexError:
                        break

                    pixel -= rhs[i]

            else:
                for i in range(self.len):
                    try:
                        pixel = rhs[i]
                    except IndexError:
                        break

                    self[i] -= pixel
        else:
            for pixel in self.leds:
                pixel -= rhs

        return self

    # Divide every led by the given value
    def __idiv__(self, d):
        for pixel in self.leds:
            pixel //= d

        return self

    def __imul__(self, d):
        for pixel in self.leds:
            pixel *= d

        return self

    def __irshift__(self, d):
        for pixel in self.leds:
            pixel >>= d

        return self

    # Scale every led by the given scale
    def nscale8_video(self, scaledown):
        for pixel in self.leds:
            pixel.nscale8_video(scaledown)

        return self

    # Scale down every led by the given scale
    def __imod__(self, scaledown):
        for pixel in self.leds:
            pixel.nscale8_video(scaledown)

        return self

    # Fade every led down by the given scale
    def fadeLightBy(self, fadefactor):
        return self.nscale8_video(255 - fadefactor)

    # Scale every led by the given scale
    def nscale8(self, scaledown):
        if isinstance(scaledown, CPixelView):
            if scaledown.len() > self.len():
                for i in range(scaledown.len()):
                    try:
                        pixel = self[i]
                    except IndexError:
                        break

                    pixel.nscale8(scaledown[i])
            else:
                for i in range(self.len()):
                    try:
                        pixel = scaledown[i]
                    except IndexError:
                        break

                    self[i].nscale8(pixel)
        else:

            for pixel in self.leds:
                pixel.nscale8(scaledown)

        return self

    # Fade every led down by the given scale
    def fadeToBlackBy(self, fade):
        return self.nscale8(255 - fade)

    def __ior__(self, rhs):
        if isinstance(rhs, CPixelView):
            if rhs.len > self.len:
                for i in range(rhs.len):
                    try:
                        pixel = self[i]
                    except IndexError:
                        break

                    pixel |= rhs[i]
            else:
                for i in range(self.len):
                    try:
                        pixel = rhs[i]
                    except IndexError:
                        break

                    self[i] |= pixel
        else:
            for pixel in self.leds:
                pixel |= rhs

        return self

    def __iand__(self, rhs):
        if isinstance(rhs, CPixelView):
            if rhs.len > self.len:
                for i in range(rhs.len):
                    try:
                        pixel = self[i]
                    except IndexError:
                        break

                    pixel &= rhs[i]
            else:
                for i in range(self.len):
                    try:
                        pixel = rhs[i]
                    except IndexError:
                        break

                    self[i] &= pixel
        else:
            for pixel in self.leds:
                pixel &= rhs

        return self

    # Returns whether or not any leds in this set are non-zero
    def __bool__(self):
        for pixel in self.leds:
            if pixel:
                return True

        return False

    # Color util functions
    def fill_solid(self, color):
        for pixel in self.leds:
            if isinstance(color, CHSV):
                pixel.setHSV(color)
            else:
                pixel.setRGB(color)

        return self

    def fill_rainbow(self, initialhue, deltahue=5):
        if self.dir >= 0:
            fill_rainbow(self.leds, self.len, initialhue, deltahue)
        else:
            fill_rainbow(self.leds[:self.len + 1], -self.len, initialhue, deltahue)

        return self

    def fill_gradient(
            self,
            c1,
            c2,
            c3=None,
            c4=None,
            directionCode=SHORTEST_HUES
    ):

        if self.dir >= 0:
            fill_gradient(self.leds, self.len, c1, c2, c3, c4, directionCode)
        else:
            fill_gradient(self.leds[:self.len + 1], -self.len, c1, c2, c3, c4, directionCode)

        return self

    def fill_gradient_RGB(
            self,
            c1,
            c2,
            c3=None,
            c4=None,
            directionCode=SHORTEST_HUES
    ):

        if self.dir >= 0:
            fill_gradient_RGB(self.leds, self.len, c1, c2, c3, c4, directionCode)
        else:
            fill_gradient_RGB(self.leds[:self.len + 1], -self.len, c1, c2, c3, c4, directionCode)

        return self

    def nblend(self, overlay, amountOfOverlay):
        if isinstance(overlay, CPixelView):
            if overlay.len() > self.len():
                for i in range(overlay.len()):
                    try:
                        pixel = self[i]
                    except IndexError:
                        break

                    nblend(pixel, overlay[i], amountOfOverlay)

            else:
                for i in range(self.len()):
                    try:
                        pixel = overlay[i]
                    except IndexError:
                        break

                    nblend(self[i], pixel, amountOfOverlay)

        else:
            for pixel in self.leds:
                nblend(pixel, overlay, amountOfOverlay)

    # Note: only bringing in a 1d blur, not sure 2d blur makes sense when looking at sub arrays
    def blur1d(self, blur_amount):
        if self.dir >= 0:
            blur1d(self.leds, self.len, blur_amount)
        else:
            blur1d(self.leds[self.len + 1], -self.len, blur_amount)

        return self

    def napplyGamma_video(self, gammaR, gammaG=None, gammaB=None):
        if gammaG is None and gammaB is None:
            if self.dir >= 0:
                napplyGamma_video(self.leds, self.len, gammaR)
            else:
                napplyGamma_video(self.leds[self.len + 1], -self.len, gammaR)
        else:
            if self.dir >= 0:
                napplyGamma_video(self.leds, self.len, gammaR, gammaG, gammaB)
            else:
                napplyGamma_video(self.leds[self.len + 1], -self.len, gammaR, gammaG, gammaB)

        return self


CRGBSet = CPixelView


class CRGBArray(CRGBSet):

    def __init__(self, *args, **kwargs):
        super(CRGBArray, self).__init__(*args, **kwargs)

        self.rawleds = [pixel for pixel in self.leds]
