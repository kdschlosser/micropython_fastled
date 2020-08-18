
from .scale8 import *

# @ingroup lib8tion

# @defgroup Math Basic math operations
# Fast, efficient 8-bit math functions specifically
# designed for high-performance LED programming.
# 
# Because of the AVR(Arduino) and ARM assembly language
# implementations provided, using these functions often
# results in smaller and faster code than the equivalent
# program using plain "C" arithmetic and logic.
# @{


# add one byte to another, saturating at 0xFF
# @param i - first byte to add
# @param j - second byte to add
# @returns the sum of i & j, capped at 0xFF
def qadd8(i, j):
    t = i + j
    if t > 255:
        t = 255

    return t


# Add one byte to another, saturating at 0x7F
# @param i - first byte to add
# @param j - second byte to add
# @returns the sum of i & j, capped at 0xFF
def qadd7(i, j):
    t = i + j
    if t > 127:
        t = 127
    return t


# subtract one byte from another, saturating at 0x00
# @returns i - j with a floor of 0
def qsub8(i, j):
    t = i - j
    if t < 0:
        t = 0

    return t


# add one byte to another, with one byte result
def add8(i, j):
    t = i + j
    return t


# add one byte to another, with one byte result
def add8to16(i, j):
    t = i + j
    return t


# subtract one byte from another, 8-bit result
def sub8(i, j):
    t = i - j
    return t


# Calculate an integer average of two unsigned
#       8-bit integer values (uint8_t).
#       Fractional results are rounded down, e.g. avg8(20,41) = 30
def avg8(i, j):
    return (i + j) >> 1


# Calculate an integer average of two unsigned
#       16-bit integer values (uint16_t).
#       Fractional results are rounded down, e.g. avg16(20,41) = 30
def avg16(i, j):
    return (i + j) >> 1


# Calculate an integer average of two signed 7-bit
#       integers (int8_t)
#       If the first argument is even, result is rounded down.
#       If the first argument is odd, result is result up.
def avg7(i, j):
    return ((i + j) >> 1) + (i & 0x1)


# Calculate an integer average of two signed 15-bit
#       integers (int16_t)
#       If the first argument is even, result is rounded down.
#       If the first argument is odd, result is result up.
def avg15(i, j):
    return ((i + j) >> 1) + (i & 0x1)


#       Calculate the remainder of one unsigned 8-bit
#       value divided by anoter, aka A % M.
#       Implemented by repeated subtraction, which is
#       very compact, and very fast if A is 'probably'
#       less than M.  If A is a large multiple of M,
#       the loop has to execute multiple times.  However,
#       even in that case, the loop is only two
#       instructions long on AVR, i.e., quick.
def mod8(a, m):
    while a >= m:
        a -= m

    return a


#          Add two numbers, and calculate the modulo
#          of the sum and a third number, M.
#          In other words, it returns (A+B) % M.
#          It is designed as a compact mechanism for
#          incrementing a 'mode' switch and wrapping
#          around back to 'mode 0' when the switch
#          goes past the end of the available range.
#          e.g. if you have seven modes, this switches
#          to the next one and wraps around if needed:
#            mode = addmod8( mode, 1, 7);
# LIB8STATIC_ALWAYS_INLINESee 'mod8' for notes on performance.
def addmod8(a, b, m):
    a += b
    while a >= m:
        a -= m
    return a


#          Subtract two numbers, and calculate the modulo
#          of the difference and a third number, M.
#          In other words, it returns (A-B) % M.
#          It is designed as a compact mechanism for
#          incrementing a 'mode' switch and wrapping
#          around back to 'mode 0' when the switch
#          goes past the end of the available range.
#          e.g. if you have seven modes, this switches
#          to the next one and wraps around if needed:
#            mode = addmod8( mode, 1, 7);
# LIB8STATIC_ALWAYS_INLINESee 'mod8' for notes on performance.
def submod8(a, b, m):
    a -= b
    while a >= m:
        a -= m

    return a


# 8x8 bit multiplication, with 8 bit result
def mul8(i, j):
    return (i * j) & 0xFF


# saturating 8x8 bit multiplication, with 8 bit result
# @returns the product of i * j, capping at 0xFF
def qmul8(i, j):
    p = i * j
    if p > 255:
        p = 255

    return p


# take abs() of a signed 8-bit uint8_t
def abs8(i):
    return abs(i)


#         square root for 16-bit integers
#         About three times faster and five times smaller
#         than Arduino's general sqrt on AVR.
def sqrt16(x):
    if x <= 1:
        return x

    low = 1

    if x > 7904:
        hi = 255
    else:
        hi = (x >> 5) + 8  # initial estimate for upper bound

    while hi >= low:
        mid = (low + hi) >> 1

        if (mid * mid) > x:
            hi = mid - 1
        else:
            if mid == 255:
                return 255

            low = mid + 1

    return low - 1


# blend a variable proproportion(0-255) of one byte to another
# @param a - the starting byte value
# @param b - the byte value to blend toward
# @param amountOfB - the proportion (0-255) of b to blend
# @returns a byte value between a and b, inclusive
def blend8(a, b, amountOfB):
    if FASTLED_BLEND_FIXED == 1:
        amountOfA = 255 - amountOfB
        partial = (a * amountOfA)

        if FASTLED_SCALE8_FIXED == 1:
            partial += a
            # partial = add8to16( a, partial)
    
        partial += b * amountOfB

        if FASTLED_SCALE8_FIXED == 1:
            partial += b
            # partial = add8to16( b, partial)
    
        result = partial >> 8
    
        return result

    else:
        # This version loses precision in the integer math
        # and can actually return results outside of the range
        # from a to b.  Its use is not recommended.
        amountOfA = 255 - amountOfB
        result = (
            scale8_LEAVING_R1_DIRTY(a, amountOfA) +
            scale8_LEAVING_R1_DIRTY(b, amountOfB)
        )
        cleanup_R1()
        return result
