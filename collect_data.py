# -*- coding: utf-8 -*-

from transactions import TransactionsList
from apriori import Apriori
from dic import Dic
from stats import Stats
from rules import RulesGenerator

infile = 'data/mushroom.dat'

algorithms = ['apriori', 'dic']
supports = [0.9]
confidencies = [0.8]
ms = [1000]

def process(transactions, algorithm_name, support, confidence, m):
    stats = Stats()
    if algorithm_name == 'apriori':
        algorithm = Apriori(transactions, support)
    else:
        algorithm = Dic(transactions, support, m)
    large_sets, counter = algorithm.get_large_sets_and_counter()
    stats.record_post_large_sets()
    rules = RulesGenerator.generate_rules(large_sets, confidence, counter, transactions)
    stats.record_post_rules()
    total_time = stats.real_time
    user_time = stats.user_time
    large_sets_time = stats.set_gen_time
    memory = stats.memory_use
    rules_no = len(rules)

    print "{algorithm_name};{support};{confidence};{m};{total_time};{user_time};{large_sets_time};{memory};{rules_no};".format(**locals())

if __name__ == '__main__':
    transactions = TransactionsList(infile)
    print "Alg_name;supp;conf;m;tot_t;usr_t;set_t;mem;rl_no;"
    for algorithm in algorithms:
        for support in supports:
            for confidence in confidencies:
                if algorithm == 'dic':
                    for m in ms:
                        process(transactions, algorithm, support, confidence, m)
                else:
                    process(transactions, algorithm, support, confidence, "n/a")
