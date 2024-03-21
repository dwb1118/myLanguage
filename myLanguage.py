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

class BasicParser(Parser): 
    #tokens are passed from lexer to parser 
    tokens = BasicLexer.tokens 
  
    precedence = ( 
        ('left', '+', '-'), 
        ('left', '*', '/'), 
        ('right', 'UMINUS'), 
    ) 
  
    def __init__(self): 
        self.env = { } 
  
    @_('') 
    def statement(self, p): 
        pass
  
    @_('var_assign') 
    def statement(self, p): 
        return p.var_assign 
  
    @_('NAME "=" expr') 
    def var_assign(self, p): 
        return ('var_assign', p.NAME, p.expr) 
  
    @_('NAME "=" STRING') 
    def var_assign(self, p): 
        return ('var_assign', p.NAME, p.STRING) 
  
    @_('expr') 
    def statement(self, p): 
        return (p.expr) 
  
    @_('expr "+" expr') 
    def expr(self, p): 
        return ('add', p.expr0, p.expr1) 
  
    @_('expr "-" expr') 
    def expr(self, p): 
        return ('sub', p.expr0, p.expr1) 
  
    @_('expr "*" expr') 
    def expr(self, p): 
        return ('mul', p.expr0, p.expr1) 
  
    @_('expr "/" expr') 
    def expr(self, p): 
        return ('div', p.expr0, p.expr1) 
  
    @_('"-" expr %prec UMINUS') 
    def expr(self, p): 
        return p.expr 
  
    @_('NAME') 
    def expr(self, p): 
        return ('var', p.NAME) 
  
    @_('NUMBER') 
    def expr(self, p): 
        return ('num', p.NUMBER)
