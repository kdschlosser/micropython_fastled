
from . import *


def FORCE_REFERENCE(_):
    pass


# hsv2rgb_rainbow - convert a hue, saturation, and value to RGB
#                   using a visually balanced rainbow (vs a straight
#                   mathematical spectrum).
#                   This 'rainbow' yields better yellow and orange
#                   than a straight 'spectrum'.
# 
#                   NOTE: here hue is 0-255, not just 0-191
def hsv2rgb_rainbow(hsv, rgb, numLeds=None):
    if numLeds is None:
        # Yellow has a higher inherent brightness than
        # any other color; 'pure' yellow is perceived to
        # be 93% as bright as white.  In order to make
        # yellow appear the correct relative brightness,
        # it has to be rendered brighter than all other
        # colors.
        # Level Y1 is a moderate boost, the default.
        # Level Y2 is a strong boost.
        Y1 = 1
        Y2 = 0

        # G2: Whether to divide all greens by two.
        # Depends GREATLY on your particular LEDs
        G2 = 0

        # Gscale: what to scale green down by.
        # Depends GREATLY on your particular LEDs
        Gscale = 0

        hue = hsv.hue
        sat = hsv.sat
        val = hsv.val

        offset = hue & 0x1F  # 0..31

        # offset8 = offset * 8
        offset8 = offset

        # On ARM and other non-AVR platforms, we just shift 3.
        offset8 <<= 3

        third = scale8(offset8, (256 / 3))  # max = 85
        r = 0
        g = 0
        b = 0

        if not hue & 0x80:
            # 0XX
            if not hue & 0x40:
                # 00X
                # section 0-1
                if not hue & 0x20:
                    # 000
                    # case 0: # R -> O
                    r = K255 - third
                    g = third
                    b = 0
                    FORCE_REFERENCE(b)
                else:
                    # 001
                    # case 1: # O -> Y
                    if Y1:
                        r = K171
                        g = K85 + third
                        b = 0
                        FORCE_REFERENCE(b)

                    if Y2:
                        r = K170 + third
                        # uint8_t twothirds = (third << 1);
                        twothirds = scale8(offset8, ((256 * 2) / 3))  # max=170
                        g = K85 + twothirds
                        b = 0
                        FORCE_REFERENCE(b)

            else:
                # 01X
                # section 2-3
                if not hue & 0x20:
                    # 010
                    # case 2: # Y -> G
                    if Y1:
                        # uint8_t twothirds = (third << 1);
                        twothirds = scale8(offset8, ((256 * 2) / 3))  # max=170
                        r = K171 - twothirds
                        g = K170 + third
                        b = 0
                        FORCE_REFERENCE(b)

                    if Y2:
                        r = K255 - offset8
                        g = K255
                        b = 0
                        FORCE_REFERENCE(b)

                else:
                    # 011
                    # case 3: # G -> A
                    r = 0
                    FORCE_REFERENCE(r)
                    g = K255 - third
                    b = third

        else:
            # section 4-7
            # 1XX
            if not hue & 0x40:
                # 10X
                if not hue & 0x20:
                    # 100
                    # case 4: # A -> B
                    r = 0
                    FORCE_REFERENCE(r)
                    # uint8_t twothirds = (third << 1);
                    twothirds = scale8(offset8, ((256 * 2) / 3))  # max=170
                    g = K171 - twothirds  # K170?
                    b = K85 + twothirds

                else:
                    # 101
                    # case 5: # B -> P
                    r = third
                    g = 0
                    FORCE_REFERENCE(g)
                    b = K255 - third

            else:
                if not hue & 0x20:
                    # 110
                    # case 6: # P -- K
                    r = K85 + third
                    g = 0
                    FORCE_REFERENCE(g)
                    b = K171 - third

                else:
                    # 111
                    # case 7: # K -> R
                    r = K170 + third
                    g = 0
                    FORCE_REFERENCE(g)
                    b = K85 - third

        # This is one of the good places to scale the green down,
        # although the client can scale green down as well.
        if G2:
            g >>= 1

        if Gscale:
            g = scale8_video_LEAVING_R1_DIRTY(g, Gscale)

        # Scale down colors if we're desaturated at all
        # and add the brightness_floor to r, g, and b.
        if sat != 255:
            if sat == 0:
                r = 255
                g = 255
                b = 255
            else:
                # nscale8x3_video( r, g, b, sat);
                if FASTLED_SCALE8_FIXED == 1:
                    if r:
                        r = scale8_LEAVING_R1_DIRTY(r, sat)
                    if g:
                        g = scale8_LEAVING_R1_DIRTY(g, sat)
                    if b:
                        b = scale8_LEAVING_R1_DIRTY(b, sat)
                else:
                    if r:
                        r = scale8_LEAVING_R1_DIRTY(r, sat) + 1
                    if g:
                        g = scale8_LEAVING_R1_DIRTY(g, sat) + 1
                    if b:
                        b = scale8_LEAVING_R1_DIRTY(b, sat) + 1

                cleanup_R1()

                desat = 255 - sat
                desat = scale8(desat, desat)

                brightness_floor = desat
                r += brightness_floor
                g += brightness_floor
                b += brightness_floor

        # Now scale everything down if we're at value < 255.
        if val != 255:
            val = scale8_video_LEAVING_R1_DIRTY(val, val)
            if val == 0:
                r = 0
                g = 0
                b = 0
            else:
                # nscale8x3_video( r, g, b, val);
                if FASTLED_SCALE8_FIXED == 1:
                    if r:
                        r = scale8_LEAVING_R1_DIRTY(r, val)
                    if g:
                        g = scale8_LEAVING_R1_DIRTY(g, val)
                    if b:
                        b = scale8_LEAVING_R1_DIRTY(b, val)
                else:
                    if r:
                        r = scale8_LEAVING_R1_DIRTY(r, val) + 1
                    if g:
                        g = scale8_LEAVING_R1_DIRTY(g, val) + 1
                    if b:
                        b = scale8_LEAVING_R1_DIRTY(b, val) + 1

                cleanup_R1()

        # Here we have the old AVR "missing std X+n" problem again
        # It turns out that fixing it winds up costing more than
        # not fixing it.
        # To paraphrase Dr Bronner, profile! profile! profile!
        # asm volatile(  ""  :  :  : "r26", "r27" );
        # asm volatile (" movw r30, r26 \n" : : : "r30", "r31");
        rgb.r = r
        rgb.g = g
        rgb.b = b

    else:
        for i in range(numLeds):
            hsv2rgb_rainbow(hsv[i], rgb[i])


