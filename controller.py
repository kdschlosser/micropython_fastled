
# @file controller.h
# base definitions used by led controllers for writing out led data

from . import **
from .led_sysdefs import *
from .pixeltypes import *
from .color import *
from .lib8tion import *


from . import NO_DITHERING, FASTLED_SCALE8_FIXED, NO_CORRECTION

def RO(RGB_ORDER, X):
    return RGB_BYTE(RGB_ORDER, X)


def RGB_BYTE(RO, X):
    return (RO >> (3 * (2 - X))) & 0x3


def RGB_BYTE0(RO):
    return (RO >> 6) & 0x3


def RGB_BYTE1(RO):
    return (RO >> 3) & 0x3


def RGB_BYTE2(RO):
    return RO & 0x3

# operator byte *(struct CRGB[] arr) { return (byte*)arr; }

DISABLE_DITHER = 0x00
BINARY_DITHER = 0x01

class EDitherMode(int):
    pass

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # /
# 
# LED Controller interface definition
# 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # /

# Base definition for an LED controller.  Pretty much the methods that every LED controller object will make available.
# Note that the showARGB method is not impelemented for all controllers yet.   Note also the methods for eventual checking
# of background writing of data (I'm looking at you, teensy 3.0 DMA controller!).  If you want to pass LED controllers around
# to methods, make them references to this type, keeps your code saner.  However, most people won't be seeing/using these objects
# directly at all
class CLEDController(object):
    m_pHead = None
    m_pTail = None

    # create an led controller object, add it to the chain of controllers
    def __init__(self):
        self.m_Data = None
        self.m_ColorCorrection = CRGB(UncorrectedColor)
        self.m_ColorTemperature = CRGB(UncorrectedTemperature)
        self.m_DitherMode = BINARY_DITHER
        self.m_nLeds = 0

        self.m_pNext = None
        if self.m_pHead is None:
            self.m_pHead = self

        if self.m_pTail is not None:
            self.m_pTail.m_pNext = self
            
        self.m_pTail = self

    # initialize the LED controller
    def init(self):
        pass

    # clear out/zero out the given number of leds.
    def clearLeds(self, nLeds):
        self.showColor(CRGB.Black, nLeds, CRGB.Black)

    # show function w/integer brightness, will scale for color correction and temperature
    def show(self, data, nLeds, brightness):
        self.show(data, nLeds, self.getAdjustment(brightness))

    # show function using the "attached to this controller" led data
    def showLeds(self, brightness=255):
        self.show(self.m_Data, self.m_nLeds, self.getAdjustment(brightness))

    # show function w/integer brightness, will scale for color correction and temperature
    def showColor(self, data, nLeds, brightness=None):
        if brightness is None:
            brightness = nLeds
            nLeds = None
        if nLeds is None:
            self.showColor(data, self.m_nLeds, self.getAdjustment(brightness))
        else:
            self.showColor(data, nLeds, self.getAdjustment(brightness))
   
    # get the first led controller in the chain of controllers
    def head(self):
        return self.m_pHead

    # get the next controller in the chain after this one.  will return NULL at the end of the chain
    def next(self):
        return self.m_pNext

    # set the default array of leds to be used by this controller
    def setLeds(self, data, nLeds):
        self.m_Data = data
        self.m_nLeds = nLeds
        return self

    # zero out the led data managed by this controller
    def clearLedData(self):
        del self.m_Data[:]

    # How many leds does this controller manage?
    def size(self):
        return self.m_nLeds

    # Pointer to the CRGB array for this controller
    def leds(self):
        return self.m_Data

    # Reference to the n'th item in the controller
    def __getitem__(self, x):
        return self.m_Data[x]

    # set the dithering mode for this controller to use
    def setDither(self, ditherMode=BINARY_DITHER):
        self.m_DitherMode = ditherMode
        return self
    
    # get the dithering option currently set for this controller
    def getDither(self):
        return self.m_DitherMode

    # the the color corrction to use for this controller, expressed as an rgb object
    def setCorrection(self, correction):
        self.m_ColorCorrection = correction
        return self

    # get the correction value used by this controller
    def getCorrection(self):
        return self.m_ColorCorrection

    # set the color temperature, aka white point, for this controller
    def setTemperature(self, temperature):
        self.m_ColorTemperature = temperature
        return self

    # get the color temperature, aka whipe point, for this controller
    def getTemperature(self):
        return self.m_ColorTemperature

    # Get the combined brightness/color adjustment for this controller
    def getAdjustment(self, scale):
        return self.computeAdjustment(scale, self.m_ColorCorrection, self.m_ColorTemperature)

    def computeAdjustment(self, scale, colorCorrection, colorTemperature):
        if NO_CORRECTION == 1:
            return CRGB(scale, scale, scale)
        else:
            adj = CRGB(0, 0, 0)
            
            if scale > 0:
                for i in range(3):
                    cc = colorCorrection.raw[i]
                    ct = colorTemperature.raw[i]
                    if cc > 0 < ct:
                        work = (cc + 1) * (ct + 1) * scale

                        work /= 0x10000
                        adj.raw[i] = work & 0xFF

            return adj

    def getMaxRefreshRate(self):
        return 0


