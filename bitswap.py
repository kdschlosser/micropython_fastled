
from . import *


# @file bitswap.h
# Functions for rotating bits/bytes

# @defgroup Bitswap Bit swapping/rotate
# Functions for doing a rotation of bits/bytes used by parallel output
# @{
# structure representing 8 bits of access

class just8bits(object):
    
    @staticmethod
    def _get_bit(value):
        return bool((value >> 1) & 1)

    def __init__(self, raw=None, a0=0, a1=0, a2=0, a3=0, a4=0, a5=0, a6=0, a7=0):
        self.a0 = self._get_bit(a0)
        self.a1 = self._get_bit(a1)
        self.a2 = self._get_bit(a2)
        self.a3 = self._get_bit(a3)
        self.a4 = self._get_bit(a4)
        self.a5 = self._get_bit(a5)
        self.a6 = self._get_bit(a6)
        self.a7 = self._get_bit(a7)
        
        self.raw = raw


class sub4(object):

    @staticmethod
    def _get_bit(value):
        return bool((value >> 1) & 1)

    def __init__(
        self, 
        raw=None,
        a0=0,
        a1=0,
        a2=0,
        a3=0,
        a4=0,
        a5=0,
        a6=0,
        a7=0,
        b0=0,
        b1=0,
        b2=0,
        b3=0,
        b4=0,
        b5=0,
        b6=0,
        b7=0,
        c0=0,
        c1=0,
        c2=0,
        c3=0,
        c4=0,
        c5=0,
        c6=0,
        c7=0,
        d0=0,
        d1=0,
        d2=0,
        d3=0,
        d4=0,
        d5=0,
        d6=0,
        d7=0
    ):
        self.a0 = self._get_bit(a0)
        self.a1 = self._get_bit(a1)
        self.a2 = self._get_bit(a2)
        self.a3 = self._get_bit(a3)
        self.a4 = self._get_bit(a4)
        self.a5 = self._get_bit(a5)
        self.a6 = self._get_bit(a6)
        self.a7 = self._get_bit(a7)
        self.b0 = self._get_bit(b0)
        self.b1 = self._get_bit(b1)
        self.b2 = self._get_bit(b2)
        self.b3 = self._get_bit(b3)
        self.b4 = self._get_bit(b4)
        self.b5 = self._get_bit(b5)
        self.b6 = self._get_bit(b6)
        self.b7 = self._get_bit(b7)
        self.c0 = self._get_bit(c0)
        self.c1 = self._get_bit(c1)
        self.c2 = self._get_bit(c2)
        self.c3 = self._get_bit(c3)
        self.c4 = self._get_bit(c4)
        self.c5 = self._get_bit(c5)
        self.c6 = self._get_bit(c6)
        self.c7 = self._get_bit(c7)
        self.d0 = self._get_bit(d0)
        self.d1 = self._get_bit(d1)
        self.d2 = self._get_bit(d2)
        self.d3 = self._get_bit(d3)
        self.d4 = self._get_bit(d4)
        self.d5 = self._get_bit(d5)
        self.d6 = self._get_bit(d6)
        self.d7 = self._get_bit(d7)

        self.raw = raw


class bitswap_type(object):
    def __init__(self, word=None, bytes_=None, a=None, b=None):
        if word is None:
            word = [0] * 2
        
        if bytes_ is None:
            bytes_ = [0] * 8
            
        if a is None:
            a = sub4()
            
        if b is None:
            b = sub4()
        
        self.word = word
        self.bytes_ = bytes_
        self.a = a
        self.b = b
#
# #define SWAPSA(X,N) out.  X ## 0 = in.a.a ## N; \
#   out.  X ## 1 = in.a.b ## N; \
#   out.  X ## 2 = in.a.c ## N; \
#   out.  X ## 3 = in.a.d ## N;
#
# #define SWAPSB(X,N) out.  X ## 0 = in.b.a ## N; \
#   out.  X ## 1 = in.b.b ## N; \
#   out.  X ## 2 = in.b.c ## N; \
#   out.  X ## 3 = in.b.d ## N;
#
# #define SWAPS(X,N) out.  X ## 0 = in.a.a ## N; \
#   out.  X ## 1 = in.a.b ## N; \
#   out.  X ## 2 = in.a.c ## N; \
#   out.  X ## 3 = in.a.d ## N; \
#   out.  X ## 4 = in.b.a ## N; \
#   out.  X ## 5 = in.b.b ## N; \
#   out.  X ## 6 = in.b.c ## N; \
#   out.  X ## 7 = in.b.d ## N;


