# -*- coding: utf-8 -*-

from transactions import TransactionsList
from apriori import Apriori
from dic import Dic
from stats import Stats
from rules import RulesGenerator

infile = 'data/accidents.dat'

algorithms = ['apriori']
supports = reversed([0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
confidencies = [0.7]
ms = [100, 1000, 10000]

last_total_time = 0
last_user_time = 0

def process(transactions, algorithm_name, support, confidence, m):
    global last_total_time
    global last_user_time
    global infile
    filename = infile
    stats = Stats()
    if algorithm_name == 'apriori':
        algorithm = Apriori(transactions, support)
    else:
        algorithm = Dic(transactions, support, m)
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

    print "{algorithm_name}\t{filename}\t{support}\t{confidence}\t{m}\t{rules_no}\t{large_len}\t{memory}\t{total_time}\t{user_time}\t{large_sets_time}".format(**locals())

if __name__ == '__main__':
    transactions = TransactionsList(infile)
    print "Alg_name\tdataset\tsupp\tconf\tm\trl_no\tlrg_len\tmem\ttot_t\tusr_t\tset_t"
    for algorithm in algorithms:
        for support in supports:
            for confidence in confidencies:
                if algorithm == 'dic':
                    for m in ms:
                        process(transactions, algorithm, support, confidence, m)
                else:
                    process(transactions, algorithm, support, confidence, "n/a")
