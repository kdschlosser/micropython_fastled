
from . import *
from .lib8tion import *


# Noise functions provided by the library.
def P(x):
    return p[x]


p = [
    151, 160, 137,  91,  90,  15, 131,  13, 201,  95,  96,  53, 194, 233,   7, 225,
    140,  36, 103,  30,  69, 142,   8,  99,  37, 240,  21,  10,  23, 190,   6, 148,
    247, 120, 234,  75,   0,  26, 197,  62,  94, 252, 219, 203, 117,  35,  11,  32,
    57, 177,  33,  88, 237, 149,  56,  87, 174,  20, 125, 136, 171, 168,  68, 175,
    74, 165,  71, 134, 139,  48,  27, 166,  77, 146, 158, 231,  83, 111, 229, 122,
    60, 211, 133, 230, 220, 105,  92,  41,  55,  46, 245,  40, 244, 102, 143,  54,
    65,  25,  63, 161,   1, 216,  80,  73, 209,  76, 132, 187, 208,  89,  18, 169,
    200, 196, 135, 130, 116, 188, 159,  86, 164, 100, 109, 198, 173, 186,   3,  64,
    52, 217, 226, 250, 124, 123,   5, 202,  38, 147, 118, 126, 255,  82,  85, 212,
    207, 206,  59, 227,  47,  16,  58,  17, 182, 189,  28,  42, 223, 183, 170, 213,
    119, 248, 152,   2,  44, 154, 163,  70, 221, 153, 101, 155, 167,  43, 172,   9,
    129,  22,  39, 253,  19,  98, 108, 110,  79, 113, 224, 232, 178, 185, 112, 104,
    218, 246,  97, 228, 251,  34, 242, 193, 238, 210, 144,  12, 191, 179, 162, 241,
    81,  51, 145, 235, 249,  14, 239, 107,  49, 192, 214,  31, 181, 199, 106, 157,
    184,  84, 204, 176, 115, 121,  50,  45, 127,   4, 150, 254, 138, 236, 205,  93,
    222, 114,  67,  29,  24,  72, 243, 141, 128, 195,  78,  66, 215,  61, 156, 180,
    151
]


def AVG15(U, V):
    if FASTLED_NOISE_ALLOW_AVERAGE_TO_OVERFLOW == 1:
        return (U + V) >> 1

    return avg15(U, V)


# See fastled_config.h for notes on this;
# "#define FASTLED_NOISE_FIXED 1" is the correct value

def EASE8(x):
    if FASTLED_NOISE_FIXED == 0:
        return FADE(x)

    return ease8InOutQuad(x)


def EASE16(x):
    if FASTLED_NOISE_FIXED == 0:
        return FADE(x)

    return ease16InOutQuad(x)


# #define FADE_12
FADE_12 = 0
FADE_16 = 1


def FADE(*args, **kwargs):
    if FADE_12:
        return logfade12(*args, **kwargs)

    return scale16(*args, **kwargs)


def LERP(a, b, u):
    if FADE_12:
        return lerp15by12(a, b, u)

    return lerp15by16(a, b, u)


def grad16(hash_, x, y=None, z=None):
    if y is None:
        hash_ &= 15
        if hash_ > 8:
            u = x
            v = x
        elif hash_ < 4:
            u = x
            v = 1
        else:
            u = 1
            v = x

    elif z is None:
        hash_ &= 7

        if hash_ < 4:
            u = x
            v = y
        else:
            u = y
            v = x

    else:
        hash_ &= 15
        u = x if hash_ < 8 else y

        if hash_ < 4:
            v = y
        elif hash_ in (12, 14):
            v = x
        else:
            v = z

    if hash_ & 1:
        u = -u

    if hash_ & 2:
        v = -v

    return AVG15(u, v)


# selectBasedOnHashBit performs this:
#   result = (hash & (1<<bitnumber)) ? a : b
# but with an AVR asm version that's smaller and quicker than C
# (and probably not worth including in lib8tion)
def selectBasedOnHashBit(hash_, bitnumber, a, b):
    if hash_ & (1 << bitnumber):
        return a

    return b


