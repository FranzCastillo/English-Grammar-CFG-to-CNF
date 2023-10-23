from Grammar import Grammar


class CNF:
    def __init__(self, cfg):
        self.cfg = cfg
        self.terminals = cfg.terminals
        self.variables = cfg.variables
        self.start = cfg.start
        self.productions = cfg.productions

    def _addProduction(self, variable, production):
        """
        Adds a new production to the CNF grammar
        :param variable: The variable to add the production to
        :param production: The production to add
        :return: None
        """
        if variable not in self.variables:
            self.variables.append(variable)
        if variable not in self.productions:
            self.productions[variable] = []
        self.productions[variable].append(production)

    def _eliminateStartSymbolFromRHS(self):
        """
        Eliminates the start symbol from the RHS of the productions
        :return: None
        """
        newStart = self.start + "'"  # S0
        self._addProduction(newStart, self.start)
        self.start = newStart

    def _binaryProductions(self):
        pass

    def _eliminateEpsilonProductions(self):
        pass

    def _eliminateUnitProductions(self):
        pass

    def _eliminateUselessProductions(self):
        pass

    def _eliminateUselessSymbols(self):
        pass

    def parseCFG(self):
        # Step 1: Eliminate the start symbol from the RHS of the productions
        self._eliminateStartSymbolFromRHS()
        # Step 2: Binary productions
        self._binaryProductions()
        # Step 3: Eliminate epsilon productions
        self._eliminateEpsilonProductions()
        # Step 4: Eliminate unit productions
        self._eliminateUnitProductions()
        # Step 5: Eliminate useless productions
        self._eliminateUselessProductions()
        # Step 6: Eliminate useless symbols
        self._eliminateUselessSymbols()

        return Grammar(self.terminals, self.variables, self.start, self.productions)
