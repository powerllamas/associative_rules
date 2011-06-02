# -*- coding: utf-8 -*-

from trie import node, root

class Dic:
    def __init__(self, transactions, minsup, M):
        self.__minsup = minsup
        self.__transactions = transactions
        self.__M = M

    def get_large_sets(self):
        """
        Calculates large sets from transactions. Returns dictionary where the key is arity and the value is list of item sets.
        """
        large_sets = {}
        
        root = Root()
        finished = False
        while not finished:
            i = (i + 1) % len(transactions)
            position = i / M
            finished = root.increment(transactions[i], position)
        large_sets = root.get_large_sets()
        return large_sets
