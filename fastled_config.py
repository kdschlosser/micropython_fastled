# @file fastled_config.h
# contains definitions that can be used to configure FastLED at compile time

# Use this option only for debugging pin access and forcing software pin access.  Note that
# software pin access only works in Arduino based environments.  Forces use of digitalWrite
# methods for pin access vs. direct hardware port access
FASTLED_FORCE_SOFTWARE_PINS = 0

# Use this option only for debugging bitbang'd spi access or to work around bugs in hardware
# spi access.  Forces use of bit-banged spi, even on pins that has hardware SPI available.
FASTLED_FORCE_SOFTWARE_SPI = 0

# Use this to force FastLED to allow interrupts in the clockless chipsets (or to force it to
# disallow), overriding the default on platforms that support this.  Set the value to 1 to
# allow interrupts or 0 to disallow them.
FASTLED_ALLOW_INTERRUPTS = 0
# FASTLED_ALLOW_INTERRUPTS = 1

# Use this to allow some integer overflows/underflows in the inoise functions.
# The original implementions allowed this, and had some discontinuties in the noise
# output.  It's technically an implementation bug, and was fixed, but you may wish
# to preserve the old look and feel of the inoise functions in your existing animations.
# The default is 0:  NO overflow, and 'continuous' noise output, aka the fixed way.
FASTLED_NOISE_ALLOW_AVERAGE_TO_OVERFLOW = 0
# FASTLED_NOISE_ALLOW_AVERAGE_TO_OVERFLOW = 1

# Use this toggle whether or not to use the 'fixed' FastLED scale8.  The initial scale8
# had a problem where scale8(255,255) would give you 254.  This is now fixed, and that
# fix is enabled by default.  However, if for some reason you have code that is not
# working right as a result of this (e.g. code that was expecting the old scale8 behavior)
# you can disable it here.
FASTLED_SCALE8_FIXED = 1
# FASTLED_SCALE8_FIXED = 0

# Use this toggle whether to use 'fixed' FastLED pixel blending, including ColorFromPalette.
# The prior pixel blend functions had integer-rounding math errors that led to
# small errors being inadvertently added to the low bits of blended colors, including colors
# retrieved from color palettes using LINEAR_BLEND.  This is now fixed, and the
# fix is enabled by default.  However, if for some reason you wish to run with the old
# blending, including the integer rounding and color errors, you can disable the bugfix here.
FASTLED_BLEND_FIXED = 1
# FASTLED_BLEND_FIXED = 0

# Use this toggle whether to use 'fixed' FastLED 8- and 16-bit noise functions.
# The prior noise functions had some math errors that led to 'discontinuities' in the
# output, which by definition should be smooth and continuous.  The bug led to 
# noise function output that had 'edges' and glitches in it.  This is now fixed, and the
# fix is enabled by default.  However, if for some reason you wish to run with the old
# noise code, including the glitches, you can disable the bugfix here.
FASTLED_NOISE_FIXED = 1
# FASTLED_NOISE_FIXED = 0

# Use this to determine how many times FastLED will attempt to re-transmit a frame if interrupted
# for too long by interrupts.
FASTLED_INTERRUPT_RETRY_COUNT = 2

# Use this toggle to enable global brightness in contollers that support is (ADA102 and SK9822).
# It changes how color scaling works and uses global brightness before scaling down color values.
# This enable much more accurate color control on low brightness settings.
FASTLED_USE_GLOBAL_BRIGHTNESS = 0
# FASTLED_USE_GLOBAL_BRIGHTNESS = 1


NO_DITHERING = 0
NO_CORRECTION = 0
FASTLED_HAS_BLOCKLESS = 0
PORTA_FIRST_PIN = 0
PORTB_FIRST_PIN = 0
PORTC_FIRST_PIN = 0
PORTD_FIRST_PIN = 0
HAS_PORTDC = 0
SmartMatrix_h = 0
USE_WS2812SERIAL = 0
USE_OCTOWS2811 = 0
FASTSPI_USE_DMX_SIMPLE = 0
__FASTLED_HAS_FIBCC = 0
FASTLED_HAS_CLOCKLESS = 0
SPI_DATA = 0
FASTLED_ACCURATE_CLOCK = 1
