
# @file colorutils.h
# functions for color fill, paletters, blending, and more

from .FatsLED import *
from .pixeltypes import *
from fastled_progmem import *
from math import *




# @defgroup Colorutils Color utility functions
# A variety of functions for working with color, palletes, and leds
# @{

def fill_solid(leds, numToFill, color):

    for i in range(numToFill):
        if isinstance(color, CHSV):
            leds[i].setHSV(*color.raw)
        else:
            leds[i].setRGB(*color.raw)




# fill_rainbow - fill a range of LEDs with a rainbow of colors, at
#                full saturation and full value (brightness)
def fill_rainbow(targetArray, numToFill, initialhue, deltahue):
    hsv = CHSV(initialhue, 240, 255)

    for i in range(numToFill):
        targetArray[i].setHSV(*hsv.raw)
        hsv.hue += deltahue


# fill_gradient - fill an array of colors with a smooth HSV gradient
#                 between two specified HSV colors.
#                 Since 'hue' is a value around a color wheel,
#                 there are always two ways to sweep from one hue
#                 to another.
#                 This function lets you specify which way you want
#                 the hue gradient to sweep around the color wheel:
#                   FORWARD_HUES: hue always goes clockwise
#                   BACKWARD_HUES: hue always goes counter-clockwise
#                   SHORTEST_HUES: hue goes whichever way is shortest
#                   LONGEST_HUES: hue goes whichever way is longest
#                 The default is SHORTEST_HUES, as this is nearly
#                 always what is wanted.
# 
# fill_gradient can write the gradient colors EITHER
#     (1) into an array of CRGBs (e.g., into leds[] array, or an RGB Palette)
#   OR
#     (2) into an array of CHSVs (e.g. an HSV Palette).
# 
#   In the case of writing into a CRGB array, the gradient is
#   computed in HSV space, and then HSV values are converted to RGB
#   as they're written into the RGB array.

FORWARD_HUES = 0
BACKWARD_HUES = 1
SHORTEST_HUES = 2
LONGEST_HUES = 3

saccum87 = int

# fill_gradient - fill an array of colors with a smooth HSV gradient
# between two specified HSV colors.
# Since 'hue' is a value around a color wheel,
# there are always two ways to sweep from one hue
# to another.
# This function lets you specify which way you want
# the hue gradient to sweep around the color wheel:
# 
#     FORWARD_HUES: hue always goes clockwise
#     BACKWARD_HUES: hue always goes counter-clockwise
#     SHORTEST_HUES: hue goes whichever way is shortest
#     LONGEST_HUES: hue goes whichever way is longest
# 
# The default is SHORTEST_HUES, as this is nearly
# always what is wanted.
# 
# fill_gradient can write the gradient colors EITHER
#     (1) into an array of CRGBs (e.g., into leds[] array, or an RGB Palette)
#   OR
#     (2) into an array of CHSVs (e.g. an HSV Palette).
# 
#   In the case of writing into a CRGB array, the gradient is
#   computed in HSV space, and then HSV values are converted to RGB
#   as they're written into the RGB array.


# Convenience functions to fill an array of colors with a
# two-color, three-color, or four-color gradient
def fill_gradient(targetArray, startpos, startcolor, endpos, endcolor=SHORTEST_HUES, directionCode=SHORTEST_HUES, c1=SHORTEST_HUES, c2=None, c3=None, c4=None, numLeds=None):
    
    if isinstance(directionCode, CHSV):
        directionCode, c4 = c4, directionCode
        c1 = startcolor
        c2 = endpos
        c3 = endcolor
    elif isinstance(endcolor, CHSV):
        c3 = endcolor
        c2 = endpos
        c1 = startcolor        
    elif isinstance(endpos, CHSV):
        c2 = endpos
        c1 = startcolor
        directionCode = endcolor

    if c4 is not None:
        onethird = numLeds / 3
        twothirds = (numLeds * 2) / 3
        last = numLeds - 1
        fill_gradient(targetArray, 0, c1, onethird, c2, directionCode)
        fill_gradient(targetArray, onethird, c2, twothirds, c3, directionCode)
        fill_gradient(targetArray, twothirds, c3, last, c4, directionCode)
    elif c3 is not None:
        half = (numLeds / 2)
        last = numLeds - 1
        fill_gradient(targetArray, 0, c1, half, c2, directionCode)
        fill_gradient(targetArray, half, c2, last, c3, directionCode)
    elif c2 is not None:
        last = numLeds - 1
        fill_gradient(targetArray, 0, c1, last, c2, directionCode)
    else:
        # if the points are in the wrong order, straighten them
        if endpos < startpos:
            t = endpos
            tc = CHSV(endcolor)
            endcolor = startcolor
            endpos = startpos
            startpos = t
            startcolor = tc
    
        # If we're fading toward black (val=0) or white (sat=0),
        # then set the endhue to the starthue.
        # This lets us ramp smoothly to black or white, regardless
        # of what 'hue' was set in the endcolor (since it doesn't matter)
        if endcolor.value == 0 == endcolor.saturation:
            endcolor.hue = startcolor.hue
    
        # Similarly, if we're fading in from black (val=0) or white (sat=0)
        # then set the starthue to the endhue.
        # This lets us ramp smoothly up from black or white, regardless
        # of what 'hue' was set in the startcolor (since it doesn't matter)
        if startcolor.value == 0 == startcolor.saturation:
            startcolor.hue = endcolor.hue
    
        satdistance87 = saccum87((endcolor.sat - startcolor.sat) << 7)
        valdistance87 = saccum87((endcolor.val - startcolor.val) << 7)
    
        huedelta8 = endcolor.hue - startcolor.hue
    
        if  directionCode == SHORTEST_HUES:
            directionCode = FORWARD_HUES
            if huedelta8 > 127:
                directionCode = BACKWARD_HUES
            
        if directionCode == LONGEST_HUES:
            directionCode = FORWARD_HUES
            if huedelta8 < 128:
                directionCode = BACKWARD_HUES
    
        if directionCode == FORWARD_HUES:
            huedistance87 = saccum87(huedelta8 << 7)
        else:  # directionCode == BACKWARD_HUES 
            huedistance87 = saccum87((256 - huedelta8) << 7)
            huedistance87 = -huedistance87
    
        pixeldistance = endpos - startpos
        
        
        divisor = pixeldistance if pixeldistance else 1
    
        huedelta87 = saccum87(huedistance87 / divisor)
        satdelta87 = saccum87(satdistance87 / divisor)
        valdelta87 = saccum87(valdistance87 / divisor)
    
        huedelta87 *= 2
        satdelta87 *= 2
        valdelta87 *= 2
    
        hue88 = accum88(startcolor.hue << 8)
        sat88 = accum88(startcolor.sat << 8)
        val88 = accum88(startcolor.val << 8)
        
        for i in range(startpos + 1):
            targetArray[i] = CHSV(hue88 >> 8, sat88 >> 8, val88 >> 8)
            hue88 += huedelta87
            sat88 += satdelta87
            val88 += valdelta87



# convenience synonym
fill_gradient_HSV = fill_gradient


# fill_gradient_RGB - fill a range of LEDs with a smooth RGB gradient
#                     between two specified RGB colors.
#                     Unlike HSV, there is no 'color wheel' in RGB space,
#                     and therefore there's only one 'direction' for the
#                     gradient to go, and no 'direction code' is needed.
def fill_gradient_RGB(leds, startpos, startcolor, endpos, endcolor, c1=None, c2=None, c3=None, c4=None):
    if isinstance(endpos, CRGB):
        c4 = endpos
        c3 = startcolor
        c2 = startpos
        c1 = leds
        leds = FastLED[0].leds()
        numLeds = FastLED[0].size()

        onethird = (numLeds / 3)
        twothirds = ((numLeds * 2) / 3)
        last = numLeds - 1
        fill_gradient_RGB(leds, 0, c1, onethird, c2)
        fill_gradient_RGB(leds, onethird, c2, twothirds, c3)
        fill_gradient_RGB(leds, twothirds, c3, last, c4)

    elif isinstance(startcolor, CRGB) and isinstance(startpos, CRGB):
        c3 = startcolor
        c2 = startpos
        c1 = leds
        leds = FastLED[0].leds()
        numLeds = FastLED[0].size()

        half = (numLeds / 2)
        last = numLeds - 1
        fill_gradient_RGB(leds, 0, c1, half, c2)
        fill_gradient_RGB(leds, half, c2, last, c3)

    elif isinstance(startpos, CRGB):
        c2 = startpos
        c1 = leds
        leds = FastLED[0].leds()
        numLeds = FastLED[0].size()
        last = numLeds - 1
        fill_gradient_RGB(leds, 0, c1, last, c2)
    else:

        # if the points are in the wrong order, straighten them
        if endpos < startpos:
            t = endpos
            tc = endcolor
            endcolor = startcolor
            endpos = startpos
            startpos = t
            startcolor = tc

        rdistance87 = saccum87((endcolor.r - startcolor.r) << 7)
        gdistance87 = saccum87((endcolor.g - startcolor.g) << 7)
        bdistance87 = saccum87((endcolor.b - startcolor.b) << 7)

        pixeldistance = endpos - startpos
        divisor = pixeldistance if pixeldistance else 1

        rdelta87 = saccum87(rdistance87 / divisor)
        gdelta87 = saccum87(gdistance87 / divisor)
        bdelta87 = saccum87(bdistance87 / divisor)

        rdelta87 *= 2
        gdelta87 *= 2
        bdelta87 *= 2

        r88 = accum88(startcolor.r << 8)
        g88 = accum88(startcolor.g << 8)
        b88 = accum88(startcolor.b << 8)
        for i in range(startpos, endpos):
            leds[i] = CRGB(r88 >> 8, g88 >> 8, b88 >> 8)
            r88 += rdelta87
            g88 += gdelta87
            b88 += bdelta87