MAX_LIKELY_UPDATE_RATE_HZ = 400
MIN_ACCEPTABLE_DITHER_RATE_HZ = 50
UPDATES_PER_FULL_DITHER_CYCLE = (MAX_LIKELY_UPDATE_RATE_HZ / MIN_ACCEPTABLE_DITHER_RATE_HZ)
RECOMMENDED_VIRTUAL_BITS = (
    (UPDATES_PER_FULL_DITHER_CYCLE > 1) +
    (UPDATES_PER_FULL_DITHER_CYCLE > 2) +
    (UPDATES_PER_FULL_DITHER_CYCLE > 4) +
    (UPDATES_PER_FULL_DITHER_CYCLE > 8) +
    (UPDATES_PER_FULL_DITHER_CYCLE > 16) +
    (UPDATES_PER_FULL_DITHER_CYCLE > 32) +
    (UPDATES_PER_FULL_DITHER_CYCLE > 64) +
    (UPDATES_PER_FULL_DITHER_CYCLE > 128)
)

VIRTUAL_BITS = RECOMMENDED_VIRTUAL_BITS
            
            
# Pixel controller class.  This is the class that we use to centralize pixel access in a block of data, including
# support for things like RGB reordering, scaling, dithering, skipping (for ARGB data), and eventually, we will
# centralize 8/12/16 conversions here as well.
class PixelController(object):

    def __call__(
        self,
        d,
        len_=None,
        s=None,
        dither=BINARY_DITHER,
        advance=True,
        skip=0
    ):
        if isinstance(d, PixelController):
            other = d
            
            self.d = other.d[:]
            self.e = other.e[:]
            self.mData = other.mData
            self.mScale = other.mScale
            self.mAdvance = other.mAdvance
            self.mLenRemaining = other.mLen
            self.mLen = other.mLen
            self.mOffsets = [0] * self._LANES
            for i in range(self._LANES):
                self.mOffsets[i] = other.mOffsets[i]

        elif isinstance(d, list) and isinstance(d[0], int):
            self.mData = d[:]
            self.mLen = len_
            self.mLenRemaining = len_
            self.mScale = s
            self.enable_dithering(dither)
            self.mData = self.mData[skip:]
            self.mAdvance = 3 + skip if advance else 0
            self.initOffsets(len_)

        else:
            self.mData = list(int(item) for item in d)
            self.mLen = len_
            self.mLenRemaining = len_
            self.mScale = s
            self.enable_dithering(dither)
            self.mAdvance = 3
            self.initOffsets(len_)

    def __init__(
        self,
        RGB_ORDER,
        LANES=1,
        MASK=0xFFFFFFFF
    ):
        self._LANES = LANES
        self._RGB_ORDER = RGB_ORDER
        self._MASK = MASK

        self.mData = []
        self.mLen = 0
        self.mLenRemaining = 0
        self.d = [0] * 3
        self.e = [0] * 3
        self.mScale = CRGB()
        self.mAdvance = 0
        self.mOffsets = [0] * LANES

    def initOffsets(self, len_):
        nOffset = 0
        for i in range(self._LANES):
            self.mOffsets[i] = nOffset
            if (1 << i) & self._MASK:
                nOffset += len_ * self.mAdvance

    def init_binary_dithering(self):
        if NO_DITHERING != 1:
            # Set 'virtual bits' of dithering to the highest level
            # that is not likely to cause excessive flickering at
            # low brightness levels + low update rates.
            # These pre-set values are a little ambitious, since
            # a 400Hz update rate for WS2811-family LEDs is only
            # possible with 85 pixels or fewer.
            # Once we have a 'number of milliseconds since last update'
            # value available here, we can quickly calculate the correct
            # number of 'virtual bits' on the fly with a couple of 'if'
            # statements -- no division required.  At this point,
            # the division is done at compile time, so there's no runtime
            # cost, but the values are still hard-coded.

            # R is the digther signal 'counter'.
            R = 1

            # R is wrapped around at 2^ditherBits,
            # so if ditherBits is 2, R will cycle through (0,1,2,3)
            ditherBits = VIRTUAL_BITS
            R &= (0x01 << ditherBits) - 1

            # Q is the "unscaled dither signal" itself.
            # It's initialized to the reversed bits of R.
            # If 'ditherBits' is 2, Q here will cycle through (0,128,64,192)
            Q = 0

            # Reverse bits in a byte
            for i in range(8):
                Q = set_bit(Q, ~(i - 8), get_bit(R, i))

            # Now we adjust Q to fall in the center of each range,
            # instead of at the start of the range.
            # If ditherBits is 2, Q will be (0, 128, 64, 192) at first,
            # and this adjustment makes it (31, 159, 95, 223).
            if ditherBits < 8:
                Q += 0x01 << (7 - ditherBits)

            # D and E form the "scaled dither signal"
            # which is added to pixel values to affect the
            # actual dithering.

            # Setup the initial D and E values
            for i in range(3):
                s = self.mScale.raw[i]
                self.e[i] = (256 // s) + 1 if s else 0
                self.d[i] = scale8(Q, self.e[i])
                
                if FASTLED_SCALE8_FIXED == 1:
                    if self.d[i]:
                        self.d[i] -= 1
                        
                if self.e[i]:
                    self.e[i] -= 1

    # Do we have n pixels left to process?
    def has(self, n):
        return self.mLenRemaining >= n

    # toggle dithering enable
    def enable_dithering(self, dither):
        if dither == BINARY_DITHER:
            self.init_binary_dithering()
        else:
            self.d = [0] * 3
            self.e = [0] * 3

    def size(self):
        return self.mLen

    # get the amount to advance the pointer by
    def advanceBy(self):
        return self.mAdvance

    # advance the data pointer forward, adjust position counter
    def advanceData(self):
        self.mData = self.mData[self.mAdvance:]
        self.mLenRemaining -= 1

    # step the dithering forward
    def stepDithering(self):
        # IF UPDATING HERE, BE SURE TO UPDATE THE ASM VERSION IN
        # clockless_trinket.h!
        self.d[0] = self.e[0] - self.d[0]
        self.d[1] = self.e[1] - self.d[1]
        self.d[2] = self.e[2] - self.d[2]

    # Some chipsets pre-cycle the first byte, which means we want to cycle byte 0's dithering separately
    def preStepFirstByteDithering(self):
        self.d[RO(self._RGB_ORDER, 0)] = self.e[RO(self._RGB_ORDER, 0)] - self.d[RO(self._RGB_ORDER, 0)]
        
    def loadByte(self, SLOT, pc, lane=None):
        if lane is None:
            return pc.mData[RO(self._RGB_ORDER, SLOT)]
        else:
            return pc.mData[pc.mOffsets[lane] + RO(self._RGB_ORDER, SLOT)]

    def dither(self, SLOT, pc, b, d=None):
        if d is None:
            return qadd8(b, pc.d[RO(self._RGB_ORDER, SLOT)]) if b else 0            
        else:
            return qadd8(b, d) if b else 0

    def scale(self, SLOT, pc, b, scale=None):
        if scale is None:
            return scale8(b, pc.mScale.raw[RO(self._RGB_ORDER, SLOT)])
        else:
            return scale8(b, scale)

    # composite shortcut functions for loading, dithering, and scaling
    def loadAndScale(self, SLOT, pc, lane=None, d=None, scale=None):
        if lane is None and d is None and scale is None:
            return self.scale(self, SLOT, pc, pc.dither(SLOT, pc, pc.loadByte(SLOT, pc)))
        elif d is None and scale is None:
            return self.scale(SLOT, pc, pc.dither(SLOT, pc, pc.loadByte(SLOT, pc, lane)))
        elif scale is not None and d is not None:
            return scale8(pc.dither(SLOT, pc, pc.loadByte(SLOT, pc, lane), d), scale)
            
        else:
            if scale is None:
                scale = d
                
            return scale8(pc.loadByte(SLOT, pc, lane), scale)

    def advanceAndLoadAndScale(self, SLOT, pc, lane=None, scale=None):
        if lane is None and scale is None:
            pc.advanceData()
            return pc.loadAndScale(SLOT, pc)
        elif scale is None:
            pc.advanceData()
            return pc.loadAndScale(SLOT, pc, lane)
        else:
            pc.advanceData()
            return pc.loadAndScale(SLOT, pc, lane, scale)

    def getd(self, SLOT, pc):
        return pc.d[RO(self._RGB_ORDER, SLOT)]
        
    def getscale(self, SLOT, pc):
        return pc.mScale.raw[RO(self._RGB_ORDER, SLOT)]

    # Helper functions to get around gcc stupidities
    def loadAndScale0(self, lane=None, scale=None):
        if lane is None and scale is None:
            return self.loadAndScale(0, self)
        elif scale is None:
            return self.loadAndScale(0, self, lane)
        else:
            return self.loadAndScale(0, self, lane, scale)
        
    def loadAndScale1(self, lane=None, scale=None):
        if lane is None and scale is None:
            return self.loadAndScale(1, self)
        elif scale is None:
            return self.loadAndScale(1, self, lane)
        else:
            return self.loadAndScale(1, self, lane, scale)
    
    def loadAndScale2(self, lane=None, scale=None):
        if lane is None and scale is None:
            return self.loadAndScale(2, self)
        elif scale is None:
            return self.loadAndScale(2, self, lane)
        else:
            return self.loadAndScale(2, self, lane, scale)
        
    def advanceAndLoadAndScale0(self, lane=None, scale=None):
        if lane is None and scale is None:
            return self.advanceAndLoadAndScale(0, self)
        elif scale is None:
            return self.advanceAndLoadAndScale(0, self, lane)
        else:
            return self.advanceAndLoadAndScale(0, self, lane, scale)
    
    def stepAdvanceAndLoadAndScale0(self, lane=None, scale=None):
        self.stepDithering()
        
        if lane is None and scale is None:
            return self.advanceAndLoadAndScale(0, self)
        elif scale is None:
            return self.advanceAndLoadAndScale(0, self, lane)
        else:
            return self.advanceAndLoadAndScale(0, self, lane, scale)
        
    def getScale0(self):
        return self.getscale(0, self)
        
    def getScale1(self):
        return self.getscale(1, self)
    
    def getScale2(self):
        return self.getscale(2, self)


class CPixelLEDController(CLEDController):

    def __init__(self, RGB_ORDER, LANES=1, MASK=0xFFFFFFFF):
        self._RGB_ORDER = RGB_ORDER
        self._LANES = LANES
        self._MASK = MASK

        CLEDController.__init__(self)

    def showPixels(self, pixels):
        pass

    # set all the leds on the controller to a given color
    # @param data the crgb color to set the leds to
    # @param nLeds the numner of leds to set to this color
    # @param scale the rgb scaling value for outputting color
    def showColor(self, data, nLeds, scale):
        pixels = PixelController(self._RGB_ORDER, self._LANES, self._MASK)
        pixels(data, nLeds, scale, self.getDither())
        self.showPixels(pixels)

    # write the passed in rgb data out to the leds managed by this controller
    # @param data the rgb data to write out to the strip
    # @param nLeds the number of leds being written out
    # @param scale the rgb scaling to apply to each led before writing it out
    def show(self, data, nLeds, scale):
        pixels = PixelController(self._RGB_ORDER, self._LANES, self._MASK)
        pixels(data, nLeds, scale, self.getDither())
        self.showPixels(pixels)
