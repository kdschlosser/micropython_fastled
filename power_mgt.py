
from . import *

gRed_mW = 16 * 5  # 16mA @ 5v = 80mW
gGreen_mW = 11 * 5  # 11mA @ 5v = 55mW
gBlue_mW = 15 * 5  # 15mA @ 5v = 75mW
gDark_mW =  1 * 5  # 1mA @ 5v =  5mW


# Alternate calibration by RAtkins via pre-PSU wattage measurments;
# these are all probably about 20%-25% too high due to PSU heat losses,
# but if you're measuring wattage on the PSU input side, this may
# be a better set of calibrations.  (WS2812B)
#  gRed_mW = 100
#  gGreen_mW = 48
#  gBlue_mW = 100
#  gDark_mW = 12

POWER_LED = 1
POWER_DEBUG_PRINT = 0

# Power consumed by the MCU
gMCU_mW  =  25 * 5  # 25mA @ 5v = 125 mW

gMaxPowerIndicatorLEDPinNumber = 0  # default = Arduino onboard LED pin.  set to zero to skip this.

def calculate_unscaled_power_mW(ledbuffer, numLeds):  # 25354
    red32 = 0
    green32 = 0
    blue32 = 0

    # This loop might benefit from an AVR assembly version -MEK
    for led in ledbuffer:
        red32 += led.r
        green32 += led.g
        blue32  += led.b

    red32 *= gRed_mW
    green32 *= gGreen_mW
    blue32  *= gBlue_mW

    red32 >>= 8
    green32 >>= 8
    blue32 >>= 8

    total = red32 + green32 + blue32 + (gDark_mW * numLeds)
    return total


def calculate_max_brightness_for_power_vmA(
    ledbuffer,
    numLeds,
    target_brightness,
    max_power_V,
    max_power_mA
):
    return calculate_max_brightness_for_power_mW(
        ledbuffer,
        numLeds,
        target_brightness,
        max_power_V * max_power_mA
    )


def calculate_max_brightness_for_power_mW(
    ledbuffer,
    numLeds=None,
    target_brightness=None,
    max_power_mW=None,
):
    if isinstance(ledbuffer, int):
        target_brightness = ledbuffer
        max_power_mW = numLeds

        total_mW = gMCU_mW

        pCur = CLEDController.head()

        while pCur:
            total_mW += calculate_unscaled_power_mW(pCur.leds(), pCur.size())
            pCur = pCur.next()


        if POWER_DEBUG_PRINT == 1:
            print("power demand at full brightness mW =", total_mW)

        requested_power_mW = (total_mW * target_brightness) / 256

        if POWER_DEBUG_PRINT == 1:
            if target_brightness != 255:
                print("power demand at scaled brightness mW =", requested_power_mW)

            print("power limit mW =", max_power_mW)


        if requested_power_mW < max_power_mW:
            if POWER_LED > 0:
                if gMaxPowerIndicatorLEDPinNumber:
                    Pin(gMaxPowerIndicatorLEDPinNumber).lo()
                }

            if POWER_DEBUG_PRINT == 1:
                print("demand is under the limit")

            return target_brightness

        recommended_brightness = (target_brightness * max_power_mW) / requested_power_mW
        if POWER_DEBUG_PRINT == 1:
            print("recommended brightness # =", recommended_brightness)

            resultant_power_mW = (total_mW * recommended_brightness) / 256
            print("resultant power demand mW =", resultant_power_mW)
            print()

        if POWER_LED > 0:
            if gMaxPowerIndicatorLEDPinNumber:
                Pin(gMaxPowerIndicatorLEDPinNumber).hi()

        return recommended_brightness

    else:
        total_mW = calculate_unscaled_power_mW(ledbuffer, numLeds)
        requested_power_mW = (total_mW * target_brightness) / 256

        recommended_brightness = target_brightness

        if requested_power_mW > max_power_mW:
            recommended_brightness = (target_brightness * max_power_mW) / requested_power_mW

        return recommended_brightness


def set_max_power_indicator_LED(pinNumber):
    global gMaxPowerIndicatorLEDPinNumber
    gMaxPowerIndicatorLEDPinNumber = pinNumber

def set_max_power_in_volts_and_milliamps(volts, milliamps):
    FastLED.setMaxPowerInVoltsAndMilliamps(volts, milliamps)

def set_max_power_in_milliwatts(powerInmW):
    FastLED.setMaxPowerInMilliWatts(powerInmW)

def show_at_max_brightness_for_power():
    # power management usage is now in FastLED.show, no need for this function
    FastLED.show()

def delay_at_max_brightness_for_power(ms):
    FastLED.delay(ms)
