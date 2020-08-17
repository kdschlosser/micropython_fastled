
from ..FastLED import *
from ..bitswap import get_bit, set_bit

# 
#  Fast, efficient 8-bit math functions specifically
#  designed for high-performance LED programming.
# 
#  Because of the AVR(Arduino) and ARM assembly language
#  implementations provided, using these functions often
#  results in smaller and faster code than the equivalent
#  program using plain "C" arithmetic and logic.
# 
# 
#  Included are:
# 
# 
#  - Saturating unsigned 8-bit add and subtract.
#    Instead of wrapping around if an overflow occurs,
#    these routines just 'clamp' the output at a maxumum
#    of 255, or a minimum of 0.  Useful for adding pixel
#    values.  E.g., qadd8( 200, 100) = 255.
# 
#      qadd8( i, j) == MIN( (i + j), 0xFF )
#      qsub8( i, j) == MAX( (i - j), 0 )
# 
#  - Saturating signed 8-bit ("7-bit") add.
#      qadd7( i, j) == MIN( (i + j), 0x7F)
# 
# 
#  - Scaling (down) of unsigned 8- and 16- bit values.
#    Scaledown value is specified in 1/256ths.
#      scale8( i, sc) == (i * sc) / 256
#      scale16by8( i, sc) == (i * sc) / 256
# 
#    Example: scaling a 0-255 value down into a
#    range from 0-99:
#      downscaled = scale8( originalnumber, 100);
# 
#    A special version of scale8 is provided for scaling
#    LED brightness values, to make sure that they don't
#    accidentally scale down to total black at low
#    dimming levels, since that would look wrong:
#      scale8_video( i, sc) = ((i * sc) / 256) +? 1
# 
#    Example: reducing an LED brightness by a
#    dimming factor:
#      new_bright = scale8_video( orig_bright, dimming);
# 
# 
#  - Fast 8- and 16- bit unsigned random numbers.
#    Significantly faster than Arduino random(), but
#    also somewhat less random.  You can add entropy.
#      random8()       == random from 0..255
#      random8( n)     == random from 0..(N-1)
#      random8( n, m)  == random from N..(M-1)
# 
#      random16()      == random from 0..65535
#      random16( n)    == random from 0..(N-1)
#      random16( n, m) == random from N..(M-1)
# 
#      random16_set_seed( k)    ==  seed = k
#      random16_add_entropy( k) ==  seed += k
# 
# 
#  - Absolute value of a signed 8-bit value.
#      abs8( i)     == abs( i)
# 
# 
#  - 8-bit math operations which return 8-bit values.
#    These are provided mostly for completeness,
#    not particularly for performance.
#      mul8( i, j)  == (i * j) & 0xFF
#      add8( i, j)  == (i + j) & 0xFF
#      sub8( i, j)  == (i - j) & 0xFF
# 
# 
#  - Fast 16-bit approximations of sin and cos.
#    Input angle is a uint16_t from 0-65535.
#    Output is a signed int16_t from -32767 to 32767.
#       sin16( x)  == sin( (x/32768.0) * pi) * 32767
#       cos16( x)  == cos( (x/32768.0) * pi) * 32767
#    Accurate to more than 99% in all cases.
# 
#  - Fast 8-bit approximations of sin and cos.
#    Input angle is a uint8_t from 0-255.
#    Output is an UNsigned uint8_t from 0 to 255.
#        sin8( x)  == (sin( (x/128.0) * pi) * 128) + 128
#        cos8( x)  == (cos( (x/128.0) * pi) * 128) + 128
#    Accurate to within about 2%.
# 
# 
#  - Fast 8-bit "easing in/out" function.
#      ease8InOutCubic(x) == 3(x^i) - 2(x^3)
#      ease8InOutApprox(x) ==
#        faster, rougher, approximation of cubic easing
#      ease8InOutQuad(x) == quadratic (vs cubic) easing
# 
#  - Cubic, Quadratic, and Triangle wave functions.
#    Input is a uint8_t representing phase withing the wave,
#      similar to how sin8 takes an angle 'theta'.
#    Output is a uint8_t representing the amplitude of
#      the wave at that point.
#        cubicwave8( x)
#        quadwave8( x)
#        triwave8( x)
# 
#  - Square root for 16-bit integers.  About three times
#    faster and five times smaller than Arduino's built-in
#    generic 32-bit sqrt routine.
#      sqrt16( uint16_t x ) == sqrt( x)
# 
#  - Dimming and brightening functions for 8-bit
#    light values.
#      dim8_video( x)  == scale8_video( x, x)
#      dim8_raw( x)    == scale8( x, x)
#      dim8_lin( x)    == (x<128) ? ((x+1)/2) : scale8(x,x)
#      brighten8_video( x) == 255 - dim8_video( 255 - x)
#      brighten8_raw( x) == 255 - dim8_raw( 255 - x)
#      brighten8_lin( x) == 255 - dim8_lin( 255 - x)
#    The dimming functions in particular are suitable
#    for making LED light output appear more 'linear'.
# 
# 
#  - Linear interpolation between two values, with the
#    fraction between them expressed as an 8- or 16-bit
#    fixed point fraction (fract8 or fract16).
#      lerp8by8(   fromU8, toU8, fract8 )
#      lerp16by8(  fromU16, toU16, fract8 )
#      lerp15by8(  fromS16, toS16, fract8 )
#        == from + (( to - from ) * fract8) / 256)
#      lerp16by16( fromU16, toU16, fract16 )
#        == from + (( to - from ) * fract16) / 65536)
#      map8( in, rangeStart, rangeEnd)
#        == map( in, 0, 255, rangeStart, rangeEnd);
# 
#  - Optimized memmove, memcpy, and memset, that are
#    faster than standard avr-libc 1.8.
#       memmove8( dest, src,  bytecount)
#       memcpy8(  dest, src,  bytecount)
#       memset8(  buf, value, bytecount)
# 
#  - Beat generators which return sine or sawtooth
#    waves in a specified number of Beats Per Minute.
#    Sine wave beat generators can specify a low and
#    high range for the output.  Sawtooth wave beat
#    generators always range 0-255 or 0-65535.
#      beatsin8( BPM, low8, high8)
#          = (sine(beatphase) * (high8-low8)) + low8
#      beatsin16( BPM, low16, high16)
#          = (sine(beatphase) * (high16-low16)) + low16
#      beatsin88( BPM88, low16, high16)
#          = (sine(beatphase) * (high16-low16)) + low16
#      beat8( BPM)  = 8-bit repeating sawtooth wave
#      beat16( BPM) = 16-bit repeating sawtooth wave
#      beat88( BPM88) = 16-bit repeating sawtooth wave
#    BPM is beats per minute in either simple form
#    e.g. 120, or Q8.8 fixed-point form.
#    BPM88 is beats per minute in ONLY Q8.8 fixed-point
#    form.
# 
# Lib8tion is pronounced like 'libation': lie-BAY-shun

