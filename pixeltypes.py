
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
        return [self._red, self._green, self._blue]

    def __getitem__(self, index):
        return self.raw[index]

    def __init__(self, iR=None, iG=None, iB=None, colorcode=None, rhs=None):
        if isinstance(iR, CRGB):
            self._red, self._green, self._blue = iR.raw

        if isinstance(iR, CHSV):
            self._red = 0
            self._green = 0
            self._blue = 0
            hsv2rgb_rainbow(iR, self)

        elif isinstance(rhs, CRGB):
            self._red, self._green, self._blue = rhs.raw

        elif isinstance(rhs, CHSV):
            self._red = 0
            self._green = 0
            self._blue = 0
            hsv2rgb_rainbow(rhs, self)

        elif isinstance(colorcode, int):
            self._red = (colorcode >> 16) & 0xFF
            self._green = (colorcode >> 8) & 0xFF
            self._blue = (colorcode >> 0) & 0xFF

        else:
            if iR is None:
                iR = 0
            if iG is None:
                iG = 0
            if iB is None:
                iB = 0

            self._red = iR
            self._green = iG
            self._blue - iB

    def setRGB(self, nR, nG, nB):
        self._red = nR
        self._green = nG
        self._blue = nB
        return self

    def setHSV(self, hue, sat, val):
        hsv2rgb_rainbow(CHSV(hue, sat, val), self)
        return self

    def setHue(self, hue):
        hsv2rgb_rainbow(CHSV(hue, 255, 255), self)
        return self

    def setColorCode(self, colorcode):
        self._red = (colorcode >> 16) & 0xFF
        self._green = (colorcode >> 8) & 0xFF
        self._blue = (colorcode >> 0) & 0xFF
        return self

    def __iadd__(self, rhs):
        self._red = qadd8(self._red, rhs.r)
        self._green = qadd8(self._green, rhs.g)
        self._blue = qadd8(self._blue, rhs.b)
        return self

    def addToRGB(self, d):
        self._red = qadd8(self._red, d)
        self._green = qadd8(self._green, d)
        self._blue = qadd8(self._blue, d)
        return self

    def __isub__(self, rhs):
        if isinstance(rhs, CRGB):
            self._red = qsub8(self._red, rhs.r)
            self._green = qsub8(self._green, rhs.g)
            self._blue = qsub8(self._blue, rhs.b)
        else:
            self.subtractFromRGB(rhs)
        return self

    def subtractFromRGB(self, d):
        self._red = qsub8(self._red, d)
        self._green = qsub8(self._green, d)
        self._blue = qsub8(self._blue, d)
        return self

    def __idiv__(self, d):
        self._red /= d
        self._green /= d
        self._blue /= d
        return self

    def __irshift__(self, d):
        self._red >>= d
        self._green >>= d
        self._blue >>= d
        return self

    def __imul__(self, d):
        self._red = qmul8(self._red, d)
        self._green = qmul8(self._green, d)
        self._blue = qmul8(self._blue, d)
        return self

    def nscale8_video(self, scaledown):
        self._red, self._green, self._blue = nscale8x3_video(
            self._red,
            self._green,
            self._blue,
            scaledown
        )
        return self

    def __imod__(self, scaledown):
        self._red, self._green, self._blue = nscale8x3_video(
            self._red,
            self._green,
            self._blue,
            scaledown
        )
        return self

    def fadeLightBy(self, fadefactor):
        self._red, self._green, self._blue = nscale8x3_video(
            self._red,
            self._green,
            self._blue,
            255 - fadefactor
        )
        return self

    def scale8(self, scaledown):
        if isinstance(scaledown, CRGB):
            out = CRGB()
            out.r = scale8(self._red, scaledown.r)
            out.g = scale8(self._green, scaledown.g)
            out.b = scale8(self._blue, scaledown.b)
            return out
        else:
            self._red, self._green, self._blue = nscale8x3(
                self._red,
                self._green,
                self._blue,
                scaledown
            )
            return self

    def nscale8(self, scaledown):
        self._red = scale8(self._red, scaledown.r)
        self._green = scale8(self._green, scaledown.g)
        self._blue = scale8(self._blue, scaledown.b)
        return self

    def fadeToBlackBy(self, fadefactor):
        self._red, self._green, self._blue = nscale8x3(
            self._red,
            self._green,
            self._blue,
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
        else:
            if rhs > self._red:
                self._red = rhs
            if rhs > self._green:
                self._green = rhs
            if rhs > self._blue:
                self._blue = rhs

        return self

    def __iand__(self, rhs):
        if isinstance(rhs, CRGB):
            if rhs.r < self._red:
                self._red = rhs.r
            if rhs.g < self._green:
                self._green = rhs.g
            if rhs.b < self._blue:
                self._blue = rhs.b
        else:
            if rhs < self._red:
                self._red = rhs
            if rhs < self._green:
                self._green = rhs
            if rhs < self._blue:
                self._blue = rhs

        return self

    def __bool__(self):
        return self._red != 0 or self._green != 0 or self._blue != 0

    def __neg__(self):
        retval = CRGB()
        retval.r = 255 - self._red
        retval.g = 255 - self._green
        retval.b = 255 - self._blue
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
        luma = (
                scale8_LEAVING_R1_DIRTY(self._red, 54) +
                scale8_LEAVING_R1_DIRTY(self._green, 183) +
                scale8_LEAVING_R1_DIRTY(self._blue, 18)
        )
        cleanup_R1()
        return luma

    def getAverageLight(self):
        if FASTLED_SCALE8_FIXED == 1:
            eightyfive = 85
        else:
            eightyfive = 86

        avg = (
                scale8_LEAVING_R1_DIRTY(self._red, eightyfive) +
                scale8_LEAVING_R1_DIRTY(self._green, eightyfive) +
                scale8_LEAVING_R1_DIRTY(self._blue, eightyfive)
        )
        cleanup_R1()
        return avg

    def maximizeBrightness(self, limit=255):
        max_ = self._red
        if self._green > max_:
            max_ = self._green
        if self._blue > max_:
            max_ = self._blue

        # stop div/0 when color is black
        if max_ > 0:
            factor = (limit * 256) / max_
            self._red = (self._red * factor) / 256
            self._green = (self._green * factor) / 256
            self._blue = (self._blue * factor) / 256

    def lerp8(self, other, frac):
        ret = CRGB()
        ret.r = lerp8by8(self._red, other.r, frac)
        ret.g = lerp8by8(self._green, other.g, frac)
        ret.b = lerp8by8(self._blue, other.b, frac)

        return ret

    def lerp16(self, other, frac):
        ret = CRGB()
        ret.r = lerp16by16(self._red << 8, other.r << 8, frac) >> 8
        ret.g = lerp16by16(self._green << 8, other.g << 8, frac) >> 8
        ret.b = lerp16by16(self._blue << 8, other.b << 8, frac) >> 8

        return ret

    def getParity(self):
        sum_ = self._red + self._green + self._blue
        return sum_ & 0x01

    def setParity(self, parity):
        curparity = self.getParity()

        if parity == curparity:
            return

        if parity:
            # going 'up'
            if 255 > self._blue > 0:
                if self._red == self._green == self._blue:
                    self._red += 1
                    self._green += 1

                self._blue += 1
            elif 255 > self._red > 0:
                self._red += 1
            elif 255 > self._green > 0:
                self._green += 1
            else:
                if self._red == self._green == self._blue:
                    self._red ^= 0x01
                    self._green ^= 0x01

                self._blue ^= 0x01

        else:
            # going 'down'
            if self._blue > 1:
                if self._red == self._green == self._blue:
                    self._red -= 1
                    self._green -= 1

                self._blue -= 1
            elif self._green > 1:
                self._green -= 1
            elif self._red > 1:
                self._red -= 1
            else:
                if self._red == self._green == self._blue:
                    self._red ^= 0x01
                    self._green ^= 0x01

                self._blue ^= 0x01

    def __eq__(self, rhs):
        return self._red == rhs.r and self._green == rhs.g and self._blue == rhs.b

    def __ne__(self, rhs):
        return not self.__eq__(rhs)

    def __lt__(self, rhs):
        sl = self._red + self._green + self._blue
        sr = rhs.r + rhs.g + rhs.b
        return sl < sr

    def __gt__(self, rhs):
        sl = self._red + self._green + self._blue
        sr = rhs.r + rhs.g + rhs.b
        return sl > sr

    def __le__(self, rhs):
        sl = self._red + self._green + self._blue
        sr = rhs.r + rhs.g + rhs.b
        return sl <= sr

    def __ge__(self, rhs):
        sl = self._red + self._green + self._blue
        sr = rhs.r + rhs.g + rhs.b
        return sl >= sr

    def __add__(self, p2):
        return CRGB(
            qadd8(self._red, p2.r),
            qadd8(self._green, p2.g),
            qadd8(self._blue, p2.b)
        )

    def __sub__(self, p2):
        return CRGB(
            qsub8(self._red, p2.r),
            qsub8(self._green, p2.g),
            qsub8(self._blue, p2.b)
        )

    def __mul__(self, d):
        return CRGB(
            qmul8(self._red, d),
            qmul8(self._green, d),
            qmul8(self._blue, d)
        )

    def __floordiv__(self, d):
        return CRGB(
            self._red // d,
            self._green // d,
            self._blue // d
        )

    def __and__(self, p2):
        return CRGB(
            self._red if self._red < p2.r else p2.r,
            self._green if self._green < p2.g else p2.g,
            self._blue if self._blue < p2.b else p2.b
        )

    def __or__(self, p2):
        return CRGB(
            self._red if self._red > p2.r else p2.r,
            self._green if self._green > p2.g else p2.g,
            self._blue if self._blue > p2.b else p2.b
        )

    def __mod__(self, d):
        retval = CRGB(self)
        retval.nscale8_video(d)
        return retval


# RGB orderings, used when instantiating controllers to determine what
# order the controller should send RGB data out in, RGB being the default
# ordering.
RGB = 12
RBG = 21
GRB = 102
GBR = 120
BRG = 201
BGR = 210

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
