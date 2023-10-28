from Grammar import Grammar
from Token import Token
from VariableController import VariableController


class CNF:
    def __init__(self, cfg):
        self.cfg = cfg
        self.terminals = cfg.terminals
        self.terminalsDictionary = cfg.terminalsDictionary
        self.variables = cfg.variables
        self.variablesDictionary = cfg.variablesDictionary
        self.start = cfg.start
        self.productions = cfg.productions
        del self.cfg
        self.vc = VariableController(self.variables)

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
            self.productions[variable] = set()
        self.productions[variable].add(production)

    def _eliminateStartSymbolFromRHS(self):
        """
        Eliminates the start symbol from the RHS of the productions
        :return: None
        """
        newStart = Token(self.start.name + "'")
        newTuple = (self.start, )
        self._addProduction(newStart, newTuple)
        self.start = newStart

    def _getVariablesWithEpsilonProductions(self):
        """
        Gets the variables with epsilon productions
        :return:
        """
        variablesWithEpsilon = set()
        for key in list(self.productions):
            for production in self.productions[key].copy():
                for token in production:
                    if token.isEpsilon:
                        variablesWithEpsilon.add(key)
                        break
        return variablesWithEpsilon

    def _eliminateEpsilonProductions(self):
        """
        Eliminates epsilon productions
        :return: None
        """
        variablesWithEpsilon = self._getVariablesWithEpsilonProductions()
        # Step 1: Remove the productions with epsilon
        while len(variablesWithEpsilon) != 0:
            for variable in variablesWithEpsilon:
                for production in self.productions[variable].copy():
                    for token in production:
                        if token.isEpsilon:
                            self.productions[variable].remove(production)
                            break

        # Step 2: Append the productions of the removed production
            for variable in list(self.productions):
                productionsToAppend = set()
                for production in self.productions[variable].copy():
                    productionsToAppend.add(production)
                    listToConvertToTuple = list()
                    # Remove single variables
                    for variableWithEpsilon in variablesWithEpsilon:
                        for token in production:
                            if token != variableWithEpsilon:
                                listToConvertToTuple.append(token)
                        if len(listToConvertToTuple) == 0:
                            listToConvertToTuple.append(Token('ε', isEpsilon=True))
                        newTuple = tuple(listToConvertToTuple)
                        productionsToAppend.add(newTuple)
                        listToConvertToTuple = list()
                    # Remove multiple variables
                    for token in production:
                        if token not in variablesWithEpsilon:
                            listToConvertToTuple.append(token)
                    if len(listToConvertToTuple) == 0:
                        listToConvertToTuple.append(Token('ε', isEpsilon=True))
                    else:
                        newTuple = tuple(listToConvertToTuple)
                        productionsToAppend.add(newTuple)

                    self.productions[variable].update(productionsToAppend)
            variablesWithEpsilon = self._getVariablesWithEpsilonProductions()

    def _getUnitProductions(self):
        productionsWithUnits = dict()  # Variable: set(UnitVariables)
        for variable in self.productions:
            productionsWithUnits[variable] = set()
            for production in self.productions[variable]:
                if len(production) == 1:
                    if production[0] in self.variables:
                        newTuple = (production[0], )
                        productionsWithUnits[variable].add(newTuple)

        # Deletes empty sets
        for variable in list(productionsWithUnits.keys()):
            if len(productionsWithUnits[variable]) == 0:
                del productionsWithUnits[variable]

        return productionsWithUnits

    def _eliminateUnitProductions(self):
        """
        Eliminates unit productions
        :return: None
        """
        productionsWithUnits = self._getUnitProductions()
        # Step 1: Remove the unit production
        for variable in list(productionsWithUnits.keys()):
            for unitVariable in productionsWithUnits[variable].copy():
                self.productions[variable].remove(unitVariable)

        # Step 2: Append the productions of the removed production
        for variable in list(productionsWithUnits.keys()):
            for unitVariable in productionsWithUnits[variable]:
                self.productions[variable].update(self.productions[unitVariable[0]])

    def _getReachable(self):
        """
        Gets the variables that are reachable from the start symbol
        :return: set(ReachableVariables)
        """
        reachableVariables = {self.start}
        reachableTerminals = set()
        areDifferent = True
        while areDifferent:
            areDifferent = False
            for variable in self.productions:
                if variable in list(reachableVariables):
                    for production in self.productions[variable].copy():
                        for token in production:
                            if token in self.variables and token not in reachableVariables:
                                reachableVariables.add(token)
                                areDifferent = True
                            elif token in self.terminals and token not in reachableTerminals:
                                reachableTerminals.add(token)
                                areDifferent = True
        return reachableVariables, reachableTerminals

    def _eliminateUselessProductions(self):
        """
        Eliminates useless productions
        :return: None
        """
        # Step 1: Eliminate productions with variables that are not reachable from the start symbol
        reachableVariables, reachableTerminals = self._getReachable()
        for variable in list(self.productions.keys()):
            if variable not in reachableVariables:
                del self.productions[variable]

        # Step 2: Eliminate productions with terminals that are not reachable from the start symbol
        for key in list(self.productions):
            for production in self.productions[key].copy():
                for token in production:
                    if token in self.terminals and token not in reachableTerminals:
                        self.productions[key].remove(production)
                        break

        # Step 3: Eliminate productions with empty sets
        removedVariables = set()
        for variable in list(self.productions.keys()):
            if len(self.productions[variable]) == 0:
                del self.productions[variable]
                removedVariables.add(variable)

        for variable in list(self.productions.keys()):
            for production in self.productions[variable].copy():
                for token in production:
                    if token in removedVariables:
                        self.productions[variable].remove(production)
                        break

    def _separateTerminalsFromVariables(self):
        """
        Separates terminals from variables in the RHS of the productions
        :return: None
        """
        separatedTerminals = {}  # Terminal: VariableToReplace
        for terminal in self.terminals:
            newVariable = self.vc.getVariable()
            separatedTerminals[terminal] = newVariable
            self._addProduction(newVariable, (terminal, ))
        return separatedTerminals

    def _replaceTerminalsWithVariables(self, replaceDictionary):
        """
        Replaces the terminals with the new variables
        :return:
        """
        dontReplace = replaceDictionary.values()
        for variable in list(self.productions.keys()):
            if variable in dontReplace:
                continue
            for production in self.productions[variable].copy():
                if len(production) == 1 and production[0] in self.terminals:
                    continue
                listToConvertToTuple = []
                for token in production:
                    if token in replaceDictionary:
                        listToConvertToTuple.append(replaceDictionary[token])
                    else:
                        listToConvertToTuple.append(token)
                newTuple = tuple(listToConvertToTuple)
                self.productions[variable].remove(production)
                self.productions[variable].add(newTuple)

    def _areProductionsWithMoreThan2Variables(self):
        for variable in self.productions:
            for production in self.productions[variable]:
                if len(production) > 2:
                    return True
        return False

    def _eliminateProductionsWithMoreThan2Variables(self):
        """
        Eliminates productions with more than 2 variables in the RHS
        :return: None
        """
        while self._areProductionsWithMoreThan2Variables():
            for variable in list(self.productions.keys()):
                for production in self.productions[variable].copy():
                    if len(production) > 2:
                        self.productions[variable].remove(production)

                        newVar = self.vc.getVariable()
                        newTuple = (newVar, production[-1])
                        self._addProduction(newVar, production[:-1])
                        self._addProduction(variable, newTuple)

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
        # Step 5: Separate terminals from variables
        replaceDictionary = self._separateTerminalsFromVariables()
        # Step 6: Replace the terminals with the new variables
        self._replaceTerminalsWithVariables(replaceDictionary)
        # Step 7: Eliminate productions with more than 2 variables in the RHS
        self._eliminateProductionsWithMoreThan2Variables()

        # Step 8: Eliminate useless productions (extra)
        self._eliminateUselessProductions()
        return Grammar(
            self.terminals,
            self.variables,
            self.start,
            self.productions,
            terminalsDictionary=self.terminalsDictionary,
            variablesDictionary=self.variablesDictionary
        )

