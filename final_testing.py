
from tqdm import tqdm
import numpy as np
import pickle, time, random, math
from gmpy2 import is_strong_prp, is_strong_selfridge_prp

from utils.base_number import BaseNumber

base_number = BaseNumber('data/aspect_twin_prime_small.txt')
is_actually_prime = is_strong_prp(base_number.int,2) and is_strong_selfridge_prp(base_number.int) and is_strong_prp(base_number.int,3)
is_actually_twin_prime = is_strong_prp(base_number.int+2,2) and is_strong_selfridge_prp(base_number.int+2) and is_strong_prp(base_number.int+2,3)
