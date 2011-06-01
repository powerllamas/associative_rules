min_supp = 0.7

class Node:
    def __init__(self, level):
        self.counter = 0
        self.branches = {}
        self.large = None
        self.suspected = None
        self.position = 0;
        self.large_subsets_counter = 0
        self.level = level
        if level == 1:
            self.large = False
            self.suspected = True
        
    def increment(self, transaction, count_subset, position):
        size_changed = False
        if self.suspected:
            if(self.counter == 0):
                self.position = position
            self.counter += 1
            if(self.large != True and self.counter >= min_supp):
                self.large = True
                size_changed = True
        if self.suspected != None and len(transaction) > 0:
            for i in range(len(transaction)):
                self.branches.setdefault(transaction[i], Node(self.level + 1)).increment(transaction[i+1:], size_changed, position)
        elif self.suspected == None and count_subset:
            #TODO: sprawdzanie czy wszystkie bezpośrednie podziory są częste
            #Zbiór n-elementowy ma n bezpośrednich podzbiorów (podzbiorów n-1 elementowych)
            #dlatego utrzymujemy licznik częstych bezpośrednich podzbiorów każdego zbioru
            self.large_subsets_counter += 1
            if self.large_subsets_counter == self.level:
                self.large = False
                self.suspected = True

    def print_node(self):
        for key in self.branches:
            for i in range(self.level):
                print "\t",
            print "%s: [%d, %s, %s]" % (key, self.branches[key].counter, self.branches[key].suspected, self.branches[key].large)
            self.branches[key].print_node()
            
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