HUE_MAX_RAINBOW = 255


# hsv2rgb_spectrum - convert a hue, saturation, and value to RGB
#                    using a mathematically straight spectrum (vs
#                    a visually balanced rainbow).
#                    This 'spectrum' will have more green & blue
#                    than a 'rainbow', and less yellow and orange.
# 
#                    NOTE: here hue is 0-255, not just 0-191

def hsv2rgb_spectrum(hsv, rgb, numLeds=None):
    if numLeds is None:
        hsv2 = CHSV(hsv)
        hsv2.hue = scale8(hsv2.hue, 191)
        hsv2rgb_raw(hsv2, rgb)
    else:
        for i in range(numLeds):
            hsv2rgb_spectrum(hsv[i], rgb[i])


HUE_MAX_SPECTRUM = 255


# hsv2rgb_raw - convert hue, saturation, and value to RGB.
#               This 'spectrum' conversion will be more green & blue
#               than a real 'rainbow', and the hue is specified just
#               in the range 0-191.  Together, these result in a
#               slightly faster conversion speed, at the expense of
#               color balance.
# 
#               NOTE: Hue is 0-191 only!
#               Saturation & value are 0-255 each.
#

def hsv2rgb_raw(hsv, rgb, numLeds=None):
    if numLeds is None:
        hsv2rgb_raw_C(hsv, rgb)
    else:
        for i in range(numLeds):
            hsv2rgb_raw(hsv[i], rgb[i])


