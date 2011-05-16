# -*- coding: utf-8 -*-


class TransactionsDataSet:
    transactions = []

    def __init__(self, filename):
        with open(filename) as file:
            for line in file:
                transaction = (int(x) for x in line.split())
                self.transactions.append(transaction)

    def __iter__(self):
        return iter(self.transactions)

    def __len__(self):
        return len(self.transactions)
