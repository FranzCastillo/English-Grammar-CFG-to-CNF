import CNF
import CYK
from Grammar import Grammar
from GrammarAnalyzer import GrammarAnalyzer as GA


def pfafner():
    terminals = ['a', 'b']
    variables = ['S', 'A', 'B', 'C', 'D', 'E']
    start = 'S'
    productions = {
        'S': {('A', 'C', 'D')},
        'A': {('a', )},
        'B': {('ε',)},
        'C': {('E', 'D'), ('ε',)},
        'D': {('B', 'C'), ('ε',)},
        'E': {('b',)},
    }
    return Grammar(terminals, variables, start, productions)


def geeksforgeeks():
    # https://www.geeksforgeeks.org/converting-context-free-grammar-chomsky-normal-form/
    terminals = {'a', 'b', }
    variables = {'S', 'A', 'B', }
    start = 'S'
    productions = {
        'S': {('A', 'S', 'B')},
        'A': {('a', 'A', 'S'), ('a',), ('ε',)},
        'B': {('S', 'b', 'S'), ('A',), ('b', 'b')},
    }
    return Grammar(terminals, variables, start, productions)


def proyect():
    terminals = {'cooks', 'drinks', 'eats', 'cuts', 'she', 'he', 'with', 'in', 'cat', 'dog', 'beer', 'cake', 'juice',
                 'meat', 'soup', 'fork', 'knife', 'oven', 'a', 'the', '_'}
    variables = {'S', 'VP', 'PP', 'NP', 'V', 'P', 'N', 'DET'}
    start = 'S'
    productions = {
        'S': {('NP', '_', 'VP')},
        'VP': {('VP', '_', 'PP'), ('V', '_', 'NP'), ('cooks',), ('drinks',), ('eats',), ('cuts',)},
        'PP': {('P', '_', 'NP')},
        'NP': {('DET', '_', 'N'), ('she',), ('he',)},
        'V': {('cooks',), ('drinks',), ('eats',), ('cuts',)},
        'P': {('with',), ('in',)},
        'N': {('cat',), ('dog',), ('beer',), ('cake',), ('juice',), ('meat',), ('soup',), ('fork',), ('knife',)},
        'DET': {('a',), ('the',)},
    }
    return Grammar(terminals, variables, start, productions)


def outputSeparator():
    print('\n----------------------------------------------------------------\n')

def main():
    print('Conversion to Chomsky Normal Form (CNF):\n')
    cfg = proyect()
    cnf = CNF.CNF(cfg).parseCFG()
    print(cnf)
    
    outputSeparator()
    
    print('Sentence analysis:\n')
    sentence = 'she eats a cake'
    print('Sentence: {}\n'.format(sentence))
    analyzer = GA(sentence)
    for token in analyzer.tokens:
        isInGrammarTerminals = token in cnf.terminals
        string = '{}: {}'.format(token, isInGrammarTerminals)
        print(string)
        
    outputSeparator()
    
    print('CYK algorithm:\n')
    cyk = CYK.CYK(analyzer.tokens, cnf.productions, cnf.start)
    acceptance = cyk[1]
    print('The sentence is accepted by the grammar: {}\n'.format(acceptance))
    tree = cyk[0]
    CYK.graphTree(tree, 'parseTree')
    print('Parse tree generated in graphs/parseTree.png\n')
    
if __name__ == "__main__":
    main()
