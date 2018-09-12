"""cSHAKE: SHA-3 Derived Hash Function
    Author: Ran Pang
    
    Modify from official Python implementation of Keccak
"""

from binascii import hexlify
from binascii import unhexlify

def ROL64(a, n):
    return ((a >> (64-(n%64))) + (a << (n%64))) % (1 << 64)

def KeccakF1600onLanes(lanes):
    R = 1
    for round in xrange(24):
        C = [lanes[x][0] ^ lanes[x][1] ^ lanes[x][2] ^ lanes[x][3] ^ lanes[x][4] for x in range(5)]
        D = [C[(x+4)%5] ^ ROL64(C[(x+1)%5], 1) for x in range(5)]
        lanes = [[lanes[x][y]^D[x] for y in range(5)] for x in range(5)]
        (x, y) = (1, 0)
        current = lanes[x][y]
        for t in xrange(24):
            (x, y) = (y, (2*x+3*y)%5)
            (current, lanes[x][y]) = (lanes[x][y], ROL64(current, (t+1)*(t+2)//2))
        for y in xrange(5):
            T = [lanes[x][y] for x in range(5)]
            for x in xrange(5):
                lanes[x][y] = T[x] ^((~T[(x+1)%5]) & T[(x+2)%5])
        for j in xrange(7):
            R = ((R << 1) ^ ((R >> 7)*0x71)) % 256
            if (R & 2):
                lanes[0][0] = lanes[0][0] ^ (1 << ((1<<j)-1))
    return lanes

def load64(b):
    return sum((b[i] << (8*i)) for i in range(8))

def store64(a):
    return list((a >> (8*i)) % 256 for i in range(8))

def KeccakF1600(state):
    lanes = [[load64(state[8*(x+5*y):8*(x+5*y)+8]) for y in range(5)] for x in range(5)]
    lanes = KeccakF1600onLanes(lanes)
    state = bytearray(200)
    for x in xrange(5):
        for y in xrange(5):
            state[8*(x+5*y):8*(x+5*y)+8] = store64(lanes[x][y])
    return state

def Keccak(rate, capacity, inputBytes, delimitedSuffix, outputByteLen):
    outputBytes = bytearray()
    state = bytearray([0 for i in range(200)])
    rateInBytes = rate//8
    blockSize = 0
    if (((rate + capacity) != 1600) or ((rate % 8) != 0)):
        return
    inputOffset = 0
    # === Absorb all the input blocks ===
    while(inputOffset < len(inputBytes)):
        blockSize = min(len(inputBytes)-inputOffset, rateInBytes)
        for i in xrange(blockSize):
            state[i] = state[i] ^ inputBytes[i+inputOffset]
        inputOffset = inputOffset + blockSize
        if (blockSize == rateInBytes):
            state = KeccakF1600(state)
            blockSize = 0
    # === Do the padding and switch to the squeezing phase ===
    state[blockSize] = state[blockSize] ^ delimitedSuffix
    if (((delimitedSuffix & 0x80) != 0) and (blockSize == (rateInBytes-1))):
        state = KeccakF1600(state)
    state[rateInBytes-1] = state[rateInBytes-1] ^ 0x80
    state = KeccakF1600(state)
    # === Squeeze out all the output blocks ===
    while(outputByteLen > 0):
        blockSize = min(outputByteLen, rateInBytes)
        outputBytes = outputBytes + state[0:blockSize]
        outputByteLen = outputByteLen - blockSize
        if (outputByteLen > 0):
            state = KeccakF1600(state)
    return outputBytes

def left_encode(x):
    """function bytepad
        
        left_encode(x) encodes the integer x as a byte string in a way that can be unambiguously parsed from the beginning of the string by inserting the length of the byte string before the byte string representation of x. As an example, left_encode(0) will yield 00000001 00000000.
        
        Args:
        x: the input integer
        
        Returns:
        O: binary string
    """
    if (x >= 0) and (x < (1 << 2040)):
        x_bin = '{0:b}'.format(x)
        On = x_bin
        while (len(On) % 8) != 0:
            On = '0' + On
        n = len(On) // 8
        n_bin = '{0:b}'.format(n)
        O0 = n_bin
        while (len(O0) % 8) != 0:
            O0 = '0' + O0
        O = O0 + On
        return O
    else:
        print 'Invalid bit string (left_encode)'

def encode_string(S):
    """function bytepad
        
        The encode_string function is used to encode bit strings in a way that may be parsed unambiguously from the beginning of the string S.
        
        Args:
        S: the input ascii string
        
        Returns:
        U: binary string
    """
    if S != '':
        S = '{0:b}'.format(int(hexlify(S), 16))
        while (len(S) % 8) != 0:
            S = '0' + S
    if (len(S) >= 0) and (len(S) < 2040):
        U = left_encode(len(S)) + S
        return U
    else:
        print 'Invalid bit string (encode_string)'

def bytepad(X, w):
    """function bytepad
        
        The bytepad(X, w) function prepends an encoding of the integer w to an input string X, then pads the result with zeros until it is a byte string whose length in bytes is a multiple of w. In general, bytepad is intended to be used on encoded strings-the byte string bytepad(encode_string(S), w) can be parsed unambiguously from its beginning, whereas bytepad does not provide unambiguous padding for all input strings.
        
        Args:
        X: the input binary string
        w: the rate (in bytes) of the KECCAK sponge function
        
        Returns:
        z: binary string
    """
    if w > 0:
        z = left_encode(w) + X
        while (len(z) % 8) != 0:
            z += '0'
        while ((len(z) / 8) % w) != 0:
            z += '00000000'
        return z
    else:
        print 'Invalid integer (bytepad)'

def cSHAKE128(X, L, N, S):
    """Hash function cSHAKE128
        
        Pad the input string to the specified length, add the custom parameter and call the SHAKE128 function in the library.
        
        Args:
        X: the input string
        L: the length of output
        N: a function-name string
        S: the custom parameter
        
        Returns:
        out_int: Integer hash value
    """
    if (N == '') and (S == ''):
        return hexlify(Keccak(1344, 256, bytearray(X), 0x1F, L >> 3))
    else:
        n = '{0:x}'.format(int(bytepad(encode_string(N) + encode_string(S), 168), 2))
        while (len(n) % 8) != 0:
            n = '0' + n
        return hexlify(Keccak(1344, 256, bytearray(unhexlify(n) + X), 0x04, L >> 3))

def cSHAKE256(X, L, N, S):
    """Hash function cSHAKE128
        
        Pad the input string to the specified length, add the custom parameter and call the SHAKE128 function in the library.
        
        Args:
        X: the input string
        L: the length of output
        N: a function-name string
        S: the custom parameter
        
        Returns:
        out_int: Integer hash value
    """
    if (N == '') and (S == ''):
        return hexlify(Keccak(1088, 512, bytearray(X), 0x1F, L >> 3))
    else:
        n = '{0:x}'.format(int(bytepad(encode_string(N) + encode_string(S), 136), 2))
        while (len(n) % 8) != 0:
            n = '0' + n
        return hexlify(Keccak(1088, 512, bytearray(unhexlify(n) + X), 0x04, L >> 3))
