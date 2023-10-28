from Token import Token

class GrammarAnalyzer:
    def __init__(self, sentence):
        self.sentence = sentence
        self.tokens = self._tokenizeSentence()

    def _tokenizeSentence(self):
        words = self.sentence.split()
        tokens = []
        for word in words:
            tokens.append(Token(word, True))
        return tokens