def grad8(hash_, x, y=None, z=None):
    if y is None:
        if hash_ & 8:
            u = x
            v = x
        elif hash_ & 4:
            u = 1
            v = x
        else:
            u = x
            v = 1

    elif z is None:
        if hash_ & 4:
            u = y
            v = x
        else:
            u = x
            v = y

    else:
        hash_ &= 0xF

        u = selectBasedOnHashBit(hash_, 3, y, x)
        if hash_ < 4:
            v = y
        elif hash_ in (12, 14):
            v = x
        else:
            v = z

    if hash_ & 1:
        u = -u
    if hash_ & 2:
        v = -v

    return avg7(u, v)


def logfade12(val):
    return scale16(val, val) >> 4


def lerp15by12(a, b, frac):
    # if(1) return (lerp(frac,a,b));
    if b > a:
        delta = b - a
        scaled = scale16(delta, frac << 4)
        result = a + scaled
    else:
        delta = a - b
        scaled = scale16(delta, frac << 4)
        result = a - scaled

    return result


def lerp7by8(a, b, frac):
    # int8_t delta = b - a;
    # int16_t prod = (uint16_t)delta * (uint16_t)frac;
    # int8_t scaled = prod >> 8;
    # int8_t result = a + scaled;
    # return result;

    if b > a:
        delta = b - a
        scaled = scale8(delta, frac)
        result = a + scaled
    else:
        delta = a - b
        scaled = scale8(delta, frac)
        result = a - scaled

    return result


def inoise16_raw(x, y=None, z=None):
    if y is None:
        # Find the unit cube containing the point
        X = x >> 16

        # Hash cube corner coordinates
        A = P(X)
        AA = P(A)
        B = P(X + 1)
        BA = P(B)

        # Get the relative position of the point in the cube
        u = x & 0xFFFF

        # Get a signed version of the above for the grad function
        xx = (u >> 1) & 0x7FFF
        N = 0x8000

        u = EASE16(u)

        ans = LERP(grad16(P(AA), xx), grad16(P(BA), xx - N), u)

        return ans
    elif z is None:
        # Find the unit cube containing the point
        X = x >> 16
        Y = y >> 16

        # Hash cube corner coordinates
        A = P(X) + Y
        AA = P(A)
        AB = P(A + 1)
        B = P(X + 1) + Y
        BA = P(B)
        BB = P(B + 1)

        # Get the relative position of the point in the cube
        u = x & 0xFFFF
        v = y & 0xFFFF

        # Get a signed version of the above for the grad function
        xx = (u >> 1) & 0x7FFF
        yy = (v >> 1) & 0x7FFF
        N = 0x8000

        u = EASE16(u)
        v = EASE16(v)

        X1 = LERP(grad16(P(AA), xx, yy), grad16(P(BA), xx - N, yy), u)
        X2 = LERP(grad16(P(AB), xx, yy - N), grad16(P(BB), xx - N, yy - N), u)

        ans = LERP(X1, X2, v)

        return ans
    
    else:
    
        # Find the unit cube containing the point
        X = (x >> 16) & 0xFF
        Y = (y >> 16) & 0xFF
        Z = (z >> 16) & 0xFF
    
        # Hash cube corner coordinates
        A = P(X) + Y
        AA = P(A) + Z
        AB = P(A + 1) + Z
        B = P(X + 1) + Y
        BA = P(B) + Z
        BB = P(B + 1) + Z
    
        # Get the relative position of the point in the cube
        u = x & 0xFFFF
        v = y & 0xFFFF
        w = z & 0xFFFF
    
        # Get a signed version of the above for the grad function
        xx = (u >> 1) & 0x7FFF
        yy = (v >> 1) & 0x7FFF
        zz = (w >> 1) & 0x7FFF
        N = 0x8000
    
        u = EASE16(u)
        v = EASE16(v)
        w = EASE16(w)
    
        # skip the log fade adjustment for the moment, otherwise here we would
        # adjust fade values for u,v,w
        X1 = LERP(grad16(P(AA), xx, yy, zz), grad16(P(BA), xx - N, yy, zz), u)
        X2 = LERP(grad16(P(AB), xx, yy - N, zz), grad16(P(BB), xx - N, yy - N, zz), u)
        X3 = LERP(grad16(P(AA + 1), xx, yy, zz - N), grad16(P(BA + 1), xx - N, yy, zz-N), u)
        X4 = LERP(grad16(P(AB + 1), xx, yy - N, zz - N), grad16(P(BB + 1), xx - N, yy - N, zz - N), u)
    
        Y1 = LERP(X1, X2, v)
        Y2 = LERP(X3, X4, v)
    
        ans = LERP(Y1, Y2, w)
    
        return ans


