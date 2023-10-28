class Token:
    def __init__(self, name=None, isTerminal=False, isEpsilon=False):
        self.name = name
        self.isTerminal = isTerminal
        self.isEpsilon = isEpsilon

    def __str__(self):
        return "<{}>".format(self.name)

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, Token):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == other
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def __iter__(self):
        yield self.name