HUE_MAX = 191


# rgb2hsv_approximate - recover _approximate_ HSV values from RGB.
# 
#   NOTE 1: This function is a long-term work in process; expect
#   results to change slightly over time as this function is
#   refined and improved.
# 
#   NOTE 2: This function is most accurate when the input is an
#   RGB color that came from a fully-saturated HSV color to start
#   with.  E.g. CHSV( hue, 255, 255) -> CRGB -> CHSV will give
#   best results.
# 
#   NOTE 3: This function is not nearly as fast as HSV-to-RGB.
#   It is provided for those situations when the need for this
#   function cannot be avoided, or when extremely high performance
#   is not needed.
# 
#   NOTE 4: Why is this 'only' an "approximation"?
#   Not all RGB colors have HSV equivalents!  For example, there
#   is no HSV value that will ever convert to RGB(255,255,0) using
#   the code provided in this library.   So if you try to
#   convert RGB(255,255,0) 'back' to HSV, you'll necessarily get
#   only an approximation.  Emphasis has been placed on getting
#   the 'hue' as close as usefully possible, but even that's a bit
#   of a challenge.  The 8-bit HSV and 8-bit RGB color spaces
#   are not a "bijection".
# 
#   Nevertheless, this function does a pretty good job, particularly
#   at recovering the 'hue' from fully saturated RGB colors that
#   originally came from HSV rainbow colors.  So if you start
#   with CHSV(hue_in,255,255), and convert that to RGB, and then
#   convert it back to HSV using this function, the resulting output
#   hue will either exactly the same, or very close (+/-1).
#   The more desaturated the original RGB color is, the rougher the
#   approximation, and the less accurate the results.
# 
def rgb2hsv_approximate(rgb):
    r = rgb.r
    g = rgb.g
    b = rgb.b

    # find desaturation
    desat = 255
    if r < desat:
        desat = r
    if g < desat:
        desat = g
    if b < desat:
        desat = b

    # remove saturation from all channels
    r -= desat
    g -= desat
    b -= desat

    # Serial.print("desat="); Serial.print(desat); Serial.println("");

    # uint8_t orig_desat = sqrt16( desat * 256);
    # Serial.print("orig_desat="); Serial.print(orig_desat); Serial.println("");

    # saturation is opposite of desaturation
    s = 255 - desat
    # Serial.print("s.1="); Serial.print(s); Serial.println("");

    if s != 255:
        # undo 'dimming' of saturation
        s = 255 - sqrt16((255 - s) * 256)

    # without lib8tion: float ... ew ... sqrt... double ew, or rather, ew ^ 0.5
    # if( s != 255 ) s = (255 - (256.0 * sqrt( (float)(255-s) / 256.0)));
    # Serial.print("s.2="); Serial.print(s); Serial.println("");

    # at least one channel is now zero
    # if all three channels are zero, we had a
    # shade of gray.
    if (r + g + b) == 0:
        # we pick hue zero for no special reason
        return CHSV(0, 0, 255 - s)

    # scale all channels up to compensate for desaturation
    if s < 255:
        if s == 0:
            s = 1

        scaleup = 65535 / s
        r = (r * scaleup) / 256
        g = (g * scaleup) / 256
        b = (b * scaleup) / 256

    # Serial.print("r.2="); Serial.print(r); Serial.println("");
    # Serial.print("g.2="); Serial.print(g); Serial.println("");
    # Serial.print("b.2="); Serial.print(b); Serial.println("");

    total = r + g + b

    # Serial.print("total="); Serial.print(total); Serial.println("");

    # scale all channels up to compensate for low values
    if total < 255:
        if total == 0:
            total = 1

        scaleup = 65535 / total

        r = (r * scaleup) / 256
        g = (g * scaleup) / 256
        b = (b * scaleup) / 256

    # Serial.print("r.3="); Serial.print(r); Serial.println("");
    # Serial.print("g.3="); Serial.print(g); Serial.println("");
    # Serial.print("b.3="); Serial.print(b); Serial.println("");

    if total > 255:
        v = 255
    else:
        v = qadd8(desat, total)
    # undo 'dimming' of brightness
    if v != 255:
        v = sqrt16(v * 256)

    # without lib8tion: float ... ew ... sqrt... double ew, or rather, ew ^ 0.5
    # if( v != 255) v = (256.0 * sqrt( (float)(v) / 256.0));

    # Serial.print("v="); Serial.print(v); Serial.println("");

    # Serial.print("s.3="); Serial.print(s); Serial.println("");

    # since this wasn't a pure shade of gray,
    # the interesting question is what hue is it

    # start with which channel is highest
    # (ties don't matter)
    highest = r
    if g > highest:
        highest = g
    if b > highest:
        highest = b

    if highest == r:
        # Red is highest.
        # Hue could be Purple/Pink-Red,Red-Orange,Orange-Yellow
        if g == 0:
            # if green is zero, we're in Purple/Pink-Red
            h = (HUE_PURPLE + HUE_PINK) / 2
            h += scale8(qsub8(r, 128), FIXFRAC8(48, 128))
        elif (r - g) > g:
            # if R-G > G then we're in Red-Orange
            h = HUE_RED
            h += scale8(g, FIXFRAC8(32, 85))
        else:
            # R-G < G, we're in Orange-Yellow
            h = HUE_ORANGE
            h += scale8(qsub8((g - 85) + (171 - r), 4), FIXFRAC8(32, 85))  # 221

    elif highest == g:
        # Green is highest
        # Hue could be Yellow-Green, Green-Aqua
        if b == 0:
            # if Blue is zero, we're in Yellow-Green
            #   G = 171..255
            #   R = 171..  0
            h = HUE_YELLOW
            radj = scale8(qsub8(171, r), 47)  # 171..0 -> 0..171 -> 0..31
            gadj = scale8(qsub8(g, 171), 96)  # 171..255 -> 0..84 -> 0..31;
            rgadj = radj + gadj
            hueadv = rgadj / 2
            h += hueadv
            # h += scale8( qadd8( 4, qadd8((g - 128), (128 - r))),
            #             FIXFRAC8(32,255)); #
        else:
            # if Blue is nonzero we're in Green-Aqua
            if (g - b) > b:
                h = HUE_GREEN
                h += scale8(b, FIXFRAC8(32, 85))
            else:
                h = HUE_AQUA
                h += scale8(qsub8(b, 85), FIXFRAC8(8, 42))

    else:  # /* highest == b */ {
        # Blue is highest
        # Hue could be Aqua/Blue-Blue, Blue-Purple, Purple-Pink
        if r == 0:
            # if red is zero, we're in Aqua/Blue-Blue
            h = HUE_AQUA + ((HUE_BLUE - HUE_AQUA) / 4)
            h += scale8(qsub8(b, 128), FIXFRAC8(24, 128))
        elif (b - r) > r:
            # B-R > R, we're in Blue-Purple
            h = HUE_BLUE
            h += scale8(r, FIXFRAC8(32, 85))
        else:
            # B-R < R, we're in Purple-Pink
            h = HUE_PURPLE
            h += scale8(qsub8(r, 85), FIXFRAC8(32, 85))

    h += 1
    return CHSV(h, s, v)


