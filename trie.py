# -*- coding: utf-8 -*-

from itertools import combinations

class Node(object):
    __slots__ = ['item', 'itemset', 'counter', 'branches', 'suspected', 'large', 'size_changed', 'level', 'first_pass', 'root', 'beginning_position', ]

    def __init__(self, item, itemset, level, root, position):
        self.item = item
        self.itemset = itemset
        self.counter = 0
        self.branches = {}
        self.suspected = None
        self.large = None
        self.size_changed = False
        self.level = level
        self.first_pass = True
        self.root = root
        if level == 1:
            self.large = False
            self.suspected = True
            self.beginning_position = 0

    def increment(self, transaction, position):
             
        if self.suspected:
            self.counter += 1

        #transaction = tuple(sorted(list(transaction_tuple)))
  
        if self.suspected != None and len(transaction) > 0 and self.large:
            for i in range(len(transaction)):              
               if self.branches.get(transaction[i]) == None:                   
                   newitemset = list()
                   newitemset.extend(self.itemset)
                   newitemset.append(transaction[i])
                   default_new_node = Node(transaction[i], tuple(newitemset), self.level + 1, self.root, position)
                   if default_new_node.check_subsets(position):
                       self.branches.setdefault(transaction[i], default_new_node).increment(transaction[i+1:], position)
               else:     
                   self.branches.get(transaction[i]).increment(transaction[i+1:], position)


    def get_node(self, key):
        branch = self
        for c in key: 
            branch = branch.branches.get(c)
            if branch == None:
                return branch
        return branch

    def print_node_pro(self, large_only, suspected_only, level):           
        if (not large_only or self.large) and (not suspected_only or self.suspected) and (self.level <= level or level == 0):
            print "%s %s [%d, %s, %s]" % (self.item, self.itemset, self.counter, self.suspected, self.large) 
            for key in sorted(self.branches.keys()):
                if (not large_only or self.branches[key].large) and (self.branches[key].level <= level or level == 0) and (not suspected_only or self.branches[key].suspected):
                    for i in range(self.level+1):
                        print "\t",
                self.branches[key].print_node_pro(large_only, suspected_only, level)

    def print_node(self):
        self.print_node_pro(False, False, 0)

    def start_counting(self, position):
        self.large = False
        self.suspected = True
        self.beginning_position = position

    def check_supersets(self, position):
        for superset in self.get_immediate_supersets():
            superset.check_subsets(position)

    def check_subsets(self, position):
        subsets = self.get_immediate_subsets()
        all = True
        for subset in subsets:
            subset_node = self.root.get_node(subset)
            all = all and subset_node != None and subset_node.large
            if not all:
                break
        if all:
            self.start_counting(position)
        return all

    def get_immediate_subsets(self):
        subsets = []
        length = len(self.itemset)
        subsets.extend(combinations(self.itemset, length - 1))
        return subsets

    def get_immediate_supersets(self):
        supersets = []
        for key in sorted(self.root.branches):
            if self.root.branches[key] == self:
                for superset in self.branches.values():
                    supersets.append(superset)
                return supersets            
            superset = self.root.branches[key].get_node(self.itemset)
            if superset != None:
                supersets.extend(superset.branches.values())
            
        return supersets

    def update_child_states(self, position):

        if self.suspected == True:
            if self.beginning_position == position:
                self.suspected = False

        finished = self.suspected == False
        
        if self.large:
            for node in self.branches.values():
                supersets_finished = node.update_child_states(position)
                finished = finished and supersets_finished
                
        if not self.large and self.counter >= self.root.minsup_count:
            self.large = True

        return finished

    
    def get_large_sets(self, large_sets):
        if(self.large):
            if(self != self.root):
                large_sets.setdefault(len(self.itemset), []).append(self.itemset)
            for node in self.branches.values():
                node.get_large_sets(large_sets)
        return large_sets
    
    
class Root(Node):
    def __init__(self, minsup_count):
        super(Root, self).__init__(item="*", itemset=[], level=0, root=None, position = 0)

        self.root = self
        self.large = True
        self.suspected = False
        self.beginning_position = 0
        self.first_pass = False
        self.minsup_count = minsup_count

if __file__ == '__main__':
    tree = Root(2)
    tr = ('A', 'B', 'C')
    tr2 = ('D', 'E')
    tr3 = ('B', 'D', 'C', 'A', 'E', 'F')

    tree.increment(tr2, 0)
    tree.print_node()

    tree.update_child_states()
    tree.print_node()

    tree.increment(tr3, 1)
    tree.print_node()

    tree.update_child_states(0)

    tree.increment(tr, 0)
    tree.print_node()

    tree.increment(tr2, 0)
    tree.print_node()

    tree.increment(tr3, 0)
    tree.print_node()

    finished = tree.update_child_states(1)
    tree.print_node()
    print finished

    tree.increment(tr, 1)
    tree.print_node()

    tree.increment(tr2, 1)
    tree.print_node()

    tree.increment(tr3, 1)
    tree.print_node()

    finished = tree.update_child_states(2)
    tree.print_node()
    print finished

