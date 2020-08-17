from .fastled_config import *

# @file FastLED.h
# central include file for FastLED, defines the CFastLED class/object

FASTLED_VERSION = 3003002
#  ifndef FASTLED_INTERNAL
#    ifdef FASTLED_HAS_PRAGMA_MESSAGE
#      pragma message "FastLED version 3.003.003"
#    else
#      warning FastLED version 3.003.003  (Not really a warning, just telling you here.)
#    endif
#  endif


# ifdef SmartMatrix_h
# include <SmartMatrix.h>
# endif

# ifdef DmxSimple_h
# include <DmxSimple.h>
# endif

# ifdef DmxSerial_h
# include <DMXSerial.h>
# endif

import time

from .cpp_compat import *

from .fastled_config import *
from .fastled_config import __FASTLED_HAS_FIBCC
from .led_sysdefs import *
\
# Utility functions
from .fastled_delay import *
from .bitswap import *

from .controller import *
from .fastpin import *
from .fastspi_types import *
from .dmx import *

from .platforms import *
from .fastled_progmem import *

from .lib8tion import *
from .pixeltypes import *
from .hsv2rgb import *
from .colorutils import *
from .pixelset import *
from .colorpalettes import *

from .noise import *
from .power_mgt import *

from .fastspi import *
from .chipsets import *

# definitions for the spi chipset constants
LPD6803 = 0
LPD8806 = 1
WS2801 = 2
WS2803 = 3
SM16716 = 4
P9813 = 5
APA102 = 6
SK9822 = 7
DOTSTAR = 8

SMART_MATRIX = 0
OCTOWS2811 = 0
OCTOWS2811_400 = 1
OCTOWS2813 = 2
WS2812SERIAL = 0


class PIXIE(PixieController):
    def __init__(self, DATA_PIN, RGB_ORDER):
        PixieController.__init__(self, DATA_PIN, RGB_ORDER)


class NEOPIXEL(WS2812Controller800Khz):
    def __init__(self, DATA_PIN, GRB):
        WS2812Controller800Khz.__init__(self, DATA_PIN, GRB)


class SM16703(SM16703Controller):
    def __init__(self, DATA_PIN, RGB_ORDER):
        SM16703Controller.__init__(self, DATA_PIN, RGB_ORDER)


class TM1829(TM1829Controller800Khz):
    def __init__(self, DATA_PIN, RGB_ORDER):
        TM1829Controller800Khz.__init__(self, DATA_PIN, RGB_ORDER)


class TM1812(TM1809Controller800Khz):
    def __init__(self, DATA_PIN, RGB_ORDER):
        TM1809Controller800Khz.__init__(self, DATA_PIN, RGB_ORDER)


class TM1809(TM1809Controller800Khz):
    def __init__(self, DATA_PIN, RGB_ORDER):
        TM1809Controller800Khz.__init__(self, DATA_PIN, RGB_ORDER)


class TM1804(TM1809Controller800Khz):
    def __init__(self, DATA_PIN, RGB_ORDER):
        TM1809Controller800Khz.__init__(self, DATA_PIN, RGB_ORDER)


class TM1803(TM1803Controller400Khz):
    def __init__(self, DATA_PIN, RGB_ORDER):
        TM1803Controller400Khz.__init__(self, DATA_PIN, RGB_ORDER)


class UCS1903(UCS1903Controller400Khz):
    def __init__(self, DATA_PIN, RGB_ORDER):
        UCS1903Controller400Khz.__init__(self, DATA_PIN, RGB_ORDER)


class UCS1903B(UCS1903BController800Khz):
    def __init__(self, DATA_PIN, RGB_ORDER):
        UCS1903BController800Khz.__init__(self, DATA_PIN, RGB_ORDER)


class UCS1904(UCS1904Controller800Khz):
    def __init__(self, DATA_PIN, RGB_ORDER):
        UCS1904Controller800Khz.__init__(self, DATA_PIN, RGB_ORDER)


class UCS2903(UCS2903Controller):
    def __init__(self, DATA_PIN, RGB_ORDER):
        UCS2903Controller.__init__(self, DATA_PIN, RGB_ORDER)


class WS2812(WS2812Controller800Khz):
    def __init__(self, DATA_PIN, RGB_ORDER):
        WS2812Controller800Khz.__init__(self, DATA_PIN, RGB_ORDER)


class WS2852(WS2812Controller800Khz):
    def __init__(self, DATA_PIN, RGB_ORDER):
        WS2812Controller800Khz.__init__(self, DATA_PIN, RGB_ORDER)


class WS2812B(WS2812Controller800Khz):
    def __init__(self, DATA_PIN, RGB_ORDER):
        WS2812Controller800Khz.__init__(self, DATA_PIN, RGB_ORDER)


class GS1903(WS2812Controller800Khz):
    def __init__(self, DATA_PIN, RGB_ORDER):
        WS2812Controller800Khz.__init__(self, DATA_PIN, RGB_ORDER)


class SK6812(SK6812Controller):
    def __init__(self, DATA_PIN, RGB_ORDER):
        SK6812Controller.__init__(self, DATA_PIN, RGB_ORDER)


class SK6822(SK6822Controller):
    def __init__(self, DATA_PIN, RGB_ORDER):
        SK6822Controller.__init__(self, DATA_PIN, RGB_ORDER)