# Functions to convert HSV colors to RGB colors.
# 
#  The basically fall into two groups: spectra, and rainbows.
#  Spectra and rainbows are not the same thing.  Wikipedia has a good
#  illustration here
#   http:# upload.wikimedia.org/wikipedia/commons/f/f6/Prism_compare_rainbow_01.png
#  from this article
#   http:# en.wikipedia.org/wiki/Rainbow#Number_of_colours_in_spectrum_or_rainbow
#  that shows a 'spectrum' and a 'rainbow' side by side.  Among other
#  differences, you'll see that a 'rainbow' has much more yellow than
#  a plain spectrum.  "Classic" LED color washes are spectrum based, and
#  usually show very little yellow.
# 
#  Wikipedia's page on HSV color space, with pseudocode for conversion
#  to RGB color space
#   http:# en.wikipedia.org/wiki/HSL_and_HSV
#  Note that their conversion algorithm, which is (naturally) very popular
#  is in the "maximum brightness at any given hue" style, vs the "uniform
#  brightness for all hues" style.
# 
#  You can't have both; either purple is the same brightness as red, e.g
#    red = #FF0000 and purple = #800080 -> same "total light" output
#  OR purple is 'as bright as it can be', e.g.
#    red = #FF0000 and purple = #FF00FF -> purple is much brighter than red.
#  The colorspace conversions here try to keep the apparent brightness
#  constant even as the hue varies.
# 
#  Adafruit's "Wheel" function, discussed here
#   http:# forums.adafruit.com/viewtopic.php?f=47&t=22483
#  is also of the "constant apparent brightness" variety.
# 
#  TODO: provide the 'maximum brightness no matter what' variation.
# 
#  See also some good, clear Arduino C code from Kasper Kamperman
#   http:# www.kasperkamperman.com/blog/arduino/arduino-programming-hsb-to-rgb/
#  which in turn was was based on Windows C code from "nico80"
#   http:# www.codeproject.com/Articles/9207/An-HSB-RGBA-colour-picker

