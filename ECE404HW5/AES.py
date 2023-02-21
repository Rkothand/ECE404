# Homework Number: 4
# Name: Rohith Kothandaraman
# ECN Login: rkothand
# Due Date:2/14/22


import sys
from BitVector import *
from copy import deepcopy

AES_modulus = BitVector(bitstring='100011011')
subBytesTable = []                                                  # for encryption
invSubBytesTable = []                                               # for decryption

def genTables(): #byte sustitution
    c = BitVector(bitstring='01100011')
    d = BitVector(bitstring='00000101')
    for i in range(0, 256):
        # For the encryption SBox
        a = BitVector(intVal = i, size=8).gf_MI(AES_modulus, 8) if i != 0 else BitVector(intVal=0)
        # For bit scrambling for the encryption SBox entries:
        a1,a2,a3,a4 = [a.deep_copy() for x in range(4)]
        a ^= (a1 >> 4) ^ (a2 >> 5) ^ (a3 >> 6) ^ (a4 >> 7) ^ c
        subBytesTable.append(int(a))
        # For the decryption Sbox:
        b = BitVector(intVal = i, size=8)
        # For bit scrambling for the decryption SBox entries:
        b1,b2,b3 = [b.deep_copy() for x in range(3)]
        b = (b1 >> 2) ^ (b2 >> 5) ^ (b3 >> 7) ^ d
        check = b.gf_MI(AES_modulus, 8)
        b = check if isinstance(check, BitVector) else 0
        invSubBytesTable.append(int(b))

def byte_substitution(state_array): #step 1
    for i in range(4):
        for j in range(4):
            state_array[i][j] = subBytesTable[int(state_array[i][j])]
    return state_array

def shiftRowsEncrypt(array): #step 2
    tempArray = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    shift = 0
    for i in range(0,4):
        for j in range(0,4):
            tempArray[i][j] = array[i][(j-shift)%4]
        shift += 1
    return tempArray    


def mix_columns(state_array): #step 3
    two_const = BitVector(intVal=2, size=8)
    three_const = BitVector(intVal=3, size=8)
    newStateArray = deepcopy(state_array)
    for j in range(4):
        state_array[0][j] = BitVector(intVal=state_array[0][j], size=8)
        state_array[1][j] = BitVector(intVal=state_array[1][j], size=8)
        state_array[2][j] = BitVector(intVal=state_array[2][j], size=8)
        state_array[3][j] = BitVector(intVal=state_array[3][j], size=8)

        newStateArray[0][j] = (state_array[0][j].gf_multiply_modular(two_const, AES_modulus, 8)) ^ (state_array[1][j].gf_multiply_modular(three_const, AES_modulus, 8)) ^ state_array[2][j] ^ state_array[3][j]
        newStateArray[1][j]  = (state_array[0][j] ^ (state_array[1][j].gf_multiply_modular(two_const, AES_modulus, 8))) ^ (state_array[2][j].gf_multiply_modular(three_const, AES_modulus, 8)) ^ state_array[3][j]
        newStateArray[2][j] = state_array[0][j] ^ state_array[1][j] ^ (state_array[2][j].gf_multiply_modular(two_const, AES_modulus, 8)) ^ (state_array[3][j].gf_multiply_modular(three_const, AES_modulus, 8))
        newStateArray[3][j]  = (state_array[0][j].gf_multiply_modular(three_const, AES_modulus, 8)) ^ state_array[1][j] ^ state_array[2][j] ^ (state_array[3][j].gf_multiply_modular(two_const, AES_modulus, 8))
        
        newStateArray[0][j] = newStateArray[0][j].intValue()
        newStateArray[1][j] = newStateArray[1][j].intValue()
        newStateArray[2][j] = newStateArray[2][j].intValue()
        newStateArray[3][j] = newStateArray[3][j].intValue()
    return newStateArray


def addRoundKey(state_array, round_key, idx): #step 4
    tempBitVector = BitVector(size=0)
    for i in range(4):
        for j in range(4):
            tempBitVector += BitVector(intVal=state_array[j][i], size=8)
    print(round_key)
    tempBitVector ^= round_key[idx]
    for i in range(4):
        for j in range(4):
            stateArray[i][j] = tempBitVector[i*32 + j*8 : i*32 + j*8 + 8]
    return stateArray

def gee(keyword, round_constant, byte_sub_table):
    '''
    This is the g() function you see in Figure 4 of Lecture 8.
    '''
    rotated_word = keyword.deep_copy()
    rotated_word << 8
    newword = BitVector(size = 0)
    for i in range(4):
        newword += BitVector(intVal = byte_sub_table[rotated_word[8*i:8*i+8].intValue()], size = 8)
    newword[:8] ^= round_constant
    round_constant = round_constant.gf_multiply_modular(BitVector(intVal = 0x02), AES_modulus, 8)
    return newword, round_constant

# def gen_key_schedule_128(key_bv):
#     byte_sub_table = gen_subbytes_table()
#     #  We need 44 keywords in the key schedule for 128 bit AES.  Each keyword is 32-bits
#     #  wide. The 128-bit AES uses the first four keywords to xor the input block with.
#     #  Subsequently, each of the 10 rounds uses 4 keywords from the key schedule. We will
#     #  store all 44 keywords in the following list:
#     key_words = [None for i in range(44)]
#     round_constant = BitVector(intVal = 0x01, size=8)
#     for i in range(4):
#         key_words[i] = key_bv[i*32 : i*32 + 32]
#     for i in range(4,44):
#         if i%4 == 0:
#             kwd, round_constant = gee(key_words[i-1], round_constant, byte_sub_table)
#             key_words[i] = key_words[i-4] ^ kwd
#         else:
#             key_words[i] = key_words[i-4] ^ key_words[i-1]
#     return key_words

