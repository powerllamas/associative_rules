# -*- coding: utf-8 -*-

from transactions import TransactionsList
from apriori import Apriori
from dic import Dic
from stats import Stats
from rules import RulesGenerator

infiles = ['data/mushroom.dat', 'data/kosarak.dat', 'data/accidents.dat']

algorithms = ['dic', 'apriori']
supports = [0.9]#, 0.8, 0.7, 0.6, 0.5, 0.4, 0.35, 0.3, 0.25]
confidencies = [0.8]
ms = [1250]#, 250, 500, 1000, 2000, 8124]

def process(transactions, algorithm_name, support, confidence, m, infile):
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
    ls_size = 0
    for size in large_sets.values():
      ls_size += len(size)

    print "{infile};{algorithm_name};{support};{confidence};{m};{total_time};{user_time};{large_sets_time};{memory};{rules_no};{ls_size}".format(**locals())

if __name__ == '__main__':

    print "File;Alg_name;supp;conf;m;tot_t;usr_t;set_t;mem;rl_no;ls_no"
    for infile in infiles:
      transactions = TransactionsList(infile)
      for algorithm in algorithms:
	  for support in supports:
	      for confidence in confidencies:
		  if algorithm == 'dic':
		      for m in ms:
			  process(transactions, algorithm, support, confidence, m, infile)
		  else:
		      process(transactions, algorithm, support, confidence, "n/a", infile)