QADD8_C = 1
QADD7_C = 1
QSUB8_C = 1
SCALE8_C = 1
SCALE16BY8_C = 1
SCALE16_C = 1
ABS8_C = 1
MUL8_C = 1
QMUL8_C = 1
ADD8_C = 1
SUB8_C = 1
EASE8_C = 1
AVG8_C = 1
AVG7_C = 1
AVG16_C = 1
AVG15_C = 1
BLEND8_C = 1

# @defgroup lib8tion Fast math functions
# A variety of functions for working with numbers.
# @{


# # # # # # # # # # # # # # # # # # # # # # # # 
# 
# typdefs for fixed-point fractional types.
# 
# sfract7 should be interpreted as signed 128ths.
# fract8 should be interpreted as unsigned 256ths.
# sfract15 should be interpreted as signed 32768ths.
# fract16 should be interpreted as unsigned 65536ths.
# 
# Example: if a fract8 has the value "64", that should be interpreted
#          as 64/256ths, or one-quarter.
# 
# 
#  fract8   range is 0 to 0.99609375
#                 in steps of 0.00390625
# 
#  sfract7  range is -0.9921875 to 0.9921875
#                 in steps of 0.0078125
# 
#  fract16  range is 0 to 0.99998474121
#                 in steps of 0.00001525878
# 
#  sfract15 range is -0.99996948242 to 0.99996948242
#                 in steps of 0.00003051757
# 

# ANSI unsigned short _Fract.  range is 0 to 0.99609375
#                 in steps of 0.00390625
class fract8(int):   # < ANSI: unsigned short _Fract
    pass

#  ANSI: signed short _Fract.  range is -0.9921875 to 0.9921875
#                 in steps of 0.0078125
class sfract7(int):  # < ANSI: signed   short _Fract
    pass

#  ANSI: unsigned _Fract.  range is 0 to 0.99998474121
#                 in steps of 0.00001525878
class fract16(int):  # < ANSI: unsigned       _Fract
    pass

#  ANSI: signed _Fract.  range is -0.99996948242 to 0.99996948242
#                 in steps of 0.00003051757
class sfract15(int):  # < ANSI: signed         _Fract
    pass

