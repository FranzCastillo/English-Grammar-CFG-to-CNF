from Token import Token

class GrammarAnalyzer:
    def __init__(self, sentence):
        self.sentence = sentence
        self.tokens = self._tokenizeSentence()

    def _tokenizeSentence(self):
        words = self.sentence.split()
        tokens = []
        spaceToken = Token('_', True)
        for word in words:
            tokens.append(Token(word, True))
            tokens.append(spaceToken)
        tokens.pop()
        return tokens
