
# Forward declaration of hsv2rgb_rainbow here,
# to avoid circular dependencies.
# Representation of an HSV pixel (hue, saturation, value (aka brightness)).


class CHSV(object):

    @property
    def hue(self):
        return self._hue

    @hue.setter
    def hue(self, value):
        self._hue = value

    @property
    def h(self):
        return self._hue

    @h.setter
    def h(self, value):
        self._hue = value

    @property
    def saturation(self):
        return self._saturation

    @saturation.setter
    def saturation(self, value):
        self._saturation = value

    @property
    def sat(self):
        return self._saturation

    @sat.setter
    def sat(self, value):
        self._saturation = value

    @property
    def s(self):
        return self._saturation

    @s.setter
    def s(self, value):
        self._saturation = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def val(self):
        return self._value

    @val.setter
    def val(self, value):
        self._value = value

    @property
    def v(self):
        return self._value

    @v.setter
    def v(self, value):
        self._value = value

    @property
    def raw(self):
        return [self._hue, self._saturation, self._value]

    def __getitem__(self, index):
        return self.raw[index]

    def __init__(self, iH=None, iS=None, iV=None, rhs=None):
        if isinstance(iH, CHSV):
            self._hue, self._saturation, self._value = iH.raw
        elif rhs is not None:
            self._hue, self._saturation, self._value = rhs.raw
        else:
            if iH is None:
                iH = 0
            if iS is None:
                iS = 0
            if iV is None:
                iV = 0

            self._hue = iH
            self._saturation = iS
            self._value = iV

    def setHSV(self, iH, iS, iV):
        self._hue = iH
        self._saturation = iS
        self._value = iV
        return self


# Pre-defined hue values for HSV objects
HUE_RED = 0
HUE_ORANGE = 32
HUE_YELLOW = 64
HUE_GREEN = 96
HUE_AQUA = 128
HUE_BLUE = 160
HUE_PURPLE = 192
HUE_PINK = 224


