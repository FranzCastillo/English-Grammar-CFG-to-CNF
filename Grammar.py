import BNF


class Grammar(object):
    def __init__(self, terminals, variables, start, productions, terminalsDictionary=None, variablesDictionary=None):
        if terminalsDictionary is None and variablesDictionary is None:
            self.terminals, self.terminalsDictionary = BNF.tokenizeTerminals(terminals)
            self.variables, self.variablesDictionary = BNF.tokenizeVariables(variables, self.terminalsDictionary, productions)
            self.start = self.variablesDictionary[start]
            self.productions = BNF.tokenizeProductions(productions, self.variablesDictionary, self.terminalsDictionary)
        else:
            self.terminals = terminals
            self.terminalsDictionary = terminalsDictionary
            self.variables = variables
            self.variablesDictionary = variablesDictionary
            self.start = start
            self.productions = productions

    def __str__(self):
        string = ''
        string += 'Terminals: {}\n'.format(self.terminals)
        string += 'Variables: {}\n'.format(self.variables)
        string += 'Start: {}\n'.format(self.start)
        string += 'Productions:\n'
        for key in self.productions:
            string += '\t{}\t→\t{}\n'.format(key, self.productions[key])

        return string