def inoise16(x, y=None, z=None):
    if y is None:
        return (inoise16_raw(x) + 17308) << 1
    
    elif z is None:
        ans = inoise16_raw(x, y)
        ans += 17308
        pan = ans
        # pan = (ans * 242L) >> 7.  That's the same as:
        # pan = (ans * 484L) >> 8.  And this way avoids a 7X four-byte shift-loop on AVR.
        # Identical math, except for the highest bit, which we don't care about anyway,
        # since we're returning the 'middle' 16 out of a 32-bit value anyway.
        pan *= 484
        return pan >> 8

        # return (uint32_t)(((int32_t)inoise16_raw(x,y)+(uint32_t)17308)*242)>>7;
        # return scale16by8(inoise16_raw(x,y)+17308,242)<<1;
    else:
        ans = inoise16_raw(x, y, z)
        ans += 19052
        pan = ans
        # pan = (ans * 220L) >> 7.  That's the same as:
        # pan = (ans * 440L) >> 8.  And this way avoids a 7X four-byte shift-loop on AVR.
        # Identical math, except for the highest bit, which we don't care about anyway,
        # since we're returning the 'middle' 16 out of a 32-bit value anyway.
        pan *= 440
        return pan >> 8
    
        # // return scale16by8(pan,220)<<1;
        # return ((inoise16_raw(x,y,z)+19052)*220)>>7;
        # return scale16by8(inoise16_raw(x,y,z)+19052,220)<<1;


def inoise8_raw(x, y=None, z=None):
    if y is None:
        
        # Find the unit cube containing the point
        X = x >> 8
    
        # Hash cube corner coordinates
        A = P(X)
        AA = P(A)
        B = P(X + 1)
        BA = P(B)
    
        # Get the relative position of the point in the cube
        u = x
    
        # Get a signed version of the above for the grad function
        xx = (x >> 1) & 0x7F
        N = 0x80
    
        u = EASE8(u)
      
        ans = lerp7by8(grad8(P(AA), xx), grad8(P(BA), xx - N), u)
    
        return ans
        
    elif z is None:
        # Find the unit cube containing the point
        X = x >> 8
        Y = y >> 8
    
        # Hash cube corner coordinates
        A = P(X) + Y
        AA = P(A)
        AB = P(A + 1)
        B = P(X + 1) + Y
        BA = P(B)
        BB = P(B + 1)
    
        # Get the relative position of the point in the cube
        u = x
        v = y
    
        # Get a signed version of the above for the grad function
        xx = (x >> 1) & 0x7F
        yy = (y >> 1) & 0x7F
        N = 0x80
    
        u = EASE8(u)
        v = EASE8(v)
    
        X1 = lerp7by8(grad8(P(AA), xx, yy), grad8(P(BA), xx - N, yy), u)
        X2 = lerp7by8(grad8(P(AB), xx, yy-N), grad8(P(BB), xx - N, yy - N), u)
    
        ans = lerp7by8(X1, X2, v)
    
        return ans
        # return scale8((70+(ans)),234)<<1
        
    else:
        # Find the unit cube containing the point
        X = x >> 8
        Y = y >> 8
        Z = z >> 8
    
        # Hash cube corner coordinates
        A = P(X) + Y
        AA = P(A) + Z
        AB = P(A + 1) + Z
        B = P(X + 1) + Y
        BA = P(B) + Z
        BB = P(B + 1) + Z
    
        # Get the relative position of the point in the cube
        u = x
        v = y
        w = z
    
        # Get a signed version of the above for the grad function
        xx = (x >> 1) & 0x7F
        yy = (y >> 1) & 0x7F
        zz = (z >> 1) & 0x7F
        N = 0x80
    
        u = EASE8(u)
        v = EASE8(v)
        w = EASE8(w)
    
        X1 = lerp7by8(grad8(P(AA), xx, yy, zz), grad8(P(BA), xx - N, yy, zz), u)
        X2 = lerp7by8(grad8(P(AB), xx, yy - N, zz), grad8(P(BB), xx - N, yy - N, zz), u)
        X3 = lerp7by8(grad8(P(AA + 1), xx, yy, zz - N), grad8(P(BA + 1), xx - N, yy, zz - N), u)
        X4 = lerp7by8(grad8(P(AB + 1), xx, yy - N, zz - N), grad8(P(BB + 1), xx - N, yy - N, zz - N), u)
    
        Y1 = lerp7by8(X1, X2, v)
        Y2 = lerp7by8(X3, X4, v)
    
        ans = lerp7by8(Y1, Y2, w)
    
        return ans