# Representation of an RGB pixel (Red, Green, Blue)
class CRGB(object):

    @property
    def white(self):
        return self._white

    @white.setter
    def white(self, value):
        self._white = value

    @property
    def w(self):
        return self._white

    @w.setter
    def w(self, value):
        self._white = value

    @property
    def red(self):
        return self._red

    @red.setter
    def red(self, value):
        self._red = value

    @property
    def r(self):
        return self._red

    @r.setter
    def r(self, value):
        self._red = value

    @property
    def green(self):
        return self._green

    @green.setter
    def green(self, value):
        self._green = value

    @property
    def g(self):
        return self._green

    @g.setter
    def g(self, value):
        self._green = value

    @property
    def blue(self):
        return self._blue

    @blue.setter
    def blue(self, value):
        self._blue = value

    @property
    def b(self):
        return self._blue

    @b.setter
    def b(self, value):
        self._blue = value

    @property
    def raw(self):
        if self._white is None:
            return [self._red, self._green, self._blue]
        else:
            return [self._red, self._green, self._blue, self._white]

    def get_data_stream(self, rgb_order):
        rgb_order = str(rgb_order / 10000).split('.')[-1]

        while rgb_order.count('0') > 1:
            rgb_order = rgb_order[1:]

        rgb_order = list(int(item) for item in list(rgb_order))

        if 3 in rgb_order and self._white is None:
            rgbw = CRGB()
            rgb2rgbw(self, rgbw)
            values = [rgbw.r, rgbw.b, rgbw.g, rgbw.w]
        else:
            values = [self._red, self._green, self._blue, self._white]

        bytes_ = []
        for index in rgb_order:
            bytes_.append(values[index])

        bit_array = []
        for byte in bytes_:
            bits = []
            for i in range(7, -1, -1):
                bits += [int(get_bit(byte, i))]

            bit_array += [bits[:]]

        return bit_array

    def __getitem__(self, index):
        return self.raw[index]

    def __init__(self, iR=None, iG=None, iB=None, iW=None, colorcode=None, rhs=None):
        if isinstance(iR, CRGB):
            raw = iR.raw
            if len(raw) == 4:
                self._red, self._green, self._blue, self._white = raw
            else:
                self._white = None
                self._red, self._green, self._blue = raw

        if isinstance(iR, CHSV):
            self._red = 0
            self._green = 0
            self._blue = 0
            self._white = None
            hsv2rgb_rainbow(iR, self)

        elif isinstance(rhs, CRGB):
            raw = iR.raw
            if len(raw) == 4:
                self._red, self._green, self._blue, self._white = raw
            else:
                self._white = None
                self._red, self._green, self._blue = raw

        elif isinstance(rhs, CHSV):
            self._red = 0
            self._green = 0
            self._blue = 0
            self._white = None
            hsv2rgb_rainbow(rhs, self)

        elif isinstance(colorcode, int):
            self._red = (colorcode >> 16) & 0xFF
            self._green = (colorcode >> 8) & 0xFF
            self._blue = (colorcode >> 0) & 0xFF

            if colorcode > 16777215:
                self._white = (colorcode >> 24) & 0xFF
            else:
                self._white = None

        else:
            if iR is None:
                iR = 0
            if iG is None:
                iG = 0
            if iB is None:
                iB = 0

            self._red = iR
            self._green = iG
            self._blue = iB
            self._white = iW

    def setRGB(self, nR, nG, nB, nW=None):
        self._red = nR
        self._green = nG
        self._blue = nB
        self._white = nW
        return self

    def setHSV(self, hue, sat, val):
        if self._white is not None:
            rgb = CRGB()
            hsv2rgb_rainbow(CHSV(hue, sat, val), rgb)
            rgb2rgbw(rgb, self)

        else:
            hsv2rgb_rainbow(CHSV(hue, sat, val), self)

        return self

    def setHue(self, hue):
        hsv2rgb_rainbow(CHSV(hue, 255, 255), self)
        return self

    def setColorCode(self, colorcode):
        if colorcode > 16777215:
            self._white = (colorcode >> 24) & 0xFF
        else:
            self._white = None

        self._red = (colorcode >> 16) & 0xFF
        self._green = (colorcode >> 8) & 0xFF
        self._blue = (colorcode >> 0) & 0xFF
        return self

    def __iadd__(self, rhs):
        if self._white is None and rhs.w is None:
            self._red = qadd8(self._red, rhs.r)
            self._green = qadd8(self._green, rhs.g)
            self._blue = qadd8(self._blue, rhs.b)

        elif self._white is not None and rhs.w is not None:
            self._white = qadd8(self._white, rhs.w)
            self._red = qadd8(self._red, rhs.r)
            self._green = qadd8(self._green, rhs.g)
            self._blue = qadd8(self._blue, rhs.b)
        elif rhs.w is not None:
            rgb = CRGB()
            rgbw2rgb(rhs, rgb)

            rgb.r = qadd8(self._red, rgb.r)
            rgb.g = qadd8(self._green, rgb.g)
            rgb.b = qadd8(self._blue, rgb.b)

            rgb2rgbw(rgb, self)
        else:
            rgb = CRGB()
            rgbw2rgb(self, rgb)

            rgb.r = qadd8(rgb.r, rhs.r)
            rgb.g = qadd8(rgb.g, rhs.g)
            rgb.b = qadd8(rgb.b, rhs.b)

            rgb2rgbw(rgb, self)

        return self

    def addToRGB(self, d):
        self._red = qadd8(self._red, d)
        self._green = qadd8(self._green, d)
        self._blue = qadd8(self._blue, d)

        if self._white is not None:
            self._white = qadd8(self._white, d)

        return self

    def __isub__(self, rhs):
        if isinstance(rhs, CRGB):
            if self._white is None and rhs.w is None:
                self._red = qsub8(self._red, rhs.r)
                self._green = qsub8(self._green, rhs.g)
                self._blue = qsub8(self._blue, rhs.b)

            elif self._white is not None and rhs.w is not None:
                self._white = qsub8(self._white, rhs.w)
                self._red = qsub8(self._red, rhs.r)
                self._green = qsub8(self._green, rhs.g)
                self._blue = qsub8(self._blue, rhs.b)
            elif rhs.w is not None:
                rgb = CRGB()
                rgbw2rgb(rhs, rgb)

                rgb.r = qsub8(self._red, rgb.r)
                rgb.g = qsub8(self._green, rgb.g)
                rgb.b = qsub8(self._blue, rgb.b)

                rgb2rgbw(rgb, self)
            else:
                rgb = CRGB()
                rgbw2rgb(self, rgb)

                rgb.r = qsub8(rgb.r, rhs.r)
                rgb.g = qsub8(rgb.g, rhs.g)
                rgb.b = qsub8(rgb.b, rhs.b)

                rgb2rgbw(rgb, self)

        else:
            self.subtractFromRGB(rhs)
        return self

    def subtractFromRGB(self, d):
        self._red = qsub8(self._red, d)
        self._green = qsub8(self._green, d)
        self._blue = qsub8(self._blue, d)

        if self._white is not None:
            self._white = qsub8(self._white, d)

        return self

    def __idiv__(self, d):
        self._red /= d
        self._green /= d
        self._blue /= d

        if self._white is not None:
            self._white /= d

        return self

    def __irshift__(self, d):
        self._red >>= d
        self._green >>= d
        self._blue >>= d

        if self._white is not None:
            self._white >>= d

        return self

    def __imul__(self, d):
        self._red = qmul8(self._red, d)
        self._green = qmul8(self._green, d)
        self._blue = qmul8(self._blue, d)

        if self._white is not None:
            self._white = qmul8(self._white, d)

        return self

    def nscale8_video(self, scaledown):
        if self._white is None:
            self._red, self._green, self._blue = nscale8x3_video(
                self._red,
                self._green,
                self._blue,
                scaledown
            )
        else:
            self._red, self._green, self._blue, self._white = nscale8x4_video(
                self._red,
                self._green,
                self._blue,
                self._white,
                scaledown
            )

        return self

    def __imod__(self, scaledown):
        self.nscale8_video(scaledown)
        return self

    def fadeLightBy(self, fadefactor):
        self.nscale8_video(255 - fadefactor)
        return self

    def scale8(self, scaledown):
        if isinstance(scaledown, CRGB):
            out = CRGB()
            out.r = scale8(self._red, scaledown.r)
            out.g = scale8(self._green, scaledown.g)
            out.b = scale8(self._blue, scaledown.b)
            out.w = scale8(self._white, scaledown.w)

            return out
        else:
            if self._white is None:
                self._red, self._green, self._blue = nscale8x3(
                    self._red,
                    self._green,
                    self._blue,
                    scaledown
                )
            else:
                self._red, self._green, self._blue, self._white = nscale8x4(
                    self._red,
                    self._green,
                    self._blue,
                    self._white,
                    scaledown
                )

            return self

    def nscale8(self, scaledown):
        self._red = scale8(self._red, scaledown.r)
        self._green = scale8(self._green, scaledown.g)
        self._blue = scale8(self._blue, scaledown.b)

        self._white = scale8(self._white, scaledown.w)
        return self

    def fadeToBlackBy(self, fadefactor):
        if self._white is None:
            self._red, self._green, self._blue = nscale8x3(
                self._red,
                self._green,
                self._blue,
                255 - fadefactor
            )
        else:
            self._red, self._green, self._blue, self._white = nscale8x4(
                self._red,
                self._green,
                self._blue,
                self._white,
                255 - fadefactor
            )

        return self

    def __ior__(self, rhs):
        if isinstance(rhs, CRGB):
            if rhs.r > self._red:
                self._red = rhs.r
            if rhs.g > self._green:
                self._green = rhs.g
            if rhs.b > self._blue:
                self._blue = rhs.b

            if self._white is not None and rhs.w is not None:
                if rhs.w > self._white:
                    self._white = rhs.w
            elif rhs.w is not None:
                self._white = rhs.w

        else:
            if rhs > self._red:
                self._red = rhs
            if rhs > self._green:
                self._green = rhs
            if rhs > self._blue:
                self._blue = rhs
            if self._white is not None and rhs > self._white:
                self._white = rhs

        return self

    def __iand__(self, rhs):
        if isinstance(rhs, CRGB):
            if rhs.r < self._red:
                self._red = rhs.r
            if rhs.g < self._green:
                self._green = rhs.g
            if rhs.b < self._blue:
                self._blue = rhs.b

            if self._white is not None and rhs.w is not None:
                if rhs.w < self.white:
                    self._white = rhs.w
            elif rhs.w is not None:
                self._white = rhs.w

        else:
            if rhs < self._red:
                self._red = rhs
            if rhs < self._green:
                self._green = rhs
            if rhs < self._blue:
                self._blue = rhs
            if self._white is not None and rhs < self._white:
                self._white = rhs

        return self

    def __bool__(self):
        return self._red != 0 or self._green != 0 or self._blue != 0 or int(self._white) != 0

    def __neg__(self):
        retval = CRGB()
        retval.r = 255 - self._red
        retval.g = 255 - self._green
        retval.b = 255 - self._blue
        if self._white is not None:
            retval.w = 255 - self._white

        return retval

    #
    # #if (defined SmartMatrix_h || defined SmartMatrix3_h)
    #     operator rgb24() const {
    #         rgb24 ret;
    #         ret.red = r;
    #         ret.green = g;
    #         ret.blue = b;
    #         return ret;
    #     }
    # #endif

    def getLuma(self):
        # Y' = 0.2126 R' + 0.7152 G' + 0.0722 B'
        #      54            183       18 (!)

        if self._white is None:
            rgb = self
        else:
            rgb = CRGB()
            rgbw2rgb(self, rgb)

        luma = (
            scale8_LEAVING_R1_DIRTY(rgb.r, 54) +
            scale8_LEAVING_R1_DIRTY(rgb.g, 183) +
            scale8_LEAVING_R1_DIRTY(rgb.b, 18)
        )
        cleanup_R1()

        return luma

    def getAverageLight(self):
        if FASTLED_SCALE8_FIXED == 1:
            eightyfive = 85
        else:
            eightyfive = 86

        if self._white is None:
            rgb = self
        else:
            rgb = CRGB()
            rgbw2rgb(self, rgb)

        avg = (
            scale8_LEAVING_R1_DIRTY(rgb.r, eightyfive) +
            scale8_LEAVING_R1_DIRTY(rgb.g, eightyfive) +
            scale8_LEAVING_R1_DIRTY(rgb.b, eightyfive)
        )
        cleanup_R1()
        return avg

    def maximizeBrightness(self, limit=255):
        if self.white is None:
            rgb = self

        else:
            rgb = CRGB()
            rgbw2rgb(self, rgb)

        max_ = rgb.r
        if rgb.g > max_:
            max_ = rgb.g
        if rgb.b > max_:
            max_ = rgb.b

        # stop div/0 when color is black
        if max_ > 0:
            factor = (limit * 256) / max_
            rgb.r = (rgb.r * factor) / 256
            rgb.g = (rgb.g * factor) / 256
            rgb.b = (rgb.b * factor) / 256

        if self._white is None:
            self._red = rgb.r
            self._green = rgb.g
            self._blue = rgb.b
        else:
            rgb2rgbw(rgb, self)

    def lerp8(self, other, frac):
        if self._white is None:
            rgb = self
        else:
            rgb = CRGB()
            rgbw2rgb(self, rgb)

        rgb.r = lerp8by8(rgb.r << 8, other.r << 8, frac)
        rgb.g = lerp8by8(rgb.g << 8, other.g << 8, frac)
        rgb.b = lerp8by8(rgb.b << 8, other.b << 8, frac)

        return rgb

    def lerp16(self, other, frac):
        if self._white is None:
            rgb = self
        else:
            rgb = CRGB()
            rgbw2rgb(self, rgb)

        rgb.r = lerp16by16(rgb.r << 8, other.r << 8, frac) >> 8
        rgb.g = lerp16by16(rgb.g << 8, other.g << 8, frac) >> 8
        rgb.b = lerp16by16(rgb.b << 8, other.b << 8, frac) >> 8

        return rgb

    def getParity(self):
        if self._white is None:
            rgb = self
        else:
            rgb = CRGB()
            rgbw2rgb(self, rgb)

        sum_ = rgb.r + rgb.g + rgb.b
        return sum_ & 0x01

    def setParity(self, parity):
        curparity = self.getParity()

        if parity == curparity:
            return
        if self._white is None:
            rgb = self
        else:
            rgb = CRGB()
            rgbw2rgb(self, rgb)

        if parity:
            # going 'up'
            if 255 > rgb.b > 0:
                if rgb.r == rgb.g == rgb.b:
                    rgb.r += 1
                    rgb.g += 1

                rgb.b += 1
            elif 255 > rgb.r > 0:
                rgb.r += 1
            elif 255 > rgb.g > 0:
                rgb.g += 1
            else:
                if rgb.r == rgb.g == rgb.b:
                    rgb.r ^= 0x01
                    rgb.g ^= 0x01

                rgb.b ^= 0x01

        else:
            # going 'down'
            if rgb.b > 1:
                if rgb.r == rgb.g == rgb.b:
                    rgb.r -= 1
                    rgb.g -= 1

                rgb.b -= 1
            elif rgb.g > 1:
                rgb.g -= 1
            elif rgb.r > 1:
                rgb.r -= 1
            else:
                if rgb.r == rgb.g == rgb.b:
                    rgb.r ^= 0x01
                    rgb.g ^= 0x01

                rgb.b ^= 0x01

        if self._white is None:
            self._red = rgb.r
            self._green = rgb.g
            self._blue = rgb.b
        else:
            rgb2rgbw(rgb, self)

    def __eq__(self, rhs):
        return self._red == rhs.r and self._green == rhs.g and self._blue == rhs.b and self._white == rhs.w

    def __ne__(self, rhs):
        return not self.__eq__(rhs)

    def __lt__(self, rhs):
        sl = self._red + self._green + self._blue + int(self._white)
        sr = rhs.r + rhs.g + rhs.b + int(rhs.w)
        return sl < sr

    def __gt__(self, rhs):
        sl = self._red + self._green + self._blue + int(self._white)
        sr = rhs.r + rhs.g + rhs.b + int(rhs.w)
        return sl > sr

    def __le__(self, rhs):
        sl = self._red + self._green + self._blue + int(self._white)
        sr = rhs.r + rhs.g + rhs.b + int(rhs.w)
        return sl <= sr

    def __ge__(self, rhs):
        sl = self._red + self._green + self._blue + int(self._white)
        sr = rhs.r + rhs.g + rhs.b + int(rhs.w)
        return sl >= sr

    def __add__(self, p2):
        if self._white is None and p2.w is None:
            return CRGB(
                qadd8(self._red, p2.r),
                qadd8(self._green, p2.g),
                qadd8(self._blue, p2.b)
            )
        elif self._white is not None and p2.w is not None:
            return CRGB(
                qadd8(self._red, p2.r),
                qadd8(self._green, p2.g),
                qadd8(self._blue, p2.b),
                qadd8(self._white, p2.w)
            )
        elif self._white is not None:
            return CRGB(
                qadd8(self._red, p2.r),
                qadd8(self._green, p2.g),
                qadd8(self._blue, p2.b),
                self._white
            )
        else:
            return CRGB(
                qadd8(self._red, p2.r),
                qadd8(self._green, p2.g),
                qadd8(self._blue, p2.b),
                p2.w
            )

    def __sub__(self, p2):
        if self._white is None and p2.w is None:
            return CRGB(
                qsub8(self._red, p2.r),
                qsub8(self._green, p2.g),
                qsub8(self._blue, p2.b)
            )
        elif self._white is not None and p2.w is not None:
            return CRGB(
                qsub8(self._red, p2.r),
                qsub8(self._green, p2.g),
                qsub8(self._blue, p2.b),
                qsub8(self._white, p2.w)
            )
        elif self._white is not None:
            return CRGB(
                qsub8(self._red, p2.r),
                qsub8(self._green, p2.g),
                qsub8(self._blue, p2.b),
                self._white
            )
        else:
            return CRGB(
                qsub8(self._red, p2.r),
                qsub8(self._green, p2.g),
                qsub8(self._blue, p2.b),
                p2.w
            )

    def __mul__(self, d):
        if self._white is None:
            return CRGB(
                qmul8(self._red, d),
                qmul8(self._green, d),
                qmul8(self._blue, d)
            )
        else:
            return CRGB(
                qmul8(self._red, d),
                qmul8(self._green, d),
                qmul8(self._blue, d),
                qmul8(self._white, d)
            )

    def __floordiv__(self, d):
        if self._white is None:
            return CRGB(
                self._red // d,
                self._green // d,
                self._blue // d
            )
        else:
            return CRGB(
                self._red // d,
                self._green // d,
                self._blue // d,
                self._white // d
            )

    def __and__(self, p2):
        if self._white is None and p2.w is None:
            return CRGB(
                self._red if self._red < p2.r else p2.r,
                self._green if self._green < p2.g else p2.g,
                self._blue if self._blue < p2.b else p2.b
            )
        elif self._white is not None and p2.w is not None:
            return CRGB(
                self._red if self._red < p2.r else p2.r,
                self._green if self._green < p2.g else p2.g,
                self._blue if self._blue < p2.b else p2.b,
                self._white if self._white < p2.w else p2.w
            )
        elif self._white is not None:
            return CRGB(
                self._red if self._red < p2.r else p2.r,
                self._green if self._green < p2.g else p2.g,
                self._blue if self._blue < p2.b else p2.b,
                self._white
            )
        else:
            return CRGB(
                self._red if self._red < p2.r else p2.r,
                self._green if self._green < p2.g else p2.g,
                self._blue if self._blue < p2.b else p2.b,
                p2.w
            )

    def __or__(self, p2):

        if self._white is None and p2.w is None:
            return CRGB(
                self._red if self._red > p2.r else p2.r,
                self._green if self._green > p2.g else p2.g,
                self._blue if self._blue > p2.b else p2.b,
            )
        elif self._white is not None and p2.w is not None:
            return CRGB(
                self._red if self._red > p2.r else p2.r,
                self._green if self._green > p2.g else p2.g,
                self._blue if self._blue > p2.b else p2.b,
                self._white if self._white > p2.w else p2.w
            )
        elif self._white is not None:
            return CRGB(
                self._red if self._red > p2.r else p2.r,
                self._green if self._green > p2.g else p2.g,
                self._blue if self._blue > p2.b else p2.b,
                self._white
            )
        else:
            return CRGB(
                self._red if self._red > p2.r else p2.r,
                self._green if self._green > p2.g else p2.g,
                self._blue if self._blue > p2.b else p2.b,
                p2.w
            )

    def __mod__(self, d):
        retval = CRGB(self)
        retval.nscale8_video(d)
        return retval


