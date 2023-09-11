import pickle
import numpy as np
from tqdm import tqdm
from gmpy2 import is_strong_prp, is_strong_selfridge_prp

    def isPrimeHandle(p):
        return is_strong_prp(p, 2) and is_strong_selfridge_prp(p) and is_strong_prp(p, 3)

if __name__ == '__main__':
    with open('data/cached_primes.pickle', 'rb') as fp:
        [probably_prime_candidates,probably_twin_prime_candidates] = pickle.load(fp)


    ## Test probable primes
    is_actually_prime = np.full_like(probably_prime_candidates,False)
    for i,p in tqdm(enumerate(probably_prime_candidates),desc='Checking Primes',total=len(probably_prime_candidates)):
        is_p_prime = isPrimeHandle(p)
        is_actually_prime[i] = is_p_prime

    print(is_actually_prime.mean()," % of probably primes are primes")


    ## Test twin primes
    is_actually_twin_prime = np.full_like(probably_twin_prime_candidates,False)
    for j,q in enumerate(probably_twin_prime_candidates):
        is_actually_twin_prime[j] = isPrimeHandle(q) & isPrimeHandle(q-2)
        if not is_actually_twin_prime[j]:
            is_actually_twin_prime[j] = isPrimeHandle(q) & isPrimeHandle(q + 2)

    print(is_actually_twin_prime.mean()," % of probably twin primes are twin primes")




