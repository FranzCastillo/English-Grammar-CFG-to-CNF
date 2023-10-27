"""
Class CYK. This class implements the CYK algorithm for context-free grammars given in Chomsky normal form (CNF).
"""

class CYK:
    def __init__(self, sentence, cnf):
        self.sentence = sentence
        self.cnf = cnf
        self.start = self.cnf.start
        self.terminals = self.cnf.terminals
        self.variables = self.cnf.variables
        self.rules = self.cnf.productions
        self.table = []
        
    def dissectSentence(self):
        if ' ' in self.sentence:
            return self.sentence.split()
        else:
            return list(self.sentence)

        
    def parseCYK(self):
        w = self.dissectSentence()
        n = len(w)
        m = len(self.variables)
        
        # Step 1: Initialize the table
        P = [[set() for j in range(n-i)] for i in range(n)]
        
        # Step 2: Fill base of the table
        for i, letter in enumerate(self.sentence):
            for variable, production in self.rules.items():
                if letter in production:
                    P[0][i].add(variable)
        
        # Step 3: Fill the rest of the table
        for i in range(1, n):
            for j in range(n-i):
                for k in range(i):
                    for variable, production in self.rules.items():
                        for prod in production:
                            if len(prod) == 2:
                                B, C = prod
                                if B in P[k][j] and C in P[i-k-1][j+k+1]:
                                    P[i][j].add(variable)
        
        self.table = P
        
        # Step 4: Check if start symbol is in the top right cell of the table
        return self.start in P[-1][0]
    
    def printTable(self):
        for row in self.table:
            print(' '.join([str(cell) for cell in row]))
        