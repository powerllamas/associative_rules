# -*- coding: utf-8 -*-

from collections import defaultdict

minconf = 0.7
minsup = 0.3
filename = "data/mushroom.dat"

def get_transactions(filename):
    with open(filename) as file:
        for line in file:
            transaction = line.split()
            yield transaction

def print_counter(counter):
    keys = counter.keys()
    for key in sorted(keys, key=int):
        print "{0}:\t{1}".format(key, counter[key])

if __name__ == '__main__':
    counter = defaultdict(int)
    for transaction in get_transactions(filename):
        for item in transaction:
            counter[item] += 1
    print_counter(counter)