# fadeLightBy and fade_video - reduce the brightness of an array
#                              of pixels all at once.  Guaranteed
#                              to never fade all the way to black.
#                              (The two names are synonyms.)
def fadeLightBy(leds, num_leds, fadeBy):
    nscale8_video(leds, num_leds, 255 - fadeBy)


def fade_video(leds, num_leds, fadeBy):
    nscale8_video(leds, num_leds, 255 - fadeBy)


# nscale8_video - scale down the brightness of an array of pixels
#                 all at once.  Guaranteed to never scale a pixel
#                 all the way down to black, unless 'scale' is zero.
def nscale8_video(leds, num_leds, scale):
    for i in range(num_leds):
        leds[i].nscale8_video(scale)

# fadeToBlackBy and fade_raw - reduce the brightness of an array
#                              of pixels all at once.  These
#                              functions will eventually fade all
#                              the way to black.
#                              (The two names are synonyms.)
def fadeToBlackBy(leds, num_leds, fadeBy):
    nscale8(leds, num_leds, 255 - fadeBy)


def fade_raw(leds, num_leds, fadeBy):
    nscale8( leds, num_leds, 255 - fadeBy)


# nscale8 - scale down the brightness of an array of pixels
#           all at once.  This function can scale pixels all the
#           way down to black even if 'scale' is not zero.
def nscale8(leds, num_leds, scale):
    for i in range(num_leds):
        leds[i].nscale8(scale)


def nscale8_raw(leds, num_leds, scale):
    nscale8(leds, num_leds, scale)


# fadeUsingColor - scale down the brightness of an array of pixels,
#                  as though it were seen through a transparent
#                  filter with the specified color.
#                  For example, if the colormask is
#                    CRGB( 200, 100, 50)
#                  then the pixels' red will be faded to 200/256ths,
#                  their green to 100/256ths, and their blue to 50/256ths.
#                  This particular example give a 'hot fade' look,
#                  with white fading to yellow, then red, then black.
#                  You can also use colormasks like CRGB::Blue to
#                  zero out the red and green elements, leaving blue
#                  (largely) the same.
def fadeUsingColor(leds, numLeds, colormask):
    fr = colormask.r
    fg = colormask.g
    fb = colormask.b

    for i in range(numLeds):
        leds[i].r = scale8_LEAVING_R1_DIRTY( leds[i].r, fr)
        leds[i].g = scale8_LEAVING_R1_DIRTY( leds[i].g, fg)
        leds[i].b = scale8(leds[i].b, fb)


# Pixel blending
# 
# blend - computes a new color blended some fraction of the way
#         between two other colors.

def blend(src1, src2, dest, count=None, amountOfsrc2=None, directionCode=SHORTEST_HUES):
    if isinstance(dest, CRGB):
        for i in range(count):
            dest[i] = blend(src1[i], src2[i], amountOfsrc2)
        return dest

    elif isinstance(dest, CHSV):
        for i in range(count):
            dest[i] = blend(src1[i], src2[i], amountOfsrc2, directionCode)
        return dest
    elif count is None:
        amountOfsrc2 = dest
        nu = CRGB(src1)
        nblend(nu, src2, amountOfsrc2)
        return nu
    else:
        amountOfsrc2 = dest
        directionCode = count if count is not None else directionCode
        nu = CHSV(src1)
        nblend(nu, src2, amountOfsrc2, directionCode)
        return nu


# nblend - destructively modifies one color, blending
#          in a given fraction of an overlay color
def nblend(existing, overlay, count, amountOfOverlay=None, directionCode=SHORTEST_HUES):
    if isinstance(existing, CRGB):
        if amountOfOverlay is None:
            amountOfOverlay = count
            if amountOfOverlay == 0:
                return existing
            if amountOfOverlay == 255:
                existing = overlay
                return existing

            # Corrected blend method, with no loss-of-precision rounding errors
            existing.red = blend8(existing.red, overlay.red, amountOfOverlay)
            existing.green = blend8(existing.green, overlay.green, amountOfOverlay)
            existing.blue = blend8(existing.blue, overlay.blue, amountOfOverlay)
            return existing

        else:
            pos = 0
            for i in range(count, -1, -1):
                nblend(existing[pos:], overlay[pos:], amountOfOverlay)
                pos += 1
    else:
        if isinstance(count, fract8):
            directionCode = amountOfOverlay if amountOfOverlay is not None else directionCode
            amountOfOverlay = count

            if amountOfOverlay == 0:
                return existing

            if amountOfOverlay == 255:
                existing = overlay
                return existing

            amountOfKeep = fract8(255 - amountOfOverlay)
            huedelta8 = overlay.hue - existing.hue

            if directionCode == SHORTEST_HUES:
                directionCode = FORWARD_HUES
                if huedelta8 > 127:
                    directionCode = BACKWARD_HUES

            if directionCode == LONGEST_HUES:
                directionCode = FORWARD_HUES
                if huedelta8 < 128:
                    directionCode = BACKWARD_HUES

            if directionCode == FORWARD_HUES:
                existing.hue = existing.hue + scale8(huedelta8, amountOfOverlay)
            else:  # directionCode == BACKWARD_HUES
                huedelta8 = -huedelta8
                existing.hue = existing.hue - scale8(huedelta8, amountOfOverlay)


            existing.sat = (
                scale8_LEAVING_R1_DIRTY(existing.sat, amountOfKeep) +
                scale8_LEAVING_R1_DIRTY(overlay.sat, amountOfOverlay)
            )
            existing.val = (
                scale8_LEAVING_R1_DIRTY(existing.val, amountOfKeep) +
                scale8_LEAVING_R1_DIRTY(overlay.val,  amountOfOverlay)
            )

            cleanup_R1()

            return existing

        else:
            if existing == overlay:
                return

            pos = 0
            for i in range(count, 0, -1):
                nblend(existing[pos:], overlay[pos:], amountOfOverlay, directionCode)

                pos += 1

# blur1d: one-dimensional blur filter. Spreads light to 2 line neighbors.
# blur2d: two-dimensional blur filter. Spreads light to 8 XY neighbors.
# 
#           0 = no spread at all
#          64 = moderate spreading
#         172 = maximum smooth, even spreading
# 
#         173..255 = wider spreading, but increasing flicker
# 
#         Total light is NOT entirely conserved, so many repeated
#         calls to 'blur' will also result in the light fading,
#         eventually all the way to black this is by design so that
#         it can be used to (slowly) clear the LEDs to black.
def blur1d(leds, numLeds, blur_amount):
    keep = 255 - blur_amount
    seep = blur_amount >> 1
    carryover = CRGB(CRGB.Black)

    for i in range(numLeds):
        cur = CRGB(leds[i])

        part = CRGB(cur)
        part.nscale8(seep)
        cur.nscale8(keep)
        cur += carryover
        if i:
            leds[i - 1] += part

        leds[i] = cur
        carryover = part

def blur2d(leds, width, height, blur_amount):
    blurRows(leds, width, height, blur_amount)
    blurColumns(leds, width, height, blur_amount)

# blurRows: perform a blur1d on every row of a rectangular matrix
def blurRows(leds, width, height, blur_amount):
    for row in range(height):
        rowbase = leds[row * width:]

        blur1d(rowbase, width, blur_amount)

# blurColumns: perform a blur1d on each column of a rectangular matrix
def blurColumns(leds, width, height, blur_amount):
    keep = 255 - blur_amount
    seep = blur_amount >> 1

    for col in range(width):
        carryover = CRGB(CRGB.Black)
        for i in range(height):
            cur = CRGB(leds[XY(col, i)])

            part = CRGB(cur)
            part.nscale8(seep)
            cur.nscale8(keep)
            cur += carryover

            if i:
                leds[XY(col, i - 1)] += part

            leds[XY(col, i)] = cur
            carryover = part



