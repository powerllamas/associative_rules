# -*- coding: utf-8 -*-

from collections import defaultdict, OrderedDict

from transactions import TransactionsDataSet

minconf = 0.7
minsup = 0.3
filename = "data/mushroom.dat"

large_sets = {}
candidate_sets = {}

transactions = TransactionsDataSet(filename)


def print_counter(counter):
    keys = counter.keys()
    for key in sorted(keys, key=int):
        print "{0}:\t{1}".format(key, counter[key])


def apriori_gen(large_set):
    L = OrderedDict()
    items = large_set.keys()
    print items
    if len(items) >= 2:
        for x in xrange(len(items)-1):
            item1, item2 = items[x:x+2]
            if item1[:-1] == item2[:-1] and item1[-1] < item2[-1]:
                candidate = item1[:] + item2[-1:]
                L[candidate] = 0
    print L
    return L

def generate_subsets(candidate_set, transaction):
    subsets = set()
    for item in candidate_set:
        if all([ x in transaction for x in item ]):
            subsets.add(item)
    return subsets

def get_minsup_count():
    return int(len(transactions) * minsup)


def count_items(transactions):
    counter = defaultdict(int)
    for transaction in transactions:
        for item in transaction:
            counter[item] += 1
    return counter


def getL1(counter, minsup_count):
    L1 = OrderedDict()
    for k, v in counter.iteritems():
        if v >= minsup_count:
            L1[(k,)] = v
    return L1


def is_last_set_empty(large_sets):
    last_index = len(large_sets)
    last_set = large_sets[last_index]
    return not bool(last_set)


def collect_results(large_sets):
    results = []
    for L in large_sets.iteritems():
        for item in L:
            results.append(item)
    return results


def filter_candidates(candidate_set, minsup_count):
    filtered = set()
    for item in candidate_set:
        if item[1] >= minsup_count:
            filtered.add(item)
    return filtered

if __name__ == '__main__':
    counter = count_items(transactions)
    minsup_count = get_minsup_count()
    L1 = getL1(counter, minsup_count)
    large_sets[1] = L1
    current_iter = 2
    while not is_last_set_empty(large_sets):
        C = apriori_gen(large_sets[current_iter-1])
        L = filter_candidates(C, minsup_count)
        for transaction in transactions:
            subset = generate_subsets(C, transaction)
            for item in subset:
                item[1] += 1
        large_sets[current_iter] = L
        current_iter += 1
    results = collect_results(large_sets)

