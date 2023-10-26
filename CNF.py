from VariableController import VariableController
from Grammar import Grammar


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

        # Append the epsilon production to the variables that have the variable with epsilon production
        while len(variablesWithEpsilon) != 0:
            # Eliminate the epsilon production
            for variable in variablesWithEpsilon:
                self.productions[variable].remove('')
            for variable in self.productions:
                tempProductions = []
                for production in self.productions[variable]:
                    for epsilonVariable in variablesWithEpsilon:
                        tempProductions.append(production)
                        if epsilonVariable in production:
                            tempProductions.append(production.replace(epsilonVariable, ''))
                self.productions[variable] = tempProductions
            variablesWithEpsilon = self._getVariablesWithEpsilonProductions()

    def _getUnitProductions(self):
        productionsWithUnits = {}  # Variable: UnitVariable
        for variable in self.productions:
            for production in self.productions[variable]:
                if len(production) == 1 and production in self.variables:
                    productionsWithUnits[variable] = production
        return productionsWithUnits

    def _eliminateUnitProductions(self):
        """
        Eliminates unit productions
        :return: None
        """
        print(self.productions)
        productionsWithUnits = self._getUnitProductions()
        for variable in productionsWithUnits:
            self.productions[variable].remove(productionsWithUnits[variable])
        for variable in self.productions:
            tempProductions = self.productions[variable]
            if variable in productionsWithUnits:
                for production in self.productions[productionsWithUnits[variable]]:
                    tempProductions.append(production)
            self.productions[variable] = tempProductions
        print(self.productions)


    def _eliminateUselessProductions(self):
        """
        Eliminates useless productions
        As reference: https://www.geeksforgeeks.org/simplifying-context-free-grammars/
        :return: None
        """
        # Step 1: Eliminate productions with variables that are not reachable from the start symbol
        reachableVariables = {self.start}
        for variable in self.variables:
            for production in self.productions[variable]:
                for character in production:
                    if character in self.variables:
                        reachableVariables.add(character)

        removedVariables = []
        for variable in self.variables:
            if variable not in reachableVariables:
                del self.productions[variable]
                self.variables.remove(variable)
                removedVariables.append(variable)
        # Step 2: Eliminate productions with variables that cannot derive a string of terminals
        for variable in self.variables:
            for production in self.productions[variable]:
                for character in production:
                    if character in removedVariables:
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

        for variable in self.variables:
            tempProductions = []
            for production in self.productions[variable]:
                newProduction = ''
                if len(production) > 1:
                    for character in production:
                        if character in self.terminals:
                            newProduction += separatedTerminals[character]
                        else:
                            newProduction += character
                else:
                    newProduction = production
                tempProductions.append(newProduction)
                self.productions[variable] = tempProductions

        for terminal in separatedTerminals:
            self._addProduction(separatedTerminals[terminal], terminal)

    def _eliminateProductionsWithMoreThan2Variables(self):
        """
        Eliminates productions with more than 2 variables in the RHS
        :return: None
        """
        newProductions = {}
        for variable in self.productions:
            tempProductions = []
            for production in self.productions[variable]:
                if len(production) > 2:
                    newVariable = self.vc.getVariable()
                    newProduction = newVariable + production[-1]
                    tempProductions.append(newProduction)
                    newProductions[newVariable] = production[:-1]
                else:
                    tempProductions.append(production)
            self.productions[variable] = tempProductions

        for newVariable in newProductions:
            self._addProduction(newVariable, newProductions[newVariable])

    def parseCFG(self):
        """
        Parses the CFG into CNF
        It uses the following steps: https://www.geeksforgeeks.org/converting-context-free-grammar-chomsky-normal-form/
        :return: Grammar in CNF
        """
        # Step 1: Eliminate the start symbol from the RHS of the productions
        self._eliminateStartSymbolFromRHS()
        # Step 2: Remove terminals with variables
        self._separateTerminalsFromVariables()
        # Step 3: Get all productions to 2 variables
        self._eliminateProductionsWithMoreThan2Variables()
        # Step 4: Eliminate epsilon productions
        self._eliminateEpsilonProductions()
        # Step 5: Eliminate unit productions
        self._eliminateUnitProductions()
        # Step 6: Eliminate useless productions
        # self._eliminateUselessProductions()
        # Step 7: Eliminate useless symbols


        return Grammar(self.terminals, self.variables, self.start, self.productions)
