from tqdm import tqdm
import numpy as np
import pickle, time, random, math
from gmpy2 import is_strong_prp, is_strong_selfridge_prp

from utils.base_number import BaseNumber

# REF =  https://gmpy2.readthedocs.io/en/latest/advmpz.html#advanced-number-theory-functions





def test(candidates):
    probably_primes = np.full_like(candidates,False)
    probably_twin_primes = np.full_like(candidates,False)

    for i in tqdm(range(len(candidates)),desc='Primality Test'):
        pass_prp_test = is_strong_prp(candidates[i],2)
        if pass_prp_test:
            pass_strong_selfridge_prp_test = is_strong_selfridge_prp(candidates[i])
            if pass_strong_selfridge_prp_test:
                probably_primes[i] = True

                test_up = is_strong_prp(candidates[i]+2,2)
                test_dowm = is_strong_prp(candidates[i]-2,2)
                if test_up or test_dowm:
                    probably_twin_primes[i] = True
                    print("Index {i} is a likely twin prime")

    probably_prime_candidates = [candidates[i] for i,t in enumerate(probably_primes) if t]
    probably_twin_prime_candidates = [candidates[i] for i,t in enumerate(probably_twin_primes) if t]
    return probably_primes,probably_twin_primes,probably_prime_candidates,probably_twin_prime_candidates




if __name__ == '__main__':
    with open('data/cached_candidates.pickle', 'rb') as fp:
        candidates = pickle.load(fp)

    probably_primes, probably_twin_primes, probably_prime_candidates, probably_twin_prime_candidates = test(candidates)

    with open('data/cached_primes.pickle', 'wb') as fp:
        pickle.dump([probably_prime_candidates,probably_twin_prime_candidates], fp)