# accumXY types should be interpreted as X bits of integer,
#         and Y bits of fraction.
#         E.g., accum88 has 8 bits of int, 8 bits of fraction


class accum88(int):  # < ANSI: unsigned short _Accum.  8 bits int, 8 bits fraction
    pass


class saccum78(int):  # < ANSI: signed   short _Accum.  7 bits int, 8 bits fraction
    pass


class accum1616(int):  # < ANSI: signed         _Accum. 16 bits int, 16 bits fraction
    pass


class saccum1516(int):  # < ANSI: signed         _Accum. 15 bits int, 16 bits fraction
    pass


class accum124(int):  # < no direct ANSI counterpart. 12 bits int, 4 bits fraction
    pass


class saccum114(int):  # < no direct ANSI counterpart. 1 bit int, 14 bits fraction
    pass


# typedef for IEEE754 "binary32" float type internals
class IEEE754binary32_t(object):
    def __init__(
        self,
        i=0,
        f=0.0,
        mantissa=0,
        exponent=0,
        signbit=0,
        mant7=0,
        mant16=0,
        exp_=0,
        sb_=0,
        mant_lo8=0,
        mant_hi16_exp_lo1=0,
        sb_exphi7=0
    ):

        self.i = i
        self.f = f

        def _get_bits(value, num_bits):
            res = 0
            for i in range(num_bits):
                res = set_bit(res, i, get_bit(value, i))

            return res

        self.mantissa = _get_bits(mantissa, 23)
        self.exponent = _get_bits(exponent, 8)
        self.signbit = _get_bits(signbit, 1)

        self.mant7 = _get_bits(mant7, 7)
        self.mant16 = _get_bits(mant16, 16)
        self.exp_ = _get_bits(exp_, 8)
        self.sb_ = _get_bits(sb_, 1)

        self.mant_lo8 = _get_bits(mant_lo8, 8)
        self.mant_hi16_exp_lo1 = _get_bits(mant_hi16_exp_lo1, 16)
        self.sb_exphi7 = _get_bits(sb_exphi7, 8)


from .math8 import *
from .random8 import *
from .scale8 import *
from .trig8 import *

# # # # # # # # # # # # # # # # # # # # # # # # 

# # # # # # # # # # # # # # # # # # # # # # # # 
# 
# float-to-fixed and fixed-to-float conversions
# 
# Note that anything involving a 'float' on AVR will be slower.

# sfract15ToFloat: conversion from sfract15 fixed point to
#                  IEEE754 32-bit float.
def sfract15ToFloat(y):
    return y / 32768.0


# conversion from IEEE754 float in the range (-1,1)
#                  to 16-bit fixed point.  Note that the extremes of
#                  one and negative one are NOT representable.  The
#                  representable range is basically
def floatToSfract15(f):
    return f * 32768.0


# # # # # # # # # # # # # # # # # # # # # # # # 
# 
# linear interpolation, such as could be used for Perlin noise, etc.
# 

# A note on the structure of the lerp functions:
# The cases for b>a and b<=a are handled separately for
# speed: without knowing the relative order of a and b,
# the value (a-b) might be overflow the width of a or b,
# and have to be promoted to a wider, slower type.
# To avoid that, we separate the two cases, and are able
# to do all the math in the same width as the arguments,
# which is much faster and smaller on AVR.

# linear interpolation between two unsigned 8-bit values,
# with 8-bit fraction
def lerp8by8(a, b, frac):
    if b > a:
        delta = b - a
        scaled = scale8(delta, frac)
        result = a + scaled
    else:
        delta = a - b
        scaled = scale8(delta, frac)
        result = a - scaled

    return result


# linear interpolation between two unsigned 16-bit values,
# with 16-bit fraction
def lerp16by16(a, b, frac):
    if b > a:
        delta = b - a
        scaled = scale16(delta, frac)
        result = a + scaled
    else:
        delta = a - b
        scaled = scale16( delta, frac)
        result = a - scaled

    return result


# linear interpolation between two unsigned 16-bit values,
# with 8-bit fraction
def lerp16by8(a, b, frac):
    if b > a:
        delta = b - a
        scaled = scale16by8(delta, frac)
        result = a + scaled
    else:
        delta = a - b
        scaled = scale16by8(delta, frac)
        result = a - scaled

    return result

# linear interpolation between two signed 15-bit values,
# with 8-bit fraction
def lerp15by8(a, b, frac):
    if b > a:
        delta = b - a
        scaled = scale16by8(delta, frac)
        result = a + scaled
    else:
        delta = a - b
        scaled = scale16by8(delta, frac)
        result = a - scaled

    return result


