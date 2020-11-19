import numpy as np
import flag

key1 = flag.flag
blocklen = 16

Sleft = [
    [6, 9, 0xA, 3, 4, 0xD, 7, 8, 0xE, 1, 2, 0xB, 5, 0xC, 0xF, 0],
    [9, 0xE, 0xB, 0xA, 4, 5, 0, 7, 8, 6, 3, 2, 0xC, 0xD, 1, 0xF],
    [8, 1, 0xC, 2, 0xD, 3, 0xE, 0xF, 0, 9, 5, 0xA, 4, 0xB, 6, 7],
    [9, 0, 2, 5, 0xA, 0xD, 6, 0xE, 1, 8, 0xB, 0xC, 3, 4, 7, 0xF]
]

sright = [
    [0xc, 5, 0, 0xa, 0xe, 7, 2, 8, 0xd, 4, 3, 9, 6, 0xf, 1, 0xb],
    [1, 0xc, 9, 6, 3, 0xe, 0xb, 2, 0xf, 8, 4, 5, 0xd, 0xa, 0, 7],
    [0xf, 0xa, 0xe, 6, 0xd, 8, 2, 4, 1, 7, 9, 0, 3, 5, 0xb, 0xc],
    [0, 0xa, 3, 0xc, 8, 2, 1, 0xe, 9, 7, 0xf, 6, 0xb, 5, 0xd, 4]
]


def TDES_encrypt(cipher,mykey=key1):
    # grouping cipher as 0 1
    Bin = str2bin(cipher)
    cBin = zeroPadding(Bin)
    cBin = cBin.reshape(-1, 16)
    # rounding
    for i in range(len(cBin)):
        key = str2bin(mykey)
        for j in range(4):
            cBin[i], key = round(cBin[i], key)

    return cBin


def round(block, key):
    block = block.reshape(-1, 8)
    key = key.reshape(-1, 8)
    L = block[0]
    R = block[1]
    res = np.array([])
    for i in range(len(R)):
        res = np.append(res, R[i])
    R = expend(R)
    compress, key = keyRound(key)
    key = key.reshape(-1)
    R = XOR(R, compress)
    R = R.reshape(-1, 6)

    tempL = Sboxleft(R[0])
    tempR = Sboxright(R[1])

    R = R.reshape(-1, 4)
    R = np.delete(R, 1, 0)
    R[0] = tempL
    R[1] = tempR
    R = R.reshape(-1)
    R = XOR(L, R)
    for i in range(len(R)):
        res = np.append(res, R[i])
    return res, key


def Sboxleft(block):
    a = block[0] + block[5]
    b = block[1] + block[2] + block[3] + block[4]
    a = int(a, 2)
    b = int(b, 2)
    result = num2bin(Sleft[a][b])
    return result


def Sboxright(block):
    a = block[0] + block[5]
    b = block[1] + block[2] + block[3] + block[4]
    a = int(a, 2)
    b = int(b, 2)
    result = num2bin(sright[a][b])
    return result


def XOR(a, b):
    for i in range(len(a)):
        a[i] = int(a[i]) ^ int(b[i])
    return a


def keyRound(key):
    key[0] = leftShift(key[0])
    key[1] = rightShift(key[1])
    compress = np.array([])
    compress = np.append(compress, key[0][0])
    compress = np.append(compress, key[0][2])
    compress = np.append(compress, key[0][3])
    compress = np.append(compress, key[0][4])
    compress = np.append(compress, key[0][5])
    compress = np.append(compress, key[0][7])

    compress = np.append(compress, key[1][1])
    compress = np.append(compress, key[1][2])
    compress = np.append(compress, key[1][3])
    compress = np.append(compress, key[1][5])
    compress = np.append(compress, key[1][6])
    compress = np.append(compress, key[1][7])

    return compress, key


def leftShift(left):
    left = np.append(left, left[0])
    left = np.append(left, left[1])
    index = [0, 1]
    left = np.delete(left, index)
    return left


def rightShift(right):
    right = np.concatenate([[right[len(right) - 1]], right])
    right = np.delete(right, [8])
    return right


def expend(R):
    res = np.array([])
    res = np.append(res, R[4])
    res = np.append(res, R[7])
    res = np.append(res, R[2])
    res = np.append(res, R[1])

    res = np.append(res, R[5])
    res = np.append(res, R[7])
    res = np.append(res, R[0])
    res = np.append(res, R[2])

    res = np.append(res, R[6])
    res = np.append(res, R[5])
    res = np.append(res, R[0])
    res = np.append(res, R[3])

    return res


def num2bin(s):
    result = np.array([])
    temp = bin(s).replace('0b', '')
    for i in range(4 - len(temp)):
        temp = '0' + temp
    for i in range(len(temp)):
        result = np.append(result, temp[i])
    return result


def str2bin(s):
    result = np.array([])

    for c in s:
        temp = bin(ord(c)).replace('0b', '')
        for i in range(8 - len(temp)):
            temp = '0' + temp
        for i in range(len(temp)):
            result = np.append(result, temp[i])
    return result


def zeroPadding(cBin):
    for i in range(blocklen - len(cBin) % blocklen):
        cBin = np.append(cBin, 0)
    return cBin

p = "a"

p1 = p + chr(0x85)
p2 = p + chr(0x87)

result1 = TDES_encrypt(p1)[0]
result2 = TDES_encrypt(p2)[0]

