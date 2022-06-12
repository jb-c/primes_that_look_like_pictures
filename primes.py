import numpy as np
import pickle

'''
Quick prime finding utilities
'''

def primesfrom2to(n):
    '''
    A prime sieve that computes primes up to n >= 6. n is not inclusive
    https://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n
    '''
    sieve = np.ones(n//3 + (n%6==2), dtype=bool)
    for i in range(1,int(n**0.5)//3+1):
        if sieve[i]:
            k=3*i+1|1
            sieve[       k*k//3     ::2*k] = False
            sieve[k*(k-2*(i&1)+4)//3::2*k] = False
    return np.r_[2,3,((3*np.nonzero(sieve)[0][1:]+1)|1)]


def compute_ten_to_the_a_mod_p(primes,H=1000):
    '''
    Computes 10^a mod p for p in primes and a in range(H)
    Returns an np array of size (len(primes),H) with (i,j)-th entry 10^(j+1) % primes[i]
    
    '''
    ten_mod_p = 10 % primes
    ten_to_the_a_mod_p = np.tile(ten_mod_p, (H, 1))  # Has shape (num_primes,H)

    for a in range(1, H):
        ten_to_the_a_mod_p[a, :] = (ten_to_the_a_mod_p[a - 1, :] * ten_mod_p) % primes

    return ten_to_the_a_mod_p







'''
1 million  -  15,485,863
5 million  -  86,028,121
10 million -  179,424,673
50 million -  982,451,653
'''
if __name__ == '__main__':
    primes = primesfrom2to(982451653+1)
    with open('data/primes.pickle', 'wb') as fp:
        pickle.dump(primes, fp)
else:
    with open('data/primes.pickle', 'rb') as fp:
        primes = pickle.load(fp)