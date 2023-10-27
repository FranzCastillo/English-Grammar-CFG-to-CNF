import CNF
import CYK
from Grammar import Grammar


def pfafner():
    terminals = ['a', 'b']
    variables = ['S', 'A', 'B', 'C', 'D', 'E']
    start = 'S'
    productions = {
        'S': {'ACD'},
        'A': {'a'},
        'B': {''},
        'C': {'ED', ''},
        'D': {'BC', ''},
        'E': {'b'},
    }
    return Grammar(terminals, variables, start, productions)


def geeksforgeeks():
    # https://www.geeksforgeeks.org/converting-context-free-grammar-chomsky-normal-form/
    terminals = ['a', 'b', ]
    variables = ['S', 'A', 'B', ]
    start = 'S'
    productions = {
        'S': {'ASB'},
        'A': {'aAS', 'a', ''},
        'B': {'SbS', 'A', 'bb'},
    }
    return Grammar(terminals, variables, start, productions)


def pruebaCYK():
    terminals = ['a', 'b']
    variables = ['S', 'A', 'B', 'C']
    start = 'S'
    productions = {
        'S': {'AB', 'BC'},
        'A': {'BA', 'a'},
        'B': {'CC', 'b'},
        'C': {'AB', 'a'}
    }
    return Grammar(terminals, variables, start, productions)
     
# def proyect():
#     # BNF would work better T.T
#     productions = {
#         'S': {'N', 'V'},  # S -> NP VP
#         'V': {'V', 'P', 'B', 'N', 'c', 'd', 'e', 'u'},  # VP → VP PP
#
#     }
# 
#
#     pass


def main():
    cfg = geeksforgeeks()
    print(cfg)
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
