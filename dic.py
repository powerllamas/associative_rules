# -*- coding: utf-8 -*-

from trie import Root
from collections import defaultdict
import math, time

class Dic(object):
    def __init__(self, transactions, minsup, M):
        self.__minsup = minsup
        self.__transactions = transactions
        self.__M = M
        self.__minsup_count = self.__get_minsup_count()

    def get_large_sets(self):
        """
        Calculates large sets from transactions. Returns dictionary where the key is arity and the value is list of item sets.
        """
        large_sets = {}
        counter = self.__count_items_in_transactions(self.__transactions)
        minsup_count = self.__get_minsup_count()
        L1 = self.__getL1(counter, minsup_count)

        self.root = Root(self.__minsup, len(self.__transactions), L1)
        self.root.update_states(0, 0)
        
        parts_no = math.ceil(float(len(self.__transactions)) / float(self.__M))
        finished = False
        pass_counter = 1
        while not finished:
#            print "pass: %d" % (pass_counter)
            for i, transaction in enumerate(self.__transactions):
                position = i / self.__M
                self.root.increment(transaction, position)
                if (i+1) % self.__M == 0 or (i+1) == len(self.__transactions):
                    #print "\tpart %d" % (position + 1)
                    trans_in_last_part = (i+1) - position * self.__M
                    next_position = (position + 1)% parts_no
                    finished = self.root.update_states(next_position, trans_in_last_part)                    
                    if finished:
                        break
            pass_counter += 1

        #self.root.print_node(large_only = True)
        #print "%d passes" % (pass_counter)
        large_sets = self.root.get_large_sets(large_sets)
        return large_sets

    def get_counter(self):
        return DicCounter(self.root)
        
    def get_large_sets_and_counter(self):
        return self.get_large_sets(), self.get_counter()

    @staticmethod
    def __count_items_in_transactions(transactions):
        """
        Counts items and returns dictionary with them as keys and their count as value.
        """
        counter = defaultdict(int)
        for transaction in transactions:
            for item in transaction:
                counter[(item,)] += 1
        return counter

    def __get_minsup_count(self):
        """
        Calculates and returns miniumum support given in number of transactions.
        """
        return int(len(self.__transactions) * self.__minsup)

    @staticmethod
    def __getL1(counter, minsup_count):
        """
        Calculates and returns first large set.
        """
        L1 = []
        for k, v in counter.iteritems():
            if v >= minsup_count:
                L1.append(k)
        return sorted(L1)    

class DicCounter:
    def __init__(self, root):
        self.__root = root

    def __getitem__(self, key):
        node = self.__root.get_node(key)
        if node is None:
            raise KeyError(u"No key '{0}' in DicCounter".format(key))
        else:
            return node.counter

#__file__ = '__main__'

if __file__ == '__main__':

    from transactions import TransactionsList
    transactions = TransactionsList("data\mushroom.dat")
    dic = Dic(transactions, 0.8, 1000)
    start = time.clock()
    ls = dic.get_large_sets()
    stop = time.clock()
    elapsed = stop - start
    count = 0
    for sets in ls.values():
        count += len(sets)
    print "Large sets number: %d" % (count,)
    print elapsed
    print ls
