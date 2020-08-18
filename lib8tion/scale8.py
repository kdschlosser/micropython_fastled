
from . import *
# @ingroup lib8tion

# @defgroup Scaling Scaling functions
# Fast, efficient 8-bit scaling functions specifically
# designed for high-performance LED programming.
# 
# Because of the AVR(Arduino) and ARM assembly language
# implementations provided, using these functions often
# results in smaller and faster code than the equivalent
# program using plain "C" arithmetic and logic.
# @{


#  scale one byte by a second one, which is treated as
#  the numerator of a fraction whose denominator is 256
#  In other words, it computes i * (scale / 256)
#  4 clocks AVR with MUL, 2 clocks ARM
def scale8(i, scale):
    if FASTLED_SCALE8_FIXED == 1:
        return (i * (1 + scale)) >> 8
    else:
        return (i * scale) >> 8


#  The "video" version of scale8 guarantees that the output will
#  be only be zero if one or both of the inputs are zero.  If both
#  inputs are non-zero, the output is guaranteed to be non-zero.
#  This makes for better 'video'/LED dimming, at the cost of
#  several additional cycles.
def scale8_video(i, scale):
    if i and scale:
        j = ((i * scale) >> 8) + 1
    else:
        j = (i * scale) >> 8

    # uint8_t nonzeroscale = (scale != 0) ? 1 : 0;
    # uint8_t j = (i == 0) ? 0 : (((int)i * (int)(scale) ) >> 8) + nonzeroscale;
    return j


# This version of scale8 does not clean up the R1 register on AVR
# If you are doing several 'scale8's in a row, use this, and
# then explicitly call cleanup_R1.
def scale8_LEAVING_R1_DIRTY(i, scale):
    if FASTLED_SCALE8_FIXED == 1:
        return (i * (scale + 1)) >> 8
    else:
        return (i * scale) >> 8


# In place modifying version of scale8, also this version of nscale8 does not
# clean up the R1 register on AVR
# If you are doing several 'scale8's in a row, use this, and
# then explicitly call cleanup_R1.
def nscale8_LEAVING_R1_DIRTY(i, scale):
    if FASTLED_SCALE8_FIXED == 1:
        i = (i * (scale + 1)) >> 8
    else:
        i = (i * scale) >> 8

    return i


# This version of scale8_video does not clean up the R1 register on AVR
# If you are doing several 'scale8_video's in a row, use this, and
# then explicitly call cleanup_R1.
def scale8_video_LEAVING_R1_DIRTY(i, scale):
    j = ((i * scale) >> 8)

    if i and scale:
        j += 1

    # uint8_t nonzeroscale = (scale != 0) ? 1 : 0;
    # uint8_t j = (i == 0) ? 0 : (((int)i * (int)(scale) ) >> 8) + nonzeroscale;
    return j


# In place modifying version of scale8_video, also this version of nscale8_video
# does not clean up the R1 register on AVR
# If you are doing several 'scale8_video's in a row, use this, and
# then explicitly call cleanup_R1.
def nscale8_video_LEAVING_R1_DIRTY(i, scale):
    j = (i * scale) >> 8
    if i and scale:
        j += 1

    return i


# Clean up the r1 register after a series of *LEAVING_R1_DIRTY calls
def cleanup_R1():
    pass


# scale three one byte values by a fourth one, which is treated as
#         the numerator of a fraction whose demominator is 256
#         In other words, it computes r,g,b * (scale / 256)
# 
#         THIS FUNCTION ALWAYS MODIFIES ITS ARGUMENTS IN PLACE

def nscale8x3(r, g, b, scale):
    if FASTLED_SCALE8_FIXED == 1:
        scale_fixed = scale + 1
        r = (r * scale_fixed) >> 8
        g = (g * scale_fixed) >> 8
        b = (b * scale_fixed) >> 8
    else:
        r = (r * scale) >> 8
        g = (g * scale) >> 8
        b = (b * scale) >> 8

    return r, g, b


def nscale8x4(r, g, b, w, scale):
    if FASTLED_SCALE8_FIXED == 1:
        scale_fixed = scale + 1
        r = (r * scale_fixed) >> 8
        g = (g * scale_fixed) >> 8
        b = (b * scale_fixed) >> 8
        w = (w * scale_fixed) >> 8
    else:
        r = (r * scale) >> 8
        g = (g * scale) >> 8
        b = (b * scale) >> 8
        w = (w * scale) >> 8

    return r, g, b, w