class APA106(SK6822Controller):
    def __init__(self, DATA_PIN, RGB_ORDER):
        SK6822Controller.__init__(self, DATA_PIN, RGB_ORDER)


class PL9823(PL9823Controller):
    def __init__(self, DATA_PIN, RGB_ORDER):
        PL9823Controller.__init__(self, DATA_PIN, RGB_ORDER)


class WS2811(WS2811Controller800Khz):
    def __init__(self, DATA_PIN, RGB_ORDER):
        WS2811Controller800Khz.__init__(self, DATA_PIN, RGB_ORDER)


class WS2813(WS2813Controller):
    def __init__(self, DATA_PIN, RGB_ORDER):
        WS2813Controller.__init__(self, DATA_PIN, RGB_ORDER)


class APA104(WS2811Controller800Khz):
    def __init__(self, DATA_PIN, RGB_ORDER):
        WS2811Controller800Khz.__init__(self, DATA_PIN, RGB_ORDER)


class WS2811_400(WS2811Controller400Khz):
    def __init__(self, DATA_PIN, RGB_ORDER):
        WS2811Controller400Khz.__init__(self, DATA_PIN, RGB_ORDER)


class GE8822(GE8822Controller800Khz):
    def __init__(self, DATA_PIN, RGB_ORDER):
        GE8822Controller800Khz.__init__(self, DATA_PIN, RGB_ORDER)


class GW6205(GW6205Controller800Khz):
    def __init__(self, DATA_PIN, RGB_ORDER):
        GW6205Controller800Khz.__init__(self, DATA_PIN, RGB_ORDER)


class GW6205_400(GW6205Controller400Khz):
    def __init__(self, DATA_PIN, RGB_ORDER):
        GW6205Controller400Khz.__init__(self, DATA_PIN, RGB_ORDER)


class LPD1886(LPD1886Controller1250Khz):
    def __init__(self, DATA_PIN, RGB_ORDER):
        LPD1886Controller1250Khz.__init__(self, DATA_PIN, RGB_ORDER)


class LPD1886_8BIT(LPD1886Controller1250Khz_8bit):
    def __init__(self, DATA_PIN, RGB_ORDER):
        LPD1886Controller1250Khz_8bit.__init__(self, DATA_PIN, RGB_ORDER)


class DMXSIMPLE(DMXSimpleController):
    def __init__(self, DATA_PIN, RGB_ORDER):
        DMXSimpleController.__init__(self, DATA_PIN, RGB_ORDER)


class DMXSERIAL(DMXSerialController):
    def __init__(self, RGB_ORDER):
        DMXSerialController.__init__(self, RGB_ORDER)


WS2811_PORTA = 0
WS2813_PORTA = 1
WS2811_400_PORTA = 2
TM1803_PORTA = 3
UCS1903_PORTA = 4

WS2811_PORTB = 0
WS2813_PORTB = 1
WS2811_400_PORTB = 2
TM1803_PORTB = 3
UCS1903_PORTB = 4

WS2811_PORTC = 0
WS2813_PORTC = 1
WS2811_400_PORTC = 2
TM1803_PORTC = 3
UCS1903_PORTC = 4

WS2811_PORTD = 0
WS2813_PORTD = 1
WS2811_400_PORTD = 2
TM1803_PORTD = 3
UCS1903_PORTD = 4

WS2811_PORTDC = 5
WS2813_PORTDC = 6
WS2811_400_PORTDC = 7
TM1803_PORTDC = 8
UCS1903_PORTDC = 9

NUM_CONTROLLERS = 8


