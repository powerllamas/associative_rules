# -*- coding: utf-8 -*-

from transactions import TransactionsList
from apriori import Apriori
from dic import Dic
from stats import Stats
from rules import RulesGenerator

infile = 'data/kosarak.dat'

algorithms = ['apriori']
supports = reversed([0.05, 0.15, 0.25, 0.35])
confidencies = [0.7]
ms = [1000, 5000, 25000]

last_total_time = 0
last_user_time = 0

def process(infile, algorithm_name, support, confidence, m):
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

    print "{algorithm_name}\t{infile}\t{support}\t{confidence}\t{m}\t{rules_no}\t{large_len}\t{memory}\t{total_time}\t{user_time}\t{large_sets_time}".format(**locals())

if __name__ == '__main__':
    print "Alg_name\tdataset\tsupp\tconf\tm\trl_no\tlrg_len\tmem\ttot_t\tusr_t\tset_t"
    for algorithm in algorithms:
        for support in supports:
            for confidence in confidencies:
                if algorithm == 'dic':
                    for m in ms:
                        process(infile, algorithm, support, confidence, m)
                else:
                    process(infile, algorithm, support, confidence, "n/a")
>>>>>>> 6637a9a5e0711001e2d0e88274b7cf827b46458d