def APPLY_DIMMING(X):
    return X


HSV_SECTION_6 = 0x20
HSV_SECTION_3 = 0x40


def hsv2rgb_raw_C(hsv, rgb):
    # Convert hue, saturation and brightness ( HSV/HSB ) to RGB
    # "Dimming" is used on saturation and brightness to make
    # the output more visually linear.

    # Apply dimming curves
    value = APPLY_DIMMING(hsv.val)
    saturation = hsv.sat

    # The brightness floor is minimum number that all of
    # R, G, and B will be set to.
    invsat = APPLY_DIMMING(255 - saturation)
    brightness_floor = (value * invsat) / 256

    # The color amplitude is the maximum amount of R, G, and B
    # that will be added on top of the brightness_floor to
    # create the specific hue desired.
    color_amplitude = value - brightness_floor

    # Figure out which section of the hue wheel we're in,
    # and how far offset we are withing that section
    section = hsv.hue / HSV_SECTION_3  # 0..2
    offset = hsv.hue % HSV_SECTION_3   # 0..63

    rampup = offset  # 0..63
    rampdown = (HSV_SECTION_3 - 1) - offset  # 63..0

    # We now scale rampup and rampdown to a 0-255 range -- at least
    # in theory, but here's where architecture-specific decsions
    # come in to play:
    # To scale them up to 0-255, we'd want to multiply by 4.
    # But in the very next step, we multiply the ramps by other
    # values and then divide the resulting product by 256.
    # So which is faster?
    #   ((ramp * 4) * othervalue) / 256
    # or
    #   ((ramp    ) * othervalue) /  64
    # It depends on your processor architecture.
    # On 8-bit AVR, the "/ 256" is just a one-cycle register move,
    # but the "/ 64" might be a multicycle shift process. So on AVR
    # it's faster do multiply the ramp values by four, and then
    # divide by 256.
    # On ARM, the "/ 256" and "/ 64" are one cycle each, so it's
    # faster to NOT multiply the ramp values by four, and just to
    # divide the resulting product by 64 (instead of 256).
    # Moral of the story: trust your profiler, not your insticts.

    # Since there's an AVR assembly version elsewhere, we'll
    # assume what we're on an architecture where any number of
    # bit shifts has roughly the same cost, and we'll remove the
    # redundant math at the source level:

    #  # scale up to 255 range
    #  # rampup *= 4; # 0..252
    #  # rampdown *= 4; # 0..252

    # compute color-amplitude-scaled-down versions of rampup and rampdown
    rampup_amp_adj = (rampup * color_amplitude) / (256 / 4)
    rampdown_amp_adj = (rampdown * color_amplitude) / (256 / 4)

    # add brightness_floor offset to everything
    rampup_adj_with_floor = rampup_amp_adj + brightness_floor
    rampdown_adj_with_floor = rampdown_amp_adj + brightness_floor

    if section:
        if section == 1:
            # section 1: 0x40..0x7F
            rgb.r = brightness_floor
            rgb.g = rampdown_adj_with_floor
            rgb.b = rampup_adj_with_floor
        else:
            # section 2; 0x80..0xBF
            rgb.r = rampup_adj_with_floor
            rgb.g = brightness_floor
            rgb.b = rampdown_adj_with_floor

    else:
        # section 0: 0x00..0x3F
        rgb.r = rampdown_adj_with_floor
        rgb.g = rampup_adj_with_floor
        rgb.b = brightness_floor


