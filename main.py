from base_number import base_number
from primes import primes,compute_ten_to_the_a_mod_p
import numpy as np
import pickle

ten_to_the_a_mod_p = compute_ten_to_the_a_mod_p(primes[:100_000],10000)
with open('data/ten_to_the_a_mod_p.pickle', 'wb') as fp:
    pickle.dump(ten_to_the_a_mod_p, fp)
