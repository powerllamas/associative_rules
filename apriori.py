# -*- coding: utf-8 -*-

from collections import defaultdict
from itertools import combinations

class Apriori(object):
    def __init__(self, transactions, minsup):
        self.__minsup = minsup
        self.__transactions = transactions

    def get_large_sets_and_counter(self):
        """
        Calculates large sets from transactions. Returns dictionary where the key is arity and the value is list of item sets.
        """
        large_sets = {}
        counter = self.__count_items_in_transactions(self.__transactions)
        minsup_count = self.__get_minsup_count()
        L1 = self.__getL1(counter, minsup_count)
        large_sets[1] = L1
        current_iter = 2
        while not self.__is_last_set_empty(large_sets):
            candidate_set = self.__apriori_gen(large_sets[current_iter-1])
            for transaction in self.__transactions:
                subset = self.__generate_subsets(candidate_set, transaction)
                for item in subset:
                    counter[item] += 1
            large_set = self.__filter_candidates(candidate_set, counter, minsup_count)
            large_sets[current_iter] = large_set
            current_iter += 1
        return large_sets, counter

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

    @staticmethod
    def __is_last_set_empty(large_sets):
        """
        Return True if last set in dictionary is empty, False otherwise.
        """
        last_index = len(large_sets)
        last_set = large_sets[last_index]
        return not bool(last_set)

    @staticmethod
    def __apriori_gen(large_set):
        """
        Generates and return list of candidates for inclusion in next large set.
        """
        L = []
        if len(large_set) >= 2:
            for item1, item2 in combinations(large_set, 2):
                if item1[:-1] == item2[:-1] and item1[-1] < item2[-1]:
                    candidate = item1[:] + item2[-1:]
                    L.append(candidate)
        for item in L:
            subsets = Apriori.__get_subsets(item)
            if any([ x not in large_set for x in subsets ]):
                L.remove(item)
        return L

    @staticmethod
    def __get_subsets(itemset):
        """
        Generates and returns subsets of an itemset. Subsets are generated by removing one element from itemset.
        """
        subsets = []
        length = len(itemset)
        for x in xrange(length):
            subset = itemset[:x] + itemset[x+1:]
            subsets.append(subset)
        return subsets

    @staticmethod
    def __generate_subsets(candidate_set, transaction):
        """
        Generates and returns subset of item sets from candidate set that are present in transaction.
        """
        subsets = []
        for item in candidate_set:
            if all([ x in transaction for x in item ]):
                subsets.append(item)
        return subsets

    @staticmethod
    def __filter_candidates(candidate_set, counter, minsup_count):
        """
        Returns filtered candidate set with only the item sets that have minimum support.
        """
        filtered = []
        for item in candidate_set:
            if counter[item] >= minsup_count:
                filtered.append(item)
        return filtered

