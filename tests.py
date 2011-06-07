# -*- coding: utf-8 -*-

import unittest

from apriori import Apriori
from rules import RulesGenerator

class TestAprioriGenerateSubsets(unittest.TestCase):

    def setUp(self):
        self.candidate_set_2 = [(1, 2), (2, 9), (1, 4)]
        self.candidate_set_3 = [(1, 2, 9), (2, 3, 9), (1, 4, 9)]
        self.candidate_set_4 = [(1, 2, 3, 7), (2, 3, 8, 9), (1, 2, 3, 4)]
        self.transaction = (1, 2, 3, 7, 8, 9)

    def testGenerateSubsets2(self):
        result = Apriori._Apriori__generate_subsets(self.candidate_set_2, self.transaction)
        expected = [(1, 2), (2, 9)]
        self.assertEqual(result, expected)

    def testGenerateSubsets3(self):
        result = Apriori._Apriori__generate_subsets(self.candidate_set_3, self.transaction)
        expected = [(1, 2, 9), (2, 3, 9)]
        self.assertEqual(result, expected)

    def testGenerateSubsets4(self):
        result = Apriori._Apriori__generate_subsets(self.candidate_set_4, self.transaction)
        expected = [(1, 2, 3, 7), (2, 3, 8, 9)]
        self.assertEqual(result, expected)

class TestAprioriGen(unittest.TestCase):

    def setUp(self):
        self.large_set_k1 = [(1, ), (2, ), (3, )]
        self.large_set_k2 = [(1, 2), (2, 3), (3, 4), (3, 5), (4, 5)]
        self.large_set_k3 = [(3, 4, 5), (3, 4, 7), (3, 5, 7), (4, 5, 6), (4, 5, 7), (4, 6, 7)]

    def testAprioriGenK1(self):
        result = Apriori._Apriori__apriori_gen(self.large_set_k1)
        expected = [(1, 2), (1, 3), (2, 3)]
        self.assertEqual(result, expected)  

    def testAprioriGenK2(self):
        result = Apriori._Apriori__apriori_gen(self.large_set_k2)
        expected = [(3, 4, 5)]
        self.assertEqual(result, expected)

    def testAprioriGenK3(self):
        result = Apriori._Apriori__apriori_gen(self.large_set_k3)
        expected = [(3, 4, 5, 7)]
        self.assertEqual(result, expected)
        
class TestRules(unittest.TestCase):

    def setUp(self):
        self.large_sets = {1 : [(1, ), (2, ), (3, ), (4, )],  2 : [(1, 2), (2, 3), (2, 4), (3, 4)], 3 :  [(2, 3, 4)]}
        self.transactions = [(1, 2), (2, 3, 4), (1,), (1, 2, 3), (2, 3, 4)]
        self.minconf = 0.7
        self.counter = {
                (1,): 3,
                (2,): 4,
                (3,): 3,
                (4,): 2,
                (1, 2): 2,
                (1, 3): 1,
                (1, 4): 0,
                (2, 3): 3,
                (2, 4): 2,
                (3, 4): 2,
                (1, 2, 3): 1,
                (1, 2, 4): 0,
                (1, 3, 4): 0,
                (2, 3, 4): 1,
            }
    
    def testRules(self):
        extract = lambda x: (x[0], tuple(x[1]))
        result = RulesGenerator.generate_rules(self.large_sets, self.minconf, self.counter, self.transactions)
        result = [ extract(x) for x in result ]
        expected = [
                ((2,), (3,)), #conf=0.75
                ((3,), (2,)), #conf=1.0
                ((4,), (2,)), #conf=1.0
                ((4,), (3,)), #conf=1.0
                #((4,), (2, 3)), #conf=0.5
                #((2, 4), (3,)), #conf=0.5
                #((3, 4), (2,)), #conf=0.5
            ]
        self.assertEqual(result, expected)
        
class TestRulesGetAllSubsets(unittest.TestCase):

    def setUp(self):
        self.set = set([1, 2, 3])
    
    def testGetAllSubsets(self):
        result = RulesGenerator._RulesGenerator__get_all_subsets(self.set)
        expected = [(1,), (2,), (3,), (1, 2), (2, 3), (1, 3)]
        self.assertEqual(sorted(result), sorted(expected))

if __name__ == '__main__':
    unittest.main()
