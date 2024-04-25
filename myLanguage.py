# mylanguage.py
# Daniel Bell & Taylor Kiker

from sly import Lexer # tokenizes input text
from sly import Parser # generates a tree from tokenized input

# Begin Lexer ----------------------------------------------------------------------------------
class BasicLexer(Lexer):
    tokens = { NAME, NUMBER, STRING, DOUBLE_SLASH }
    ignore = '\t '
    literals = {'=', '+', '-', '/', '*', ',', ';', '//', '(', ')', '%'}

    # Token definitions
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    STRING = r'\".*?\"'
    DOUBLE_SLASH = r'//'

    @_(r'\d+')
    def NUMBER(self, t):

        t.value = int(t.value)
        return t

    @_(r'\n+')
    def newline(self, t):
        self.lineno = t.value.count('\n')

    # Begin Parser ----------------------------------------------------------------------------
class BasicParser(Parser): 
	
    # Copy tokens from lexer
    tokens = BasicLexer.tokens 
  
    precedence = ( 
        ('left', '+', '-'), 
        ('left', '*', '/',), 
        ('right', 'UMINUS'), 
    )
  
    # Constructor
    def __init__(self): 
        self.env = { } 
  
    # Matching input to functions -------------------------------------------------------------
    # p = token
    # self = parser instance
		
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
    
    @_('expr "%" expr') 
    def expr(self, p): 
        return ('modulo', p.expr0, p.expr1) 
  
    @_('"-" expr %prec UMINUS') 
    def expr(self, p): 
        return p.expr 
  
    @_('NAME') 
    def expr(self, p): 
        return ('var', p.NAME) 
  
    @_('NUMBER') 
    def expr(self, p): 
        return ('num', p.NUMBER)
	
    @_('expr DOUBLE_SLASH expr')
    def expr(self, p):
        return ('div_int', p.expr0, p.expr1)

    
class BasicExecute: 
	
    def __init__(self, tree, env):
        self.env = env

        result = self.walkTree(tree)

        if result is not None and isinstance(result, int): # print integers
            print(result)

        if result is not None and isinstance(result, float): # print doubles
            print(result)

        if isinstance(result, str) and result[0] == '"': # print strings
            print(result)

    def walkTree(self, node): 

        if isinstance(node, int): 
            return node 
        if isinstance(node, str): 
            return node 

        if node is None: 
            return None

        if node[0] == 'program': 
            if node[1] == None: 
                self.walkTree(node[2]) 
            else: 
                self.walkTree(node[1]) 
                self.walkTree(node[2]) 

        if node[0] == 'num': 
            return node[1] 

        if node[0] == 'str': 
            return node[1] 

        if node[0] == 'add': 

            if(isinstance(self.walkTree(node[1]), str) and isinstance(self.walkTree(node[2]), str)):
                 # Reassign strings
                a = self.walkTree(node[1])
                b = self.walkTree(node[2])
                # Remove inner quotes
                a = a[:-1]
                b = b[1:]

                return a + b
            else:
                return self.walkTree(node[1]) + self.walkTree(node[2]) 

        elif node[0] == 'sub': 
            if(isinstance(self.walkTree(node[1]), str) and isinstance(self.walkTree(node[2]), str)):
                 # Reassign strings
                a = self.walkTree(node[1])
                b = self.walkTree(node[2])
                # Remove inner quotes
                a = a[:-1] 
                b = b[:-1]
                b = b[1:]
                a = a[1:]
                a = a.replace(b, '')
                a = '"' + a + '"'
                return a
            else:
                return self.walkTree(node[1]) - self.walkTree(node[2]) 
        
        elif node[0] == 'mul': 
            return self.walkTree(node[1]) * self.walkTree(node[2]) 

        elif node[0] == 'div': 
            return self.walkTree(node[1]) / self.walkTree(node[2])
        
        elif node[0] == 'modulo':
            return self.walkTree(node[1]) % self.walkTree(node[2])
        
        elif node[0] == 'div_int':
            return self.walkTree(node[1]) // self.walkTree(node[2])
              

        if node[0] == 'var_assign': 
            self.env[node[1]] = self.walkTree(node[2]) 
            return node[1] 

        if node[0] == 'var': 
            try: 
                return self.env[node[1]] 
            except LookupError: 
                print("Undefined variable '"+node[1]+"' found!") 
                return 0


if __name__ == '__main__':
	lexer = BasicLexer()
	parser = BasicParser()
	print('Biker') 
	env = {} 
	
	while True: 
		
		try:
			text = input('Biker > ') 
		
		except EOFError: 
			break
		
		if text: 
			tree = parser.parse(lexer.tokenize(text)) 
			BasicExecute(tree, env)