# CRGB HeatColor( uint8_t temperature)
# 
# Approximates a 'black body radiation' spectrum for
# a given 'heat' level.  This is useful for animations of 'fire'.
# Heat is specified as an arbitrary scale from 0 (cool) to 255 (hot).
# This is NOT a chromatically correct 'black body radiation'
# spectrum, but it's surprisingly close, and it's fast and small.
def HeatColor(temperature):
    heatcolor = CRGB()

    # Scale 'heat' down from 0-255 to 0-191,
    # which can then be easily divided into three
    # equal 'thirds' of 64 units each.
    t192 = scale8_video(temperature, 191)

    # calculate a value that ramps up from
    # zero to 255 in each 'third' of the scale.
    heatramp = t192 & 0x3F # 0..63
    heatramp <<= 2 # scale up to 0..252

    # now figure out which third of the spectrum we're in:
    if t192 & 0x80:
        # we're in the hottest third
        heatcolor.r = 255 # full red
        heatcolor.g = 255 # full green
        heatcolor.b = heatramp # ramp up blue
    elif t192 & 0x40:
        # we're in the middle third
        heatcolor.r = 255 # full red
        heatcolor.g = heatramp # ramp up green
        heatcolor.b = 0 # no blue
    else:
        # we're in the coolest third
        heatcolor.r = heatramp # ramp up red
        heatcolor.g = 0 # no green
        heatcolor.b = 0 # no blue

    return heatcolor


# Palettes
# 
# RGB Palettes map an 8-bit value (0..255) to an RGB color.
# 
# You can create any color palette you wish a couple of starters
# are provided: Forest, Clouds, Lava, Ocean, Rainbow, and Rainbow Stripes.
# 
# Palettes come in the traditional 256-entry variety, which take
# up 768 bytes of RAM, and lightweight 16-entry varieties.  The 16-entry
# variety automatically interpolates between its entries to produce
# a full 256-element color map, but at a cost of only 48 bytes or RAM.
# 
# Basic operation is like this: (example shows the 16-entry variety)
# 1. Declare your palette storage:
#    CRGBPalette16 myPalette
# 
# 2. Fill myPalette with your own 16 colors, or with a preset color scheme.
#    You can specify your 16 colors a variety of ways:
#      CRGBPalette16 myPalette(
#          CRGB::Black,
#          CRGB::Black,
#          CRGB::Red,
#          CRGB::Yellow,
#          CRGB::Green,
#          CRGB::Blue,
#          CRGB::Purple,
#          CRGB::Black,
# 
#          0x100000,
#          0x200000,
#          0x400000,
#          0x800000,
# 
#          CHSV( 30,255,255),
#          CHSV( 50,255,255),
#          CHSV( 70,255,255),
#          CHSV( 90,255,255)
#      )
# 
#    Or you can initiaize your palette with a preset color scheme:
#      myPalette = RainbowStripesColors_p
# 
# 3. Any time you want to set a pixel to a color from your palette, use
#    "ColorFromPalette(...)" as shown:
# 
#      uint8_t index = /* any value 0..255 */
#      leds[i] = ColorFromPalette( myPalette, index)
# 
#    Even though your palette has only 16 explicily defined entries, you
#    can use an 'index' from 0..255.  The 16 explicit palette entries will
#    be spread evenly across the 0..255 range, and the intermedate values
#    will be RGB-interpolated between adjacent explicit entries.
# 
#    It's easier to use than it sounds.
# 


class TProgmemRGBPalette16(list):

    def __new__(cls, value=None):
        if value is None:
            value = [0] * 16

        elif len(value) < 16:
            value += [0] * (16 - len(value))

        elif len(value) > 16:
            raise ValueError('16 entries are allowed in this array')

        return super(TProgmemRGBPalette16, cls).__new__(value)


class TProgmemHSVPalette16(list):
    def __new__(cls, value=None):
        if value is None:
            value = [0] * 16

        elif len(value) < 16:
            value += [0] * (16 - len(value))

        elif len(value) > 16:
            raise ValueError('16 entries are allowed in this array')

        return super(TProgmemHSVPalette16, cls).__new__(value)

TProgmemPalette16 = TProgmemRGBPalette16

class TProgmemRGBPalette32(list):
    def __new__(cls, value=None):
        if value is None:
            value = [0] * 32

        elif len(value) < 32:
            value += [0] * (32 - len(value))

        elif len(value) > 32:
            raise ValueError('32 entries are allowed in this array')

        return super(TProgmemRGBPalette32, cls).__new__(value)

class TProgmemHSVPalette32(list):
    def __new__(cls, value=None):
        if value is None:
            value = [0] * 32

        elif len(value) < 32:
            value += [0] * (32 - len(value))

        elif len(value) > 32:
            raise ValueError('32 entries are allowed in this array')

        return super(TProgmemHSVPalette32, cls).__new__(value)


TProgmemPalette32 = TProgmemRGBPalette32

TProgmemRGBGradientPalette_byte = int
TProgmemRGBGradientPalette_bytes = list
TProgmemRGBGradientPalettePtr = TProgmemRGBGradientPalette_bytes

class TRGBGradientPaletteEntryUnion(object):
    def __init__(self, index=0, r=0, g=0, b=0, dword=0, bytes_=None):
        if bytes_ is None:
            bytes_ = [0] * 4
        
        self.index = index
        self.r = r
        self.g = g
        self.b = b
        self.dword = dword
        self.bytes = bytes_
        
        
        
    
TDynamicRGBGradientPalette_byte = int
TDynamicRGBGradientPalette_bytes = list
TDynamicRGBGradientPalettePtr = TDynamicRGBGradientPalette_bytes


'''











'''
# Convert a 16-entry palette to a 256-entry palette
def UpscalePalette(srcpal, destpal):
    if isinstance(srcpal, CRGBPalette16) and isinstance(destpal, CRGBPalette256):
        for i in range(256):
            try:
                destpal[i] = ColorFromPalette(srcpal, i)
            except IndexError:
                break
    elif isinstance(srcpal, CHSVPalette16) and isinstance(destpal, CHSVPalette256):
        for i in range(256):
            try:
                destpal[i] = ColorFromPalette(srcpal, i)
            except IndexError:
                break

    elif isinstance(srcpal, CRGBPalette16) and isinstance(destpal, CRGBPalette32):
        for i in range(16):
            j = i * 2
            destpal[j + 0] = srcpal[i]
            destpal[j + 1] = srcpal[i]

    elif isinstance(srcpal, CRGBPalette32) and isinstance(destpal, CRGBPalette256):
        for i in range(256):
            try:
                destpal[i] = ColorFromPalette(srcpal, i)
            except IndexError:
                break

    elif isinstance(srcpal, CHSVPalette32) and isinstance(destpal, CHSVPalette256):
        for i in range(256):
            try:
                destpal[i] = ColorFromPalette(srcpal, i)
            except IndexError:
                break

class CHSVPalette16(object):

    def __init__(
        self,
        c00=None,
        c01=None,
        c02=None,
        c03=None,
        c04=None,
        c05=None,
        c06=None,
        c07=None,
        c08=None,
        c09=None,
        c10=None,
        c11=None,
        c12=None,
        c13=None,
        c14=None,
        c15=None,
        rhs=None
    ):
        if isinstance(c00, CHSVPalette16):
            self.entries = c00.entries[:]

        elif isinstance(c00, TProgmemHSVPalette16):
            self.entries = []
            for i in range(16):
                self.entries.append(CHSV(*FL_PGM_READ_DWORD_NEAR(c00[i])))
        elif isinstance(rhs, CHSVPalette16):
            self.entries = rhs.entries[:]
        elif isinstance(rhs, TProgmemHSVPalette16):
            self.entries = []
            for i in range(16):
                self.entries.append(CHSV(*FL_PGM_READ_DWORD_NEAR(rhs[i])))
        else:
            if c01 is not None and c02 is None:
                self.entries = []
                for i in range(16):
                    self.entries += [CHSV()]
                    
                fill_solid(self.entries, 16, c01)

            elif None not in (c01, c02) and c03 is None:
                self.entries = []
                for i in range(16):
                    self.entries += [CHSV()]
                
                fill_gradient_HSV(self.entries, 16, c01, c02)

            elif None not in (c01, c02, c03) and c04 is None:
                self.entries = []
                for i in range(16):
                    self.entries += [CHSV()]
                
                fill_gradient_HSV(self.entries, 16, c01, c02, c03)

            elif None not in (c01, c02, c03, c04) and c05 is None:
                self.entries = []
                for i in range(16):
                    self.entries += [CHSV()]
                
                fill_gradient_HSV(self.entries, 16, c01, c02, c03, c04)

            else:
                if c00 is None:
                    c00 = CHSV()
                if c01 is None:
                    c01 = CHSV()
                if c02 is None:
                    c02 = CHSV()
                if c03 is None:
                    c03 = CHSV()
                if c04 is None:
                    c04 = CHSV()
                if c05 is None:
                    c05 = CHSV()
                if c06 is None:
                    c06 = CHSV()
                if c07 is None:
                    c07 = CHSV()
                if c08 is None:
                    c08 = CHSV()
                if c09 is None:
                    c09 = CHSV()
                if c10 is None:
                    c10 = CHSV()
                if c11 is None:
                    c11 = CHSV()
                if c12 is None:
                    c12 = CHSV()
                if c13 is None:
                    c13 = CHSV()
                if c14 is None:
                    c14 = CHSV()
                if c15 is None:
                    c15 = CHSV()

                self.entries = [
                    c00,
                    c01,
                    c02,
                    c03,
                    c04,
                    c05,
                    c06,
                    c07,
                    c08,
                    c09,
                    c10,
                    c11,
                    c12,
                    c13,
                    c14,
                    c15
                ]

    def __getitem__(self, x):
        return self.entries[x]

    def __eq__(self, rhs):
        if isinstance(rhs, CHSVPalette16):
            for i in range(len(self.entries)):
                if self.entries[i] == rhs.entries[i]:
                    continue
                break
            else:
                return True

        return False

    def __ne__(self, rhs):
        return not self.__eq__(rhs)