#  Do an 8byte by 8bit rotation
def swapbits8(in_, out):
    # SWAPS(a.a,7);
    # SWAPS(a.b,6);
    # SWAPS(a.c,5);
    # SWAPS(a.d,4);
    # SWAPS(b.a,3);
    # SWAPS(b.b,2);
    # SWAPS(b.c,1);
    # SWAPS(b.d,0);

    # SWAPSA(a.a,7);
    # SWAPSA(a.b,6);
    # SWAPSA(a.c,5);
    # SWAPSA(a.d,4);
    
    # SWAPSB(a.a,7);
    # SWAPSB(a.b,6);
    # SWAPSB(a.c,5);
    # SWAPSB(a.d,4);
  
    # SWAPSA(b.a,3);
    # SWAPSA(b.b,2);
    # SWAPSA(b.c,1);
    # SWAPSA(b.d,0);
  
    # SWAPSB(b.a,3);
    # SWAPSB(b.b,2);
    # SWAPSB(b.c,1);
    # SWAPSB(b.d,0);

    for i in range(8):
        work = just8bits()
        work.a3 = in_.word[0] >> 31
        work.a2 = in_.word[0] >> 23
        work.a1 = in_.word[0] >> 15
        work.a0 = in_.word[0] >> 7
        
        in_.word[0] <<= 1
        work.a7 = in_.word[1] >> 31
        work.a6 = in_.word[1] >> 23
        work.a5 = in_.word[1] >> 15
        work.a4 = in_.word[1] >> 7
        
        in_.word[1] <<= 1
        out.bytes[i] = work.raw


#  Slow version of the 8 byte by 8 bit rotation
def slowswap(A, B):
    for row in range(7):
        x = A[row]

        bit = 1 << row
        p_ = B
        
        mask = 1 << 7
        index = 0
        while mask:
           
            if x & mask:
                p_[index] |= bit
            else:
                p_[index] &= ~bit
        
            index += 1
            mask >>= 1
            
    # B[7] |= (x & 0x01) << row; x >>= 1;
    # B[6] |= (x & 0x01) << row; x >>= 1;
    # B[5] |= (x & 0x01) << row; x >>= 1;
    # B[4] |= (x & 0x01) << row; x >>= 1;
    # B[3] |= (x & 0x01) << row; x >>= 1;
    # B[2] |= (x & 0x01) << row; x >>= 1;
    # B[1] |= (x & 0x01) << row; x >>= 1;
    # B[0] |= (x & 0x01) << row; x >>= 1;


#  Simplified form of bits rotating function.  Based on code found here -
#  http://www.hackersdelight.org/hdcodetxt/transpose8.c.txt - rotating
#  data into LSB for a faster write (the code using this data can happily walk the array backwards)
def transpose8x1(A, B):

    # Load the array and pack it into x and y.
    y = A
    x = A + 4

    # pre-transform x
    t = (x ^ (x >> 7)) & 0x00AA00AA
    x = x ^ t ^ (t << 7)
    t = (x ^ (x >> 14)) & 0x0000CCCC
    x = x ^ t ^ (t << 14)

    # pre-transform y
    t = (y ^ (y >> 7)) & 0x00AA00AA
    y = y ^ t ^ (t << 7)
    t = (y ^ (y >> 14)) & 0x0000CCCC
    y = y ^ t ^ (t << 14)

    # final transform
    t = (x & 0xF0F0F0F0) | ((y >> 4) & 0x0F0F0F0F)
    y = ((x << 4) & 0xF0F0F0F0) | (y & 0x0F0F0F0F)
    x = t

    B = y
    B[4] = x


