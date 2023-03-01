# Homework Number: 6
# Name: Rohith Kothandaraman
# ECN Login: rkothand
# Due Date:2/28/22

import sys
from BitVector import *
from PrimeGenerator import * 

def MI(num, mod):
    '''
    This function uses ordinary integer arithmetic implementation of the
    Extended Euclid's Algorithm to find the MI of the first-arg integer
    vis-a-vis the second-arg integer.
    '''
    NUM = num; MOD = mod
    x, x_old = 0, 1
    y, y_old = 1, 0
    while mod:
        q = num // mod
        num, mod = mod, num % mod
        x, x_old = x_old - q * x, x
        y, y_old = y_old - q * y, y
    if num != 1:
        print("\nNO MI. However, the GCD of %d and %d is %u\n" % (NUM, MOD, num))
    else:
        MI = (x_old + MOD) % MOD
        print("\nMI of %d modulo %d is: %d\n" % (NUM, MOD, MI))

def RSAKeyGen(pin,qin):
    pfile = open(pin, 'w')
    qfile = open(qin, 'w')
    generator = PrimeGenerator(bits = 128)
    p=0
    q=0
    # n = p*q
    # totient = (p-1)*(q-1)
    e = 65537
    bv1 = BitVector(intVal=0, size =128)
    bv2 = BitVector(intVal=0, size =128)

    while p == q:
        p = generator.findPrime()
        ptemp = p-1
        etemp1 = e

        while etemp1:
            p1 = etemp1
            etemp1 = p1 % etemp1

        while not bv1[0] and bv2[0] and etemp1 != 1:
            p = generator.findPrime()
            ptemp = p-1
            etemp1 = e

            while etemp1:
                p1 = etemp1
                etemp1 = p1 % etemp1
        
        q = generator.findPrime()
        bv2.set_value(intVal = q)
        qtemp = q-1
        etemp2 = e

        while etemp2:
            q1 = etemp2
            etemp2 = q1 % etemp2

        pfile.write(str(p))
        qfile.write(str(q))





def RSAEncrypt(message ,p,q,encryptedfile):
    p = int(p)
    q = int(q)
    encryptedfile = open(encryptedfile, 'w')
    n = p*q
    totient = (p-1)*(q-1)
    e = 65537
    inputBV = BitVector(filename=message)

    while(inputBV.more_to_read):
        bitvec = inputBV.read_bits_from_file(128)
        if (bitvec.length() > 0) and (bitvec.length() != 128):
                bitvec.pad_from_right(128-bitvec.length())

        publicK = pow(int(bitvec) ,e, n)
        publicK = BitVector(intVal=publicK)

        if publicK._getsize() != 256:
            publicK.pad_from_left(256-publicK.length())

        encryptedfile.write(publicK.get_bitvector_in_hex())
    encryptedfile.close()





def RSADecrypt(encryptedfile, p, q, decryptedfile):
    p = int(p)
    q = int(q)
    n = p*q
    totient = (p-1)*(q-1)
    e = 65537
    d = pow(e, -1, totient)
    encryptedfile = open(encryptedfile, 'r')
    decryptedfile = open(decryptedfile, 'w')

    encryptedBV = BitVector(hexstring=encryptedfile.read())
    
    
    for i in range(0, int(encryptedBV.length()/256)):
        encrypted = encryptedBV[i*256:(i+1)*256]
        if encrypted.length() >0 and encrypted.length():
            encrypted.pad_from_right(256-encrypted.length())

        decrypted = pow(int(encrypted), d, n)
        decrypted = BitVector(intVal=decrypted, size =256)
        decrypted = decrypted[128:]
        decryptedfile.write(decrypted.get_bitvector_in_ascii())



if __name__ == "__main__":
    if sys.argv[1] == "-e": #encryption
        input = sys.argv[2]
        output = sys.argv[5]
        pfile = sys.argv[3]  
        p = open(pfile, "r")
        p = p.readline()
        qfile = sys.argv[4]
        q = open(qfile, "r")
        q =q.readline()
        RSAEncrypt(input,p, q, output)

    elif sys.argv[1] == "-d": #decryption
        input = sys.argv[2]
        output = sys.argv[5]
        pfile = sys.argv[3]  
        p = open(pfile, "r")
        p = p.readline()
        qfile = sys.argv[4]
        q = open(qfile, "r")
        q =q.readline()
        RSADecrypt(input, p, q, output)

    elif sys.argv[1] == "-g": #keygen
        pfile = sys.argv[2]
        # p = open(pfile, "w")
        qfile = sys.argv[3]
        # q = open(qfile, "w")
        RSAKeyGen(pfile,qfile)

