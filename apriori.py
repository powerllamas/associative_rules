# -*- coding: utf-8 -*-

import argparse
from collections import defaultdict
from itertools import combinations

from transactions import TransactionsDataSet

minconf = 0.7
minsup = 0.4
filename = "data/mushroom.dat"


def process_args():
    def percent_value(string):
        val = float(string)
        if 0.0 <= val <=1.0:
            return val
        else:
            raise argparse.ArgumentTypeError("{0} is not from the range of 0..1".format(string))

    parser = argparse.ArgumentParser(
            description=u"Induction of associative rules from datasets.",
            epilog=u"For current version check 'http://github.com/KrzysztofUrban/associative_rules'."
        )
    parser.add_argument('infile',
            help=u"input file")
    parser.add_argument('outfile',
            nargs='?',
            help=u"output file"
        )
    parser.add_argument('-c, --confidence',
            dest='minconf',
            type=percent_value,
            default=0.7,
            help=u"minimum confidence (0..1)"
        )
    parser.add_argument('-s, --support',
            dest="minsup",
            type=percent_value,
            default=0.4,
            help=u"minimum support (0..1)"
        )
    parser.add_argument('-p, --profile', 
            dest="display_stats",
            action='store_true', 
            help=u"display time and memory statistics"
        )
    return parser.parse_args()

def apriori_gen(large_set):
    L = []
    if len(large_set) >= 2:
        for item1, item2 in combinations(large_set, 2):
            if item1[:-1] == item2[:-1] and item1[-1] < item2[-1]:
                candidate = item1[:] + item2[-1:]
                L.append(candidate)
    for item in L:
        subsets = get_subsets(item)
        if any([ x not in large_set for x in subsets ]):
            L.remove(item)
    return L


def get_subsets(itemset):
    subsets = []
    length = len(itemset)
    for x in xrange(length):
        subset = itemset[:x] + itemset[x+1:]
        subsets.append(subset)
    return subsets


def generate_subsets(candidate_set, transaction):
    subsets = []
    for item in candidate_set:
        if all([ x in transaction for x in item ]):
            subsets.append(item)
    return subsets

def get_minsup_count():
    return int(len(transactions) * minsup)


def count_items(transactions):
    counter = defaultdict(int)
    for transaction in transactions:
        for item in transaction:
            counter[(item,)] += 1
    return counter


def getL1(counter, minsup_count):
    L1 = []
    for k, v in counter.iteritems():
        if v >= minsup_count:
            L1.append(k)
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


def filter_candidates(candidate_set, counter, minsup_count):
    filtered = []
    for item in candidate_set:
        if counter[item] >= minsup_count:
            filtered.append(item)
    return filtered

if __name__ == '__main__':

    args = process_args()
    large_sets = {}
    candidate_sets = {}
    transactions = TransactionsDataSet(filename)
    counter = count_items(transactions)
    minsup_count = get_minsup_count()
    L1 = getL1(counter, minsup_count)
    large_sets[1] = L1
    current_iter = 2
    while not is_last_set_empty(large_sets):
        C = apriori_gen(large_sets[current_iter-1])
        for transaction in transactions:
            subset = generate_subsets(C, transaction)
            for item in subset:
                counter[item] += 1
        L = filter_candidates(C, counter, minsup_count)
        large_sets[current_iter] = L
        current_iter += 1
    results = collect_results(large_sets)
    print large_sets

