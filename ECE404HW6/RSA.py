# Homework Number: 5
# Name: Rohith Kothandaraman
# ECN Login: rkothand
# Due Date:2/14/22

import sys
from BitVector import *
import PrimeGenerator


if __name__ == "__main__":

    num_of_bits_desired = int(sys.argv[1])
    generator = PrimeGenerator.PrimeGenerator(bits=num_of_bits_desired)
