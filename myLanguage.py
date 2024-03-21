# myLanguage.py
# Daniel Bell & Taylor Kiker

from sly import Lexer

class BasicLexer(Lexer):
    tokens = { NAME, NUMBER, STRING }
    ignore = '\t '
    literals = {'=', '+', '-', '/', '*', '(', ')', ',', ';'}
