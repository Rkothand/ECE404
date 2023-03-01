from BitVector import *
from sys import *
from PrimeGenerator import PrimeGenerator


breakRSAEncrypt():
    # Read in the encrypted message from the file

breakRSADecryption():
    # Read in the encrypted message from the file


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

