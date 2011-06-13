<<<<<<< HEAD
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
##        if level == 1:
##            self.large = False
##            self.suspected = True
##            self.beginning_position = 0


          
    def increment(self, transaction, position):
        if not (self.finished and self.large == False):
            if self.suspected:
                self.counter += 1
            if self.large:
                if self.counter > self.root.transactions_no:
                    print "!!!!!!!!!!!!!!!"
                    self.print_node()
                    print "!!!!!!!!!!!!!!!"
                for i in range(len(transaction)):              
                    node = self.branches.get(transaction[i])
                    if node != None:
                        node.increment(transaction[i+1:], position)


    def update_states(self, position, trans_in_last_part):

        if not (self.finished and self.large == False) and self.suspected != None:
            if self.suspected == True:
                self.counted_transactions += trans_in_last_part
            if self.counted_transactions >= self.root.transactions_no:
                self.suspected = False
                
            self.finished = self.suspected == False

            for key in sorted(self.branches):
                supersets_finished = self.branches[key].update_states(position, trans_in_last_part)
                self.finished = self.finished and supersets_finished

            if self.is_large():
                if self.large == False:
                    self.large = True
                    new_supersets = self.check_subsets_of_supersets()
                    self.finished = self.finished and not new_supersets
            elif self != self.root:
                self.large = False

        return self.finished


    def check_subsets_of_supersets(self):
        some = False
        for key in sorted(self.root.L1):
            #print "key: %s" % (key,)
            if len(self.itemset) > 0 and key == self.itemset[0]:
                for my_key in sorted(self.root.L1):
                    if my_key > self.item:
                        new_node, all_subsets_large = self.get_or_set_node(my_key)
                        some = some or all_subsets_large
                break
            new_node, all_subsets_large = self.root.get_or_set_node(key + self.itemset)
            some = some or all_subsets_large
        return some
            

    def get_or_set_node(self, key):
        new_node_added = False
        branch = self
        for c in sorted(key): 
            existing_branch = branch.branches.get(c)
            if existing_branch == None:
                newitemset = branch.itemset + (c,)
                #print "%s + %s = %s" % (branch.itemset , (c,), newitemset)
                new_node = Node(c, newitemset, branch.level + 1, self.root)
                all_subsets_large = new_node.check_subsets()
                #print "\tsuperset: %s, %s" % (new_node.itemset, all_subsets_large)
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
            #print "subsets: %s" % (subset,)
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
        return subsets

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
        #minsup_count = self.root.minsup * self.counted_transactions
        minsup_count = self.root.minsup * self.root.transactions_no
        #print "%d, minsup: %d" % (self.counted_transactions, minsup_count)
        return minsup_count

    
    def get_large_sets(self, large_sets):
        if self.large:
            if self != self.root:
                large_sets.setdefault(len(self.itemset), []).append(self.itemset)
            for node in self.branches.values():
                node.get_large_sets(large_sets)
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

class Root(Node):
    __slots__ = ['minsup', 'transactions_no', 'L1']
    def __init__(self, minsup, transactions_no, L1):
        super(Root, self).__init__(item="*", itemset=tuple(), level=0, root=None)

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

##__file__= '__main__'
##
##if __file__ == '__main__':
##    L1 = ('A', 'B', 'C', 'D', 'E', 'F')
##    tree = Root(0.7, 3, L1)
##    tr = ('A', 'B', 'C')
##    tr2 = ('D', 'E')
##    tr3 = ('A', 'B', 'C', 'D', 'E', 'F')
##
####    tree.increment(tr, 0)
####    tree.print_node()
####
####    tree.update_states(1, 1)
####    tree.print_node()
####
####    tree.increment(tr3, 1)
####    tree.increment(tr, 1)
####    tree.print_node()
####
####    tree.update_states(2, 2)
####    tree.print_node()
####    
####    tree.update_states(0, 1)
####    tree.print_node()
##
##    tree.update_states(0, 0)
##    tree.print_node()
##    
##    tree.increment(tr, 0)
##    tree.increment(tr3, 0)
##    tree.increment(tr, 0)
##    tree.print_node()
##
##    tree.update_states(0, 3)
##    tree.print_node()
##
##    tree.increment(tr, 1)
##    tree.increment(tr3, 1)
##    tree.increment(tr, 1)
##    tree.print_node()
##
##    tree.update_states(1, 3)
##    tree.print_node()
