# -*- coding: utf-8 -*-

import unittest

from apriori import Apriori


class TestAprioriGenerateSubsets(unittest.TestCase):

    def setUp(self):
        self.candidate_set = [(1, 2), (2, 9), (1, 4)]
        self.transaction = (1, 2, 3, 7, 8, 9)

    def testGenerateSubsets(self):
        result = Apriori._Apriori__generate_subsets(self.candidate_set, self.transaction)
        expected = [(1, 2), (2, 9)]
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

if __name__ == '__main__':
    unittest.main()