# High level controller interface for FastLED.  This class manages controllers, global settings and trackings
# such as brightness, and refresh rates, and provides access functions for driving led data to controllers
# via the show/showColor/clear methods.
# @nosubgrouping
class CFastLED(object):
    # int m_nControllers

    def __init__(self):
        self.m_Scale = 255  # < The current global brightness scale setting
        self.m_nFPS = 0  # < Tracking for current FPS value
        self.m_nMinMicros = 0  # < minimum µs between frames, used for capping frame rates.
        self.m_nPowerData = 0xFFFFFFFF  # < max power use parameter
        self.m_pPowerFunc = None  # < function for overriding brightness when using FastLED.show()

    # Add a CLEDController instance to the world.  Exposed to the public to allow people to implement their own
    # CLEDController objects or instances.  There are two ways to call this method (as well as the other addLeds)
    # variations.  The first is with 3 arguments, in which case the arguments are the controller, a pointer to
    # led data, and the number of leds used by this controller.  The second is with 4 arguments, in which case
    # the first two arguments are the same, the third argument is an offset into the CRGB data where this controller's
    # CRGB data begins, and the fourth argument is the number of leds for this controller object.
    # @param pLed - the led controller being added
    # @param data - base point to an array of CRGB data structures
    # @param nLedsOrOffset - number of leds (3 argument version) or offset into the data array
    # @param nLedsIfOffset - number of leds (4 argument version)
    # @returns a reference to the added controller
    def addLeds(self, pLed, data, nLedsOrOffset, nLedsIfOffset=0):
        nOffset = nLedsOrOffset if nLedsIfOffset > 0 else 0
        nLeds = nLedsIfOffset if nLedsIfOffset > 0 else nLedsOrOffset

        pLed.init()
        pLed.setLeds(data[nOffset:], nLeds)
        self.setMaxRefreshRate(pLed.getMaxRefreshRate(), True)
        return pLed

    # @name Adding SPI based controllers
    # @{
    # Add an SPI based  CLEDController instance to the world.
    # There are two ways to call this method (as well as the other addLeds)
    # variations.  The first is with 2 arguments, in which case the arguments are  a pointer to
    # led data, and the number of leds used by this controller.  The second is with 3 arguments, in which case
    # the first  argument is the same, the second argument is an offset into the CRGB data where this controller's
    # CRGB data begins, and the third argument is the number of leds for this controller object.
    #
    # This method also takes a 1 to 5 template parameters for identifying the specific chipset, data and clock pins,
    # RGB ordering, and SPI data rate
    # @param data - base point to an array of CRGB data structures
    # @param nLedsOrOffset - number of leds (3 argument version) or offset into the data array
    # @param nLedsIfOffset - number of leds (4 argument version)
    # @tparam CHIPSET - the chipset type
    # @tparam DATA_PIN - the optional data pin for the leds (if omitted, will default to the first hardware SPI MOSI pin)
    # @tparam CLOCK_PIN - the optional clock pin for the leds (if omitted, will default to the first hardware SPI clock pin)
    # @tparam RGB_ORDER - the rgb ordering for the leds (e.g. what order red, green, and blue data is written out in)
    # @tparam SPI_DATA_RATE - the data rate to drive the SPI clock at, defined using DATA_RATE_MHZ or DATA_RATE_KHZ macros
    # @returns a reference to the added controller
    def addLeds(self, CHIPSET, DATA_PIN, CLOCK_PIN, RGB_ORDER, SPI_DATA_RATE, data, nLedsOrOffset, nLedsIfOffset=0):
        if CHIPSET == LPD6803:
            c = LPD6803Controller(DATA_PIN, CLOCK_PIN, RGB_ORDER, SPI_DATA_RATE)
            return addLeds(c, data, nLedsOrOffset, nLedsIfOffset)
        if CHIPSET == LPD8806:
            c = LPD8806Controller(DATA_PIN, CLOCK_PIN, RGB_ORDER, SPI_DATA_RATE)
            return addLeds(c, data, nLedsOrOffset, nLedsIfOffset)
        if CHIPSET == WS2801:
            c = WS2801Controller(DATA_PIN, CLOCK_PIN, RGB_ORDER, SPI_DATA_RATE)
            return addLeds(c, data, nLedsOrOffset, nLedsIfOffset)
        if CHIPSET == WS2803:
            c = WS2803Controller(DATA_PIN, CLOCK_PIN, RGB_ORDER, SPI_DATA_RATE)
            return addLeds(c, data, nLedsOrOffset, nLedsIfOffset)
        if CHIPSET == SM16716:
            c = SM16716Controller(DATA_PIN, CLOCK_PIN, RGB_ORDER, SPI_DATA_RATE)
            return addLeds(c, data, nLedsOrOffset, nLedsIfOffset)
        if CHIPSET == P9813:
            c = P9813Controller(DATA_PIN, CLOCK_PIN, RGB_ORDER, SPI_DATA_RATE)
            return addLeds(c, data, nLedsOrOffset, nLedsIfOffset)
        if CHIPSET in (DOTSTAR, APA102):
            c = APA102Controller(DATA_PIN, CLOCK_PIN, RGB_ORDER, SPI_DATA_RATE)
            return addLeds(c, data, nLedsOrOffset, nLedsIfOffset)
        if CHIPSET == SK9822:
            c = SK9822Controller(DATA_PIN, CLOCK_PIN, RGB_ORDER, SPI_DATA_RATE)
            return addLeds(c, data, nLedsOrOffset, nLedsIfOffset)

    def addLeds(self, CHIPSET, DATA_PIN, CLOCK_PIN, data, nLedsOrOffset, nLedsIfOffset=0):
        if CHIPSET == LPD6803:
            c = LPD6803Controller(DATA_PIN, CLOCK_PIN)
            return addLeds(c, data, nLedsOrOffset, nLedsIfOffset)
        if CHIPSET == LPD8806:
            c = LPD8806Controller(DATA_PIN, CLOCK_PIN)
            return addLeds(c, data, nLedsOrOffset, nLedsIfOffset)
        if CHIPSET == WS2801:
            c = WS2801Controller(DATA_PIN, CLOCK_PIN)
            return addLeds(c, data, nLedsOrOffset, nLedsIfOffset)
        if CHIPSET == WS2803:
            c = WS2803Controller(DATA_PIN, CLOCK_PIN)
            return addLeds(c, data, nLedsOrOffset, nLedsIfOffset)
        if CHIPSET == SM16716:
            c = SM16716Controller(DATA_PIN, CLOCK_PIN)
            return addLeds(c, data, nLedsOrOffset, nLedsIfOffset)
        if CHIPSET == P9813:
            c = P9813Controller(DATA_PIN, CLOCK_PIN)
            return addLeds(c, data, nLedsOrOffset, nLedsIfOffset)
        if CHIPSET in (DOTSTAR, APA102):
            c = APA102Controller(DATA_PIN, CLOCK_PIN)
            return addLeds(c, data, nLedsOrOffset, nLedsIfOffset)
        if CHIPSET == SK9822:
            c = SK9822Controller(DATA_PIN, CLOCK_PIN)
            return addLeds(c, data, nLedsOrOffset, nLedsIfOffset)

    def addLeds(self, CHIPSET, DATA_PIN, CLOCK_PIN, RGB_ORDER, data, nLedsOrOffset, nLedsIfOffset=0):
        if CHIPSET == LPD6803:
            c = LPD6803Controller(DATA_PIN, CLOCK_PIN, RGB_ORDER)
            return addLeds(c, data, nLedsOrOffset, nLedsIfOffset)
        if CHIPSET == LPD8806:
            c = LPD8806Controller(DATA_PIN, CLOCK_PIN, RGB_ORDER)
            return addLeds(c, data, nLedsOrOffset, nLedsIfOffset)
        if CHIPSET == WS2801:
            c = WS2801Controller(DATA_PIN, CLOCK_PIN, RGB_ORDER)
            return addLeds(c, data, nLedsOrOffset, nLedsIfOffset)
        if CHIPSET == WS2803:
            c = WS2803Controller(DATA_PIN, CLOCK_PIN, RGB_ORDER)
            return addLeds(c, data, nLedsOrOffset, nLedsIfOffset)
        if CHIPSET == SM16716:
            c = SM16716Controller(DATA_PIN, CLOCK_PIN, RGB_ORDER)
            return addLeds(c, data, nLedsOrOffset, nLedsIfOffset)
        if CHIPSET == P9813:
            c = P9813Controller(DATA_PIN, CLOCK_PIN, RGB_ORDER)
            return addLeds(c, data, nLedsOrOffset, nLedsIfOffset)
        if CHIPSET in (DOTSTAR, APA102):
            c = APA102Controller(DATA_PIN, CLOCK_PIN, RGB_ORDER)
            return addLeds(c, data, nLedsOrOffset, nLedsIfOffset)
        if CHIPSET == SK9822:
            c = SK9822Controller(DATA_PIN, CLOCK_PIN, RGB_ORDER)
            return addLeds(c, data, nLedsOrOffset, nLedsIfOffset)

    def addLeds(self, CHIPSET, data, nLedsOrOffset, nLedsIfOffset=0):
        if SPI_DATA:
            return addLeds(CHIPSET, SPI_DATA, SPI_CLOCK, RGB, data, nLedsOrOffset, nLedsIfOffset)

    def addLeds(self, CHIPSET, RGB_ORDER, CRGB, nLedsOrOffset, nLedsIfOffset=0):
        if SPI_DATA:
            return addLeds(CHIPSET, SPI_DATA, SPI_CLOCK, RGB_ORDER, data, nLedsOrOffset, nLedsIfOffset)

    def addLeds(self, CHIPSET, RGB_ORDER, SPI_DATA_RATE, data, nLedsOrOffset, nLedsIfOffset=0):
        return addLeds(CHIPSET, SPI_DATA, SPI_CLOCK, RGB_ORDER, SPI_DATA_RATE, data, nLedsOrOffset, nLedsIfOffset)

    # @name Adding 3-wire led controllers
    # @{
    # Add a clockless (aka 3wire, also DMX) based CLEDController instance to the world.
    # There are two ways to call this method (as well as the other addLeds)
    # variations.  The first is with 2 arguments, in which case the arguments are  a pointer to
    # led data, and the number of leds used by this controller.  The second is with 3 arguments, in which case
    # the first  argument is the same, the second argument is an offset into the CRGB data where this controller's
    # CRGB data begins, and the third argument is the number of leds for this controller object.
    #
    # This method also takes a 2 to 3 template parameters for identifying the specific chipset, data pin, and rgb ordering
    # RGB ordering, and SPI data rate
    # @param data - base point to an array of CRGB data structures
    # @param nLedsOrOffset - number of leds (3 argument version) or offset into the data array
    # @param nLedsIfOffset - number of leds (4 argument version)
    # @tparam CHIPSET - the chipset type (required)
    # @tparam DATA_PIN - the optional data pin for the leds (required)
    # @tparam RGB_ORDER - the rgb ordering for the leds (e.g. what order red, green, and blue data is written out in)
    # @returns a reference to the added controller
    def addLeds(self, DATA_PIN, RGB_ORDER, CHIPSET, data, nLedsOrOffset, nLedsIfOffset=0):
        if FASTLED_HAS_CLOCKLESS:
            c = CHIPSET(DATA_PIN, RGB_ORDER)
            return addLeds(c, data, nLedsOrOffset, nLedsIfOffset)

    def addLeds(self, DATA_PIN, RGB_ORDER, CHIPSET, data, nLedsOrOffset, nLedsIfOffset=0):
        if FASTLED_HAS_CLOCKLESS:
            c = CHIPSET(DATA_PIN, RGB)
            return addLeds(c, data, nLedsOrOffset, nLedsIfOffset)

    def addLeds(self, DATA_PIN, CHIPSET, data, nLedsOrOffset, nLedsIfOffset=0):
        if FASTLED_HAS_CLOCKLESS:
            c = CHIPSET(DATA_PIN)
            return addLeds(c, data, nLedsOrOffset, nLedsIfOffset)

    def addLeds(self, NUM_LANES, DATA_PIN, RGB_ORDER, CHIPSET, data, nLeds):
        if __FASTLED_HAS_FIBCC == 1:
            c = __FIBCC(CHIPSET, DATA_PIN, NUM_LANES, RGB_ORDER)
            return addLeds(c, data, nLeds)

    def addLeds(self, CHIPSET, DATA_PIN, RGB_ORDER, data, nLedsOrOffset, nLedsIfOffset=0):

        if FASTSPI_USE_DMX_SIMPLE:
            if CHIPSET == DMX:
                c = DMXController(DATA_PIN)
            return addLeds(c, data, nLedsOrOffset, nLedsIfOffset)

    # @name Adding 3rd party library controllers
    # @{
    # Add a 3rd party library based CLEDController instance to the world.
    # There are two ways to call this method (as well as the other addLeds)
    # variations.  The first is with 2 arguments, in which case the arguments are  a pointer to
    # led data, and the number of leds used by this controller.  The second is with 3 arguments, in which case
    # the first  argument is the same, the second argument is an offset into the CRGB data where this controller's
    # CRGB data begins, and the third argument is the number of leds for this controller object. This class includes the SmartMatrix
    # and OctoWS2811 based controllers
    #
    # This method also takes a 1 to 2 template parameters for identifying the specific chipset and rgb ordering
    # RGB ordering, and SPI data rate
    # @param data - base point to an array of CRGB data structures
    # @param nLedsOrOffset - number of leds (3 argument version) or offset into the data array
    # @param nLedsIfOffset - number of leds (4 argument version)
    # @tparam CHIPSET - the chipset type (required)
    # @tparam RGB_ORDER - the rgb ordering for the leds (e.g. what order red, green, and blue data is written out in)
    # @returns a reference to the added controller
    def addLeds(self, RGB_ORDER, CHIPSET, data, nLedsOrOffset, nLedsIfOffset=0):
        c = CHIPSET(RGB_ORDER)
        return addLeds(c, data, nLedsOrOffset, nLedsIfOffset)

    def addLeds(self, CHIPSET, data, nLedsOrOffset, nLedsIfOffset=0):
        c = CHIPSET(RGB)
        return addLeds(c, data, nLedsOrOffset, nLedsIfOffset)

    def addLeds(self, CHIPSET, RGB_ORDER, data, nLedsOrOffset, nLedsIfOffset=0):
        if USE_OCTOWS2811:
            if CHIPSET == OCTOWS2811:
                c = COctoWS2811Controller(RGB_ORDER, WS2811_800kHz)
                return addLeds(c, data, nLedsOrOffset, nLedsIfOffset)
            if CHIPSET == OCTOWS2811_400:
                c = COctoWS2811Controller(RGB_ORDER, WS2811_400kHz)
                return addLeds(cr, data, nLedsOrOffset, nLedsIfOffset)
        if WS2813_800kHz
            if CHIPSET == OCTOWS2813:
                c = COctoWS2811Controller(RGB_ORDER, WS2813_800kHz)
                return addLeds(c, data, nLedsOrOffset, nLedsIfOffset)

    def addLeds(self, CHIPSET, data, nLedsOrOffset, nLedsIfOffset=0):
        if USE_OCTOWS2811:
            return addLeds(CHIPSET, GRB, data, nLedsOrOffset, nLedsIfOffset)

    def addLeds(self, CHIPSET, DATA_PIN, RGB_ORDER, data, nLedsOrOffset, nLedsIfOffset=0):
        if USE_WS2812SERIAL:
            c = CWS2812SerialController(DATA_PIN, RGB_ORDER)
            return addLeds(c, data, nLedsOrOffset, nLedsIfOffset)

    def addLeds(self, CHIPSET, data, nLedsOrOffset, nLedsIfOffset=0):
        if SmartMatrix_h:
            if CHIPSET == SMART_MATRIX:
                c = CSmartMatrixController
                return addLeds(c, data, nLedsOrOffset, nLedsIfOffset)

    # ifdef

    # @name adding parallel output controllers
    # @{
    # Add a block based CLEDController instance to the world.
    # There are two ways to call this method (as well as the other addLeds)
    # variations.  The first is with 2 arguments, in which case the arguments are  a pointer to
    # led data, and the number of leds used by this controller.  The second is with 3 arguments, in which case
    # the first  argument is the same, the second argument is an offset into the CRGB data where this controller's
    # CRGB data begins, and the third argument is the number of leds for this controller object.
    #
    # This method also takes a 2 to 3 template parameters for identifying the specific chipset and rgb ordering
    # RGB ordering, and SPI data rate
    # @param data - base point to an array of CRGB data structures
    # @param nLedsOrOffset - number of leds (3 argument version) or offset into the data array
    # @param nLedsIfOffset - number of leds (4 argument version)
    # @tparam CHIPSET - the chipset/port type (required)
    # @tparam NUM_LANES - how many parallel lanes of output to write
    # @tparam RGB_ORDER - the rgb ordering for the leds (e.g. what order red, green, and blue data is written out in)
    # @returns a reference to the added controller

    def addLeds(self, CHIPSET, NUM_LANES, RGB_ORDER, data, nLedsOrOffset, nLedsIfOffset=0):
        if FASTLED_HAS_BLOCKLESS:
            if PORTA_FIRST_PIN:
                if CHIPSET == WS2811_PORTA:
                    return addLeds(
                        InlineBlockClocklessController(NUM_LANES, PORTA_FIRST_PIN, NS(320), NS(320), NS(640),
                                                       RGB_ORDER),
                        data,
                        nLedsOrOffset,
                        nLedsIfOffset
                    )
                if CHIPSET == WS2811_400_PORTA:
                    return addLeds(
                        InlineBlockClocklessController(NUM_LANES, PORTA_FIRST_PIN, NS(800), NS(800), NS(900),
                                                       RGB_ORDER),
                        data,
                        nLedsOrOffset,
                        nLedsIfOffset
                    )
                if CHIPSET == WS2813_PORTA:
                    return addLeds(
                        InlineBlockClocklessController(NUM_LANES, PORTA_FIRST_PIN, NS(320), NS(320), NS(640), RGB_ORDER,
                                                       0, false, 300),
                        data,
                        nLedsOrOffset,
                        nLedsIfOffset
                    )
                if CHIPSET == TM1803_PORTA:
                    return addLeds(
                        InlineBlockClocklessController(NUM_LANES, PORTA_FIRST_PIN, NS(700), NS(1100), NS(700),
                                                       RGB_ORDER),
                        data,
                        nLedsOrOffset,
                        nLedsIfOffset
                    )
                if CHIPSET == UCS1903_PORTA:
                    return addLeds(
                        InlineBlockClocklessController(NUM_LANES, PORTA_FIRST_PIN, NS(500), NS(1500), NS(500),
                                                       RGB_ORDER),
                        data,
                        nLedsOrOffset,
                        nLedsIfOffset
                    )

            if PORTB_FIRST_PIN
                if CHIPSET == WS2811_PORTB:
                    return addLeds(
                        InlineBlockClocklessController(NUM_LANES, PORTB_FIRST_PIN, NS(320), NS(320), NS(640),
                                                       RGB_ORDER),
                        data,
                        nLedsOrOffset,
                        nLedsIfOffset
                    )
                if CHIPSET == WS2811_400_PORTB:
                    return addLeds(
                        InlineBlockClocklessController(NUM_LANES, PORTB_FIRST_PIN, NS(800), NS(800), NS(900),
                                                       RGB_ORDER),
                        data,
                        nLedsOrOffset,
                        nLedsIfOffset
                    )
                if CHIPSET == WS2813_PORTB:
                    return addLeds(
                        InlineBlockClocklessController(NUM_LANES, PORTB_FIRST_PIN, NS(320), NS(320), NS(640), RGB_ORDER,
                                                       0, false, 300),
                        data,
                        nLedsOrOffset,
                        nLedsIfOffset
                    )
                if CHIPSET == TM1803_PORTB:
                    return addLeds(
                        InlineBlockClocklessController(NUM_LANES, PORTB_FIRST_PIN, NS(700), NS(1100), NS(700),
                                                       RGB_ORDER),
                        data,
                        nLedsOrOffset,
                        nLedsIfOffset
                    )
                if CHIPSET == UCS1903_PORTB:
                    return addLeds(
                        InlineBlockClocklessController(NUM_LANES, PORTB_FIRST_PIN, NS(500), NS(1500), NS(500),
                                                       RGB_ORDER),
                        data,
                        nLedsOrOffset,
                        nLedsIfOffset
                    )

            if PORTC_FIRST_PIN:
                if CHIPSET == WS2811_PORTC:
                    return addLeds(
                        InlineBlockClocklessController(NUM_LANES, PORTC_FIRST_PIN, NS(320), NS(320), NS(640),
                                                       RGB_ORDER),
                        data,
                        nLedsOrOffset,
                        nLedsIfOffset
                    )
                if CHIPSET == WS2811_400_PORTC:
                    return addLeds(
                        InlineBlockClocklessController(NUM_LANES, PORTC_FIRST_PIN, NS(800), NS(800), NS(900),
                                                       RGB_ORDER),
                        data,
                        nLedsOrOffset,
                        nLedsIfOffset
                    )
                if CHIPSET == WS2813_PORTC:
                    return addLeds(
                        InlineBlockClocklessController(NUM_LANES, PORTC_FIRST_PIN, NS(320), NS(320), NS(640), RGB_ORDER,
                                                       0, false, 300),
                        data,
                        nLedsOrOffset,
                        nLedsIfOffset
                    )
                if CHIPSET == TM1803_PORTC:
                    return addLeds(
                        InlineBlockClocklessController(NUM_LANES, PORTC_FIRST_PIN, NS(700), NS(1100), NS(700),
                                                       RGB_ORDER),
                        data,
                        nLedsOrOffset,
                        nLedsIfOffset
                    )
                if CHIPSET == UCS1903_PORTC:
                    return addLeds(
                        InlineBlockClocklessController(NUM_LANES, PORTC_FIRST_PIN, NS(500), NS(1500), NS(500),
                                                       RGB_ORDER),
                        data,
                        nLedsOrOffset,
                        nLedsIfOffset
                    )

            if PORTD_FIRST_PIN:
                if CHIPSET == WS2811_PORTD:
                    return addLeds(
                        InlineBlockClocklessController(NUM_LANES, PORTD_FIRST_PIN, NS(320), NS(320), NS(640),
                                                       RGB_ORDER),
                        data,
                        nLedsOrOffset,
                        nLedsIfOffset
                    )
                if CHIPSET == WS2811_400_PORTD:
                    return addLeds(
                        InlineBlockClocklessController(NUM_LANES, PORTD_FIRST_PIN, NS(800), NS(800), NS(900),
                                                       RGB_ORDER),
                        data,
                        nLedsOrOffset,
                        nLedsIfOffset
                    )
                if CHIPSET == WS2813_PORTD:
                    return addLeds(
                        InlineBlockClocklessController(NUM_LANES, PORTD_FIRST_PIN, NS(320), NS(320), NS(640), RGB_ORDER,
                                                       0, false, 300),
                        data,
                        nLedsOrOffset,
                        nLedsIfOffset
                    )
                if CHIPSET == TM1803_PORTD:
                    return addLeds(
                        InlineBlockClocklessController(NUM_LANES, PORTD_FIRST_PIN, NS(700), NS(1100), NS(700),
                                                       RGB_ORDER),
                        data,
                        nLedsOrOffset,
                        nLedsIfOffset
                    )
                if CHIPSET == UCS1903_PORTD:
                    return addLeds(
                        InlineBlockClocklessController(NUM_LANES, PORTD_FIRST_PIN, NS(500), NS(1500), NS(500),
                                                       RGB_ORDER),
                        data,
                        nLedsOrOffset,
                        nLedsIfOffset
                    )

            if HAS_PORTDC:
                if CHIPSET == WS2811_PORTDC:
                    return addLeds(
                        SixteenWayInlineBlockClocklessController(NUM_LANES, NS(320), NS(320), NS(640), RGB_ORDER),
                        data,
                        nLedsOrOffset,
                        nLedsIfOffset
                    )
                if CHIPSET == WS2811_400_PORTDC:
                    return addLeds(
                        SixteenWayInlineBlockClocklessController(NUM_LANES, NS(800), NS(800), NS(900), RGB_ORDER),
                        data,
                        nLedsOrOffset,
                        nLedsIfOffset
                    )
                if CHIPSET == WS2813_PORTDC:
                    return addLeds(
                        SixteenWayInlineBlockClocklessController(NUM_LANES, NS(320), NS(320), NS(640), RGB_ORDER, 0,
                                                                 false, 300),
                        data,
                        nLedsOrOffset,
                        nLedsIfOffset
                    )
                if CHIPSET == TM1803_PORTDC:
                    return addLeds(
                        SixteenWayInlineBlockClocklessController(NUM_LANES, NS(700), NS(1100), NS(700), RGB_ORDER),
                        data,
                        nLedsOrOffset,
                        nLedsIfOffset
                    )
                if CHIPSET == UCS1903_PORTDC:
                    return addLeds(
                        SixteenWayInlineBlockClocklessController(NUM_LANES, NS(500), NS(1500), NS(500), RGB_ORDER),
                        data,
                        nLedsOrOffset,
                        nLedsIfOffset
                    )

    def addLeds(self, CHIPSET, NUM_LANES, data, nLedsOrOffset, nLedsIfOffset=0):
        if FASTLED_HAS_BLOCKLESS:
            return addLeds(CHIPSET, NUM_LANES, GRB, data, nLedsOrOffset, nLedsIfOffset)

    # Set the global brightness scaling
    # @param scale a 0-255 value for how much to scale all leds before writing them out
    def setBrightness(self, scale):
        self.m_Scale = scale

    # Get the current global brightness setting
    # @returns the current global brightness value
    def getBrightness(self):
        return self.m_Scale

    # Set the maximum power to be used, given in volts and milliamps.
    # @param volts - how many volts the leds are being driven at (usually 5)
    # @param milliamps - the maximum milliamps of power draw you want
    def setMaxPowerInVoltsAndMilliamps(self, volts, milliamps):
        self.setMaxPowerInMilliWatts(volts * milliamps)

    # Set the maximum power to be used, given in milliwatts
    # @param milliwatts - the max power draw desired, in milliwatts
    def setMaxPowerInMilliWatts(self, milliwatts):
        self.m_pPowerFunc = calculate_max_brightness_for_power_mW
        self.m_nPowerData = milliwatts

    # Update all our controllers with the current led colors, using the passed in brightness
    # @param scale temporarily override the scale
    def show(self, scale=None):
        if scale is None:
            scale = self.m_Scale

        # guard against showing too rapidly
        global lastshow
        while self.m_nMinMicros and time.ticks_diff(time.ticks_us(), lastshow) < self.m_nMinMicros:
            lastshow = time.ticks_us()

        # If we have a function for computing power, use it!
        if self.m_pPowerFunc:
            scale = self.m_pPowerFunc(scale, self.m_nPowerData)

        pCur = CLEDController.head()
        while pCur:
            d = pCur.getDither()
            if self.m_nFPS < 100:
                pCur.setDither(0)

            pCur.showLeds(scale)
            pCur.setDither(d)
            pCur = pCur.next()

        self.countFPS()

    # clear the leds, wiping the local array of data, optionally black out the leds as well
    # @param writeData whether or not to write out to the leds as well
    def clear(self, writeData=False):
        if writeData:
            self.showColor(CRGB(0, 0, 0), 0)
        self.clearData()

    # clear out the local data array
    def clearData(self):
        pCur = CLEDController.head()
        while pCur:
            pCur.clearLedData()
            pCur = pCur.next()

    # Set all leds on all controllers to the given color/scale
    # @param color what color to set the leds to
    # @param scale what brightness scale to show at
    def showColor(self, color, scale=None):
        if scale is None:
            scale = self.m_Scale

        global lastshow
        while self.m_nMinMicros and time.ticks_diff(time.ticks_us(), lastshow) < self.m_nMinMicros:
            lastshow = time.ticks_us()

        # If we have a function for computing power, use it!
        if self.m_pPowerFunc:
            scale = self.m_pPowerFunc(scale, self.m_nPowerData)

        pCur = CLEDController.head()
        while pCur:
            d = pCur.getDither()
            if self.m_nFPS < 100:
                pCur.setDither(0)

            pCur.showColor(color, scale)
            pCur.setDither(d)
            pCur = pCur.next()

        self.countFPS()

    # Delay for the given number of milliseconds.  Provided to allow the library to be used on platforms
    # that don't have a delay function (to allow code to be more portable).  Note: this will call show
    # constantly to drive the dithering engine (and will call show at least once).
    # @param ms the number of milliseconds to pause for
    def delay(self, ms):
        start = time.ticks_ms()

        while time.ticks_diff(time.ticks_ms(), start) < ms:
            if FASTLED_ACCURATE_CLOCK:
                # make sure to allow at least one ms to pass to ensure the clock moves
                # forward
                time.sleep_ms(1)

            self.show()

    # Set a global color temperature.  Sets the color temperature for all added led strips, overriding whatever
    # previous color temperature those controllers may have had
    # @param temp A CRGB structure describing the color temperature
    def setTemperature(self, temp):
        pCur = CLEDController.head()
        while pCur:
            pCur.setTemperature(temp)
            pCur = pCur.next()

    # Set a global color correction.  Sets the color correction for all added led strips,
    # overriding whatever previous color correction those controllers may have had.
    # @param correction A CRGB structure describin the color correction.
    def setCorrection(self, correction):
        pCur = CLEDController.head()
        while pCur:
            pCur.setCorrection(correction)
            pCur = pCur.next()

    # Set the dithering mode.  Sets the dithering mode for all added led strips, overriding
    # whatever previous dithering option those controllers may have had.
    # @param ditherMode - what type of dithering to use, either BINARY_DITHER or DISABLE_DITHER
    def setDither(self, ditherMode=BINARY_DITHER):
        pCur = CLEDController.head()
        while pCur:
            pCur.setDither(ditherMode)
            pCur = pCur.next()

    # Set the maximum refresh rate.  This is global for all leds.  Attempts to
    # call show faster than this rate will simply wait.  Note that the refresh rate
    # defaults to the slowest refresh rate of all the leds added through addLeds.  If
    # you wish to set/override this rate, be sure to call setMaxRefreshRate _after_
    # adding all of your leds.
    # @param refresh - maximum refresh rate in hz
    # @param constrain - constrain refresh rate to the slowest speed yet set
    def setMaxRefreshRate(self, refresh, constrain):
        if constrain:
            # if we're constraining, the new value of m_nMinMicros _must_ be higher than previously (because we're only
            # allowed to slow things down if constraining)
            if refresh > 0 and (1000000 / refresh) > self.m_nMinMicros:
                self.m_nMinMicros = 1000000 / refresh

        elif refresh > 0:
            self.m_nMinMicros = 1000000 / refresh
        else:
            self.m_nMinMicros = 0

    # for debugging, will keep track of time between calls to countFPS, and every
    # nFrames calls, it will update an internal counter for the current FPS.
    # @todo make this a rolling counter
    # @param nFrames - how many frames to time for determining FPS
    def countFPS(self, nFrames=25):
        br = 1
        lastframe = 0  # millis()

        if br >= nFrames:
            now = time.ticks_ms()
            now -= lastframe

            if now == 0:
                now = 1  # prevent division by zero below

            self.m_nFPS = (br * 1000) / now
            br = 0
            lastframe = time.ticks_ms()

    # Get the number of frames/second being written out
    # @returns the most recently computed FPS value
    def getFPS(self):
        return self.m_nFPS

    # Get how many controllers have been registered
    # @returns the number of controllers (strips) that have been added with addLeds
    def count(self):
        x = 0
        pCur = CLEDController.head()
        while pCur:
            x += 1
            pCur = pCur.next()

        return x

    # Get a reference to a registered controller
    # @returns a reference to the Nth controller
    def __getitem__(self, x):
        pCur = CLEDController.head()
        while x and pCur:
            x -= 1
            pCur = pCur.next()

        if pCur is None:
            return CLEDController.head()
        else:
            return pCur

    # Get the number of leds in the first controller
    # @returns the number of LEDs in the first controller
    def size(self):
        return self[0].size()

    # Get a pointer to led data for the first controller
    # @returns pointer to the CRGB buffer for the first controller
    def leds(self):
        return self[0].leds()


FastLED = CFastLED
FastSPI_LED = CFastLED
FastSPI_LED2 = CFastLED
LEDS = FastLED

fuckit = 0
pSmartMatrix = None

CLEDController.m_pHead = None
CLEDController.m_pTail = None
lastshow = 0

_frame_cnt = 0
_retry_cnt = 0
noise_min = 0
noise_max = 0


# uint32_t CRGB::Squant = ((uint32_t)((__TIME__[4]-'0') * 28))<<16 | ((__TIME__[6]-'0')*50)<<8 | ((__TIME__[7]-'0')*28)






