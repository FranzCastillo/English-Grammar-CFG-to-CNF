class Grammar(object):
    def __init__(self, terminals, variables, start, productions):
        self.terminals = terminals
        self.variables = variables
        self.start = start
        self.productions = productions

    def __str__(self):
        temp = "Terminals: {}\nVariables: {}\nStart: {}\nProductions:\n".format(self.terminals, self.variables, self.start)
        for variable in self.productions:
            temp += "\t{} -> {}\n".format(variable, self.productions[variable])
        return temp
