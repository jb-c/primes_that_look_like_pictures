from utils.base_number import BaseNumber
from utils.primes import primesfrom2to
from tqdm import tqdm
import numpy as np
import pickle, time
from test_candidates import test

start_time = time.time()
cache_mode = 0 # 0 = no cache & recompute, 1 = use cached computations
verbose = True

#--------------------------------------------------------------------------------------------------#
#----------------------------- Finding Primes That Look Like Pictures -----------------------------#
#--------------------------------------------------------------------------------------------------#
def main(K = 1, big_P = 1_000_000):

    if verbose: print(f'0. Program started.')
    # Load in the base number, compute the first few primes and the base number mod p
    # Store the result in a pickle, load to save time
    if cache_mode == 0:
        base_number = BaseNumber('data/aspect_number_small.txt')
        primes = primesfrom2to(big_P) # 982_451_653+1
        b_mod_p = base_number.int % primes
        with open('data/cache.pickle', 'wb') as fp:
            pickle.dump([base_number,primes,b_mod_p], fp)
    else:
        with open('data/cache.pickle', 'rb') as fp:
            [base_number,primes,b_mod_p] = pickle.load(fp)

    if verbose: print(f'1. Computed base number mod p. We are using {len(primes)} primes.')

    if cache_mode == 1:
        with open('data/cached_candidates.pickle', 'rb') as fp:
            candidates = pickle.load(fp)
    else:
        s = np.arange(1,10**K) # The numbers up to 10**K
        s = np.concatenate([-np.flip(s),s]) # Include the negative shifts as well - nb zero not included

        ten_mod_p = 10 % primes
        ten_to_the_a_mod_p = np.ones_like(primes) # As a is zero initially

        tuples_to_check = np.zeros([1,2])

        # Check if [b + (s * 10**a)] % p == 0
        for a in tqdm(range(0,base_number.len - K), desc='Sieve Checks'):
            digits = int(base_number.string[base_number.len - K - a :base_number.len - a])
            s_is_valid = (s > -digits) & (s < 10 ** K - digits)  # ex: If digits = 87 then anything bigger than 12 is an invalid shift

            valid_shifts_mod_p = (b_mod_p + (np.atleast_2d(s[s_is_valid]).T * ten_to_the_a_mod_p)) % primes

            investigate_valid_shift_further = ~(valid_shifts_mod_p == 0).any(axis=1)  # If b+(s*10^a) % p != 0 for all p
            shifts_to_investigate_further = s[s_is_valid][investigate_valid_shift_further] # The shifts to investigate
            tuples_to_investigate_further = np.stack([a * np.ones_like(shifts_to_investigate_further),
                                                                       shifts_to_investigate_further]).T

            ten_to_the_a_mod_p = (ten_to_the_a_mod_p * ten_mod_p) % primes # Increment
            tuples_to_check = np.vstack([tuples_to_check, tuples_to_investigate_further]) # Add to global array

        if verbose: print(f'2. Completed initial sieve checks. We have {len(tuples_to_check)} candidates. \n\t Time Elapsed = {np.round((time.time()-start_time) / 60,decimals=2)} mins')

        # Unpack the tuples_to_check array
        shifts = tuples_to_check[:, 1].astype(int)
        # s & e are arrays of indecies for the start and end chars/digits we want to shift
        e = base_number.len - tuples_to_check[:, 0].astype(int)
        s = e - K

        candidates = [
            int(base_number.string[:si] +  # beginning of base number
            str(int(base_number.string[si:ei]) + shift).zfill(K) +  # new shifted middle bit
            base_number.string[ei:])  # end of base number
            for (si, ei, shift) in tqdm(zip(s, e, shifts),desc='Formatting candidates',total=len(tuples_to_check))
        ]

        candidates = np.array(candidates)

        with open('data/cached_candidates.pickle', 'wb') as fp:
            pickle.dump(candidates, fp)

    if verbose: print(f'3. Ready to start primality testing. \n\t Time Elapsed = {np.round((time.time()-start_time) / 60,decimals=2)} mins')
    return candidates


if __name__ == '__main__':
    out = main(K=3,big_P=1_000_00)
    probably_primes, probably_twin_primes, probably_prime_candidates, probably_twin_prime_candidates = test(out)

    print(f"We have {probably_primes.sum()} primes")
    print(f"We have {probably_twin_primes.sum()} twin primes")

    with open('data/cached_primes.pickle', 'wb') as fp:
        pickle.dump([probably_prime_candidates,probably_twin_prime_candidates], fp)
