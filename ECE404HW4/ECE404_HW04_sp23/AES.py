# Homework Number: 4
# Name: Rohith Kothandaraman
# ECN Login: rkothand
# Due Date:2/14/22


import sys
from BitVector import *

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

def mixColumns(array,round):
    
    return 

def shiftRowsEncrypt(array):
    tempArray = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    shift = 0
    for i in range(0,4):
        for j in range(0,4):
            tempArray[i][j] = array[i][(j-shift)%4]
        shift += 1
    return tempArray    


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

if __name__ == "__main__":
    array = [1,2,3,4,], [5,6,7,8,], [9,10,11,12,], [13,14,15,16]
    print(array[0][3])
    arr = shiftRowsEncrypt(array)
    print(arr)