# -*- coding: utf-8 -*-

from itertools import combinations

class RulesGenerator:
    def __init__(self):
        pass

    @staticmethod
    def generate_rules(large_sets, minconf, counter, transactions):
        rules = []
        for large_sets_k in large_sets.values():
            for large_set in large_sets_k:
                if(len(large_set) >= 2):
                    subsets = RulesGenerator.__get_all_subsets(large_set)
                    for subset in subsets:
                        antecedent = subset
                        conf = RulesGenerator.__get_confidence(large_set, antecedent, counter)
                        if  conf >= minconf:
                            consequent = tuple(RulesGenerator.__tuples_difference(large_set, antecedent))
                            supp = float(counter[large_set]) / float(len(transactions))
                            rules.append((antecedent, consequent, supp, conf))
        return sorted(rules)

    @staticmethod
    def __get_all_subsets(large_set):
        subsets = []
        length = len(large_set)
        for i in range(1,length):
            subsets.extend(combinations(large_set, i))
        return subsets

    @staticmethod
    def __tuples_difference(large_set, subset):
        return (x for x in large_set if x not in subset)

    @staticmethod
    def __get_confidence(large_set, antecedent, counter):
        return float(counter[large_set]) / float(counter[antecedent])
