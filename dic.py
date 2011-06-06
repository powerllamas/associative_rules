# -*- coding: utf-8 -*-

from trie import Root

class Dic:
    def __init__(self, transactions, minsup, M):
        self.__minsup = minsup
        self.__transactions = transactions
        self.__M = M
        self.__minsup_count = self.get_minsup_count()

    def get_large_sets(self):
        """
        Calculates large sets from transactions. Returns dictionary where the key is arity and the value is list of item sets.
        """
        large_sets = {}
        
        minsup_count = self.get_minsup_count()
        print minsup_count
        self.root = Root(minsup_count)
        finished = False
        pass_counter = 0
        while not finished:
            print "pass %d" % (pass_counter)
            for i, transaction in enumerate(self.__transactions):
                position = i / self.__M
                if i % self.__M == 0:
                    #print "\tpart %d" % (position)
                    finished = self.root.update_child_states(position)                    
                    if finished and (position > 0 or pass_counter > 0):
                        break
                self.root.increment(transaction, position)
            pass_counter += 1

        large_sets = self.root.get_large_sets(large_sets)
        return large_sets
        
    def get_minsup_count(self):
        """
        Calculates and returns miniumum support given in number of transactions.
        """
        return int(len(self.__transactions) * self.__minsup)

if __file__ == '__main__':
    from transactions import TransactionsList
    transactions = TransactionsList("data\mushroom.dat")
    dic = Dic(transactions, 0.8, 500)
    #dic.get_large_sets()