class CHSVPalette256(object):

    def __init__(
            self,
            c00=None,
            c01=None,
            c02=None,
            c03=None,
            c04=None,
            c05=None,
            c06=None,
            c07=None,
            c08=None,
            c09=None,
            c10=None,
            c11=None,
            c12=None,
            c13=None,
            c14=None,
            c15=None,
            rhs=None,
            rhs16=None
    ):
        if isinstance(c00, CHSVPalette256):
            self.entries = c00.entries[:]
        elif isinstance(c00, CHSVPalette16):
            self.entries = []

            for i in range(256):
                self.entries += [CHSV()]
                
            UpscalePalette(c00, self)
                        
        elif isinstance(c00, TProgmemHSVPalette16):
            self.entries = []
            
            for i in range(256):
                self.entries += [CHSV()]

            c00 = CHSVPalette16(c00)
            
            UpscalePalette(c00, self)
           
        elif isinstance(rhs, CHSVPalette256):
            self.entries = rhs.entries[:]
        
        elif isinstance(rhs, TProgmemHSVPalette16):
            self.entries = []

            for i in range(256):
                self.entries += [CHSV()]

            rhs = CHSVPalette16(rhs)

            UpscalePalette(rhs, self)

        elif isinstance(rhs16, CHSVPalette16):
            self.entries = []

            for i in range(256):
                self.entries += [CHSV()]

            UpscalePalette(rhs16, self)

        else:
            if c01 is not None and c02 is None:
                self.entries = []
                for i in range(256):
                    self.entries += [CHSV()]
                fill_solid(self.entries, 16, c01)

            elif None not in (c01, c02) and c03 is None:
                self.entries = []
                for i in range(256):
                    self.entries += [CHSV()]
                fill_gradient_HSV(self.entries, 256, c01, c02)

            elif None not in (c01, c02, c03) and c04 is None:
                for i in range(256):
                    self.entries += [CHSV()]
                fill_gradient_HSV(self.entries, 256, c01, c02, c03)

            elif None not in (c01, c02, c03, c04) and c05 is None:
                self.entries = []
                for i in range(256):
                    self.entries += [CHSV()]
                fill_gradient_HSV(self.entries, 256, c01, c02, c03, c04)

            else:
                if c00 is None:
                    c00 = CHSV()
                if c01 is None:
                    c01 = CHSV()
                if c02 is None:
                    c02 = CHSV()
                if c03 is None:
                    c03 = CHSV()
                if c04 is None:
                    c04 = CHSV()
                if c05 is None:
                    c05 = CHSV()
                if c06 is None:
                    c06 = CHSV()
                if c07 is None:
                    c07 = CHSV()
                if c08 is None:
                    c08 = CHSV()
                if c09 is None:
                    c09 = CHSV()
                if c10 is None:
                    c10 = CHSV()
                if c11 is None:
                    c11 = CHSV()
                if c12 is None:
                    c12 = CHSV()
                if c13 is None:
                    c13 = CHSV()
                if c14 is None:
                    c14 = CHSV()
                if c15 is None:
                    c15 = CHSV()

                self.entries = [CHSV()] * 256
                p16 = CHSVPalette16(c00, c01, c02, c03, c04, c05, c06, c07, c08, c09, c10, c11, c12, c13, c14, c15)
                UpscalePalette(p16, self)

    def __getitem__(self, x):
        return self.entries[x]

    def __eq__(self, rhs):
        if isinstance(rhs, CHSVPalette16):
            for i in range(len(self.entries)):
                if self.entries[i] == rhs.entries[i]:
                    continue
                break
            else:
                return True

        return False

    def __ne__(self, rhs):
        return not self.__eq__(rhs)


class CRGBPalette16(object):

    def __init__(
            self,
            c00=None,
            c01=None,
            c02=None,
            c03=None,
            c04=None,
            c05=None,
            c06=None,
            c07=None,
            c08=None,
            c09=None,
            c10=None,
            c11=None,
            c12=None,
            c13=None,
            c14=None,
            c15=None,
            rhs=None,
    ):

        if isinstance(c00, CRGBPalette16):
            self.entries = c00.entries[:]
        elif isinstance(c00, TProgmemRGBPalette16):
            self.entries = []
            for i in range(16):
                self.entries.append(CRGB(*FL_PGM_READ_DWORD_NEAR(c00[i])))

        elif isinstance(rhs, CRGBPalette16):
            self.entries = rhs.entries[:]
        elif isinstance(rhs, TProgmemRGBPalette16):
            self.entries = []
            for i in range(16):
                self.entries.append(CRGB(*FL_PGM_READ_DWORD_NEAR(c00[i])))
        else:
            if c01 is not None and c02 is None:
                self.entries = []
                for i in range(16):
                    self.entries += [CRGB()]

                fill_solid(self.entries, 16, c01)

            elif None not in (c01, c02) and c03 is None:
                self.entries = []
                for i in range(16):
                    self.entries += [CRGB()]

                if isinstance(c01, CHSV):
                    tmp = []
                    fill_gradient_HSV(tmp, 16, c01, c02)
                    for i, item in tmp:
                        self.entries[i].setHSV(*item.raw)

                else:
                    fill_gradient_RGB(self.entries, 16, c01, c02)

            elif None not in (c01, c02, c03) and c04 is None:
                self.entries = []
                for i in range(16):
                    self.entries += [CRGB()]

                if isinstance(c01, CHSV):
                    tmp = []
                    fill_gradient_HSV(tmp, 16, c01, c02, c03)
                    for i, item in tmp:
                        self.entries[i].setHSV(*item.raw)

                else:
                    fill_gradient_RGB(self.entries, 16, c01, c02, c03)

            elif None not in (c01, c02, c03, c04) and c05 is None:
                self.entries = []
                for i in range(16):
                    self.entries += [CRGB()]

                if isinstance(c01, CHSV):
                    tmp = []
                    fill_gradient_HSV(tmp, 16, c01, c02, c03, c04)
                    for i, item in tmp:
                        self.entries[i].setHSV(*item.raw)

                else:
                    fill_gradient_RGB(self.entries, 16, c01, c02, c03, c04)

            else:
                if c00 is None:
                    c00 = CRGB()
                if c01 is None:
                    c01 = CRGB()
                if c02 is None:
                    c02 = CRGB()
                if c03 is None:
                    c03 = CRGB()
                if c04 is None:
                    c04 = CRGB()
                if c05 is None:
                    c05 = CRGB()
                if c06 is None:
                    c06 = CRGB()
                if c07 is None:
                    c07 = CRGB()
                if c08 is None:
                    c08 = CRGB()
                if c09 is None:
                    c09 = CRGB()
                if c10 is None:
                    c10 = CRGB()
                if c11 is None:
                    c11 = CRGB()
                if c12 is None:
                    c12 = CRGB()
                if c13 is None:
                    c13 = CRGB()
                if c14 is None:
                    c14 = CRGB()
                if c15 is None:
                    c15 = CRGB()

                self.entries = [
                    c00,
                    c01,
                    c02,
                    c03,
                    c04,
                    c05,
                    c06,
                    c07,
                    c08,
                    c09,
                    c10,
                    c11,
                    c12,
                    c13,
                    c14,
                    c15
                ]

    def __getitem__(self, x):
        return self.entries[x]

    def __eq__(self, rhs):
        if isinstance(rhs, CRGBPalette16):
            for i in range(len(self.entries)):
                if self.entries[i] == rhs.entries[i]:
                    continue
                break
            else:
                return True

        return False

    def __ne__(self, rhs):
        return not self.__eq__(rhs)


