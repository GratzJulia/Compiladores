from sly import Lexer, Parser

class CalcLexer(Lexer):
    # Set of token names.   This is always required
    tokens = {NUMBER, PLUS, MINUS, TIMES, COMMA, SEMICOLON, LBRACKET, RBRACKET, LPAREN, RPAREN, TRANSP}

    # String containing ignored characters between tokens
    ignore = ' \t'

    # Regular expression rules for tokens
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
        # converte qualquer entrada numérica para valor inteiro
        t.value = int(t.value)
        return t

class CalcParser(Parser):
    # Get the token list from the lexer (required)
    tokens = CalcLexer.tokens

    precedence = (
       ('left', PLUS, MINUS),
       ('left', TIMES),
       ('left', TRANSP),
       ('left', LPAREN, RPAREN)
    )

    # Grammar rules and actions
    @_('M')
    def S(self, p):
        print('\n--- S ---')
        return p.M

    @_('S PLUS M')
    def S(self, p):
        print('\n--- S soma ---')        
        copyS = list(p.S)
        copyM = list (p.M)
        copyM[2] = copyS[2] + copyM[2]
        copyM[4] = copyS[4] + copyM[4]
        copyM[6] = copyS[6] + copyM[6]
        copyM[8] = copyS[8] + copyM[8]
        print(tuple(copyM))
        return tuple(copyM)

    @_('S MINUS M')
    def S(self, p):
        print('\n--- S subtração ---')
        copyS = list(p.S)
        copyM = list (p.M)
        copyM[2] = copyS[2] - copyM[2]
        copyM[4] = copyS[4] - copyM[4]
        copyM[6] = copyS[6] - copyM[6]
        copyM[8] = copyS[8] - copyM[8]
        print(tuple(copyM))
        return tuple(copyM)
  
    @_('matrix')
    def M(self, p):
        print('\n--- M ---')
        return p.matrix

    @_('M TIMES matrix')
    def M(self, p):
        # print('--- M vezes ---')
        return p 

    @_('TRANSP matrix')
    def matrix(self, p):
        print('\n--- operação transposta ---')
        # p.matrix é uma tupla!
        print(p.matrix)
        a01 = p.matrix[4]
        a10 = p.matrix[6]
        
        copy = list(p.matrix)
        copy[4] = a10
        copy[6] = a01
        print(tuple(copy))
        return tuple(copy)

    @_('LPAREN S RPAREN')
    def matrix(self, p):
        print('\n--- () ---')
        # apenas remove os parênteses!
        return p.S

    @_('LBRACKET NUMBER COMMA NUMBER SEMICOLON NUMBER COMMA NUMBER RBRACKET')
    def matrix(self, p):
        print('\n--- leitura de uma matrix ---')
        # realiza a leitura de uma matriz. Respeita as regras de precedência!
        return p


if __name__ == '__main__':
    data = input('Digite a sua expressão:')
    lexer = CalcLexer()
    parser = CalcParser()
    # for tok in lexer.tokenize(data):
    #     print('type=%r, value=%r' % (tok.type, tok.value))
   
    
    result = parser.parse(lexer.tokenize(data))
    print('\n--- RESULTADO FINAL ---')
    print(result)
