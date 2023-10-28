from Token import Token

class VariableController:
    def __init__(self, variables):
        # A list with numbers and letters from A to Z
        self.availableVariables = [chr(i) for i in range(65, 91)] + [str(i) for i in range(0, 10)]
        self.variables = variables
        self._removeVariablesFromAvailableVariables()

    def _removeVariablesFromAvailableVariables(self):
        """
        Removes the variables from the available variables
        :return: None
        """
        for variable in self.variables:
            if variable in self.availableVariables:
                self.availableVariables.remove(variable)

    def getVariable(self):
        """
        Gets a variable from the available variables
        :return: A variable
        """
        variable = self.availableVariables[0]
        self.availableVariables.remove(variable)
        return Token(variable)
