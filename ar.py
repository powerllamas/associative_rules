# -*- coding: utf-8 -*-

from transactions import TransactionsList
from args import process_args
from apriori import Apriori
from stats import is_posix, get_stats

def main(args):
    transactions = TransactionsList(args.infile)
    apriori = Apriori(transactions, args.minsup, args.minconf)
    large_sets = apriori.get_large_sets();
	print "Large sets:\n"
	print large_sets
	print "\nRules:\n"
	print apriori.get_rules(large_sets)

if __name__ == '__main__':
    args = process_args()
    stats = []
    if is_posix() and args.display_stats:
        main = get_stats(stats)(main)
    main(args)
    if stats:
        print stats

