from sly import Lexer, Parser

class CalcLexer(Lexer):
    # Set of token names.   This is always required
    tokens = {NUMBER, PLUS, MINUS, TIMES, COMMA, SEMICOLON, LBRACKET, RBRACKET, LPAREN, RPAREN, TRANSP}

    # String containing ignored characters between tokens
    ignore = ' \t'

    # Regular expression rules for tokens
    # NUMBER  = r'\d+'
    PLUS    = r'\+'
    MINUS   = r'-'
    TIMES   = r'\*'
    COMMA = r','
    SEMICOLON = r';'
    LBRACKET = r'\['
    RBRACKET = r'\]'
    LPAREN = r'\('
    RPAREN = r'\)'
    TRANSP = r't'

    # Ignored pattern
    ignore_newline = r'\n+'     

    # Extra \n for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

    @_(r'\d+')
    def NUMBER(self, t):
        print(int(t.value))
        t.value = int(t.value)
        # return t

class CalcParser(Parser):
    # Get the token list from the lexer (required)
    tokens = CalcLexer.tokens

    precedence = (
       ('left', PLUS, MINUS),
       ('left', TIMES),
       ('left', TRANSP),
    )

    # Grammar rules and actions
    @_('S PLUS M')
    def S(self, p):
        return p.term + p.factor

    @_('S MINUS M')
    def S(self, p):
        return p.term - p.factor

    @_('M')
    def S(self, p):
        return p.term

    @_('M TIMES matrix')
    def M(self, p):
        return p.factor * p.value

    @_('matrix')
    def M(self, p):
        return p.value

    @_('TRANSP matrix')
    def matrix(self, p):
        return p.value

    @_('LPAREN S RPAREN')
    def matrix(self, p):
        return p.value

    @_('LBRACKET NUMBER COMMA NUMBER SEMICOLON NUMBER COMMA NUMBER RBRACKET')
    def matrix(self, p):
        return p.value

if __name__ == '__main__':
    data = input('Digite a sua expressão:')
    lexer = CalcLexer()
    parser = CalcParser()
    for tok in lexer.tokenize(data):
        print('type=%r, value=%r' % (tok.type, tok.value))
    
    result = parser.parse(lexer.tokenize(data))
    print(result)

