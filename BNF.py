from Token import Token


def tokenizeTerminals(terminals):
    """
    Returns a dictionary for the tokens used for each terminal
    :param terminals: The grammar to tokenize
    :return: Dictionary of tokens string: Token
    """
    tokenizedTerminals = {}
    for terminal in terminals:
        tokenizedTerminals[terminal] = Token(terminal, True)

    return list(tokenizedTerminals.values()), tokenizedTerminals


def tokenizeVariables(variables, terminals, productions):
    """
    Returns a dictionary for the tokens used for each variable
    :param variables: The grammar to tokenize
    :param terminals: The terminals dictionary
    :param productions: The productions dictionary
    :return: Dictionary of tokens string: Token
    """
    tokenizedVariables = {}
    for variable in variables:
        tokenizedVariables[variable] = Token(variable)

    for variable in productions:
        for production in productions[variable]:
            for character in production:
                if character in tokenizedVariables or character in terminals.keys():
                    continue
                elif character == 'ε':
                    tokenizedVariables[character] = Token(character, isEpsilon=True)
                else:
                    tokenizedVariables[character] = Token(character)

    return list(tokenizedVariables.values()), tokenizedVariables


def tokenizeProduction(production, variablesDictionary, terminalsDictionary):
    """
    Returns a tuple of tokens for the production
    :param production: The production to tokenize
    :param variablesDictionary: The variables dictionary
    :param terminalsDictionary: The terminals dictionary
    :return: Tuple of tokens
    """
    newProductions = tuple()
    for character in production:
        if character in variablesDictionary:
            newProductions += (variablesDictionary[character],)
        elif character in terminalsDictionary:
            newProductions += (terminalsDictionary[character],)
        else:
            raise Exception("Invalid character in production: {}".format(character))
    return newProductions


def tokenizeProductions(productions, variablesDictionary, terminalsDictionary):
    """
    Returns a dictionary for the tokens used for each production
    :param productions: The grammar to tokenize
    :param variablesDictionary: The variables dictionary
    :param terminalsDictionary: The terminals dictionary
    :return: Dictionary of tokens string: Token
    """
    newProductions = {}
    for variable in productions:
        newProductions[variablesDictionary[variable]] = set()
        for production in productions[variable]:
            newProductions[variablesDictionary[variable]].add(tokenizeProduction(production, variablesDictionary, terminalsDictionary))
    return newProductions
