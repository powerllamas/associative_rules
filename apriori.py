# -*- coding: utf-8 -*-

from collections import defaultdict

from transactions import TransactionsList

minconf = 0.7
minsup = 0.3
filename = "data/mushroom.dat"

large_sets = []
candidate_sets = []

transactions = TransactionsList(filename)

def print_counter(counter):
    keys = counter.keys()
    for key in sorted(keys, key=int):
        print "{0}:\t{1}".format(key, counter[key])

def apriori_gen(large_set):
    pass

if __name__ == '__main__':
    counter = defaultdict(int)
    for transaction in transactions:
        for item in transaction:
            counter[item] += 1

    minsup_count = int(transactions.nr_of_transactions*minsup)
    L1 = set()
    for k, v in counter.iteritems():
        if v >= minsup_count:
            item = ((k,), v)
            L1.add(item)
    large_sets.append(L1)

    