# Sometimes the compiler will do clever things to reduce
# code size that result in a net slowdown, if it thinks that
# a variable is not used in a certain location.
# This macro does its best to convince the compiler that
# the variable is used in this location, to help control
# code motion and de-duplication that would result in a slowdown.

K255 = 255
K171 = 171
K170 = 170
K85 = 85


def FIXFRAC8(N, D):
    return (N * 256) / D

# This function is only an approximation, and it is not
# nearly as fast as the normal HSV-to-RGB conversion.
# See extended notes in the .h file.


def rgb2rgbw(rgb, rgbw):
    r = rgb.r
    g = rgb.g
    b = rgb.g

    if r == 255 and g == 255 and b == 255:
        rgbw.r = 0
        rgbw.g = 0
        rgbw.b = 0
        rgbw.w = 255
        return

    elif r == 0 and g == 0 and b == 0:
        rgbw.r = 0
        rgbw.g = 0
        rgbw.b = 0
        rgbw.w = 0
        return

    hsv = rgb2hsv_approximate(rgb)

    # this conversion is close I am sure
    # that is can be done better then what
    # I am doing. I am using an RGB input
    # value and then visually matching what
    # my LED's are showing to be as close
    # to the same color as I can get.

    # first problem is I am using my eyes and not a meter.
    # second problem is (255, 255, 255, 0) and (0, 0, 0, 255)
    # are not the same color white. This is why I am as
    # close as I can get

    # the trick to this whole thing is to convert RGB to HSV
    # then think of the Saturation as how much white and
    # the Value as how bright the white is. It is kind
    # of a funky way to determine how to set the white led.

    s = hsv.s
    v = hsv.v
    hsv.s = 81.0

    hsv2rgb_rainbow(hsv, rgbw)

    s = (1 - (s / 100.0)) * 100.0
    s /= 100.0
    v /= 100.0
    rgbw.w = (255 * (s / 2)) * v


def rgbw2rgb(rgbw, rgb):
    r = rgbw.r
    g = rgbw.g
    b = rgbw.b
    w = rgbw.w

    if r == 0 and g == 0 and b == 0 and w == 255:
        rgb.r = 255
        rgb.g = 255
        rgb.b = 255
        return

    elif r == 0 and g == 0 and b == 0 and w == 0:
        rgb.r = 0
        rgb.g = 0
        rgb.b = 0
        return

    hsv = rgb2hsv_approximate(rgbw)

    try:
        w += (w / (1 - (hsv.v / 100.0))) / 2
    except ZeroDivisionError:
        pass

    s = (1 - ((w / 255.0) * 2)) * 100.0  # * 16.0) * 100.0
    hsv.s = s

    hsv2rgb_rainbow(hsv, rgb)

    if rgb.r > 255:
        rgb.r = 255
    if rgb.g > 255:
        rgb.g = 255
    if rgb.b > 255:
        rgb.b = 255
