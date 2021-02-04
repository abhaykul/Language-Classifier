"""
Abhay Kulkarni
python v3.9

Small functions used commonly
"""
from collections import Counter as c
from random import shuffle
import math


# Helper function for mapping unique/distinct data of every column
def distinct_val(tup):
    return list(set(tup))


# Returns the mode of all the columns (most common value)
def mode(data):
    [(item, count)] = c(data).most_common(1)
    return item


# Removes all instances of seq from the item list
def remove_all(item, seq):
    return [x for x in seq if x != item]


# Max value from the sequence breaking ties randomly
def argmax(seq, key=(lambda x: x)):
    shuffle(seq)
    return max(seq, key=key)


# Normalization
def normalize(dist):
    total = sum(dist)
    return [(n / total) for n in dist]


# Updates values after 0 check
def zero_update(n):
    result = 0
    if n != 0:
        result = n * (math.log2(n))
    return result

