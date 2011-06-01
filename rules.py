# -*- coding: utf-8 -*-

from itertools import combinations

class RulesGenerator:
    def __init__(self):
        pass

    @staticmethod
    def generate_rules(large_sets, minconf, transactions):
        rules = []
        for large_sets_k in large_sets.values():
            for large_set in large_sets_k:
                if(len(large_set) >= 2):
                    subsets = RulesGenerator.__get_all_subsets(large_set)
                    for subset in subsets:
                        antecedent = frozenset(subset)
                        consequent = frozenset(large_set).difference(antecedent)
                        conf = RulesGenerator.__get_confidence(antecedent, consequent, transactions)
                        if  conf >= minconf:
                            rules.append((antecedent, consequent))
                           # print "%s --> %s | %f" % (antecedent, consequent, conf)
        return rules

    @staticmethod
    def __get_all_subsets(set):
        subsets = []
        length = len(set)
        for i in range(1,length):
            subsets.extend(combinations(set, i))
        return subsets
    
    @staticmethod
    def __get_confidence(antecedent, consequent, transactions):
        antecedent_counter = 0
        both_counter = 0
        for transaction in transactions:
            transaction_set = set(transaction)
            if antecedent.issubset(transaction_set):
                antecedent_counter += 1
                if consequent.issubset(transaction_set):
                    both_counter += 1
        if antecedent_counter > 0:
            return float(both_counter) / float(antecedent_counter)
        else:
            return 0
