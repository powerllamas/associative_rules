# -*- coding: utf-8 -*-

from transactions import TransactionsList
from apriori import Apriori
from dic import Dic
from stats import Stats
from rules import RulesGenerator

infiles = ['data/mushroom.dat', 'data/accidents.dat', 'data/kosarak.dat']
#infiles = ['data/kosarak.dat', 'data/accidents.dat']

algorithms = ['dic', 'apriori']
supports = {'data/mushroom.dat' : [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.35, 0.3, 0.25], 'data/kosarak.dat' : [0.6, 0.4, 0.2, 0.1, 0.05, 0.025, 0.01], 'data/accidents.dat' : [0.8, 0.6, 0.4]}
confidencies = [0.8]
ms = {'data/mushroom.dat' : [100, 500, 1000, 2000, 8124], 'data/kosarak.dat' : [100, 1000, 10000, 100000], 'data/accidents.dat' : [100, 5000, 50000]}
randoms = [0, 1]
partials = [0, 1]
last_total_time = 0
last_user_time = 0

def process(infile, algorithm_name, support, confidence, m, random, partial):
    stats = Stats()
    transactions = TransactionsList(infile)
    stats.record_post_large_sets()
    stats.record_post_rules()
    last_total_time = stats.real_time
    last_user_time = stats.user_time
    stats = Stats()
    if algorithm_name == 'apriori':
        algorithm = Apriori(transactions, support)
    else:
        algorithm = Dic(transactions, support, m, random, partial)
    large_sets, counter = algorithm.get_large_sets_and_counter()
    stats.record_post_large_sets()
    rules = RulesGenerator.generate_rules(large_sets, confidence, counter, transactions)
    stats.record_post_rules()
    large_len = len(large_sets)
    total_time = stats.real_time - last_total_time
    user_time = stats.user_time - last_user_time
    large_sets_time = stats.set_gen_time - last_total_time
    last_total_time = stats.real_time
    last_user_time = stats.user_time
    memory = stats.memory_use
    rules_no = len(rules)

    print "{infile}\t{algorithm_name}\t{support}\t{confidence}\t{m}\t{rules_no}\t{large_len}\t{memory}\t{total_time}\t{user_time}\t{large_sets_time}\t{partial}\t{random}".format(**locals())

if __name__ == '__main__':
    print "dataset\tAlg_name\tsupp\tconf\tm\trl_no\tlrg_len\tmem\ttot_t\tusr_t\tset_t\tpart\trand"
    for infile in infiles:
        transactions = TransactionsList(infile)
        for support in supports[infile]:
            for confidence in confidencies:
                for algorithm in algorithms:
                    if algorithm == 'dic':
                        for m in ms[infile]:
                            for partial in partials:
                                for random in randoms:
                                    process(infile, algorithm, support, confidence, m, random, partial)
                    else:
                        process(infile, algorithm, support, confidence, "n/a", "n/a", "n/a")
