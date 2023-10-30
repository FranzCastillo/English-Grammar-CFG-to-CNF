from graphviz import Digraph

"""
CYK algorithm for context-free grammars given in Chomsky normal form (CNF). Also the genration of the parse tree.
"""

# Class to represent a node in the parse tree
class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.leftChild = left
        self.rightChild = right

    def __str__(self):
        return self.value


# CYK Algorithm
def CYK(sentence, rules, start):
    # Example of sentence: [she, eats, a, cake, with, a, fork]
    # Example of rules: {VP: {(drinks,), (cuts,), (eats,), (Y, NP), (cooks,)}, NP: {(Z, N), (he,), (she,)}, V: {(drinks,), (cuts,), (eats,), (cooks,)}, N: {(meat,), (fork,), (cat,), (knife,), (soup,), (cake,), (beer,), (juice,), (dog,)}, DET: {(the,), (a,)}, S': {(0, VP)}, Y: {(V, _)}, Z: {(DET, _)}, 0: {(NP, _)}}
    # Example of start: S'
    
    # Create table and Parse Tree table
    n = len(sentence)
    table = [[set() for i in range(n - j)] for j in range(n)]
    parseTree = [[None for i in range(n - j)] for j in range(n)]
    
    # Fill the diagonal of the table
    for i in range(n):
        for rule in rules:
            for val in rules[rule]:
                if sentence[i] in val:
                    table[0][i].add(rule)
                    parseTree[0][i] = Node(rule.name, Node(sentence[i].name))
      
    
    for l in range(2, n+1):
        for s in range(n-l+1):
            for p in range(l-1):
                for rule in rules:
                    for val in rules[rule]:
                        if len(val) != 1:
                            v1, v2 = val
                            if v1 in table[p][s] and v2 in table[l-p-2][s+p+1]:
                                table[l-1][s].add(rule.name)
                                parseTree[l-1][s] = Node(rule.name, parseTree[p][s], parseTree[l-p-2][s+p+1])

    return parseTree[-1][0] if start in table[-1][0] else None, start in table[-1][0]

def graphTree(tree, filename):
    dot = Digraph(comment='Parse Tree', format='png')
    
    def addNode(node):
        
        dot.node(str(id(node)), str(node))
        
        if node:
            
            if node.leftChild:
                dot.edge(str(id(node)), str(id(node.leftChild)))
                addNode(node.leftChild)
            
            if node.rightChild:
                dot.edge(str(id(node)), str(id(node.rightChild)))
                addNode(node.rightChild)
                
    addNode(tree)
    
    dot.render('graphs/{}'.format(filename), view=True)
