class VariableController:
    def __init__(self, variables):
        self.availableVariables = [chr(i) for i in range(65, 91)]  # A-Z
        self.variables = variables
        self._removeVariablesFromAvailableVariables()

    def _removeVariablesFromAvailableVariables(self):
        """
        Removes the variables from the available variables
        :return: None
        """
        for variable in self.variables:
            self.availableVariables.remove(variable)

    def getVariable(self):
        """
        Gets a variable from the available variables
        :return: A variable
        """
        variable = self.availableVariables[0]
        self.availableVariables.remove(variable)
        return variable