# linear interpolation between two signed 15-bit values,
# with 8-bit fraction
def lerp15by16(a, b, frac):
    if b > a:
        delta = b - a
        scaled = scale16(delta, frac)
        result = a + scaled
    else:
        delta = a - b
        scaled = scale16(delta, frac)
        result = a - scaled

    return result


#  map8: map from one full-range 8-bit value into a narrower
# range of 8-bit values, possibly a range of hues.
# 
# E.g. map myValue into a hue in the range blue..purple..pink..red
# hue = map8( myValue, HUE_BLUE, HUE_RED);
# 
# Combines nicely with the waveform functions (like sin8, etc)
# to produce continuous hue gradients back and forth:
# 
#          hue = map8( sin8( myValue), HUE_BLUE, HUE_RED);
# 
# Mathematically simiar to lerp8by8, but arguments are more
# like Arduino's "map"; this function is similar to
# 
#          map( in, 0, 255, rangeStart, rangeEnd)
# 
# but faster and specifically designed for 8-bit values.
def map8(in_, rangeStart, rangeEnd):
    rangeWidth = rangeEnd - rangeStart
    out = scale8(in_, rangeWidth)
    out += rangeStart
    return out


# # # # # # # # # # # # # # # # # # # # # # # # 
# 
# easing functions; see http:# easings.net
# 

# ease8InOutQuad: 8-bit quadratic ease-in / ease-out function
#                Takes around 13 cycles on AVR

def ease8InOutQuad(i):
    j = i
    if j & 0x80:
        j = 255 - j

    jj  = scale8(j, j)
    jj2 = jj << 1
    if i & 0x80:
        jj2 = 255 - jj2

    return jj2


# ease16InOutQuad: 16-bit quadratic ease-in / ease-out function
# C implementation at this point
def ease16InOutQuad(i):
    j = i
    if j & 0x8000:
        j = 65535 - j

    jj = scale16(j, j)
    jj2 = jj << 1
    if i & 0x8000:
        jj2 = 65535 - jj2

    return jj2


# ease8InOutCubic: 8-bit cubic ease-in / ease-out function
#                 Takes around 18 cycles on AVR
def ease8InOutCubic(i):
    ii  = scale8_LEAVING_R1_DIRTY(i, i)
    iii = scale8_LEAVING_R1_DIRTY(ii, i)

    r1 = (3 * ii) - ( 2 * iii)

    # the code generated for the above *'s automatically
    # cleans up R1, so there's no need to explicitily call
    cleanup_R1()

    result = r1

    # if we got "256", return 255:
    if r1 & 0x100:
        result = 255

    return result

# ease8InOutApprox: fast, rough 8-bit ease-in/ease-out function
#                   shaped approximately like 'ease8InOutCubic',
#                   it's never off by more than a couple of percent
#                   from the actual cubic S-curve, and it executes
#                   more than twice as fast.  Use when the cycles
#                   are more important than visual smoothness.
#                   Asm version takes around 7 cycles on AVR.
def ease8InOutApprox(i):
    if i < 64:
        # start with slope 0.5
        i /= 2.0

    elif i > (255 - 64):
        # end with slope 0.5
        i = 255 - i
        i /= 2.0
        i = 255 - i
    else:
        # in the middle, use slope 192/128 = 1.5
        i -= 64
        i += i / 2.0
        i += 32

    return i

# triwave8: triangle (sawtooth) wave generator.  Useful for
#           turning a one-byte ever-increasing value into a
#           one-byte value that oscillates up and down.
# 
#           input         output
#           0..127        0..254 (positive slope)
#           128..255      254..0 (negative slope)
# 
# On AVR this function takes just three cycles.
# 
def triwave8(in_):
    if in_ & 0x80:
        in_ = 255 - in_

    out = in_ << 1
    return out


# quadwave8 and cubicwave8: S-shaped wave generators (like 'sine').
#           Useful for turning a one-byte 'counter' value into a
#           one-byte oscillating value that moves smoothly up and down,
#           with an 'acceleration' and 'deceleration' curve.
# 
#           These are even faster than 'sin8', and have
#           slightly different curve shapes.
# 

# quadwave8: quadratic waveform generator.  Spends just a little more
#            time at the limits than 'sine' does.
def quadwave8(in_):
    return ease8InOutQuad(triwave8(in_))

# cubicwave8: cubic waveform generator.  Spends visibly more time
#             at the limits than 'sine' does.
def cubicwave8(in_):
    return ease8InOutCubic(triwave8(in_))

