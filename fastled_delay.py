
from . import *
import utime
# @file fastled_delay.h
# Utility functions and classes for managing delaycycles


# Class to ensure that a minimum amount of time has kicked since the last time run - and delay if not enough
# time has passed yet this should make sure that chipsets that have

class CMinWait(object):

    def __init__(self, WAIT):
        self.mLastMicros = 0
        self._wait = WAIT

    def wait(self):
        diff = 0

        while diff < self._wait:
            diff = (utime.ticks_us() & 0xFFFF) - self.mLastMicros

    def mark(self):
        self.mLastMicros = utime.ticks_us() & 0xFFFF


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# 
# Clock cycle counted delay loop
# 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Default is now just 'nop', with special case for AVR

# ESP32 core has it's own definition of NOP, so undef it first
# ifdef ESP32
# undef NOP
# undef NOP2
# endif

# if defined(__AVR__)
#  define FL_NOP __asm__ __volatile__ ("cp r0,r0\n");
#  define FL_NOP2 __asm__ __volatile__ ("rjmp .+0");
# else
#  define FL_NOP __asm__ __volatile__ ("nop\n");
#  define FL_NOP2 __asm__ __volatile__ ("nop\n\t nop\n");
# endif

# TODO: ARM version of _delaycycles_

def __delaycycles_template(CYCLES=None):
    def wrapper1(func):
        def wrapper():
            # _delaycycles_ARM<CYCLES / 3, CYCLES % 3>();
            func(CYCLES - 1)

        return wrapper

    return wrapper1


# pre-instantiations for values small enough to not need the loop, as well as sanity holders
# for some negative values.


@__delaycycles_template(-10)
def delaycycles():
    pass


@__delaycycles_template(-9)
def delaycycles(_):
    pass


@__delaycycles_template(-8)
def delaycycles(_):
    pass


@__delaycycles_template(-7)
def delaycycles(_):
    pass


@__delaycycles_template(-6)
def delaycycles(_):
    pass


@__delaycycles_template(-5)
def delaycycles(_):
    pass


@__delaycycles_template(-4)
def delaycycles(_):
    pass


@__delaycycles_template(-3)
def delaycycles(_):
    pass


@__delaycycles_template(-2)
def delaycycles(_):
    pass


@__delaycycles_template(-1)
def delaycycles(_):
    pass


@__delaycycles_template(0)
def delaycycles():
    pass


@__delaycycles_template(1)
def delaycycles(_):
    FL_NOP


@__delaycycles_template(2)
def delaycycles(_):
    FL_NOP2


@__delaycycles_template(3)
def delaycycles(_):
    FL_NOP
    FL_NOP2


@__delaycycles_template(4)
def delaycycles(_):
    FL_NOP2
    FL_NOP2


@__delaycycles_template(5)
def delaycycles(_):
    FL_NOP2
    FL_NOP2
    FL_NOP


# Some timing related macros/definitions

# Macro to convert from nano-seconds to clocks and clocks to nano-seconds
# #define NS(_NS) (_NS / (1000 / (F_CPU / 1000000L)))
F_CPU_MHZ = F_CPU / 1000000


# #define NS(_NS) ( (_NS * (F_CPU / 1000000L))) / 1000
def NS(_NS):
    return ((_NS * F_CPU_MHZ) + 999) / 1000


def CLKS_TO_MICROS(_CLKS):
    return _CLKS / (F_CPU / 1000000)


#  Macro for making sure there's enough time available
def NO_TIME(A, B, C):
    return NS(A) < 3 or NS(B) < 3 or NS(C) < 6
