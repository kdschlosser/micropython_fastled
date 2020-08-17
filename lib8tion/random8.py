
# @ingroup lib8tion

# @defgroup Random Fast random number generators
# Fast 8- and 16- bit unsigned random numbers.
#  Significantly faster than Arduino random(), but
#  also somewhat less random.  You can add entropy.
# @{

# X(n+1) = (2053 * X(n)) + 13849)
FASTLED_RAND16_2053 = 2053
FASTLED_RAND16_13849 = 13849


def APPLY_FASTLED_RAND16_2053(x):
    return x * FASTLED_RAND16_2053


# random number seed
rand16seed = 0  # = RAND16_SEED;


# Generate an 8-bit random number between 0 and lim
# @param lim the upper bound for the result
def random8(min_=None, lim=None):
    if min_ is None and lim is None:
        global rand16seed
        rand16seed = APPLY_FASTLED_RAND16_2053(rand16seed) + FASTLED_RAND16_13849

        # return the sum of the high and low bytes, for better
        #  mixing and non-sequential correlation
        return (
                (rand16seed & 0xFF) +
                (rand16seed >> 8)
        )
    elif lim is None:
        lim = min_
        r = random8()
        r = (r * lim) >> 8
        return r

    else:
        # Generate an 8-bit random number in the given range
        # @param min the lower bound for the random number
        # @param lim the upper bound for the random number
        delta = lim - min_
        r = random8(delta) + min_
        return r


# Generate a 16 bit random number
def random16(min_=None, lim=None):
    if min_ is None and lim is None:
        global rand16seed
        rand16seed = APPLY_FASTLED_RAND16_2053(rand16seed) + FASTLED_RAND16_13849
        return rand16seed

    elif lim is None:
        # Generate an 16-bit random number between 0 and lim
        # @param lim the upper bound for the result
        lim = min_
        r = random16()
        p = lim * r
        r = p >> 16
        return r

    else:
        # Generate an 16-bit random number in the given range
        # @param min the lower bound for the random number
        # @param lim the upper bound for the random number
        delta = lim - min
        r = random16(delta) + min
        return r


# Set the 16-bit seed used for the random number generator
def random16_set_seed(seed):
    global rand16seed
    rand16seed = seed


# Get the current seed value for the random number generator
def random16_get_seed():
    return rand16seed


# Add entropy into the random number generator
def random16_add_entropy(entropy):
    global rand16seed
    rand16seed += entropy