def inoise8(x, y=None, z=None):
    if z is None:
        # return scale8(69+inoise8_raw(x,y),237)<<1;
        n = inoise8_raw(x, y)  # -64..+64
        n += 64  # 0..128
        ans = qadd8(n, n)  # 0..255
        return ans

    elif y is None:
        n = inoise8_raw(x)  # -64..+64
        n += 64  # 0..128
        ans = qadd8(n, n)  # 0..255
        return ans

    else:
        # return scale8(76+(inoise8_raw(x,y,z)),215)<<1;
        n = inoise8_raw(x, y, z)  # -64..+64
        n += 64  # 0..128
        ans = qadd8(n, n)  # 0..255
        return ans


class q44(object):
    def __init__(self, _i, _f):
        self.i = (_i >> 4) & 0xF
        self.f = (_f >> 4) & 0xF


# // uint32_t mul44(uint32_t v, q44 mulby44) {
# //     return (v *mulby44.i)  + ((v * mulby44.f) >> 4);
# // }
# //
# // uint16_t mul44_16(uint16_t v, q44 mulby44) {
# //     return (v *mulby44.i)  + ((v * mulby44.f) >> 4);
# // }

def fill_raw_noise8(pData, num_points, octaves, x, scale, time_):
    _xx = x
    scx = scale
    for o in range(octaves):
        xx = _xx
        for i in range(num_points):
            pData[i] = qadd8(pData[i], inoise8(xx, time_) >> o)
            xx += scx

    _xx <<= 1
    scx <<= 1


def fill_raw_noise16into8(pData, num_points, octaves, x, scale, time_):
    _xx = x
    scx = scale
    for o in range(octaves):
        xx = _xx
        for i in range(num_points):
            accum = inoise16(xx, time_) >> o
            accum += pData[i] << 8
            if accum > 65535:
                accum = 65535

            pData[i] = accum >> 8

            xx += scx

    _xx <<= 1
    scx <<= 1


