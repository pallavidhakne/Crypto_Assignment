import sys
import random
import string
import time 
import argparse

Sbox = [
    [99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118],
    [202, 130, 201, 125, 250, 89, 71, 240, 173, 212, 162, 175, 156, 164, 114, 192],
    [183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229, 241, 113, 216, 49, 21],
    [4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226, 235, 39, 178, 117],
    [9, 131, 44, 26, 27, 110, 90, 160, 82, 59, 214, 179, 41, 227, 47, 132],
    [83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57, 74, 76, 88, 207],
    [208, 239, 170, 251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159, 168],
    [81, 163, 64, 143, 146, 157, 56, 245, 188, 182, 218, 33, 16, 255, 243, 210],
    [205, 12, 19, 236, 95, 151, 68, 23, 196, 167, 126, 61, 100, 93, 25, 115],
    [96, 129, 79, 220, 34, 42, 144, 136, 70, 238, 184, 20, 222, 94, 11, 219],
    [224, 50, 58, 10, 73, 6, 36, 92, 194, 211, 172, 98, 145, 149, 228, 121],
    [231, 200, 55, 109, 141, 213, 78, 169, 108, 86, 244, 234, 101, 122, 174, 8],
    [186, 120, 37, 46, 28, 166, 180, 198, 232, 221, 116, 31, 75, 189, 139, 138],
    [112, 62, 181, 102, 72, 3, 246, 14, 97, 53, 87, 185, 134, 193, 29, 158],
    [225, 248, 152, 17, 105, 217, 142, 148, 155, 30, 135, 233, 206, 85, 40, 223],
    [140, 161, 137, 13, 191, 230, 66, 104, 65, 153, 45, 15, 176, 84, 187, 22]
]

InvSbox = [
    [82, 9, 106, 213, 48, 54, 165, 56, 191, 64, 163, 158, 129, 243, 215, 251],
    [124, 227, 57, 130, 155, 47, 255, 135, 52, 142, 67, 68, 196, 222, 233, 203],
    [84, 123, 148, 50, 166, 194, 35, 61, 238, 76, 149, 11, 66, 250, 195, 78],
    [8, 46, 161, 102, 40, 217, 36, 178, 118, 91, 162, 73, 109, 139, 209, 37],
    [114, 248, 246, 100, 134, 104, 152, 22, 212, 164, 92, 204, 93, 101, 182, 146],
    [108, 112, 72, 80, 253, 237, 185, 218, 94, 21, 70, 87, 167, 141, 157, 132],
    [144, 216, 171, 0, 140, 188, 211, 10, 247, 228, 88, 5, 184, 179, 69, 6],
    [208, 44, 30, 143, 202, 63, 15, 2, 193, 175, 189, 3, 1, 19, 138, 107],
    [58, 145, 17, 65, 79, 103, 220, 234, 151, 242, 207, 206, 240, 180, 230, 115],
    [150, 172, 116, 34, 231, 173, 53, 133, 226, 249, 55, 232, 28, 117, 223, 110],
    [71, 241, 26, 113, 29, 41, 197, 137, 111, 183, 98, 14, 170, 24, 190, 27],
    [252, 86, 62, 75, 198, 210, 121, 32, 154, 219, 192, 254, 120, 205, 90, 244],
    [31, 221, 168, 51, 136, 7, 199, 49, 177, 18, 16, 89, 39, 128, 236, 95],
    [96, 81, 127, 169, 25, 181, 74, 13, 45, 229, 122, 159, 147, 201, 156, 239],
    [160, 224, 59, 77, 174, 42, 245, 176, 200, 235, 187, 60, 131, 83, 153, 97],
    [23, 43, 4, 126, 186, 119, 214, 38, 225, 105, 20, 99, 85, 33, 12, 125]
]

Rcon = [0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]


MixColumnsMatrix = [
    [2, 3, 1, 1],
    [1, 2, 3, 1],
    [1, 1, 2, 3],
    [3, 1, 1, 2]
]

InvMixColumnsMatrix = [
    [14, 11, 13, 9],
    [9, 14, 11, 13],
    [13, 9, 14, 11],
    [11, 13, 9, 14]
]