class CRGBPalette256(object):

    def __init__(
            self,
            c00=None,
            c01=None,
            c02=None,
            c03=None,
            c04=None,
            c05=None,
            c06=None,
            c07=None,
            c08=None,
            c09=None,
            c10=None,
            c11=None,
            c12=None,
            c13=None,
            c14=None,
            c15=None,
            rhs=None,
            rhs16=None
    ):
        if isinstance(c00, CRGBPalette256):
            self.entries = c00.entries[:]
        elif isinstance(c00, CRGBPalette16):
            self.entries = []

            for i in range(256):
                self.entries += [CRGB()]

            UpscalePalette(c00, self)

        elif isinstance(c00, TProgmemRGBPalette16):
            self.entries = []

            for i in range(256):
                self.entries += [CRGB()]

            c00 = CRGBPalette16(c00)

            UpscalePalette(c00, self)

        elif isinstance(c00, list):
            self.entries = []

            for i in range(256):
                self.entries += [CRGB()]

            for i, item in enumerate(c00):
                if isinstance(item, CRGB):
                    self.entries[i].setRGB(*item.raw)

                elif isinstance(item, CHSV):
                    self.entries[i].setHSV(*item.raw)

                else:
                    raise ValueError('array needs to be filled with CRGB or CHSV instances')

            if len(c00) <= 16:
                c00 = CRGBPalette16(*c00[:16])
                UpscalePalette(c00, self)

        elif isinstance(rhs, CRGBPalette256):
            self.entries = rhs.entries[:]

        elif isinstance(rhs, TProgmemRGBPalette16):
            self.entries = []

            for i in range(256):
                self.entries += [CRGB()]

            rhs = CRGBPalette16(rhs)

            UpscalePalette(rhs, self)

        elif isinstance(rhs, list):
            self.entries = []

            for i in range(256):
                self.entries += [CRGB()]

            for i, item in enumerate(rhs):
                if isinstance(item, CRGB):
                    self.entries[i].setRGB(*item.raw)

                elif isinstance(item, CHSV):
                    self.entries[i].setHSV(*item.raw)

                else:
                    raise ValueError('array needs to be filled with CRGB or CHSV instances')

            if len(rhs) <= 16:
                rhs = CRGBPalette16(*rhs[:16])
                UpscalePalette(rhs, self)

        elif isinstance(rhs16, CRGBPalette16):
            self.entries = []

            for i in range(256):
                self.entries += [CRGB()]

            UpscalePalette(rhs16, self)

        else:
            if c01 is not None and c02 is None:
                self.entries = []
                for i in range(256):
                    self.entries += [CRGB()]
                fill_solid(self.entries, 16, c01)

            elif None not in (c01, c02) and c03 is None:
                self.entries = []
                for i in range(256):
                    self.entries += [CRGB()]

                if isinstance(c01, CHSV):
                    tmp = []
                    fill_gradient_HSV(tmp, 256, c01, c02)
                    for i, item in tmp:
                        self.entries[i].setHSV(*item.raw)

                else:
                    fill_gradient_RGB(self.entries, 256, c01, c02)

            elif None not in (c01, c02, c03) and c04 is None:
                self.entries = []
                for i in range(256):
                    self.entries += [CRGB()]

                if isinstance(c01, CHSV):
                    tmp = []
                    fill_gradient_HSV(tmp, 256, c01, c02, c03)
                    for i, item in tmp:
                        self.entries[i].setHSV(*item.raw)

                else:
                    fill_gradient_RGB(self.entries, 256, c01, c02, c03)

            elif None not in (c01, c02, c03, c04) and c05 is None:
                self.entries = []
                for i in range(256):
                    self.entries += [CRGB()]

                if isinstance(c01, CHSV):
                    tmp = []
                    fill_gradient_HSV(tmp, 256, c01, c02, c03, c04)
                    for i, item in tmp:
                        self.entries[i].setHSV(*item.raw)

                else:
                    fill_gradient_RGB(self.entries, 256, c01, c02, c03, c04)

            else:
                if c00 is None:
                    c00 = CRGB()
                if c01 is None:
                    c01 = CRGB()
                if c02 is None:
                    c02 = CRGB()
                if c03 is None:
                    c03 = CRGB()
                if c04 is None:
                    c04 = CRGB()
                if c05 is None:
                    c05 = CRGB()
                if c06 is None:
                    c06 = CRGB()
                if c07 is None:
                    c07 = CRGB()
                if c08 is None:
                    c08 = CRGB()
                if c09 is None:
                    c09 = CRGB()
                if c10 is None:
                    c10 = CRGB()
                if c11 is None:
                    c11 = CRGB()
                if c12 is None:
                    c12 = CRGB()
                if c13 is None:
                    c13 = CRGB()
                if c14 is None:
                    c14 = CRGB()
                if c15 is None:
                    c15 = CRGB()

                self.entries = [CRGB()] * 256
                p16 = CRGBPalette16(c00, c01, c02, c03, c04, c05, c06, c07, c08, c09, c10, c11, c12, c13, c14, c15)
                UpscalePalette(p16, self)

    def __getitem__(self, x):
        return self.entries[x]

    def __eq__(self, rhs):
        if isinstance(rhs, CRGBPalette16):
            for i in range(len(self.entries)):
                if self.entries[i] == rhs.entries[i]:
                    continue
                break
            else:
                return True

        return False

    def __ne__(self, rhs):
        return not self.__eq__(rhs)


class CHSVPalette32(object):

    def __init__(
            self,
            c00=None,
            c01=None,
            c02=None,
            c03=None,
            c04=None,
            c05=None,
            c06=None,
            c07=None,
            c08=None,
            c09=None,
            c10=None,
            c11=None,
            c12=None,
            c13=None,
            c14=None,
            c15=None,
            rhs=None
    ):
        if isinstance(c00, CHSVPalette32):
            self.entries = c00.entries[:]

        elif isinstance(c00, TProgmemHSVPalette32):
            self.entries = []
            for i in range(16):
                self.entries.append(CHSV(*FL_PGM_READ_DWORD_NEAR(c00[i])))
        elif isinstance(rhs, CHSVPalette32):
            self.entries = rhs.entries[:]
        elif isinstance(rhs, TProgmemHSVPalette32):
            self.entries = []
            for i in range(16):
                self.entries.append(CHSV(*FL_PGM_READ_DWORD_NEAR(rhs[i])))

        else:
            if c01 is not None and c02 is None:
                self.entries = []
                for i in range(16):
                    self.entries += [CHSV()]

                fill_solid(self.entries, 16, c01)

            elif None not in (c01, c02) and c03 is None:
                self.entries = []
                for i in range(16):
                    self.entries += [CHSV()]

                fill_gradient_HSV(self.entries, 16, c01, c02)

            elif None not in (c01, c02, c03) and c04 is None:
                self.entries = []
                for i in range(16):
                    self.entries += [CHSV()]

                fill_gradient_HSV(self.entries, 16, c01, c02, c03)

            elif None not in (c01, c02, c03, c04) and c05 is None:
                self.entries = []
                for i in range(16):
                    self.entries += [CHSV()]

                fill_gradient_HSV(self.entries, 16, c01, c02, c03, c04)

            else:
                if c00 is None:
                    c00 = CHSV()
                if c01 is None:
                    c01 = CHSV()
                if c02 is None:
                    c02 = CHSV()
                if c03 is None:
                    c03 = CHSV()
                if c04 is None:
                    c04 = CHSV()
                if c05 is None:
                    c05 = CHSV()
                if c06 is None:
                    c06 = CHSV()
                if c07 is None:
                    c07 = CHSV()
                if c08 is None:
                    c08 = CHSV()
                if c09 is None:
                    c09 = CHSV()
                if c10 is None:
                    c10 = CHSV()
                if c11 is None:
                    c11 = CHSV()
                if c12 is None:
                    c12 = CHSV()
                if c13 is None:
                    c13 = CHSV()
                if c14 is None:
                    c14 = CHSV()
                if c15 is None:
                    c15 = CHSV()

                self.entries = [None] * 32

                for i in range(2):
                    self.entries[0 + i] = c00
                    self.entries[2 + i] = c01
                    self.entries[4 + i] = c02
                    self.entries[6 + i] = c03
                    self.entries[8 + i] = c04
                    self.entries[10 + i] = c05
                    self.entries[12 + i] = c06
                    self.entries[14 + i] = c07
                    self.entries[16 + i] = c08
                    self.entries[18 + i] = c09
                    self.entries[20 + i] = c10
                    self.entries[22 + i] = c11
                    self.entries[24 + i] = c12
                    self.entries[26 + i] = c13
                    self.entries[28 + i] = c14
                    self.entries[30 + i] = c15

    def __getitem__(self, x):
        return self.entries[x]

    def __eq__(self, rhs):
        if isinstance(rhs, CHSVPalette32):
            for i in range(len(self.entries)):
                if self.entries[i] == rhs.entries[i]:
                    continue
                break
            else:
                return True

        return False

    def __ne__(self, rhs):
        return not self.__eq__(rhs)