def fill_raw_2dnoise8(
    pData,
    width,
    height,
    octaves,
    freq44=None,
    amplitude=None,
    skip=None,
    x=None,
    scalex=None,
    y=None,
    scaley=None,
    time_=None
):

    if (
        y is None and
        scaley is None and
        time_ is None and
        freq44 is not None and
        amplitude is not None and
        skip is not None and
        x is not None and
        scalex is not None
    ):
        x, scaley = freq44, x
        scalex, time_ = amplitude, scalex
        y = skip,

        freq44 = None
        amplitude = None
        skip = None

    if freq44 is None and amplitude is None and skip is None:
        fill_raw_2dnoise8(pData, width, height, octaves, q44(2, 0), 128, 1, x, scalex, y, scaley, time_)
        return

    if octaves > 1:
        fill_raw_2dnoise8(
            pData,
            width,
            height,
            octaves - 1,
            freq44,
            amplitude,
            skip + 1,
            x * freq44,
            freq44 * scalex,
            y * freq44,
            freq44 * scaley,
            time_
        )
    else:
        # amplitude is always 255 on the lowest level
        amplitude = 255

    scalex *= skip
    scaley *= skip

    invamp = fract8(255 - amplitude)

    for i in range(height):
        pRow = pData + (i * width)
        xx = x
        for j in range(width):
            noise_base = inoise8(xx, y, time_)
            if 0x80 & noise_base:
                noise_base -= 127
            else:
                noise_base = 127 - noise_base

            noise_base = scale8(noise_base << 1, amplitude)
            if skip == 1:
                pRow[j] = scale8(pRow[j], invamp) + noise_base
            else:
                for ii in range(i + skip):
                    if ii >= height:
                        break

                    pRow = pData + (ii * width)
                    for jj in range(j + skip):
                        if jj >= width:
                            break
                        pRow[jj] = scale8(pRow[jj], invamp) + noise_base

            xx += scalex
        y += scaley


def fill_raw_2dnoise16(pData, width, height, octaves, freq88, amplitude, skip, x, scalex, y, scaley, time_):
    if octaves > 1:
        fill_raw_2dnoise16(
            pData,
            width,
            height,
            octaves - 1,
            freq88,
            amplitude,
            skip,
            x * freq88,
            scalex * freq88,
            y * freq88,
            scaley * freq88,
            time_
        )
    else:
        # amplitude is always 255 on the lowest level
        amplitude = 65535

    scalex *= skip
    scaley *= skip
    invamp = fract16(65535 - amplitude)
    for i in range(0, height, skip):
        pRow = pData + (i * width)
        xx = x
        for j in range(0, width, skip):
            noise_base = inoise16(xx, y, time_)
            if 0x8000 & noise_base:
                noise_base -= 32767
            else:
                noise_base = 32767 - noise_base

            noise_base = scale16(noise_base << 1, amplitude)
            if skip == 1:
                pRow[j] = scale16(pRow[j], invamp) + noise_base
            else:
                for ii in range(i + skip):
                    if ii >= height:
                        break

                    pRow = pData + (ii * width)

                    for jj in range(j + skip):
                        if jj >= width:
                            break

                        pRow[jj] = scale16(pRow[jj], invamp) + noise_base

            xx += scalex
        y += scaley


nmin = 11111110
nmax = 0


def fill_raw_2dnoise16into8(
        pData,
        width,
        height,
        octaves,
        freq44=None,
        amplitude=None,
        skip=None,
        x=None,
        scalex=None,
        y=None,
        scaley=None,
        time_=None
):
    if (
        y is None and
        scaley is None and
        time_ is None and
        freq44 is not None and
        amplitude is not None and
        skip is not None and
        x is not None and
        scalex is not None
    ):
        x, scaley = freq44, x
        scalex, time_ = amplitude, scalex
        y = skip,

        freq44 = None
        amplitude = None
        skip = None

    if freq44 is None and amplitude is None and skip is None:
        fill_raw_2dnoise16into8(pData, width, height, octaves, q44(2, 0), 128, 1, x, scalex, y, scaley, time_)
        return

    if octaves > 1:
        fill_raw_2dnoise16into8(
            pData,
            width,
            height,
            octaves - 1,
            freq44,
            amplitude,
            skip + 1,
            x * freq44,
            scalex * freq44,
            y * freq44,
            scaley * freq44,
            time_
        )
    else:
        # amplitude is always 255 on the lowest level
        amplitude = 255

    scalex *= skip
    scaley *= skip

    invamp = fract8(255 - amplitude)
    for i in range(0, height, skip):
        y += scaley
        pRow = pData[(i * width):]

        xx = x
        for j in range(0, width, skip):
            xx += scalex
            noise_base = inoise16(xx, y, time_)
            noise_base = noise_base - 32767 if 0x8000 & noise_base else 32767 - noise_base
            noise_base = scale8(noise_base >> 7, amplitude)
            if skip == 1:
                pRow[j] = qadd8(scale8(pRow[j], invamp), noise_base)
            else:
                for ii in range(i, i + skip if i + skip <= height else height):
                    pRow = pData[ii * width:]
                    for jj in range(j, j + skip if j + skip <= width else width):
                        pRow[jj] = scale8(pRow[jj], invamp) + noise_base


