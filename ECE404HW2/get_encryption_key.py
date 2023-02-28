#!/usr/bin/env python

## get_encryption_key.py

import sys
from BitVector import *

key_permutation_1 = [56,48,40,32,24,16,8,0,57,49,41,33,25,17,
                      9,1,58,50,42,34,26,18,10,2,59,51,43,35,
                     62,54,46,38,30,22,14,6,61,53,45,37,29,21,
                     13,5,60,52,44,36,28,20,12,4,27,19,11,3]

def get_encryption_key():
    key = ""
    while True:
        if sys.version_info[0] == 3:
            key = input("Enter a string of 8 characters for the key: ")
        else:
            key = raw_input("Enter a string of 8 characters for the key: ")
        if len(key) != 8:
            print("\nKey generation needs 8 characters exactly.  Try again.\n")
            continue
        else:
            break
    key = BitVector(textstring = key)
    key = key.permute(key_permutation_1)
    return key

key = get_encryption_key()
print("Here is the 56-bit encryption key generated from your input:\n")
print(key)

def permutation_key = [ 15, 6, 19, 20, 28, 11, 27, 16,
                        0, 14, 22, 25, 4, 17, 30, 9
                        1, 7, 23, 13, 31, 26, 2, 8,
                        18, 12, 29, 5, 21, 10, 3, 24]




if __name__=="__main__":