class CRGBPalette32(object):

    def __init__(
            self,
            c00=None,
            c01=None,
            c02=None,
            c03=None,
            c04=None,
            c05=None,
            c06=None,
            c07=None,
            c08=None,
            c09=None,
            c10=None,
            c11=None,
            c12=None,
            c13=None,
            c14=None,
            c15=None,
            rhs=None,
    ):

        if isinstance(c00, CRGBPalette32):
            self.entries = c00.entries[:]
        elif isinstance(c00, TProgmemRGBPalette32):
            self.entries = []
            for i in range(16):
                self.entries.append(CRGB(*FL_PGM_READ_DWORD_NEAR(c00[i])))

        elif isinstance(rhs, CRGBPalette32):
            self.entries = rhs.entries[:]
        elif isinstance(rhs, TProgmemRGBPalette32):
            self.entries = []
            for i in range(16):
                self.entries.append(CRGB(*FL_PGM_READ_DWORD_NEAR(c00[i])))

        elif isinstance(rhs, CRGBPalette16):
            self.entries = []

            for i in range(32):
                self.entries += [CRGB()]

            UpscalePalette(rhs, self)
        else:
            if c01 is not None and c02 is None:
                self.entries = []
                for i in range(16):
                    self.entries += [CRGB()]

                fill_solid(self.entries, 16, c01)

            elif None not in (c01, c02) and c03 is None:
                self.entries = []
                for i in range(16):
                    self.entries += [CRGB()]

                if isinstance(c01, CHSV):
                    tmp = []
                    fill_gradient_HSV(tmp, 16, c01, c02)
                    for i, item in tmp:
                        self.entries[i].setHSV(*item.raw)

                else:
                    fill_gradient_RGB(self.entries, 16, c01, c02)

            elif None not in (c01, c02, c03) and c04 is None:
                self.entries = []
                for i in range(16):
                    self.entries += [CRGB()]

                if isinstance(c01, CHSV):
                    tmp = []
                    fill_gradient_HSV(tmp, 16, c01, c02, c03)
                    for i, item in tmp:
                        self.entries[i].setHSV(*item.raw)

                else:
                    fill_gradient_RGB(self.entries, 16, c01, c02, c03)

            elif None not in (c01, c02, c03, c04) and c05 is None:
                self.entries = []
                for i in range(16):
                    self.entries += [CRGB()]

                if isinstance(c01, CHSV):
                    tmp = []
                    fill_gradient_HSV(tmp, 16, c01, c02, c03, c04)
                    for i, item in tmp:
                        self.entries[i].setHSV(*item.raw)

                else:
                    fill_gradient_RGB(self.entries, 16, c01, c02, c03, c04)

            else:
                if c00 is None:
                    c00 = CRGB()
                if c01 is None:
                    c01 = CRGB()
                if c02 is None:
                    c02 = CRGB()
                if c03 is None:
                    c03 = CRGB()
                if c04 is None:
                    c04 = CRGB()
                if c05 is None:
                    c05 = CRGB()
                if c06 is None:
                    c06 = CRGB()
                if c07 is None:
                    c07 = CRGB()
                if c08 is None:
                    c08 = CRGB()
                if c09 is None:
                    c09 = CRGB()
                if c10 is None:
                    c10 = CRGB()
                if c11 is None:
                    c11 = CRGB()
                if c12 is None:
                    c12 = CRGB()
                if c13 is None:
                    c13 = CRGB()
                if c14 is None:
                    c14 = CRGB()
                if c15 is None:
                    c15 = CRGB()

                self.entries = [None] * 32

                for i in range(2):
                    self.entries[0 + i] = c00
                    self.entries[2 + i] = c01
                    self.entries[4 + i] = c02
                    self.entries[6 + i] = c03
                    self.entries[8 + i] = c04
                    self.entries[10 + i] = c05
                    self.entries[12 + i] = c06
                    self.entries[14 + i] = c07
                    self.entries[16 + i] = c08
                    self.entries[18 + i] = c09
                    self.entries[20 + i] = c10
                    self.entries[22 + i] = c11
                    self.entries[24 + i] = c12
                    self.entries[26 + i] = c13
                    self.entries[28 + i] = c14
                    self.entries[30 + i] = c15

    def __getitem__(self, x):
        return self.entries[x]

    def __eq__(self, rhs):
        if isinstance(rhs, CRGBPalette32):
            for i in range(len(self.entries)):
                if self.entries[i] == rhs.entries[i]:
                    continue
                break
            else:
                return True

        return False

    def __ne__(self, rhs):
        return not self.__eq__(rhs)


NOBLEND = 0
LINEARBLEND = 1


