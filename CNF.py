from Grammar import Grammar


class CNF:
    def __init__(self, cfg):
        self.cfg = cfg
        self.terminals = cfg.terminals
        self.variables = cfg.variables
        self.start = cfg.start
        self.productions = cfg.productions
        del self.cfg

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

    def _getVariablesWithEpsilonProductions(self):
        """
        Gets the variables with epsilon productions
        :return:
        """
        return [variable for variable, productions in self.productions.items() if '' in productions]

    def _eliminateEpsilonProductions(self):
        """
        Eliminates epsilon productions
        :return: None
        """
        variablesWithEpsilon = self._getVariablesWithEpsilonProductions()
        while len(variablesWithEpsilon) > 0:
            for variableWithEpsilon in variablesWithEpsilon:
                for variable in self.productions:
                    for production in self.productions[variable]:
                        if variableWithEpsilon in production:
                            self.productions[variable].append(production.replace(variableWithEpsilon, ''))
                self.productions[variableWithEpsilon].remove('')
            variablesWithEpsilon = self._getVariablesWithEpsilonProductions()


    def _eliminateUnitProductions(self):
        pass

    def _eliminateUselessProductions(self):
        pass

    def _separateTerminalsFromVariables(self):
        pass

    def _eliminateProductionsWithMoreThan2Variables(self):
        pass

    def parseCFG(self):
        """
        Parses the CFG into CNF
        It uses the following steps: https://www.geeksforgeeks.org/converting-context-free-grammar-chomsky-normal-form/
        :return: Grammar in CNF
        """
        # Step 1: Eliminate the start symbol from the RHS of the productions
        self._eliminateStartSymbolFromRHS()
        # Step 2: Eliminate epsilon productions
        self._eliminateEpsilonProductions()
        # Step 3: Eliminate unit productions
        self._eliminateUnitProductions()
        # Step 4: Eliminate useless productions
        self._eliminateUselessProductions()
        # Step 5: Separate terminals from variables in the RHS of the productions
        self._separateTerminalsFromVariables()
        # Step 6: Eliminate productions with more than 2 variables in the RHS
        self._eliminateProductionsWithMoreThan2Variables()

        return Grammar(self.terminals, self.variables, self.start, self.productions)
