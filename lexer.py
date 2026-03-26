import re

# Definição dos tipos de tokens
TOKENS = [
    ('COMMENT_MULTI', r'/\*[\s\S]*?\*/'),
    ('COMMENT_SINGLE', r'//.*'),
    ('KEYWORD', r'\b(var|const|func|if|then|else|end|while|do|return|true|false|and|or|not|int|float|bool|string|void|print|begin)\b'),
    ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('FLOAT', r'\d+\.\d+'),
    ('INT', r'\d+'),
    ('STRING', r'"[^"]*"'),
    ('OP_REL', r'==|!=|<=|>=|<|>'),
    ('OP_ASSIGN', r'='),
    ('OP_ARITH', r'[\+\-\*/%]'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('LBRACE', r'\{'),
    ('RBRACE', r'\}'),
    ('COLON', r':'),
    ('COMMA', r','),
    ('SEMICOLON', r';'),
    ('NEWLINE', r'\n'),
    ('SKIP', r'[ \t]+'),
    ('MISMATCH', r'.'),
]

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, line={self.line}, col={self.column})"

def tokenize(code):
    tokens = []
    line_num = 1
    line_start = 0
    
    # Compilar regex
    regex = '|'.join('(?P<%s>%s)' % pair for pair in TOKENS)
    
    for mo in re.finditer(regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start
        
        if kind == 'SKIP':
            continue
        elif kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
            continue
        elif kind == 'COMMENT_MULTI':
            line_num += value.count('\n')
            # Atualizar line_start para a última linha do comentário multi-linha
            last_newline = value.rfind('\n')
            if last_newline != -1:
                line_start = mo.start() + last_newline + 1
            continue
        elif kind == 'COMMENT_SINGLE':
            continue
        elif kind == 'MISMATCH':
            raise SyntaxError(f'Caractere inesperado {value!r} na linha {line_num}, coluna {column}')
        
        tokens.append(Token(kind, value, line_num, column))
    
    return tokens

if __name__ == "__main__":
    sample_code = """
    var x: int = 10;
    func main(): void begin
        print("Olá");
    end
    """
    try:
        tokens = tokenize(sample_code)
        for t in tokens:
            print(t)
    except SyntaxError as e:
        print(e)
