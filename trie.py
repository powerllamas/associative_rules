# -*- coding: utf-8 -*-

from itertools import combinations

min_supp_count = 1

class Node:
    def __init__(self, item, itemset, level, position, root):
        self.item = item
        self.itemset = itemset
        self.counter = 0
        self.branches = {}
        self.large = None
        self.suspected = None
        self.large_subsets_counter = 0
        self.level = level
        self.beginning_position = position
        self.first_pass = True
        self.root = root
        if level == 1:
            self.large = False
            self.suspected = True

    def increment(self, transaction, position):
        
        if position > self.beginning_position:
            self.first_pass = False

        #Check if this node was counted over all transactions. If it was - change the status
        if position == self.beginning_position and not self.first_pass:
            self.suspected = False
        finished = True
        
        if self.suspected:
            self.counter += 1
            if(self.large != True and self.counter >= min_supp_count):
                self.large = True
                self.check_supersets()
        if self.suspected != None and len(transaction) > 0:
            for i in range(len(transaction)):              
               branches_finished = self.branches.setdefault(transaction[i], Node(transaction[i], self.itemset+transaction[i], self.level + 1, position, self.root)).increment(transaction[i+1:], position)
               finished = finished and branches_finished and self.suspected == False
        return finished

    def get_node(self, key):
        branch = self
        for c in key:
            branch = branch.branches[c]
        return branch

    def print_node(self):           
        print "%s[%s]: [%d, %s, %s]" % (self.itemset, self.item, self.counter, self.suspected, self.large) 
        for branch in sorted(self.branches.values()):
            for i in range(self.level+1):
                print "\t",
            branch.print_node()

    def update_node_status(self):
        self.large = False
        self.suspected = True

    def check_supersets(self):
        for superset in self.get_immediate_supersets():
            subsets = superset.get_immediate_subsets()
            for subset in subsets:
                subset_node = self.root.get_node(subset)
                if subset_node.large != True:
                    break
            superset.update_node_status()

    def get_immediate_subsets(self):
        subsets = []
        length = len(self.itemset)
        subsets.extend(combinations(self.itemset, length - 1))
        return subsets

    def get_immediate_supersets(self):
        supersets = []
        for branch in sorted(self.root.branches.values()):
            if branch == self:
                return supersets
            supersets.append(branch.get_node(self.itemset))
        return supersets



class Root(Node):
    def __init__(self):
        self.counter = 0
        self.branches = {}
        self.large = True
        self.suspected = False
        self.position = 0;
        self.level = 0
        self.beginning_position = 0
        self.first_pass = False
        self.item = "*"
        self.itemset = ""
        self.root = self
    
    def get_large_sets(self):
        large_sets = {}
        return large_sets

    


tree = Root()
tr = ['A', 'B', 'C']
tree.increment(tr, 0)
a = tree.get_node('A')
ac = a.get_node('C')
tree.print_node()