def ColorFromPalette(pal, index, brightness=255, blendType=None):
    if isinstance(pal, CRGBPalette16):
        if blendType is None:
            blendType = LINEARBLEND

        #      hi4 = index >> 4
        hi4 = lsrX4(index)
        lo4 = index & 0x0F

        # const CRGB* entry = &(pal[0]) + hi4
        # since hi4 is always 0..15, hi4 * sizeof(CRGB) can be a single-byte value,
        # instead of the two byte 'int' that avr-gcc defaults to.
        # So, we multiply hi4 X sizeof(CRGB), giving hi4XsizeofCRGB
        hi4XsizeofCRGB = hi4 * sizeof(CRGB)
        # We then add that to a base array pointer.
        entry = CRGB(pal[hi4XsizeofCRGB])

        blend = lo4 and blendType != NOBLEND

        red1 = entry.red
        green1 = entry.green
        blue1 = entry.blue

        if blend:
            if hi4 == 15:
                entry = CRGB(pal[0])
            else:
                entry = CRGB(pal[hi4XsizeofCRGB + 1])

            f2 = lo4 << 4
            f1 = 255 - f2

            #    rgb1.nscale8(f1)
            red2 = entry.red
            red1 = scale8_LEAVING_R1_DIRTY(red1, f1)
            red2 = scale8_LEAVING_R1_DIRTY(red2, f2)
            red1 += red2

            green2 = entry.green
            green1 = scale8_LEAVING_R1_DIRTY(green1, f1)
            green2 = scale8_LEAVING_R1_DIRTY(green2, f2)
            green1 += green2

            blue2 = entry.blue
            blue1 = scale8_LEAVING_R1_DIRTY(blue1,  f1)
            blue2 = scale8_LEAVING_R1_DIRTY(blue2,  f2)
            blue1 += blue2

            cleanup_R1()

        if brightness != 255:
            if brightness:
                brightness += 1  # adjust for rounding
                # Now, since brightness is nonzero, we don't need the full scale8_video logic
                # we can just to scale8 and then add one (unless scale8 fixed) to all nonzero inputs.
                if red1:
                    red1 = scale8_LEAVING_R1_DIRTY(red1, brightness)
                    if FASTLED_SCALE8_FIXED != 1:
                        red1 += 1
                if green1:
                    green1 = scale8_LEAVING_R1_DIRTY(green1, brightness)
                    if FASTLED_SCALE8_FIXED != 1:
                        green1 += 1

                if blue1:
                    blue1 = scale8_LEAVING_R1_DIRTY(blue1, brightness)
                    if FASTLED_SCALE8_FIXED != 1:
                        blue1 += 1

                cleanup_R1()
            else:
                red1 = 0
                green1 = 0
                blue1 = 0

        return CRGB(red1, green1, blue1)

    elif isinstance(pal, TProgmemRGBPalette16):
        if blendType is None:
            blendType = LINEARBLEND
        #      hi4 = index >> 4
        hi4 = lsrX4(index)
        lo4 = index & 0x0F

        entry = CRGB(FL_PGM_READ_DWORD_NEAR(pal[0] + hi4))

        red1 = entry.red
        green1 = entry.green
        blue1 = entry.blue

        blend = lo4 and blendType != NOBLEND

        if blend:
            if hi4 == 15:
                entry = CRGB(FL_PGM_READ_DWORD_NEAR(pal[0]))
            else:
                entry = CRGB(FL_PGM_READ_DWORD_NEAR(pal[1 + hi4]))

            f2 = lo4 << 4
            f1 = 255 - f2

            red2 = entry.red
            red1 = scale8_LEAVING_R1_DIRTY(red1, f1)
            red2 = scale8_LEAVING_R1_DIRTY(red2, f2)
            red1 += red2

            green2 = entry.green
            green1 = scale8_LEAVING_R1_DIRTY(green1, f1)
            green2 = scale8_LEAVING_R1_DIRTY(green2, f2)
            green1 += green2

            blue2 = entry.blue
            blue1 = scale8_LEAVING_R1_DIRTY(blue1, f1)
            blue2 = scale8_LEAVING_R1_DIRTY(blue2, f2)
            blue1 += blue2

            cleanup_R1()


        if brightness != 255:
            if brightness:
                brightness += 1 # adjust for rounding
                # Now, since brightness is nonzero, we don't need the full scale8_video logic
                # we can just to scale8 and then add one (unless scale8 fixed) to all nonzero inputs.
                if red1:
                    red1 = scale8_LEAVING_R1_DIRTY(red1, brightness)
                    if FASTLED_SCALE8_FIXED != 1:
                        red1 += 1

                if green1:
                    green1 = scale8_LEAVING_R1_DIRTY(green1, brightness)
                    if FASTLED_SCALE8_FIXED != 1:
                        green1 += 1

                if blue1:
                    blue1 = scale8_LEAVING_R1_DIRTY(blue1, brightness)
                    if FASTLED_SCALE8_FIXED != 1:
                        blue1 += 1

                cleanup_R1()
            else:
                red1 = 0
                green1 = 0
                blue1 = 0

        return CRGB(red1, green1, blue1)

    elif isinstance(pal, CRGBPalette256):
        if blendType is None:
            blendType = NOBLEND

        entry = CRGB(pal[index])

        red = entry.red
        green = entry.green
        blue = entry.blue

        if brightness != 255:
            brightness += 1  # adjust for rounding
            red = scale8_video_LEAVING_R1_DIRTY(red, brightness)
            green = scale8_video_LEAVING_R1_DIRTY(green, brightness)
            blue= scale8_video_LEAVING_R1_DIRTY(blue, brightness)
            cleanup_R1()

        return CRGB(red, green, blue)

    elif isinstance(pal, CHSVPalette16):
        if blendType is None:
            blendType = LINEARBLEND

        #      hi4 = index >> 4
        hi4 = lsrX4(index)
        lo4 = index & 0x0F

        #  CRGB rgb1 = pal[ hi4]
        entry = CHSV(pal[hi4])

        hue1 = entry.hue
        sat1 = entry.sat
        val1 = entry.val

        blend = lo4 and (blendType != NOBLEND)

        if blend:

            if hi4 == 15:
                entry = CHSV(pal[0])
            else:
                entry = CHSV(pal[hi4 + 1])

            f2 = lo4 << 4
            f1 = 255 - f2

            hue2 = entry.hue
            sat2 = entry.sat
            val2 = entry.val

            # Now some special casing for blending to or from
            # either black or white.  Black and white don't have
            # proper 'hue' of their own, so when ramping from
            # something else to/from black/white, we set the 'hue'
            # of the black/white color to be the same as the hue
            # of the other color, so that you get the expected
            # brightness or saturation ramp, with hue staying
            # constant:

            # If we are starting from white (sat=0)
            # or black (val=0), adopt the target hue.
            if sat1 == 0 or val1 == 0:
                hue1 = hue2

            # If we are ending at white (sat=0)
            # or black (val=0), adopt the starting hue.
            if sat2 == 0 or val2 == 0:
                hue2 = hue1

            sat1 = scale8_LEAVING_R1_DIRTY(sat1, f1)
            val1 = scale8_LEAVING_R1_DIRTY(val1, f1)

            sat2 = scale8_LEAVING_R1_DIRTY(sat2, f2)
            val2 = scale8_LEAVING_R1_DIRTY(val2, f2)

            #    cleanup_R1()

            # These sums can't overflow, so no qadd8 needed.
            sat1 += sat2
            val1 += val2

            deltaHue = hue2 - hue1
            if deltaHue & 0x80:
                # go backwards
                hue1 -= scale8(256 - deltaHue, f2)
            else:
                # go forwards
                hue1 += scale8(deltaHue, f2)

            cleanup_R1()

        if brightness != 255:
            val1 = scale8_video(val1, brightness)

        return CHSV(hue1, sat1, val1)

    elif isinstance(pal, CHSVPalette256):
        if blendType is None:
            blendType = NOBLEND

        hsv = CHSV(pal[index])

        if brightness != 255:
            hsv.value = scale8_video(hsv.value, brightness)

        return hsv

    elif isinstance(pal, CRGBPalette32):
        if blendType is None:
            blendType = LINEARBLEND

        hi5 = index
        hi5 >>= 3
        lo3 = index & 0x07

        # const CRGB* entry = &(pal[0]) + hi5
        # since hi5 is always 0..31, hi4 * sizeof(CRGB) can be a single-byte value,
        # instead of the two byte 'int' that avr-gcc defaults to.
        # So, we multiply hi5 X sizeof(CRGB), giving hi5XsizeofCRGB
        hi5XsizeofCRGB = hi5 * sizeof(CRGB)
        # We then add that to a base array pointer.
        entry = CRGB(pal[hi5XsizeofCRGB])

        red1 = entry.red
        green1 = entry.green
        blue1 = entry.blue

        blend = lo3 and blendType != NOBLEND

        if blend:

            if hi5 == 31:
                entry = CRGB(pal[0])
            else:
                entry = CRGB(pal[hi5XsizeofCRGB + 1])

            f2 = lo3 << 5
            f1 = 255 - f2

            red2 = entry.red
            red1 = scale8_LEAVING_R1_DIRTY(red1, f1)
            red2 = scale8_LEAVING_R1_DIRTY(red2, f2)
            red1 += red2

            green2 = entry.green
            green1 = scale8_LEAVING_R1_DIRTY(green1, f1)
            green2 = scale8_LEAVING_R1_DIRTY(green2, f2)
            green1 += green2

            blue2 = entry.blue
            blue1 = scale8_LEAVING_R1_DIRTY(blue1,  f1)
            blue2 = scale8_LEAVING_R1_DIRTY(blue2,  f2)
            blue1 += blue2
            cleanup_R1()

        if brightness != 255:
            if brightness:
                brightness += 1 # adjust for rounding
                # Now, since brightness is nonzero, we don't need the full scale8_video logic
                # we can just to scale8 and then add one (unless scale8 fixed) to all nonzero inputs.
                if red1:
                    red1 = scale8_LEAVING_R1_DIRTY(red1, brightness)
                    if FASTLED_SCALE8_FIXED !=1:
                        red1 += 1

                if green1:
                    green1 = scale8_LEAVING_R1_DIRTY(green1, brightness)
                    if FASTLED_SCALE8_FIXED != 1:
                        green1 += 1

                if blue1:
                    blue1 = scale8_LEAVING_R1_DIRTY(blue1, brightness)
                    if FASTLED_SCALE8_FIXED != 1:
                        blue1 += 1

                cleanup_R1()
            else:
                red1 = 0
                green1 = 0
                blue1 = 0

        return CRGB(red1, green1, blue1)

    elif isinstance(pal, TProgmemRGBPalette32):
        if blendType is None:
            blendType = LINEARBLEND

        hi5 = index
        hi5 >>= 3
        lo3 = index & 0x07

        entry = CRGB(FL_PGM_READ_DWORD_NEAR(pal[hi5]))

        red1 = entry.red
        green1 = entry.green
        blue1 = entry.blue

        blend = lo3 and blendType != NOBLEND

        if blend:
            if hi5 == 31:
                entry = CRGB(FL_PGM_READ_DWORD_NEAR(pal[0]))
            else:
                entry = CRGB(FL_PGM_READ_DWORD_NEAR(pal[1 + hi5]))

            f2 = lo3 << 5
            f1 = 255 - f2

            red2 = entry.red
            red1 = scale8_LEAVING_R1_DIRTY(red1, f1)
            red2 = scale8_LEAVING_R1_DIRTY(red2, f2)
            red1 += red2

            green2 = entry.green
            green1 = scale8_LEAVING_R1_DIRTY(green1, f1)
            green2 = scale8_LEAVING_R1_DIRTY(green2, f2)
            green1 += green2

            blue2 = entry.blue
            blue1 = scale8_LEAVING_R1_DIRTY(blue1,  f1)
            blue2 = scale8_LEAVING_R1_DIRTY(blue2,  f2)
            blue1 += blue2

            cleanup_R1()

        if brightness != 255:
            if brightness:
                brightness += 1 # adjust for rounding
                # Now, since brightness is nonzero, we don't need the full scale8_video logic
                # we can just to scale8 and then add one (unless scale8 fixed) to all nonzero inputs.
                if red1:
                    red1 = scale8_LEAVING_R1_DIRTY(red1, brightness)
                    if FASTLED_SCALE8_FIXED != 1:
                        red1 += 1

                if green1:
                    green1 = scale8_LEAVING_R1_DIRTY(green1, brightness)
                    if FASTLED_SCALE8_FIXED != 1:
                        green1 += 1

                if blue1:
                    blue1 = scale8_LEAVING_R1_DIRTY(blue1, brightness)
                    if FASTLED_SCALE8_FIXED != 1:
                        blue1 += 1

                cleanup_R1()
            else:
                red1 = 0
                green1 = 0
                blue1 = 0

        return CRGB(red1, green1, blue1)

    elif isinstance(pal, CHSVPalette32):
        if blendType is None:
            blendType = LINEARBLEND

        hi5 = index
        hi5 >>= 3
        lo3 = index & 0x07

        hi5XsizeofCHSV = hi5 * sizeof(CHSV)
        entry = CHSV(pal[hi5XsizeofCHSV])

        hue1 = entry.hue
        sat1 = entry.sat
        val1 = entry.val

        blend = lo3 and blendType != NOBLEND

        if blend:
            if hi5 == 31:
                entry = CHSV(pal[0])
            else:
                entry = CHSV(pal[hi5XsizeofCHSV + 1])

            f2 = lo3 << 5
            f1 = 255 - f2

            hue2 = entry.hue
            sat2 = entry.sat
            val2 = entry.val

            # Now some special casing for blending to or from
            # either black or white.  Black and white don't have
            # proper 'hue' of their own, so when ramping from
            # something else to/from black/white, we set the 'hue'
            # of the black/white color to be the same as the hue
            # of the other color, so that you get the expected
            # brightness or saturation ramp, with hue staying
            # constant:

            # If we are starting from white (sat=0)
            # or black (val=0), adopt the target hue.
            if sat1 == 0 or val1 == 0:
                hue1 = hue2

            # If we are ending at white (sat=0)
            # or black (val=0), adopt the starting hue.
            if sat2 == 0 or val2 == 0:
                hue2 = hue1

            sat1  = scale8_LEAVING_R1_DIRTY(sat1, f1)
            val1  = scale8_LEAVING_R1_DIRTY(val1, f1)

            sat2  = scale8_LEAVING_R1_DIRTY(sat2, f2)
            val2  = scale8_LEAVING_R1_DIRTY(val2, f2)

            #    cleanup_R1()
            # These sums can't overflow, so no qadd8 needed.
            sat1 += sat2
            val1 += val2

            deltaHue = (hue2 - hue1)
            if deltaHue & 0x80:
                # go backwards
                hue1 -= scale8(256 - deltaHue, f2)
            else:
                # go forwards
                hue1 += scale8(deltaHue, f2)

            cleanup_R1()

        if brightness != 255:
            val1 = scale8_video(val1, brightness)

        return CHSV(hue1, sat1, val1)


