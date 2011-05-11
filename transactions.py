# -*- coding: utf-8 -*-

class TransactionsList:
    transactions = []
    nr_of_transactions = 0

    def __init__(self, filename):
        with open(filename) as file:
            for line in file:
                transaction = tuple(line.split())
                self.transactions.append(transaction)
                self.nr_of_transactions += 1

    def __iter__(self):
        return iter(self.transactions)
