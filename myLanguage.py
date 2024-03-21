# myLanguage.py
# Daniel Bell & Taylor Kiker

from sly import Lexer

class BasicLexer(Lexer):
    tokens = { NAME, NUMBER, STRING }
    ignore = '\t '
    literals = {'=', '+', '-', '/', '*', '(', ')', ',', ';'}

    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    STRING = r'\".*?\"'

    @_(r'\d+')
    def NUMBER(self, t):

        t.value = int(t.value)
        return t
    
    @_(r'//.*')
    def COMMENT(self, t):
        pass

    @_(r'\n+')
    def newline(self, t):
        self.lineno = t.value.count('\n')