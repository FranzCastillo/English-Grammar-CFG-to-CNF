import CNF
import CYK
from Grammar import Grammar


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
                 'meat', 'soup', 'fork', 'knife', 'oven', 'a', 'the'}
    variables = {'S', 'VP', 'PP', 'NP', 'V', 'P', 'N', 'DET', ' '}
    start = 'S'
    productions = {
        'S': {('NP', ' ', 'VP')},
        'VP': {('V', ' ', 'NP'), ('cooks',), ('drinks',), ('eats',), ('cuts',)},
        'PP': {('P', ' ', 'NP')},
        'NP': {('DET', ' ', 'N'), ('she',), ('he',)},
        'V': {('cooks',), ('drinks',), ('eats',), ('cuts',)},
        'P': {('with',), ('in',)},
        'N': {('cat',), ('dog',), ('beer',), ('cake',), ('juice',), ('meat',), ('soup',), ('fork',), ('knife',)},
        'DET': {('a',), ('the',)},
    }
    return Grammar(terminals, variables, start, productions)


def main():
    cfg = geeksforgeeks()
    # print(cfg)
    cnf = CNF.CNF(cfg).parseCFG()
    print(cnf)
    
    sentence = "baaba"
    
    cykp = pruebaCYK()
    cyk = CYK.CYK(sentence, cykp)
    acceptance = cyk.parseCYK()
    print('Sentence -' + sentence + '- acceptance: ' + str(acceptance)) 
    cyk.printTable()
    
if __name__ == "__main__":
    main()