# RGB orderings, used when instantiating controllers to determine what
# order the controller should send RGB data out in, RGB being the default
# ordering.

RGB = 12
RGBW = 123
RGWB = 132
RWGB = 312
WRGB = 3012

RBG = 21
RBGW = 213
RBWG = 231
RWBG = 321
WRBG = 3021

GRB = 102
GRBW = 1023
GRWB = 1032
GWRB = 1302
WGRB = 3102

GBR = 120
GBRW = 1203
GBWR = 1230
GWBR = 1320
WGBR = 3120

BRG = 201
BRGW = 2013
BRWG = 2031
BWRG = 2301
WBRG = 3201

BGR = 210
BGRW = 2103
BGWR = 2130
BWGR = 2310
WBGR = 3210

AliceBlue = 0xF0F8FF
Amethyst = 0x9966CC
AntiqueWhite = 0xFAEBD7
Aqua = 0x00FFFF
Aquamarine = 0x7FFFD4
Azure = 0xF0FFFF
Beige = 0xF5F5DC
Bisque = 0xFFE4C4
Black = 0x000000
BlanchedAlmond = 0xFFEBCD
Blue = 0x0000FF
BlueViolet = 0x8A2BE2
Brown = 0xA52A2A
BurlyWood = 0xDEB887
CadetBlue = 0x5F9EA0
Chartreuse = 0x7FFF00
Chocolate = 0xD2691E
Coral = 0xFF7F50
CornflowerBlue = 0x6495ED
Cornsilk = 0xFFF8DC
Crimson = 0xDC143C
Cyan = 0x00FFFF
DarkBlue = 0x00008B
DarkCyan = 0x008B8B
DarkGoldenrod = 0xB8860B
DarkGray = 0xA9A9A9
DarkGrey = 0xA9A9A9
DarkGreen = 0x006400
DarkKhaki = 0xBDB76B
DarkMagenta = 0x8B008B
DarkOliveGreen = 0x556B2F
DarkOrange = 0xFF8C00
DarkOrchid = 0x9932CC
DarkRed = 0x8B0000
DarkSalmon = 0xE9967A
DarkSeaGreen = 0x8FBC8F
DarkSlateBlue = 0x483D8B
DarkSlateGray = 0x2F4F4F
DarkSlateGrey = 0x2F4F4F
DarkTurquoise = 0x00CED1
DarkViolet = 0x9400D3
DeepPink = 0xFF1493
DeepSkyBlue = 0x00BFFF
DimGray = 0x696969
DimGrey = 0x696969
DodgerBlue = 0x1E90FF
FireBrick = 0xB22222
FloralWhite = 0xFFFAF0
ForestGreen = 0x228B22
Fuchsia = 0xFF00FF
Gainsboro = 0xDCDCDC
GhostWhite = 0xF8F8FF
Gold = 0xFFD700
Goldenrod = 0xDAA520
Gray = 0x808080
Grey = 0x808080
Green = 0x008000
GreenYellow = 0xADFF2F
Honeydew = 0xF0FFF0
HotPink = 0xFF69B4
IndianRed = 0xCD5C5C
Indigo = 0x4B0082
Ivory = 0xFFFFF0
Khaki = 0xF0E68C
Lavender = 0xE6E6FA
LavenderBlush = 0xFFF0F5
LawnGreen = 0x7CFC00
LemonChiffon = 0xFFFACD
LightBlue = 0xADD8E6
LightCoral = 0xF08080
LightCyan = 0xE0FFFF
LightGoldenrodYellow = 0xFAFAD2
LightGreen = 0x90EE90
LightGrey = 0xD3D3D3
LightPink = 0xFFB6C1
LightSalmon = 0xFFA07A
LightSeaGreen = 0x20B2AA
LightSkyBlue = 0x87CEFA
LightSlateGray = 0x778899
LightSlateGrey = 0x778899
LightSteelBlue = 0xB0C4DE
LightYellow = 0xFFFFE0
Lime = 0x00FF00
LimeGreen = 0x32CD32
Linen = 0xFAF0E6
Magenta = 0xFF00FF
Maroon = 0x800000
MediumAquamarine = 0x66CDAA
MediumBlue = 0x0000CD
MediumOrchid = 0xBA55D3
MediumPurple = 0x9370DB
MediumSeaGreen = 0x3CB371
MediumSlateBlue = 0x7B68EE
MediumSpringGreen = 0x00FA9A
MediumTurquoise = 0x48D1CC
MediumVioletRed = 0xC71585
MidnightBlue = 0x191970
MintCream = 0xF5FFFA
MistyRose = 0xFFE4E1
Moccasin = 0xFFE4B5
NavajoWhite = 0xFFDEAD
Navy = 0x000080
OldLace = 0xFDF5E6
Olive = 0x808000
OliveDrab = 0x6B8E23
Orange = 0xFFA500
OrangeRed = 0xFF4500
Orchid = 0xDA70D6
PaleGoldenrod = 0xEEE8AA
PaleGreen = 0x98FB98
PaleTurquoise = 0xAFEEEE
PaleVioletRed = 0xDB7093
PapayaWhip = 0xFFEFD5
PeachPuff = 0xFFDAB9
Peru = 0xCD853F
Pink = 0xFFC0CB
Plaid = 0xCC5533
Plum = 0xDDA0DD
PowderBlue = 0xB0E0E6
Purple = 0x800080
Red = 0xFF0000
RosyBrown = 0xBC8F8F
RoyalBlue = 0x4169E1
SaddleBrown = 0x8B4513
Salmon = 0xFA8072
SandyBrown = 0xF4A460
SeaGreen = 0x2E8B57
Seashell = 0xFFF5EE
Sienna = 0xA0522D
Silver = 0xC0C0C0
SkyBlue = 0x87CEEB
SlateBlue = 0x6A5ACD
SlateGray = 0x708090
SlateGrey = 0x708090
Snow = 0xFFFAFA
SpringGreen = 0x00FF7F
SteelBlue = 0x4682B4
Tan = 0xD2B48C
Teal = 0x008080
Thistle = 0xD8BFD8
Tomato = 0xFF6347
Turquoise = 0x40E0D0
Violet = 0xEE82EE
Wheat = 0xF5DEB3
White = 0xFFFFFF
WhiteSmoke = 0xF5F5F5
Yellow = 0xFFFF00
YellowGreen = 0x9ACD32

# LED RGB color that roughly approximates
# the color of incandescent fairy lights,
# assuming that you're using FastLED
# color correction on your LEDs (recommended).
FairyLight = 0xFFE42D
# If you are using no color correction, use this
FairyLightNCC = 0xFF9D2A

from .lib8tion import *  # NOQA
from hsv2rgb import *  # NOQA
