# @ingroup lib8tion

# @defgroup Trig Fast trig functions
# Fast 8 and 16-bit approximations of sin(x) and cos(x).
#        Don't use these approximations for calculating the
#        trajectory of a rocket to Mars, but they're great
#        for art projects and LED displays.
# 
#        On Arduino/AVR, the 16-bit approximation is more than
#        10X faster than floating point sin(x) and cos(x), while
# the 8-bit approximation is more than 20X faster.
# @{


# Fast 16-bit approximation of sin(x). This approximation never varies more than
# 0.69% from the floating point value you'd get by doing
# 
#     float s = sin(x) * 32767.0;
# 
# @param theta input angle from 0-65535
# @returns sin of theta, value between -32767 to 32767.
def sin16_C(theta):
    base = [0, 6393, 12539, 18204, 23170, 27245, 30273, 32137]
    slope = [49, 48, 44, 38, 31, 23, 14, 4]

    offset = (theta & 0x3FFF) >> 3  # 0..2047

    if theta & 0x4000:
        offset = 2047 - offset

    section = offset / 256  # 0..7
    b = base[section]
    m = slope[section]

    secoffset8 = offset / 2

    mx = m * secoffset8
    y = mx + b

    if theta & 0x8000:
        y = -y

    return y


sin16 = sin16_C


# Fast 16-bit approximation of cos(x). This approximation never varies more than
# 0.69% from the floating point value you'd get by doing
# 
#     float s = cos(x) * 32767.0;
# 
# @param theta input angle from 0-65535
# @returns sin of theta, value between -32767 to 32767.
def cos16(theta):
    return sin16(theta + 16384)

# # # # # # # # # # # # # # # # # # # # # # # # 

# sin8 & cos8
#        Fast 8-bit approximations of sin(x) & cos(x).
#        Input angle is an unsigned int from 0-255.
#        Output is an unsigned int from 0 to 255.
# 
#        This approximation can vary to to 2%
#        from the floating point value you'd get by doing
#          float s = (sin( x ) * 128.0) + 128;
# 
#        Don't use this approximation for calculating the
#        "real" trigonometric calculations, but it's great
#        for art projects and LED displays.
# 
#        On Arduino/AVR, this approximation is more than
#        20X faster than floating point sin(x) and cos(x)


b_m16_interleave = [0, 49, 49, 41, 90, 27, 117, 10]


# Fast 8-bit approximation of sin(x). This approximation never varies more than
# 2% from the floating point value you'd get by doing
# 
#     float s = (sin(x) * 128.0) + 128;
# 
# @param theta input angle from 0-255
# @returns sin of theta, value between 0 and 255
def sin8_C(theta):
    offset = theta
    if theta & 0x40:
        offset = 255 - offset

    offset &= 0x3F  # 0..63

    secoffset = offset & 0x0F  # 0..15
    if theta & 0x40:
        secoffset += 1

    section = offset >> 4  # 0..3
    s2 = section * 2
    p = b_m16_interleave[:]
    p = p[s2:]

    b = p[0]
    p.pop(0)
    m16 = p[0]
    mx = (m16 * secoffset) >> 4

    y = mx + b
    if theta & 0x80:
        y = -y

    y += 128

    return y


sin8 = sin8_C


# Fast 8-bit approximation of cos(x). This approximation never varies more than
# 2% from the floating point value you'd get by doing
# 
#     float s = (cos(x) * 128.0) + 128;
# 
# @param theta input angle from 0-255
# @returns sin of theta, value between 0 and 255
def cos8(theta):
    return sin8(theta + 64)
