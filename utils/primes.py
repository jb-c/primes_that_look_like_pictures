import numpy as np
import pickle

'''
Quick prime finding utilities
'''

'''
1  million th prime = 15_485_863
5  million th prime = 86_028_121
10 million th prime = 179_424_673
50 million th prime = 982_451_653
'''


def primesfrom2to(n):
    '''
    A prime sieve that computes primes up to 2<=p < n for n >= 6
    https://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n


    :param n: The maxumum number to go up to (n=7 will return [2,3,5])
    :return: A list of primes up to n
    '''
    sieve = np.ones(n//3 + (n%6==2), dtype=bool)
    for i in range(1,int(n**0.5)//3+1):
        if sieve[i]:
            k=3*i+1|1
            sieve[       k*k//3     ::2*k] = False
            sieve[k*(k-2*(i&1)+4)//3::2*k] = False
    return np.r_[2,3,((3*np.nonzero(sieve)[0][1:]+1)|1)]


def compute_ten_to_the_a_mod_p(primes,H=1):
    '''
    Computes 10^a mod p for p in primes and a in range(H)


    :param primes: A list of primes, all the primes we do 10^a mod p for
    :param H: The maximum exponent to go up to
    :return: An array of size (len(primes), H) with (i,j)-th entry 10^(j+1) % primes[i]
    '''

    primes = primes.astype(int)
    ten_mod_p = (10 % primes).astype(int)
    ten_to_the_a_mod_p = (10 % primes).astype(int)
    print("Go")
    with open('data/temp_ten_to_the_a_mod_p.txt', 'ab') as fp:
        np.savetxt(fp, ten_mod_p,newline=', ')
        #for i in range(H-1):
        #    ten_to_the_a_mod_p = (ten_to_the_a_mod_p * ten_mod_p) % primes
        #    fp.write(f',\n{arr2str(ten_to_the_a_mod_p)}')

    return ten_to_the_a_mod_p
