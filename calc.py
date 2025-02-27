# Token types
EOF = 'EOF'
INTEGER = 'INTEGER'
PLUS = 'PLUS'
MINUS = 'MINUS'

class Token:
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, or EOF
        self.type = type
        # token value: integer (0, 1, 2, ..., 9), '+', or None
        self.value = value

    def __str__(self):
        return f'Token({self.type}, {repr(self.value)})'

    def __repr__(self):
        return self.__str__()

class Interpreter:
    def __init__(self, text):
        # The input expression, e.g., "3+5"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        # current token instance
        self.current_token = None
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        """Lexical analyzer (tokenizer)"""
        while self.current_char is not None:
            
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
        
            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())
                
            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')
        
            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')
        
            self.error()
        
        return Token(EOF, None)

    def eat(self, token_type):
        """Compare the current token type with the passed token type and if they match, eat the current token"""
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        """expr -> INTEGER PLUS INTEGER"""
        self.current_token = self.get_next_token()
        
        # We expect the current token to be an integer
        left = self.current_token
        self.eat(INTEGER)
        
        # We expect the current token to be a PLUS
        op = self.current_token
        if op.type == PLUS:
            self.eat(PLUS)
        else:
            self.eat(MINUS)
        
        # We expect the current token to be an integer
        right = self.current_token
        self.eat(INTEGER)
        
        # The result of adding the two integers
        if op.type == PLUS:
            result = left.value + right.value
        else:
            result = left.value - right.value
        return result
    
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  
        else:
            self.current_char = self.text[self.pos]

def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)

if __name__ == '__main__':
    main()