# scale three one byte values by a fourth one, which is treated as
#         the numerator of a fraction whose demominator is 256
#         In other words, it computes r,g,b * (scale / 256), ensuring
# that non-zero values passed in remain non zero, no matter how low the scale
# argument.
# 
#         THIS FUNCTION ALWAYS MODIFIES ITS ARGUMENTS IN PLACE
def nscale8x3_video(r, g, b, scale=None):
    nonzeroscale = int(scale != 0)
    if r != 0:
        r = ((r * scale) >> 8) + nonzeroscale
    if g != 0:
        g = ((g * scale) >> 8) + nonzeroscale
    if b != 0:
        b = ((b * scale) >> 8) + nonzeroscale

    return r, g, b


def nscale8x4_video(r, g, b, w, scale):
    nonzeroscale = int(scale != 0)
    if r != 0:
        r = ((r * scale) >> 8) + nonzeroscale
    if g != 0:
        g = ((g * scale) >> 8) + nonzeroscale
    if b != 0:
        b = ((b * scale) >> 8) + nonzeroscale
    if w != 0:
        w = ((w * scale) >> 8) + nonzeroscale

    return r, g, b, w


#  scale two one byte values by a third one, which is treated as
#         the numerator of a fraction whose demominator is 256
#         In other words, it computes i,j * (scale / 256)
# 
#         THIS FUNCTION ALWAYS MODIFIES ITS ARGUMENTS IN PLACE

def nscale8x2(i, j, scale):
    if FASTLED_SCALE8_FIXED == 1:
        scale_fixed = scale + 1
        i = (i * scale_fixed) >> 8
        j = (j * scale_fixed) >> 8
    else:
        i = (i * scale) >> 8
        j = (j * scale) >> 8

    return i, j


#  scale two one byte values by a third one, which is treated as
#         the numerator of a fraction whose demominator is 256
#         In other words, it computes i,j * (scale / 256), ensuring
# that non-zero values passed in remain non zero, no matter how low the scale
# argument.
# 
#         THIS FUNCTION ALWAYS MODIFIES ITS ARGUMENTS IN PLACE
def nscale8x2_video(i, j, scale):
    nonzeroscale = int(scale != 0)
    if i != 0:
        i = ((i * scale) >> 8) + nonzeroscale
    if j != 0:
        j = ((j * scale) >> 8) + nonzeroscale

    return i, j


# scale a 16-bit unsigned value by an 8-bit value,
#         considered as numerator of a fraction whose denominator
#         is 256. In other words, it computes i * (scale / 256)

def scale16by8(i, scale):
    if FASTLED_SCALE8_FIXED == 1:
        result = (i * (1 + scale)) >> 8
    else:
        result = (i * scale) / 256

    return result


# scale a 16-bit unsigned value by a 16-bit value,
#         considered as numerator of a fraction whose denominator
#         is 65536. In other words, it computes i * (scale / 65536)
def scale16(i, scale):
    if FASTLED_SCALE8_FIXED == 1:
        result = (i * (1 + scale)) / 65536
    else:
        result = (i * scale) / 65536

    return result


# @defgroup Dimming Dimming and brightening functions
# 
# Dimming and brightening functions
# 
# The eye does not respond in a linear way to light.
# High speed PWM'd LEDs at 50% duty cycle appear far
# brighter then the 'half as bright' you might expect.
# 
# If you want your midpoint brightness leve (128) to
# appear half as bright as 'full' brightness (255), you
# have to apply a 'dimming function'.
# @{

# Adjust a scaling value for dimming
def dim8_raw(x):
    return scale8(x, x)


# Adjust a scaling value for dimming for video (value will never go below 1)
def dim8_video(x):
    return scale8_video(x, x)


# Linear version of the dimming function that halves for values < 128
def dim8_lin(x):
    if x & 0x80:
        x = scale8(x, x)
    else:
        x += 1
        x /= 2

    return x


# inverse of the dimming function, brighten a value
def brighten8_raw(x):
    ix = 255 - x
    return 255 - scale8(ix, ix)


# inverse of the dimming function, brighten a value
def brighten8_video(x):
    ix = 255 - x
    return 255 - scale8_video(ix, ix)


# inverse of the dimming function, brighten a value
def brighten8_lin(x):
    ix = 255 - x
    if ix & 0x80:
        ix = scale8(ix, ix)
    else:
        ix += 1
        ix /= 2

    return 255 - ix