# squarewave8: square wave generator.  Useful for
#           turning a one-byte ever-increasing value
#           into a one-byte value that is either 0 or 255.
#           The width of the output 'pulse' is
#           determined by the pulsewidth argument:
# 
# ~~~
#           If pulsewidth is 255, output is always 255.
#           If pulsewidth < 255, then
#             if input < pulsewidth  then output is 255
#             if input >= pulsewidth then output is 0
# ~~~
# 
# the output looking like:
# 
# ~~~
#     255   +--pulsewidth--+
#      .    |              |
#      0    0              +--------(256-pulsewidth)--------
# ~~~
# 
# @param in
# @param pulsewidth
# @returns square wave output
def squarewave8(in_, pulsewidth=128):
    if in_ < pulsewidth or pulsewidth == 255:
        return 255
    else:
        return 0


# Template class for represneting fractional ints.
class q(object):
    def __init__(self, T, F, I):
        self._T = T
        self._F = F
        self._I = I
        self.i = T()
        self.f = T()

    def __call__(self, i, f=None):
        res = q(self._T, self._F, self._I)

        if isinstance(i, float) and f is None:
            fx = i
            res.i = self._T(fx)
            res.f = self._T((fx - self.i) * (1 << self._F))
        else:
            if not isinstance(i, self._T):
                i = self._T(i)
            if not isinstance(f, self._T):
                f = self._T(f)

            def _get_bits(value, bit_count):
                ret = 0
                for bit_num in range(bit_count):
                    ret = set_bit(ret, bit_num, get_bit(value, bit_num))

                return ret

            res.i = self._T(_get_bits(i, self._I))
            res.f = self._T(_get_bits(f, self._F))

        return res

    def __mul__(self, v):
        return (v * self.i) + ((v * self.f) >> self._F)


# A 4.4 integer (4 bits integer, 4 bits fraction)
q44 = q(int, 4, 4)
# A 6.2 integer (6 bits integer, 2 bits fraction)
q62 = q(int, 6, 2)
# A 8.8 integer (8 bits integer, 8 bits fraction)
q88 = q(int, 8, 8)
# A 12.4 integer (12 bits integer, 4 bits fraction)
q124 = q(int, 12, 4)


# Beat generators - These functions produce waves at a given
#                   number of 'beats per minute'.  Internally, they use
#                   the Arduino function 'millis' to track elapsed time.
#                   Accuracy is a bit better than one part in a thousand.
# 
#       beat8( BPM ) returns an 8-bit value that cycles 'BPM' times
#                    per minute, rising from 0 to 255, resetting to zero,
#                    rising up again, etc..  The output of this function
#                    is suitable for feeding directly into sin8, and cos8,
#                    triwave8, quadwave8, and cubicwave8.
#       beat16( BPM ) returns a 16-bit value that cycles 'BPM' times
#                    per minute, rising from 0 to 65535, resetting to zero,
#                    rising up again, etc.  The output of this function is
#                    suitable for feeding directly into sin16 and cos16.
#       beat88( BPM88) is the same as beat16, except that the BPM88 argument
#                    MUST be in Q8.8 fixed point format, e.g. 120BPM must
#                    be specified as 120*256 = 30720.
#       beatsin8( BPM, uint8_t low, uint8_t high) returns an 8-bit value that
#                    rises and falls in a sine wave, 'BPM' times per minute,
#                    between the values of 'low' and 'high'.
#       beatsin16( BPM, uint16_t low, uint16_t high) returns a 16-bit value
#                    that rises and falls in a sine wave, 'BPM' times per
#                    minute, between the values of 'low' and 'high'.
#       beatsin88( BPM88, ...) is the same as beatsin16, except that the
#                    BPM88 argument MUST be in Q8.8 fixed point format,
#                    e.g. 120BPM must be specified as 120*256 = 30720.
# 
#  BPM can be supplied two ways.  The simpler way of specifying BPM is as
#  a simple 8-bit integer from 1-255, (e.g., "120").
#  The more sophisticated way of specifying BPM allows for fractional
#  "Q8.8" fixed point number (an 'accum88') with an 8-bit integer part and
#  an 8-bit fractional part.  The easiest way to construct this is to multiply
#  a floating point BPM value (e.g. 120.3) by 256, (e.g. resulting in 30796
#  in this case), and pass that as the 16-bit BPM argument.
#  "BPM88" MUST always be specified in Q8.8 format.
# 
#  Originally designed to make an entire animation project pulse with brightness.
#  For that effect, add this line just above your existing call to "FastLED.show()":
# 
#     uint8_t bright = beatsin8( 60 /*BPM*/, 192 /*dimmest*/, 255 /*brightest*/ ));
#     FastLED.setBrightness( bright );
#     FastLED.show();
# 
#  The entire animation will now pulse between brightness 192 and 255 once per second.


