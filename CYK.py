from graphviz import Digraph
import os
os.environ["PATH"] += os.pathsep + 'D:/Programs/Graphviz/bin'

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
    # Example of sentence: [a, _, cat, _, eats, _, a, _, cake, _, with, _, a, _, fork, _, in, _, the, _, oven]
    # Example of rules:
    # <VP>	->	{(Z, NP), (0, PP), (cooks,), (cuts,), (drinks,), (eats,)}
    # <PP>	->	{(1, NP)}
    # <NP>	->	{(he,), (she,), (2, N)}
    # <V>	->	{(cooks,), (cuts,), (drinks,), (eats,)}
    # <P>	->	{(with,), (in,)}
    # <N>	->	{(meat,), (knife,), (beer,), (juice,), (dog,), (fork,), (soup,), (cake,), (cat,)}
    # <DET>	->	{(a,), (the,)}
    # <S'>	->	{(3, VP)}
    # <O>	->	{(_,)}
    # <Z>	->	{(V, O)}
    # <0>	->	{(VP, O)}
    # <1>	->	{(P, O)}
    # <2>	->	{(DET, O)}
    # <3>	->	{(NP, O)}
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
      
    
    # Fill the rest of the table
    for l in range(2, n+1):
        for s in range(n-l+1):
            for p in range(1, l):
                for rule in rules:
                    for val in rules[rule]:
                        if len(val) == 2:
                            v1, v2 = val
                            if v1 in table[p-1][s] and v2 in table[l-p-1][s+p]:
                                table[l-1][s].add(rule)
                                parseTree[l-1][s] = Node(rule.name, parseTree[p-1][s], parseTree[l-p-1][s+p])

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
    
    dot.render('graphs/{}'.format(filename), view=False, cleanup=True)