# Fill a range of LEDs with a sequece of entryies from a palette
def fill_palette(L, N, startIndex, incIndex, pal, brightness, blendType):
    colorIndex = startIndex
    for i in range(N):
        L[i] = ColorFromPalette(pal, colorIndex, brightness, blendType)
        colorIndex += incIndex


def map_data_into_colors_through_palette(
    dataArray,
    dataCount,
    targetColorArray,
    pal,
    brightness=255,
    opacity=255,
    blendType=LINEARBLEND
):
    for i in range(dataCount):
        d = dataArray[i]
        rgb = ColorFromPalette(pal, d, brightness, blendType)
        if opacity == 255:
            targetColorArray[i] = rgb
        else:
            targetColorArray[i].nscale8(256 - opacity)
            rgb.nscale8_video(opacity)
            targetColorArray[i] += rgb


# nblendPaletteTowardPalette:
#               Alter one palette by making it slightly more like
#               a 'target palette', used for palette cross-fades.
# 
#               It does this by comparing each of the R, G, and B channels
#               of each entry in the current palette to the corresponding
#               entry in the target palette and making small adjustments:
#                 If the Red channel is too low, it will be increased.
#                 If the Red channel is too high, it will be slightly reduced.
#                 ... and likewise for Green and Blue channels.
# 
#               Additionally, there are two significant visual improvements
#               to this algorithm implemented here.  First is this:
#                 When increasing a channel, it is stepped up by ONE.
#                 When decreasing a channel, it is stepped down by TWO.
#               Due to the way the eye perceives light, and the way colors
#               are represented in RGB, this produces a more uniform apparent
#               brightness when cross-fading between most palette colors.
# 
#               The second visual tweak is limiting the number of changes
#               that will be made to the palette at once.  If all the palette
#               entries are changed at once, it can give a muddled appearance.
#               However, if only a few palette entries are changed at once,
#               you get a visually smoother transition: in the middle of the
#               cross-fade your current palette will actually contain some
#               colors from the old palette, a few blended colors, and some
#               colors from the new palette.
#               The maximum number of possible palette changes per call
#               is 48 (sixteen color entries time three channels each).
#               The default 'maximim number of changes' here is 12, meaning
#               that only approximately a quarter of the palette entries
#               will be changed per call.
def nblendPaletteTowardPalette(current, target, maxChanges):
    changes = 0
    count = 0

    p1 = current.entries
    p2 = target.entries

    totalChannels = sizeof(CRGBPalette16)
    for i in range(totalChannels):
        # if the values are equal, no changes are needed
        if p1[i] == p2[i]:
            continue

        # if the current value is less than the target, increase it by one
        if p1[i] < p2[i]:
            p1[i] += 1
            changes += 1

        # if the current value is greater than the target,
        # increase it by one (or two if it's still greater).
        if p1[i] > p2[i]:
            p1[i] += 1
            changes += 1
            if p1[i] > p2[i]:
                p1[i] += 1
        # if we've hit the maximum number of changes, exit
        if changes >= maxChanges:
            break

#  You can also define a static RGB palette very compactly in terms of a series
#  of connected color gradients.
#  For example, if you want the first 3/4ths of the palette to be a slow
#  gradient ramping from black to red, and then the remaining 1/4 of the
#  palette to be a quicker ramp to white, you specify just three points: the
#  starting black point (at index 0), the red midpoint (at index 192),
#  and the final white point (at index 255).  It looks like this:
# 
#    index:  0                                    192          255
#            |----------r-r-r-rrrrrrrrRrRrRrRrRRRR-|-RRWRWWRWWW-|
#    color: (0,0,0)                           (255,0,0)    (255,255,255)
# 
#  Here's how you'd define that gradient palette:
# 
#    DEFINE_GRADIENT_PALETTE( black_to_red_to_white_p ) {
#          0,      0,  0,  0,    /* at index 0, black(0,0,0) */
#        192,    255,  0,  0,    /* at index 192, red(255,0,0) */
#        255,    255,255,255    /* at index 255, white(255,255,255) */
#    }
# 
#  This format is designed for compact storage.  The example palette here
#  takes up just 12 bytes of PROGMEM (flash) storage, and zero bytes
#  of SRAM when not currently in use.
# 
#  To use one of these gradient palettes, simply assign it into a
#  CRGBPalette16 or a CRGBPalette256, like this:
# 
#    CRGBPalette16 pal = black_to_red_to_white_p
# 
#  When the assignment is made, the gradients are expanded out into
#  either 16 or 256 palette entries, depending on the kind of palette
#  object they're assigned to.
# 
#  IMPORTANT NOTES & CAVEATS:
# 
#  - The last 'index' position MUST BE 255!  Failure to end with
#    index 255 will result in program hangs or crashes.
# 
#  - At this point, these gradient palette definitions MUST BE
#    stored in PROGMEM on AVR-based Arduinos.  If you use the
#    DEFINE_GRADIENT_PALETTE macro, this is taken care of automatically.
# 


def DEFINE_GRADIENT_PALETTE(X):
    return TProgmemRGBGradientPalette_byte(X)


def DECLARE_GRADIENT_PALETTE(X):
    return TProgmemRGBGradientPalette_byte(X)


# Functions to apply gamma adjustments, either:
# - a single gamma adjustment to a single scalar value,
# - a single gamma adjustment to each channel of a CRGB color, or
# - different gamma adjustments for each channel of a CRFB color.
# 
# Note that the gamma is specified as a traditional floating point value
# e.g., "2.5", and as such these functions should not be called in
# your innermost pixel loops, or in animations that are extremely
# low on program storage space.  Nevertheless, if you need these
# functions, here they are.
# 
# Furthermore, bear in mind that CRGB leds have only eight bits
# per channel of color resolution, and that very small, subtle shadings
# may not be visible.
def applyGamma_video(orig=None, gammaR=None, gammaG=None, gammaB=None, brightness=None, gamma=None):
    if isinstance(orig, CRGB):
        if gammaG is None:
            if gammaR is not None:
                gamma = gammaR

            adj = CRGB()
            adj.r = applyGamma_video(orig.r, gamma)
            adj.g = applyGamma_video(orig.g, gamma)
            adj.b = applyGamma_video(orig.b, gamma)
            return adj
        else:
            adj = CRGB()
            adj.r = applyGamma_video(orig.r, gammaR)
            adj.g = applyGamma_video(orig.g, gammaG)
            adj.b = applyGamma_video(orig.b, gammaB)
            return adj
    else:
        if orig is not None:
            brightness = orig
        if gammaR is not None:
            gamma = gammaR

        orig = float(brightness) / 255.0
        adj = pow(orig, gamma) * 255.0
        result = adj
        if brightness > 0 == result:
            result = 1  # never gamma-adjust a positive number down to zero

        return result


# The "n" versions below modify their arguments in-place.
def napplyGamma_video(rgbarray, count=None, gammaR=None, gammaG=None, gammaB=None):
    if isinstance(rgbarray, CRGB):
        if gammaG is not None:
            if count is not None:
                gammaR, gammaG, gammaB = count, gammaR, gammaG

            rgb = applyGamma_video(rgbarray, gammaR, gammaG, gammaB)
            return rgb

        else:
            gamma = gammaR
            rgb = applyGamma_video(rgbarray, gamma)
            return rgb

    elif isinstance(rgbarray, list):
        if None not in (count, gammaR, gammaG, gammaB):
            for i in range(count):
                rgbarray[i] = applyGamma_video(rgbarray[i], gammaR, gammaG, gammaB)
        else:
            gamma = gammaR
            for i in range(count):
                rgbarray[i] = applyGamma_video(rgbarray[i], gamma)


# lsrX4: helper function to divide a number by 16, aka four LSR's.
# On avr-gcc, "u8 >> 4" generates a loop, which is big, and slow.
# merely forcing it to be four /=2's causes avr-gcc to emit
# a SWAP instruction followed by an AND 0x0F, which is faster, and smaller.
def lsrX4(dividend):
    dividend >>= 4
    return dividend