# The beat generators need access to a millisecond counter.
# On Arduino, this is "millis()".  On other platforms, you'll
# need to provide a function with this signature:
#   uint32_t get_millisecond_timer();
# that provides similar functionality.
# You can also force use of the get_millisecond_timer function
# by #defining USE_GET_MILLISECOND_TIMER.
#if (defined(ARDUINO) || defined(SPARK) || defined(FASTLED_HAS_MILLIS)) && !defined(USE_GET_MILLISECOND_TIMER)
# Forward declaration of Arduino function 'millis'.
# uint32_t millis();

def get_millisecond_timer():
    import utime
    return utime.ticks_ms()

GET_MILLIS = get_millisecond_timer

# beat16 generates a 16-bit 'sawtooth' wave at a given BPM,
#        with BPM specified in Q8.8 fixed-point format; e.g.
#        for this function, 120 BPM MUST BE specified as
#        120*256 = 30720.
#        If you just want to specify "120", use beat16 or beat8.
def beat88(beats_per_minute_88, timebase=0):
    # BPM is 'beats per minute', or 'beats per 60000ms'.
    # To avoid using the (slower) division operator, we
    # want to convert 'beats per 60000ms' to 'beats per 65536ms',
    # and then use a simple, fast bit-shift to divide by 65536.
    # 
    # The ratio 65536:60000 is 279.620266667:256; we'll call it 280:256.
    # The conversion is accurate to about 0.05%, more or less,
    # e.g. if you ask for "120 BPM", you'll get about "119.93".
    return ((GET_MILLIS() - timebase) * beats_per_minute_88 * 280) >> 16


# beat16 generates a 16-bit 'sawtooth' wave at a given BPM
def beat16(beats_per_minute, timebase=0):
    # Convert simple 8-bit BPM's to full Q8.8 accum88's if needed
    if beats_per_minute < 256:
        beats_per_minute <<= 8

    return beat88(beats_per_minute, timebase)


# beat8 generates an 8-bit 'sawtooth' wave at a given BPM
def beat8(beats_per_minute, timebase=0):
    return beat16(beats_per_minute, timebase) >> 8


# beatsin88 generates a 16-bit sine wave at a given BPM,
#           that oscillates within a given range.
#           For this function, BPM MUST BE SPECIFIED as
#           a Q8.8 fixed-point value; e.g. 120BPM must be
#           specified as 120*256 = 30720.
#           If you just want to specify "120", use beatsin16 or beatsin8.
def beatsin88(
    beats_per_minute_88,
    lowest=0,
    highest=65535,
    timebase=0,
    phase_offset=0
):
    beat = beat88(beats_per_minute_88, timebase)
    beatsin = sin16(beat + phase_offset) + 32768
    rangewidth = highest - lowest
    scaledbeat = scale16(beatsin, rangewidth)
    result = lowest + scaledbeat
    return result


# beatsin16 generates a 16-bit sine wave at a given BPM,
#           that oscillates within a given range.
def beatsin16(
    beats_per_minute,
    lowest=0,
    highest=65535,
    timebase=0,
    phase_offset=0
):
    beat = beat16( beats_per_minute, timebase)
    beatsin = sin16( beat + phase_offset) + 32768
    rangewidth = highest - lowest
    scaledbeat = scale16(beatsin, rangewidth)
    result = lowest + scaledbeat
    return result


# beatsin8 generates an 8-bit sine wave at a given BPM,
#           that oscillates within a given range.
def beatsin8(
    beats_per_minute,
    lowest=0,
    highest=255,
    timebase=0,
    phase_offset=0
):
    beat = beat8(beats_per_minute, timebase)
    beatsin = sin8(beat + phase_offset)
    rangewidth = highest - lowest
    scaledbeat = scale8(beatsin, rangewidth)
    result = lowest + scaledbeat
    return result


# Return the current seconds since boot in a 16-bit value.  Used as part of the
# "every N time-periods" mechanism
def seconds16():
    ms = GET_MILLIS()
    s16 = int(ms / 1000)
    return s16


# Return the current minutes since boot in a 16-bit value.  Used as part of the
# "every N time-periods" mechanism
def minutes16():
    ms = GET_MILLIS()
    m16 = int(ms / 60000) & 0xFFFF
    return m16


