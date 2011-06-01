#TODO: wywo³ywanie update_node_status() gdy wszystkie bezpoœrednie podzbiory s¹ czêste

min_supp_count = 1

class Node:
    def __init__(self, item, level):
        self.item = item
        self.counter = 0
        self.branches = {}
        self.large = None
        self.suspected = None
        self.position = 0;
        self.large_subsets_counter = 0
        self.level = level
        self.size_changed = False
        if level == 1:
            self.large = False
            self.suspected = True
        
    def increment(self, transaction, position):
        if self.suspected:
            if(self.counter == 0):
                self.position = position
            self.counter += 1
            if(self.large != True and self.counter >= min_supp_count):
                self.large = True
                self.size_changed = True
        if self.suspected != None and len(transaction) > 0:
            for i in range(len(transaction)):
                self.branches.setdefault(transaction[i], Node(transaction[i], self.level + 1)).increment(transaction[i+1:], position)

    def print_node(self):
        for key in self.branches:
            for i in range(self.level):
                print "\t",
            print "%s: [%d, %s, %s]" % (key, self.branches[key].counter, self.branches[key].suspected, self.branches[key].large)
            self.branches[key].print_node()

    def update_node_status():
        self.large = False
        self.suspected = True
        
            
class Root(Node):
    def __init__(self):
        self.counter = 0
        self.branches = {}
        self.large = True
        self.suspected = False
        self.position = 0;
        self.level = 0

            

tree = Root()
tr = ['A', 'B', 'C']
