# Homework Number: 5
# Name: Rohith Kothandaraman
# ECN Login: rkothand
# Due Date:2/14/22

from bitvector import *

from Crypto.Cipher import AES
from sys import sys




def ctr_aes_image(iv, imagefile = 'image.ppm', out_file='enc_image.ppm', key_file ='keyCTR.txt'):
    fp = open(sys.argv[1], 'rb')
    ppmHeader = None
    pp1 = fp.readline()
    pp2 = fp.readline()
    pp3 = fp.readline()

    image_out = fp.read()

    image_out.write(pp1)
    image_out.write(pp2)
    image_out.write(pp3)




    with open(key_file, "r") as f:
        key = f.read()
    key4 = bytes(key, 'utf-8')
    aes_function = AES.new(key4, AES.MODE_CTR)

    bit_image = BitVector(rawbytes=image)
    segments = bit_image //16
    list_segment = [bit_image[i*16: i*16+16] for i in range(segments)]

    if __name__ == "__main__":
        iv = BitVector(textstring='computersecurity')
        ctr_aes_image(iv, 'image.ppm', 'enc_image.ppm', 'keyCTR.txt')