# Return the current hours since boot in an 8-bit value.  Used as part of the
# "every N time-periods" mechanism
def hours8():
    ms = GET_MILLIS()
    h8 = int(ms / 3600000) & 0xFF
    return h8


# Helper routine to divide a 32-bit value by 1024, returning
# only the low 16 bits. You'd think this would be just
#   result = (in32 >> 10) & 0xFFFF;
# and on ARM, that's what you want and all is well.
# But on AVR that code turns into a loop that executes
# a four-byte shift ten times: 40 shifts in all, plus loop
# overhead. This routine gets exactly the same result with
# just six shifts (vs 40), and no loop overhead.
# Used to convert millis to 'binary seconds' aka bseconds:
# one bsecond == 1024 millis.
def div1024_32_16(in32):
    out16 = int(in32 >> 10) & 0xFFFF
    return out16


# bseconds16 returns the current time-since-boot in
# "binary seconds", which are actually 1024/1000 of a
# second long.
def bseconds16():
    ms = GET_MILLIS()
    s16 = div1024_32_16(ms)
    return s16


# Classes to implement "Every N Milliseconds", "Every N Seconds",
# "Every N Minutes", "Every N Hours", and "Every N BSeconds".
#if 1


class _CEveryNTimePeriods(object):
    _TIMETYPE = None
    _TIMEGETTER = None

    def __init__(self, period=None):
        self.mPeriod = self._TIMETYPE()
        self.mPrevTrigger = self._TIMETYPE()

        self.reset()
        if period is None:
            self.mPeriod = 1
        else:
            self.setPeriod(period)

    def setPeriod(self, period):
        self.mPeriod = period

    def getTime(self):
        return self._TIMETYPE(self._TIMEGETTER())

    def getPeriod(self):
        return self.mPeriod

    def getElapsed(self):
        return self.getTime() - self.mPrevTrigger

    def getRemaining(self):
        return self.mPeriod - self.getElapsed()

    def getLastTriggerTime(self):
        return self.mPrevTrigger

    def ready(self):
        isReady = self.getElapsed() >= self.mPeriod
        if isReady:
            self.reset()

        return isReady

    def reset(self):
        self.mPrevTrigger = self.getTime()

    def trigger(self):
        self.mPrevTrigger = self.getTime() - self.mPeriod

    def __bool__(self):
        return self.ready()


def INSTANTIATE_EVERY_N_TIME_PERIODS(NAME, TIMETYPE, TIMEGETTER):
    cls = type(NAME, (_CEveryNTimePeriods,), dict(_TIMETYPE=TIMETYPE, _TIMEGETTER=TIMEGETTER))
    return cls


CEveryNMillis = INSTANTIATE_EVERY_N_TIME_PERIODS('CEveryNMillis', int, GET_MILLIS)
CEveryNSeconds = INSTANTIATE_EVERY_N_TIME_PERIODS('CEveryNSeconds', int, seconds16)
CEveryNBSeconds = INSTANTIATE_EVERY_N_TIME_PERIODS('CEveryNBSeconds', int, bseconds16)
CEveryNMinutes = INSTANTIATE_EVERY_N_TIME_PERIODS('CEveryNMinutes', int, minutes16)
CEveryNHours = INSTANTIATE_EVERY_N_TIME_PERIODS('CEveryNHours', int, hours8)


def CONCAT_HELPER(x, y):
    return str(x) + str(y)


def CONCAT_MACRO(x, y):
    return CONCAT_HELPER(x, y)


def EVERY_N_MILLIS(N):
    return EVERY_N_MILLIS_I(CONCAT_MACRO(PER, __COUNTER__ ), N)


def EVERY_N_MILLIS_I(NAME, N):
    static CEveryNMillis NAME(N)
    if( NAME )


def EVERY_N_SECONDS(N):
    return EVERY_N_SECONDS_I(CONCAT_MACRO(PER, __COUNTER__ ), N)


def EVERY_N_SECONDS_I(NAME, N):
    static CEveryNSeconds NAME(N)
    if( NAME )


def EVERY_N_BSECONDS(N):
    return EVERY_N_BSECONDS_I(CONCAT_MACRO(PER, __COUNTER__ ), N)


def EVERY_N_BSECONDS_I(NAME, N):
    static CEveryNBSeconds NAME(N)
    if( NAME )


def EVERY_N_MINUTES(N):
    return EVERY_N_MINUTES_I(CONCAT_MACRO(PER, __COUNTER__ ), N)


def EVERY_N_MINUTES_I(NAME, N):
    static CEveryNMinutes NAME(N)
    if( NAME )