State = [[0 for x in range(4)] for y in range(4)]

def keyGen(keySize):
    key = ""
    if keySize == 128:
        for i in range(16):
            key += random.choice(string.hexdigits)
    elif keySize == 192:
        for i in range(24):
            key += random.choice(string.hexdigits)
    elif keySize == 256:
        for i in range(32):
            key += random.choice(string.hexdigits)
    else:
        print("Key size must be 16, 24 or 32 bytes")
        sys.exit()
    return key


def keyExpansion(key):
    keySize = len(key)
    if keySize == 16:
        Nk = 4
        Nr = 10
    elif keySize == 24:
        Nk = 6
        Nr = 12
    elif keySize == 32:
        Nk = 8
        Nr = 14
    else:
        print("Invalid key size:", len(key), "bytes")
        print("Key size must be 16, 24 or 32 bytes")
        sys.exit()
    w = []
    for i in range(Nk):
        w.append([ord(key[4*i]), ord(key[4*i+1]), ord(key[4*i+2]), ord(key[4*i+3])])

    def g(word, round):
        word = word[1:] + word[:1]
        for i in range(4):
            row = word[i] // 16
            col = word[i] % 16
            word[i] = Sbox[row][col]
        word[0] = word[0] ^ Rcon[round]
        return word

    if Nr == 10:
        for i in range(4, 4*(Nr+1)):
            if i % 4 == 0:
                w.append([w[i-4][j] ^ g(w[i-1], i//4)[j] for j in range(4)])
            else:
                w.append([w[i-4][j] ^ w[i-1][j] for j in range(4)])
    elif Nr == 12:
        for i in range(6, 4*(Nr+1)):
            if i % 6 == 0:
                w.append([w[i-6][j] ^ g(w[i-1], i//6)[j] for j in range(4)])
            else:
                w.append([w[i-6][j] ^ w[i-1][j] for j in range(4)])
    elif Nr == 14:
        for i in range(8, 4*(Nr+1)):
            if i % 8 == 0:
                w.append([w[i-8][j] ^ g(w[i-1], i//8)[j] for j in range(4)])
            else:
                w.append([w[i-8][j] ^ w[i-1][j] for j in range(4)])

    return w, Nr

def addRoundKey(state, w, round):
    for i in range(4):
        for j in range(4):
            state[i][j] = state[i][j] ^ w[round*4 + j][i]
    return state

def subBytes(state):
    for i in range(4):
        for j in range(4):
            row = state[i][j] // 16
            col = state[i][j] % 16
            state[i][j] = Sbox[row][col]
    return state

def invSubBytes(state):
    for i in range(4):
        for j in range(4):
            row = state[i][j] // 16
            col = state[i][j] % 16
            state[i][j] = InvSbox[row][col]
    return state

def shiftRows(state):
    for i in range(1, 4):
        state[i] = state[i][i:] + state[i][:i]
    return state

def invShiftRows(state):
    for i in range(1, 4):
        state[i] = state[i][-i:] + state[i][:-i]
    return state

def gm(a, b):
    irreducible = 0x11b 
    fx = a 
    gx = b 
    result = 0
    while gx: 
        if gx & 1: 
            result ^= fx
        fx <<= 1 
        if fx & 0x100: 
            fx ^= irreducible 
        gx >>= 1 
    return result 
    

def mixColumns(state):
    for i in range(4):
        col = [state[j][i] for j in range(4)]
        for j in range(4):
            state[j][i] = gm(MixColumnsMatrix[j][0], col[0]) ^ gm(MixColumnsMatrix[j][1], col[1]) ^ gm(MixColumnsMatrix[j][2], col[2]) ^ gm(MixColumnsMatrix[j][3], col[3])
    return state

def invMixColumns(state):
    for i in range(4):
        col = [state[j][i] for j in range(4)]
        for j in range(4):
            state[j][i] = gm(InvMixColumnsMatrix[j][0], col[0]) ^ gm(InvMixColumnsMatrix[j][1], col[1]) ^ gm(InvMixColumnsMatrix[j][2], col[2]) ^ gm(InvMixColumnsMatrix[j][3], col[3])
    return state

def decTohex(dec):
    return hex(dec)[2:].zfill(2)

def AsciiToHex(key):
    lm = []
    for l in key:
        lm.append([decTohex(i) for i in l])
    print(lm)
    return lm

def plaintextToState(plaintext):
    blocks = []
    states = []
    for i in range(0, len(plaintext), 16):
        blocks.append(plaintext[i:i+16])
    if(len(blocks[-1]) < 16):
        blocks[-1] += "0" * (16 - len(blocks[-1]))

    for block in blocks:
        state = [[], [], [], []]
        for i in range(4):
            for j in range(4):
                state[j].append(ord(block[4*i + j]))
        states.append(state)
    return states

def stateToPlaintext(states):
    plaintext = ""
    for state in states:
        for i in range(4):
            for j in range(4):
                plaintext += chr(state[j][i])

    # plaintext = plaintext.rstrip("0")
    return plaintext

def stateToHexCipher(states):
    cipher = ""
    for state in states:
        for i in range(4):
            for j in range(4):
                cipher += decTohex(state[j][i])
    return cipher

def hexCipherToState(cipher):
    blocks = []
    states = []
    for i in range(0, len(cipher), 32):
        blocks.append(cipher[i:i+32])

    for block in blocks:
        state = [[], [], [], []]
        for i in range(4):
            for j in range(4):
                state[j].append(int(block[8*i + 2*j:8*i + 2*j + 2], 16))
        states.append(state)

    return states

def encryption(plaintext, key, mode="ECB", IV=None):
    start = time.time()
    if mode == "ECB":
        blocks = plaintextToState(plaintext)
        w, Nr = keyExpansion(key)
        for block in blocks:
            block = addRoundKey(block, w, 0)
            for i in range(1, Nr):
                block = subBytes(block)
                block = shiftRows(block)
                block = mixColumns(block)
                block = addRoundKey(block, w, i)
            block = subBytes(block)
            block = shiftRows(block)
            block = addRoundKey(block, w, Nr)
        cipher = stateToHexCipher(blocks)
        end = time.time()
        print("Start time: ", start)
        print("End time: ", end)
        print("Encryption time: ", end - start)
        throughput = len(plaintext) / (end - start) / 1000000
        print("Throughput: ", throughput, "MB/sec")
        return cipher, IV


    elif mode == "CBC":
        blocks = plaintextToState(plaintext)
        w, Nr = keyExpansion(key)
        IV = [[random.randint(0, 255) for i in range(4)] for j in range(4)]
        nIV = IV
        for block in blocks:
            for i in range(4):
                for j in range(4):
                    block[i][j] ^= IV[i][j]
            block = addRoundKey(block, w, 0)
            for i in range(1, Nr):
                block = subBytes(block)
                block = shiftRows(block)
                block = mixColumns(block)
                block = addRoundKey(block, w, i)
            block = subBytes(block)
            block = shiftRows(block)
            block = addRoundKey(block, w, Nr)
            IV = block
        cipher = stateToHexCipher(blocks)
        end = time.time()
        print("Start time: ", start)
        print("End time: ", end)
        print("Encryption time: ", end - start)
        throughput = len(plaintext) / (end - start) / 1000000
        print("Throughput: ", throughput, "MB/sec")
        return cipher, nIV


def decryption(cipher, key, mode="ECB", IV=None):
    start = time.time()
    if mode == "ECB":
        w, Nr = keyExpansion(key)
        blocks = hexCipherToState(cipher)
        for block in blocks:
            block = addRoundKey(block, w, Nr)
            block = invShiftRows(block)
            block = invSubBytes(block)
            for i in range(Nr-1, 0, -1):
                block = addRoundKey(block, w, i)
                block = invMixColumns(block)
                block = invShiftRows(block)
                block = invSubBytes(block)
            block = addRoundKey(block, w, 0)
        plaintext = stateToPlaintext(blocks)
        end = time.time()
        print("Start time: ", start)
        print("End time: ", end)
        print("Encryption time: ", end - start)
        throughput = len(plaintext) / (end - start) / 1000000
        print("Throughput: ", throughput, "MB/sec")
        return plaintext

    elif mode == "CBC":
        IV = hexCipherToState(IV)[0]
        w, Nr = keyExpansion(key)
        blocks = hexCipherToState(cipher)

        for block in blocks:
            nIV = [[block[i][j] for j in range(4)] for i in range(4)]
            block = addRoundKey(block, w, Nr)
            block = invShiftRows(block)
            block = invSubBytes(block)
            for i in range(Nr-1, 0, -1):
                block = addRoundKey(block, w, i)
                block = invMixColumns(block)
                block = invShiftRows(block)
                block = invSubBytes(block)
            block = addRoundKey(block, w, 0)
            for i in range(4):
                for j in range(4):
                    block[i][j] ^= IV[i][j]
            IV = nIV
        plaintext = stateToPlaintext(blocks)
        end = time.time()
        print("Start time: ", start)
        print("End time: ", end)
        print("Encryption time: ", end - start)
        throughput = len(plaintext) / (end - start) / 1000000
        print("Throughput: ", throughput, "MB/sec")
        return plaintext


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--command", help="e for encryption, d for decryption, g for key generation", required=True)
    parser.add_argument("-m", "--mode", help="ECB or CBC : default is ECB", default="ECB")
    parser.add_argument("-k", "--key", help="Key file")
    parser.add_argument("-s", "--size", help="Key size in bits : default is 128", default=128)
    parser.add_argument("-i", "--input", help="Input file")
    parser.add_argument("-o", "--output", help="Output file (optional) Default: decrypted.dec or encrypted.enc")
    parser.add_argument("-v", "--IV", help="IV file for decryption (required for CBC)")


    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()

    if args.key is None and args.command != "g":
        print("The following arguments are required: -k/--key for encryption and decryption")
        sys.exit(1)
    elif args.input is None and args.command != "g":
        print("The following arguments are required: -i/--input for encryption and decryption")
        sys.exit(1)

    if agrs.command == "g" and args.size is None:
        print("The following arguments are required: -s/--size for key generation")
        sys.exit(1)

    if args.mode == "CBC" and args.IV is None and args.command == "d":
        print("The following arguments are required: -v/--IV for CBC decryption")
        sys.exit(1)

    if args.output == None:
        if args.command == "e":
            args.output = "encrypted.enc"
        elif args.command == "d":
            args.output = "decrypted.dec"
        elif args.command == "g":
            args.output = "key.key"

    if args.command == "e":
        if args.mode == "ECB":
            with open(args.key, "r") as f:
                key = f.read()
            with open(args.input, "r") as f:
                plaintext = f.read()
            cipher, IV = encryption(plaintext, key, "ECB")
            with open(args.output, "w") as f:
                f.write(cipher)
            print("Encryption done!")
            print("Encrypted file: ", args.output)

        elif args.mode == "CBC":
            with open(args.key, "r") as f:
                key = f.read()
            with open(args.input, "r") as f:
                plaintext = f.read()
            cipher, IV = encryption(plaintext, key, "CBC")
            with open(args.output, "w") as f:
                f.write(cipher)
            with open("IV.iv", "w") as f:
                f.write(stateToHexCipher([IV]))
            print("Encryption done!")
            print("Encrypted file: ", args.output)
            print("IV file: IV.iv")
        
    elif args.command == "d":
        if args.mode == "ECB":
            with open(args.key, "r") as f:
                key = f.read()
            with open(args.input, "r") as f:
                cipher = f.read()
            plaintext = decryption(cipher, key, "ECB")
            with open(args.output, "w") as f:
                f.write(plaintext)
            print("Decryption done!")
            print("Decrypted file: ", args.output)

        elif args.mode == "CBC":
            with open(args.key, "r") as f:
                key = f.read()
            with open(args.input, "r") as f:
                cipher = f.read()
            with open(args.IV, "r") as f:
                IV = f.read()
            plaintext = decryption(cipher, key, "CBC", IV)
            with open(args.output, "w") as f:
                f.write(plaintext)
            print("Decryption done!")
            print("Decrypted file: ", args.output)

    elif args.command == "g":
        key = keyGen(int(args.size))
        with open(args.output, "w") as f:
            f.write(key)
        print("Key generation done!")
        print("Key file: ", args.output)
        


if __name__ == "__main__":
    main()