def fill_noise8(
    leds,
    num_leds,
    octaves,
    x,
    scale,
    hue_octaves,
    hue_x,
    hue_scale,
    time_
):
    V = [0] * num_leds
    H = [0] * num_leds

    fill_raw_noise8(V, num_leds, octaves, x, scale, time_)
    fill_raw_noise8(H, num_leds, hue_octaves, hue_x, hue_scale, time_)

    for i in range(num_leds):
        leds[i] = CHSV(H[i], 255, V[i])


def fill_noise16(
    leds,
    num_leds,
    octaves,
    x,
    scale,
    hue_octaves,
    hue_x,
    hue_scale,
    time_,
    hue_shift_
):
    V = [0] * num_leds
    H = [0] * num_leds

    fill_raw_noise16into8(V, num_leds, octaves, x, scale, time_)
    fill_raw_noise8(H, num_leds, hue_octaves, hue_x, hue_scale, time_)

    for i in range(num_leds):
        leds[i] = CHSV(H[i] + hue_shift_, 255, V[i])


def fill_2dnoise8(
    leds,
    width,
    height,
    serpentine,
    octaves,
    x,
    xscale,
    y,
    yscale,
    time_,
    hue_octaves,
    hue_x,
    hue_xscale,
    hue_y,
    hue_yscale,
    hue_time,
    blend_
):
    V = [[0] * width] * height
    H = [[0] * width] * height

    fill_raw_2dnoise8(V, width, height, octaves, x, xscale, y, yscale, time_)
    fill_raw_2dnoise8(H, width, height, hue_octaves, hue_x, hue_xscale, hue_y, hue_yscale, hue_time)

    w1 = width - 1
    h1 = height - 1
    for i in range(height):
        wb = i * width
        for j in range(width):
            led = CRGB(CHSV(H[h1-i][w1-j], 255, V[i][j]))

            pos = j
            if serpentine and (i & 0x1):
                pos = w1 - j

            if blend_:
                leds[wb + pos] >>= 1
                leds[wb + pos] += led >> 1
            else:
                leds[wb + pos] = led


def fill_2dnoise16(
    leds,
    width,
    height,
    serpentine,
    octaves,
    x,
    xscale,
    y,
    yscale,
    time_,
    hue_octaves,
    hue_x,
    hue_xscale,
    hue_y,
    hue_yscale,
    hue_time,
    blend_,
    hue_shift
):
    V = [[0] * width] * height
    H = [[0] * width] * height

    fill_raw_2dnoise16into8(V, width, height, octaves, q44(2, 0), 171, 1, x, xscale, y, yscale, time_)
    # fill_raw_2dnoise16into8((uint8_t*)V,width,height,octaves,x,xscale,y,yscale,time);
    # fill_raw_2dnoise8((uint8_t*)V,width,height,hue_octaves,x,xscale,y,yscale,time);
    fill_raw_2dnoise8(H, width, height, hue_octaves, hue_x, hue_xscale, hue_y, hue_yscale, hue_time)

    w1 = width - 1
    h1 = height - 1
    hue_shift >>= 8

    for i in range(height):
        wb = i * width
        for j in range(width):
            led = CRGB(CHSV(hue_shift + (H[h1 - i][w1 - j]), 196, V[i][j]))

            pos = j
            if serpentine and (i & 0x1):
                pos = w1 - j

            if blend_:
                leds[wb + pos] >>= 1
                leds[wb + pos] += led >> 1
            else:
                leds[wb + pos] = led