def EVERY_N_HOURS(N):
    return EVERY_N_HOURS_I(CONCAT_MACRO(PER, __COUNTER__ ), N)


def EVERY_N_HOURS_I(NAME, N):
    static CEveryNHours NAME(N)
    if( NAME )


class CEveryNMilliseconds(CEveryNMillis):
    pass


def EVERY_N_MILLISECONDS(N):
    return EVERY_N_MILLIS(N)


def EVERY_N_MILLISECONDS_I(NAME, N):
    return EVERY_N_MILLIS_I(NAME, N)


RAND16_SEED = 1337
rand16seed = RAND16_SEED


# memset8, memcpy8, memmove8:
#  optimized avr replacements for the standard "C" library
#  routines memset, memcpy, and memmove.
# 
#  There are two techniques that make these routines
#  faster than the standard avr-libc routines.
#  First, the loops are unrolled 2X, meaning that
#  the average loop overhead is cut in half.
#  And second, the compare-and-branch at the bottom
#  of each loop decrements the low byte of the
#  counter, and if the carry is clear, it branches
#  back up immediately.  Only if the low byte math
#  causes carry do we bother to decrement the high
#  byte and check that result for carry as well.
#  Results for a 100-byte buffer are 20-40% faster
#  than standard avr-libc, at a cost of a few extra
#  bytes of code.
#
#
# #if 0
# # TEST / VERIFICATION CODE ONLY BELOW THIS POINT
# #include <Arduino.h>
# #include "lib8tion.h"
#
# void test1abs( int8_t i)
# {
#     Serial.print("abs("); Serial.print(i); Serial.print(") = ");
#     int8_t j = abs8(i);
#     Serial.print(j); Serial.println(" ");
# }
#
# void testabs()
# {
#     delay(5000);
#     for( int8_t q = -128; q != 127; q++) {
#         test1abs(q);
#     }
#     for(;;){};
# }
#
#
# void testmul8()
# {
#     delay(5000);
#     byte r, c;
#
#     Serial.println("mul8:");
#     for( r = 0; r <= 20; r += 1) {
#         Serial.print(r); Serial.print(" : ");
#         for( c = 0; c <= 20; c += 1) {
#             byte t;
#             t = mul8( r, c);
#             Serial.print(t); Serial.print(' ');
#         }
#         Serial.println(' ');
#     }
#     Serial.println("done.");
#     for(;;){};
# }
#
#
# void testscale8()
# {
#     delay(5000);
#     byte r, c;
#
#     Serial.println("scale8:");
#     for( r = 0; r <= 240; r += 10) {
#         Serial.print(r); Serial.print(" : ");
#         for( c = 0; c <= 240; c += 10) {
#             byte t;
#             t = scale8( r, c);
#             Serial.print(t); Serial.print(' ');
#         }
#         Serial.println(' ');
#     }
#
#     Serial.println(' ');
#     Serial.println("scale8_video:");
#
#     for( r = 0; r <= 100; r += 4) {
#         Serial.print(r); Serial.print(" : ");
#         for( c = 0; c <= 100; c += 4) {
#             byte t;
#             t = scale8_video( r, c);
#             Serial.print(t); Serial.print(' ');
#         }
#         Serial.println(' ');
#     }
#
#     Serial.println("done.");
#     for(;;){};
# }
#
#
#
# void testqadd8()
# {
#     delay(5000);
#     byte r, c;
#     for( r = 0; r <= 240; r += 10) {
#         Serial.print(r); Serial.print(" : ");
#         for( c = 0; c <= 240; c += 10) {
#             byte t;
#             t = qadd8( r, c);
#             Serial.print(t); Serial.print(' ');
#         }
#         Serial.println(' ');
#     }
#     Serial.println("done.");
#     for(;;){};
# }
#
# void testnscale8x3()
# {
#     delay(5000);
#     byte r, g, b, sc;
#     for( byte z = 0; z < 10; z++) {
#         r = random8(); g = random8(); b = random8(); sc = random8();
#
#         Serial.print("nscale8x3_video( ");
#         Serial.print(r); Serial.print(", ");
#         Serial.print(g); Serial.print(", ");
#         Serial.print(b); Serial.print(", ");
#         Serial.print(sc); Serial.print(") = [ ");
#
#         nscale8x3_video( r, g, b, sc);
#
#         Serial.print(r); Serial.print(", ");
#         Serial.print(g); Serial.print(", ");
#         Serial.print(b); Serial.print("]");
#
#         Serial.println(' ');
#     }
#     Serial.println("done.");
#     for(;;){};
# }
#
# #endif