#  Simplified form of bits rotating function.  Based on code  found here -
#  http://www.hackersdelight.org/hdcodetxt/transpose8.c.txt
def transpose8x1_MSB(A, B):

    # Load the array and pack it into x and y.
    y = A
    x = A + 4

    # pre-transform x
    t = (x ^ (x >> 7)) & 0x00AA00AA
    x = x ^ t ^ (t << 7)
    t = (x ^ (x >> 14)) & 0x0000CCCC
    x = x ^ t ^ (t << 14)

    # pre-transform y
    t = (y ^ (y >> 7)) & 0x00AA00AA
    y = y ^ t ^ (t << 7)
    t = (y ^ (y >> 14)) & 0x0000CCCC
    y = y ^ t ^ (t << 14)

    # final transform
    t = (x & 0xF0F0F0F0) | ((y >> 4) & 0x0F0F0F0F)
    y = ((x << 4) & 0xF0F0F0F0) | (y & 0x0F0F0F0F)
    x = t

    B[7] = y
    y >>= 8
    B[6] = y
    y >>= 8
    B[5] = y
    y >>= 8
    B[4] = y

    B[3] = x
    x >>= 8
    B[2] = x
    x >>= 8
    B[1] = x
    x >>= 8
    B[0] = x


#  templated bit-rotating function.   Based on code found here -
#  http://www.hackersdelight.org/hdcodetxt/transpose8.c.txt
def transpose8(m, n, A, B):

    # Load the array and pack it into x and y.
    if m == 1:
        y = A
        x = A + 4
    else:
        x = (A[0] << 24) | (A[m] << 16) | (A[2 * m] << 8) | A[3 * m]
        y = (A[4 * m] << 24) | (A[5 * m] << 16) | (A[6 * m] << 8) | A[7 * m]

    # pre-transform x
    t = (x ^ (x >> 7)) & 0x00AA00AA
    x = x ^ t ^ (t << 7)
    t = (x ^ (x >> 14)) & 0x0000CCCC
    x = x ^ t ^ (t << 14)

    # pre-transform y
    t = (y ^ (y >> 7)) & 0x00AA00AA
    y = y ^ t ^ (t << 7)
    t = (y ^ (y >> 14)) & 0x0000CCCC
    y = y ^ t ^ (t << 14)

    # final transform
    t = (x & 0xF0F0F0F0) | ((y >> 4) & 0x0F0F0F0F)
    y = ((x << 4) & 0xF0F0F0F0) | (y & 0x0F0F0F0F)
    x = t

    B[7 * n] = y
    y >>= 8
    B[6 * n] = y
    y >>= 8
    B[5 * n] = y
    y >>= 8
    B[4 * n] = y

    B[3 * n] = x
    x >>= 8
    B[2 * n] = x
    x >>= 8
    B[n] = x
    x >>= 8
    B[0] = x
    # B[0]=x>>24;    B[n]=x>>16;    B[2*n]=x>>8;  B[3*n]=x>>0;
    # B[4*n]=y>>24;  B[5*n]=y>>16;  B[6*n]=y>>8;  B[7*n]=y>>0;


# Simplified form of bits rotating function.  Based on code found here - 
# http://www.hackersdelight.org/hdcodetxt/transpose8.c.txt - rotating
# data into LSB for a faster write (the code using this data can happily walk the array backwards)
def transpose8x1_noinline(A, B):
    # Load the array and pack it into x and y.
    y = A
    x = A + 4

    # pre-transform x
    t = (x ^ (x >> 7)) & 0x00AA00AA
    x = x ^ t ^ (t << 7)
    t = (x ^ (x >> 14)) & 0x0000CCCC
    x = x ^ t ^ (t << 14)

    # pre-transform y
    t = (y ^ (y >> 7)) & 0x00AA00AA  
    y = y ^ t ^ (t << 7)
    t = (y ^ (y >> 14)) & 0x0000CCCC
    y = y ^ t ^ (t << 14)

    # final transform
    t = (x & 0xF0F0F0F0) | ((y >> 4) & 0x0F0F0F0F)
    y = ((x << 4) & 0xF0F0F0F0) | (y & 0x0F0F0F0F)
    x = t

    B = y
    B[4] = x
    return B


def get_bit(value, bit_num):
    return (value >> bit_num) & 1


def set_bit(value, bit_num, state):
    if state:
        return value | (1 << bit_num)

    return value & ~(1 << bit_num)
