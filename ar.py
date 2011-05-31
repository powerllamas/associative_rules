# -*- coding: utf-8 -*-

from transactions import TransactionsList
from args import process_args
from apriori import Apriori

def main(args):
    transactions = TransactionsList(args.infile)
    apriori = Apriori(transactions, args.minsup, args.minconf)
    print "Large sets:\n"
	print apriori.get_large_sets()
	print "\nRules:\n"
	print apriori.get_rules()

if __name__ == '__main__':
    args = process_args()
    if args.display_stats:
        pass
    main(args)

