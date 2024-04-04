# myLanguage.py
# Daniel Bell & Taylor Kiker

from sly import Lexer # tokenizes input text
from sly import Parser # generates a tree from tokenized input

# Begin Lexer ----------------------------------------------------------------------------------
class BasicLexer(Lexer):
    tokens = { NAME, NUMBER, STRING, DOUBLE_SLASH, DELETE }
    ignore = '\t '
    literals = {'=', "+", '-', '/', '*', '(', ')', ',', ';', '//'}

    # Token definitions
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    STRING = r'\".*?\"'
    DOUBLE_SLASH = r'//'
    DELETE = r'Delete(NAME)'

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
    
    @_('STRING "+" STRING')
    def expr(self, p):
	    return ('Concat', p.STRING0, p.STRING1)
    
    @_('DELETE')
    def expr(self,p):
         return ('Delete', p.STRING0)
	
    
        
    
class BasicExecute: 
	
    def __init__(self, tree, env):
        self.env = env

        result = self.walkTree(tree)

        #print(result) 

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
            return self.walkTree(node[1]) + self.walkTree(node[2]) 
        elif node[0] == 'sub': 
            return self.walkTree(node[1]) - self.walkTree(node[2]) 
        elif node[0] == 'mul': 
            return self.walkTree(node[1]) * self.walkTree(node[2]) 
        elif node[0] == 'div': 
            return self.walkTree(node[1]) / self.walkTree(node[2])
        elif node[0] == 'div_int':
            return self.walkTree(node[1]) // self.walkTree(node[2])
        elif node[0] == 'Concat':
             a = self.walkTree(node[1])
             b = self.walkTree(node[2])
             '''
             a[a.size]
             '''
             return a + b
        elif node[0] == 'Delete':
            return "Deleted"
              

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
	print('myLanguage') 
	env = {} 
	
	while True: 
		
		try:
			text = input('myLanguage > ') 
		
		except EOFError: 
			break
		
		if text: 
			tree = parser.parse(lexer.tokenize(text)) 
			BasicExecute(tree, env)