# def gen_key_schedule_192(key_bv):
#     byte_sub_table = gen_subbytes_table()
#     #  We need 52 keywords (each keyword consists of 32 bits) in the key schedule for
#     #  192 bit AES.  The 192-bit AES uses the first four keywords to xor the input
#     #  block with.  Subsequently, each of the 12 rounds uses 4 keywords from the key
#     #  schedule. We will store all 52 keywords in the following list:
#     key_words = [None for i in range(52)]
#     round_constant = BitVector(intVal = 0x01, size=8)
#     for i in range(6):
#         key_words[i] = key_bv[i*32 : i*32 + 32]
#     for i in range(6,52):
#         if i%6 == 0:
#             kwd, round_constant = gee(key_words[i-1], round_constant, byte_sub_table)
#             key_words[i] = key_words[i-6] ^ kwd
#         else:
#             key_words[i] = key_words[i-6] ^ key_words[i-1]
#     return key_words

def gen_key_schedule_256(key_bv):
    byte_sub_table = gen_subbytes_table()
    #  We need 60 keywords (each keyword consists of 32 bits) in the key schedule for
    #  256 bit AES. The 256-bit AES uses the first four keywords to xor the input
    #  block with.  Subsequently, each of the 14 rounds uses 4 keywords from the key
    #  schedule. We will store all 60 keywords in the following list:
    key_words = [None for i in range(60)]
    round_constant = BitVector(intVal = 0x01, size=8)
    for i in range(8):
        key_words[i] = key_bv[i*32 : i*32 + 32]
    for i in range(8,60):
        if i%8 == 0:
            kwd, round_constant = gee(key_words[i-1], round_constant, byte_sub_table)
            key_words[i] = key_words[i-8] ^ kwd
        elif (i - (i//8)*8) < 4:
            key_words[i] = key_words[i-8] ^ key_words[i-1]
        elif (i - (i//8)*8) == 4:
            key_words[i] = BitVector(size = 0)
            for j in range(4):
                key_words[i] += BitVector(intVal = 
                                 byte_sub_table[key_words[i-1][8*j:8*j+8].intValue()], size = 8)
            key_words[i] ^= key_words[i-8] 
        elif ((i - (i//8)*8) > 4) and ((i - (i//8)*8) < 8):
            key_words[i] = key_words[i-8] ^ key_words[i-1]
        else:
            sys.exit("error in key scheduling algo for i = %d" % i)
    return key_words




def gen_subbytes_table():
    subBytesTable = []
    c = BitVector(bitstring='01100011')
    for i in range(0, 256):
        a = BitVector(intVal = i, size=8).gf_MI(AES_modulus, 8) if i != 0 else BitVector(intVal=0)
        a1,a2,a3,a4 = [a.deep_copy() for x in range(4)]
        a ^= (a1 >> 4) ^ (a2 >> 5) ^ (a3 >> 6) ^ (a4 >> 7) ^ c
        subBytesTable.append(int(a))
    return subBytesTable

def get_key(keyfile):
    key = ""
    with open(keyfile) as f:
        key = f.read()
    # key.strip()
    key_BitVector = BitVector(textstring = key)
    return key_BitVector

if __name__ == "__main__":
    #encryption
    eType = sys.argv[1]
    infile = sys.argv[2]
    keyfile = sys.argv[3]
    outfile = sys.argv[4]
    
    if eType == "-e":
        key_Bitvector = get_key(keyfile)
        key_Words = gen_key_schedule_256(key_Bitvector)

        num_rounds = 14
        round_keys = [0]*15
        # print(round_keys)
        for i in range(15):
            round_keys[i] = (key_Words[i*4], key_Words[i*4+1], key_Words[i*4+2], key_Words[i*4+3])
            

        genTables()

        bV = BitVector(filename = infile)
        out = open(outfile, 'w')
        stateArray = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        while (bV.more_to_read):
            bitvec = bV.read_bits_from_file(128)
            if bitvec.length() != 128:
                bitvec.pad_from_right(128 - bitvec.length())
            for i in range(4):
                for j in range(4):
                    stateArray[i][j] = int(bitvec[i*32 + j*8 : i*32 + j*8 + 8])
            stateArray = addRoundKey(stateArray, round_keys[0], 0)
            for i in range(num_rounds-1):
                stateArray = byte_substitution(stateArray)
                stateArray = shiftRowsEncrypt(stateArray)
                stateArray = mix_columns(stateArray)
                stateArray_BV = addRoundKey(stateArray, round_keys[i], i)
                for j in range (4):
                    for k in range(4):
                        stateArray[k][j] = stateArray_BV[j*32 + k*8 : j*32 + k*8 + 8]
                stateArray = byte_substitution(stateArray)
                stateArray = shiftRowsEncrypt(stateArray)
                stateArray = addRoundKey(stateArray, round_keys[num_rounds], num_rounds)
                for i in range(4):
                    for j in range(4):
                        out.write(stateArray[i][j].get_bitvector_in_hex())

        