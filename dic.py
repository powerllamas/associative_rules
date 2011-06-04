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
        
        i = 0
        while not finished:
            i = (i + 1) % len(self.transactions)
            position = i / M
            finished = root.increment(self.transactions[i], position)
            if i % M == 0:
                root.tree.update_child_states()
        large_sets = root.get_large_sets()
        return large_sets
