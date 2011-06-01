# -*- coding: utf-8 -*-

from transactions import TransactionsList
from args import process_args
from apriori import Apriori
from stats import get_stats
from rules import RulesGenerator

stats = []
@get_stats(stats)
def main(args):
    transactions = TransactionsList(args.infile)
    apriori = Apriori(transactions, args.minsup)
    large_sets = apriori.get_large_sets()
    rules = RulesGenerator.generate_rules(large_sets, args.minconf, transactions)
    print "Large sets:"
    print large_sets
    print "Rules:"
    print rules

if __name__ == '__main__':
    args = process_args()
    main(args)
    if stats:
        print stats
