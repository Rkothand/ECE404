# Homework Number: 5
# Name: Rohith Kothandaraman
# ECN Login: rkothand
# Due Date:2/21/22

from BitVector import *
from Crypto.Cipher import AES
#from sys import sys



def x931(v0, dt, totalNum, keyFile):
    
    with open(keyFile, "r") as f:
        key = f.read().splitlines()[0]
    key4 = bytes(key, 'UTF-8')

    aesfunc = AES.new(key4, AES.MODE_ECB)
    dates_bytes = bytes.fromhex(dt.get_bitvector_in_hex())
    date_bv = BitVector(rawbytes = aesfunc.encrypt(dates_bytes))

    vj_bv = v0

    rand_Num = [] #output of random number

    for i in range(totalNum):
        
        rj = date_bv ^ vj_bv
        rj_bytes = bytes.fromhex(rj.get_bitvector_in_hex())
        rj_bv = BitVector(rawbytes = aesfunc.encrypt(rj_bytes))

        rand_Num.append(rj_bv)

        new_vj = date_bv ^ rj_bv
        vj_bytes = bytes.fromhex(new_vj.get_bitvector_in_hex())
        vj_bv = BitVector(rawbytes = aesfunc.encrypt(vj_bytes))

    return rand_Num