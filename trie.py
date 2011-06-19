# -*- coding: utf-8 -*-

from itertools import combinations

class Node(object):
    __slots__ = ['item', 'itemset', 'counter', 'branches', 'suspected', 'large', 'size_changed', 'level', 'first_pass', 'root', 'beginning_position', 'counted_transactions', 'finished']

    def __init__(self, item, itemset, level, root):
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
        self.counted_transactions = 0
        self.finished = False
        self.beginning_position = None

          
    def increment(self, transaction):
        if not (self.finished and self.large == False):
            if self.suspected:
                self.counter += 1
            if self.large or self.root.partial:
                sorted_trans =  sorted(transaction)
                for i, item in enumerate (sorted_trans):              
                    node = self.branches.get(item)
                    if node != None:
                        node.increment(sorted_trans[i+1:])


    def update_states(self, trans_in_last_part):
        if not (self.finished and self.large == False):
            if self.suspected == True:
                self.counted_transactions += trans_in_last_part
            if self.counted_transactions >= self.root.transactions_no:
                self.suspected = False
                
            self.finished = self.suspected == False

            for key in sorted(self.branches):
                supersets_finished = self.branches[key].update_states(trans_in_last_part)
                self.finished = self.finished and supersets_finished

            if self.is_large():
                self.large = True
                new_supersets = self.check_subsets_of_supersets()
                self.finished = self.finished and not new_supersets
            elif self != self.root:
                self.large = False

        return self.finished

        
    def check_subsets_of_supersets(self):
        some = False
        for key in sorted(self.root.L1):                        
            if key[0] > self.item:
                new_node, all_subsets_large = self.get_or_set_node(key)
                some = some or all_subsets_large
        return some
            

    def get_or_set_node(self, key):
        new_node_added = False
        branch = self
        for c in sorted(key): 
            existing_branch = branch.branches.get(c)
            if existing_branch == None:
                newitemset = branch.itemset + (c,)
                new_node = Node(c, newitemset, branch.level + 1, self.root)
                all_subsets_large = new_node.check_subsets()
                if all_subsets_large:
                    branch = branch.branches.setdefault(c, new_node)
                new_node_added = all_subsets_large
                return branch, new_node_added
            else:
                branch = existing_branch
        return branch, new_node_added

    def check_subsets(self):
        subsets = self.get_immediate_subsets()
        all_big = True
        for subset in subsets:
            if subset == ():
                break
            subset_node = self.root.get_node(subset)
            all_big = all_big and subset_node!= None and subset_node.is_large()
            if not all_big:
                break
        if all_big:
            self.start_counting()
        return all_big


    def get_immediate_subsets(self):
        length = len(self.itemset)
        subsets = combinations(self.itemset, length - 1)
        return sorted(subsets)

    def start_counting(self):
        self.large = False
        self.suspected = True
        
    def get_node(self, key):
        branch = self
        for c in key: 
            branch = branch.branches.get(c)
            if branch == None:
                return branch
        return branch


    def is_large(self):
        return self.counter >= self.get_minsup_count()

    def get_minsup_count(self):
        if self.root.partial:
            minsup_count = self.root.minsup * self.counted_transactions
        else:
            minsup_count = self.root.minsup * self.root.transactions_no
        return minsup_count

    
    def get_large_sets(self, large_sets):

        if self.is_large():
            if self != self.root:
                large_sets.setdefault(len(self.itemset), []).append(self.itemset)
            for key in sorted(self.branches):
                self.branches[key].get_large_sets(large_sets)
        return large_sets
    
    
    def print_node(self, large_only = False, suspected_only = False, level = 0):           
        if (not large_only or self.large) and (not suspected_only or self.suspected) and (self.level <= level or level == 0):
            print "%s %s[%d, %d, %s, %s]" % (self.item, self.itemset, self.counter, self.counted_transactions, self.suspected, self.large) 
            for key in sorted(self.branches.keys()):
                if (not large_only or self.branches[key].large) and (self.branches[key].level <= level or level == 0) and (not suspected_only or self.branches[key].suspected):
                    for i in range(self.level+1):
                        print "\t",
                self.branches[key].print_node_pro(large_only, suspected_only, level)

    def print_node_pro(self, large_only, suspected_only, level):
        self.print_node(large_only, suspected_only, level)

    def __str__(self):
        return "{self.itemset}, L:{self.large}, S:{self.suspected}, C:{self.counter}".format(**locals())

class Root(Node):
    __slots__ = ['minsup', 'transactions_no', 'L1', 'partial']
    def __init__(self, minsup, transactions_no, L1, partial):
        super(Root, self).__init__(item="", itemset=tuple(), level=0, root=None)

        self.root = self
        self.large = False
        self.counter = transactions_no
        self.counted_transactions =  transactions_no
        self.transactions_no = transactions_no
        self.suspected = True
        self.beginning_position = 0
        self.minsup = minsup
        self.finished = False
        self.L1 = L1
        self.partial = partial
        
        for key in sorted(L1):
            new_node = Node(item=key[0], itemset=key, level = 1, root = self)
            new_node.counter = L1[key]
            new_node.suspected = False
            new_node.large = True
            new_node.counted_transactions = transactions_no
            self.branches.setdefault(key[0], new_node)
            

#__file__= '__main__'

#if __file__ == '__main__':
    #L1 = {('A',): 4, ('B',):4, ('C',): 6}
    #tree = Root(0.4, 10, L1, 0)
    #tr = ('A', 'B')
    #tr2 = ('C', 'A', 'B')
    #tr3 = ('C')

    #tree.print_node()
    #tree.update_states(0)
    
    #tree.print_node()
    
    #tree.increment(tr)
    #tree.print_node()

    #tree.update_states(1)
    #tree.print_node()

    #tree.increment(tr)
    #tree.increment(tr)
    #tree.increment(tr)
    #tree.print_node()

    #tree.update_states(2)
    #tree.print_node()

    #tree.update_states(0)
    #tree.print_node()

    #tree.increment(tr2)
    #tree.increment(tr2)
    #tree.increment(tr2)
    #tree.print_node()

    #tree.update_states(3)
    #tree.print_node()

    #tree.increment(tr2)
    #tree.increment(tr2)
    #tree.increment(tr2)
    #tree.print_node()

    #tree.update_states(3)
    #tree.print_node()

   #tree.update_states(0, 0)
   #tree.print_node()
   
   #tree.increment(tr2, 0)
   #tree.increment(tr2, 0)
   #tree.increment(tr2, 0)
   #tree.print_node()

   #tree.update_states(0, 3)
   #tree.print_node()

   #tree.increment(tr2, 0)
   #tree.increment(tr2, 0)
   #tree.increment(tr2, 0)
   #tree.print_node()

   #tree.update_states(1, 3)
   #tree.print_node()
