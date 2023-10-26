from Grammar import Grammar
import CNF


def main():
    # https://www.geeksforgeeks.org/converting-context-free-grammar-chomsky-normal-form/
    terminals = ['a', 'b']
    variables = ['S', 'A', 'B']
    start = 'S'
    productions = {
        'S': ['ASB'],
        'A': ['aAS', 'a', ''],
        'B': ['SbS', 'A', 'bb'],
    }
    # terminals = ['a', 'b', 'e']
    # variables = ['S']
    # start = 'S'
    # productions = {
    #     'S': ['aSa', 'bSb', 'a', 'b', 'e',]
    # }

    cfg = Grammar(terminals, variables, start, productions)
    print(cfg)
    cnf = CNF.CNF(cfg).parseCFG()
    print(cnf)


if __name__ == "__main__":
    main()
