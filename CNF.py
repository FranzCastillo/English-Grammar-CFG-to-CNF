from Grammar import Grammar
from VariableController import VariableController


class CNF:
    def __init__(self, cfg):
        self.cfg = cfg
        self.terminals = cfg.terminals
        self.variables = cfg.variables
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
        newStart = self.start + "'"  # S0
        self._addProduction(newStart, self.start)
        self.start = newStart

    def _getVariablesWithEpsilonProductions(self):
        """
        Gets the variables with epsilon productions
        :return:
        """
        variablesWithEpsilon = set()
        for variable in self.productions:
            for production in self.productions[variable]:
                if production == '':
                    variablesWithEpsilon.add(variable)
        return variablesWithEpsilon

    def _eliminateEpsilonProductions(self):
        """
        Eliminates epsilon productions
        :return: None
        """
        variablesWithEpsilon = self._getVariablesWithEpsilonProductions()
        while len(variablesWithEpsilon) != 0:
            for variable in variablesWithEpsilon:
                self.productions[variable].remove('')

            for variable in self.productions:
                productionsToAppend = set()
                for production in self.productions[variable]:
                    # Deletes individual epsilon productions
                    for character in production:
                        if character in variablesWithEpsilon:
                            productionsToAppend.add(production.replace(character, ''))
                    # Delete also if it has multiple epsilon productions
                    tempProduction = ''
                    for character in production:
                        if character not in variablesWithEpsilon:
                            tempProduction += character
                    if tempProduction != '':
                        productionsToAppend.add(tempProduction)

                self.productions[variable].update(productionsToAppend)
            variablesWithEpsilon = self._getVariablesWithEpsilonProductions()

    def _getUnitProductions(self):
        productionsWithUnits = dict()  # Variable: set(UnitVariables)
        for variable in self.productions:
            productionsWithUnits[variable] = set()
            for production in self.productions[variable]:
                if len(production) == 1 and production in self.variables:
                    productionsWithUnits[variable].add(production)

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
                self.productions[variable].update(self.productions[unitVariable])

    def _getReachable(self):
        """
        Gets the variables that are reachable from the start symbol
        :return: set(ReachableVariables)
        """
        reachableVariables = {self.start}
        for variable in self.productions.keys():
            for production in self.productions[variable]:
                for character in production:
                    if character in self.variables:
                        reachableVariables.add(character)

        reachableTerminals = set()
        for variable in self.productions.keys():
            for production in self.productions[variable]:
                for character in production:
                    if character in self.terminals:
                        reachableTerminals.add(character)

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
        for variable in self.productions.keys():
            for production in self.productions[variable].copy():
                for character in production:
                    if character in self.terminals and character not in reachableTerminals:
                        self.productions[variable].remove(production)
                    if character in self.variables and character not in reachableVariables:
                        self.productions[variable].remove(production)

        # Step 3: Eliminate productions with empty sets
        removedVariables = set()
        for variable in list(self.productions.keys()):
            if len(self.productions[variable]) == 0:
                del self.productions[variable]
                removedVariables.add(variable)

        for variable in list(self.productions.keys()):
            for production in self.productions[variable].copy():
                for character in production:
                    if character in removedVariables:
                        self.productions[variable].remove(production)

    def _separateTerminalsFromVariables(self):
        """
        Separates terminals from variables in the RHS of the productions
        :return: None
        """
        separatedTerminals = {}  # Terminal: VariableToReplace
        for terminal in self.terminals:
            newVariable = self.vc.getVariable()
            separatedTerminals[terminal] = newVariable
            self._addProduction(newVariable, terminal)
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
                if len(production) == 1 and production in self.terminals:
                    continue
                newProduction = ''
                for character in production:
                    if character in replaceDictionary:
                        newProduction += replaceDictionary[character]
                    else:
                        newProduction += character
                self.productions[variable].remove(production)
                self.productions[variable].add(newProduction)

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
                        newVariable = self.vc.getVariable()
                        self.productions[variable].remove(production)
                        self.productions[variable].add(newVariable + production[-1])
                        self._addProduction(newVariable, production[:-1])

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

        return Grammar(self.terminals, self.variables, self.start, self.productions)
