# Define all the metabolites that will exist
all_metabolites = ['ATP', 'ADP', 'Phosphates']

class Metabolites:
    def __init__(self, name):
        self.name = name
        self.amount = 0.0

class Reaction:
    def __init__(self, substrates, products, forward_rate, reverse_rate):
        self.substrates = substrates
        self.products = products
        self.rates = (forward_rate, reverse_rate)

class Solution():
    def __init__(self, volume):
        self.volume = volume
        self.cells = []
        self.proteins = {}
        self.metabolites = {}

        for m in all_metabolites:
            self.metabolites[m] = 0.0

    def addCell(self, volume):
        newCell = Cell(volume)
        newCell.solution = self
        self.cells.append(newCell)

class Cell(Solution):
    def addProtein(self, protein, amount):

        if protein not in self.proteins:
            self.proteins[protein] = Protein(protein, self)
        self.proteins[protein].amount += amount

    def update(self):
        print 'Cell has %d proteins' % len(self.proteins.keys())

        for p in self.proteins.values():
            p.update()

class Protein():
    def __init__(self, sequence, solution):
        self.sequence = sequence
        self.solution = solution
        self.amount = 0.0
        self.rate = 1.0
        self.functions = []
        self.interpretSequence()

    def interpretSequence(self):
        temp = self.sequence.split('-')

        if len(temp) > 1:
            self.setMetabolites([temp[1]])
        if temp[0] == 'transporter':
            self.functions.append(self.transport)

    def setMetabolites(self, substrates, products=[]):
        self.substrates = []
        self.products = []

        for s in substrates:
            self.substrates.append(s)

        for p in products:
            self.products.append(p)

    def transport(self):
        d1 = self.solution.metabolites[self.substrates[0]] / self.solution.volume
        d2 = self.solution.solution.metabolites[self.substrates[0]] / self.solution.solution.volume
        d3 = (d2 - d1) * self.rate * self.amount

        print 'transporting %s' % self.substrates
        print self.solution.metabolites[self.substrates[0]], '>',
        print self.solution.solution.metabolites[self.substrates[0]] , d3

        self.solution.metabolites[self.substrates[0]] += d3
        self.solution.solution.metabolites[self.substrates[0]] -= d3

    def update(self):
        for function in self.functions:
            function()

ATPase = Reaction(['ATP'], ['ADP', 'Phosphates'], 0.1, 0.0001)
all_reactions = [ATPase]
