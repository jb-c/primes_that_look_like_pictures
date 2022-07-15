from utils.base_number import BaseNumber
from utils.primes import primesfrom2to
from tqdm import tqdm
import numpy as np
import pickle, time

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
        base_number = BaseNumber('data/base_number.txt')
        primes = primesfrom2to(1_00) # 982_451_653+1
        b_mod_p = base_number.int % primes
        with open('data/cache.pickle', 'wb') as fp:
            pickle.dump([base_number,primes,b_mod_p], fp)
    else:
        with open('data/cache.pickle', 'rb') as fp:
            [base_number,primes,b_mod_p] = pickle.load(fp)

    if verbose: print(f'1. Computed base number mod p.')

    s = np.arange(1,10**K) # The numbers up to 10**K
    s = np.concatenate([-np.flip(s),s]) # Include the negative shifts as well - nb zero not included

    ten_mod_p = 10 % primes
    ten_to_the_a_mod_p = np.ones_like(primes) # As a is zero initially

    tuples_to_check = np.zeros([1,2])

    # Check if [b + (s * 10**a)] % p == 0
    for a in tqdm(range(1,base_number.len - K), desc='\t Sieve Checks'):
        digits = int(base_number.string[a:a + K])
        s_is_valid = (s > -digits) & (s < 10 ** K - digits)  # ex: If digits = 87 then anything bigger than 12 is an invalid shift

        valid_shifts_mod_p = (b_mod_p + (np.atleast_2d(s[s_is_valid]).T * ten_to_the_a_mod_p)) % primes

        investigate_valid_shift_further = ~(valid_shifts_mod_p == 0).any(axis=1)  # If b+(s*10^a) % p != 0 for all p
        shifts_to_investigate_further = s[s_is_valid][investigate_valid_shift_further] # The shifts to investigate
        tuples_to_investigate_further = np.stack([a * np.ones_like(shifts_to_investigate_further),
                                                                   shifts_to_investigate_further]).T

        ten_to_the_a_mod_p = (ten_to_the_a_mod_p * ten_mod_p) % primes # Increment
        tuples_to_check = np.vstack([tuples_to_check, tuples_to_investigate_further]) # Add to global array

    if verbose: print(f'2. Completed initial sieve checks. We have {len(tuples_to_check)} candidates. \n\t Time Elapsed = {np.round((time.time()-start_time) / 60,decimals=2)} mins')
    return base_number, tuples_to_check





if __name__ == '__main__':
    out = main(K=1,big_P=100)