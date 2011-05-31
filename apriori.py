# -*- coding: utf-8 -*-

from collections import defaultdict
from sets import Set
from itertools import combinations

class Apriori:
    @classmethod
    def _apriori_gen(self, large_set):
        L = []
        if len(large_set) >= 2:
            for item1, item2 in combinations(large_set, 2):
                if item1[:-1] == item2[:-1] and item1[-1] < item2[-1]:
                    candidate = item1[:] + item2[-1:]
                    L.append(candidate)
        for item in L:
            subsets = Apriori._get_subsets(item)
            if any([ x not in large_set for x in subsets ]):
                L.remove(item)
        return L

    @classmethod
    def _get_subsets(self, itemset):
        subsets = []
        length = len(itemset)
        for x in xrange(length):
            subset = itemset[:x] + itemset[x+1:]
            subsets.append(subset)
        return subsets

    @classmethod
    def _generate_subsets(self, candidate_set, transaction):
        subsets = []
        for item in candidate_set:
            if all([ x in transaction for x in item ]):
                subsets.append(item)
        return subsets

   
	@classmethod
    def _get_rules(self, L):
        rules = []
		for large_set in L:
			subsets = _get_all_subsets(large_set)
			for subset in subsets:
				antecedent = Set(subset)
				consequent = large_set - antecedent
				if _get_confidence(antecent, consequent) >= self._minconf:
					rules.append((antecent, consequent))
		return rules

    def _get_all_subsets(set):
        subsets = []
        length = len(set)
        for i in range(1,length):
            subsets.extend(combinations(set, i))
		return subsets

	def _get_confidence(antecent, consequent):
		antecent_counter = 0
		both_counter = 0
		for transaction in self.__transactions:
			if antecent in transaction:
				antecent_counter += 1
				if consequent in transaction:
				both_counter += 1
		if antecent_counter > 0:
			return both_counter / antecent_counter
		else
			return 0

    def _count_items_in_transactions(self):
        counter = defaultdict(int)
        for transaction in self._transactions:
            for item in transaction:
                counter[(item,)] += 1
        return counter

    def _get_minsup_count(self):
        return int(len(self._transactions) * self._minsup)

    def _is_last_set_empty(self):
        last_index = len(self._large_sets)
        last_set = self._large_sets[last_index]
        return not bool(last_set)


    def _collect_results(self):
        results = []
        for L in self._large_sets.iteritems():
            for item in L:
                results.append(item)
        return results

    def _filter_candidates(self, candidate_set):
        filtered = []
        for item in candidate_set:
            if self._counter[item] >= self._minsup_count:
                filtered.append(item)
        return filtered

    def _getL1(self):
        L1 = []
        for k, v in self._counter.iteritems():
            if v >= self._minsup_count:
                L1.append(k)
        return L1

    def __init__(self, transactions, minsup, minconf):
        self._large_sets = {}
        self._candidate_sets = {}
        self._minsup = minsup
        self._minconf = minconf
        self._transactions = transactions

    def get_large_sets(self):
        self._counter = self._count_items_in_transactions()
        self._minsup_count = self._get_minsup_count()
        L1 = self._getL1()
        self._large_sets[1] = L1
        current_iter = 2
        while not self._is_last_set_empty():
            C = Apriori._apriori_gen(self._large_sets[current_iter-1])
            for transaction in self._transactions:
                subset = self._generate_subsets(C, transaction)
                for item in subset:
                    self._counter[item] += 1
            L = self._filter_candidates(C)
            self._large_sets[current_iter] = L
            current_iter += 1
        self._results = self._collect_results()
        return self._large_sets

