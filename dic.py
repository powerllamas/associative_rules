# -*- coding: utf-8 -*-

from trie import Root

class Dic(object):
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
        self.root = Root(minsup_count)
        finished = False
        pass_counter = 0
        while not finished:
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

    def get_counter(self):
        return DicCounter(self.root)
        
    def get_minsup_count(self):
        """
        Calculates and returns miniumum support given in number of transactions.
        """
        return int(len(self.__transactions) * self.__minsup)

    def get_large_sets_and_counter(self):
        return self.get_large_sets(), self.get_counter()

class DicCounter:
    def __init__(self, root):
        self.__root = root

    def __getitem__(self, key):
        node = self.__root.get_node(key)
        if node is None:
            raise KeyError(u"No key '{0}' in DicCounter".format(key))
        else:
            return node.counter

if __file__ == '__main__':
    from transactions import TransactionsList
    transactions = TransactionsList("data\mushroom.dat")
    dic = Dic(transactions, 0.8, 500)
    #dic.get_large_sets()
