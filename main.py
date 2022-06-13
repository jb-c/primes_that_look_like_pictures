from utils.base_number import BaseNumber
from utils.primes import primesfrom2to, compute_ten_to_the_a_mod_p
import numpy as np
import pickle

cache_mode = 1 # 0 = no cache & recompute, 1 = use cached computations

#--------------------------------------------------------------------------------------------------#
#----------------------------- Finding Primes That Look Like Pictures -----------------------------#
#--------------------------------------------------------------------------------------------------#

# Read in the base number
base_number = BaseNumber('data/base_number.txt')

if cache_mode == 1:
    primes = primesfrom2to(982_451_653+1)
    ten_to_the_a_mod_p = compute_ten_to_the_a_mod_p(primes[:50], 10000)

    with open('data/ceched_primes.pickle', 'wb') as fp:
        pickle.dump(primes, fp)
    with open('data/cached_ten_to_the_a_mod_p.pickle', 'wb') as fp:
        pickle.dump(ten_to_the_a_mod_p, fp)
else:
    with open('data/ceched_primes.pickle', 'wb') as fp:
        primes = pickle.load(fp)
    with open('data/cached_ten_to_the_a_mod_p.pickle', 'wb') as fp:
        ten_to_the_a_mod_p = pickle.load(fp)
