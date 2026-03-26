from lexer import tokenize
from ast_nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self, offset=0):
        if self.pos + offset < len(self.tokens):
            return self.tokens[self.pos + offset]
        return None

    def consume(self, expected_type=None, expected_value=None):
        token = self.peek()
        if token is None:
            raise SyntaxError("Fim inesperado do arquivo")
        
        if expected_type and token.type != expected_type:
            raise SyntaxError(f"Esperado token {expected_type}, mas obteve {token.type} na linha {token.line}")
        
        if expected_value and token.value != expected_value:
            raise SyntaxError(f"Esperado valor '{expected_value}', mas obteve '{token.value}' na linha {token.line}")
        
        self.pos += 1
        return token

    def match(self, expected_type=None, expected_value=None):
        token = self.peek()
        if token is None:
            return False
        
        if expected_type and token.type != expected_type:
            return False
        
        if expected_value and token.value != expected_value:
            return False
        
        self.pos += 1
        return True

    def parse_program(self):
        declarations = []
        while self.peek() is not None:
            declarations.append(self.parse_declaration())
        return Program(declarations)

    def parse_declaration(self):
        token = self.peek()
        if token.value == 'var':
            return self.parse_var_decl()
        elif token.value == 'const':
            return self.parse_const_decl()
        elif token.value == 'func':
            return self.parse_func_decl()
        else:
            raise SyntaxError(f"Declaração inesperada: {token.value} na linha {token.line}")

    def parse_var_decl(self):
        self.consume('KEYWORD', 'var')
        name = self.consume('ID').value
        self.consume('COLON')
        type_name = self.consume('KEYWORD').value
        
        initial_value = None
        if self.match('OP_ASSIGN'):
            initial_value = self.parse_expression()
        
        self.consume('SEMICOLON')
        return VarDecl(name, type_name, initial_value)

    def parse_const_decl(self):
        self.consume('KEYWORD', 'const')
        name = self.consume('ID').value
        self.consume('COLON')
        type_name = self.consume('KEYWORD').value
        self.consume('OP_ASSIGN')
        initial_value = self.parse_expression()
        self.consume('SEMICOLON')
        return ConstDecl(name, type_name, initial_value)

    def parse_func_decl(self):
        self.consume('KEYWORD', 'func')
        name = self.consume('ID').value
        self.consume('LPAREN')
        
        params = []
        if not self.match('RPAREN'):
            params.append(self.parse_param())
            while self.match('COMMA'):
                params.append(self.parse_param())
            self.consume('RPAREN')
            
        self.consume('COLON')
        return_type = self.consume('KEYWORD').value
        
        self.consume('KEYWORD', 'begin')
        body = self.parse_block()
        self.consume('KEYWORD', 'end')
        
        return FuncDecl(name, params, return_type, body)

    def parse_param(self):
        name = self.consume('ID').value
        self.consume('COLON')
        type_name = self.consume('KEYWORD').value
        return Param(name, type_name)

    def parse_block(self):
        statements = []
        # Parar se encontrar 'end' ou 'else' (para if/else)
        while self.peek() and self.peek().value not in ['end', 'else']:
            statements.append(self.parse_statement())
        return Block(statements)

    def parse_statement(self):
        token = self.peek()
        if token.value == 'var':
            return self.parse_var_decl()
        elif token.value == 'const':
            return self.parse_const_decl()
        elif token.value == 'if':
            return self.parse_if_stmt()
        elif token.value == 'while':
            return self.parse_while_stmt()
        elif token.value == 'return':
            return self.parse_return_stmt()
        elif token.value == 'print':
            return self.parse_print_stmt()
        elif token.type == 'ID':
            # Pode ser atribuição ou chamada de função
            if self.peek(1) and self.peek(1).type == 'OP_ASSIGN':
                return self.parse_assign_stmt()
            else:
                expr = self.parse_expression()
                self.consume('SEMICOLON')
                return expr
        else:
            raise SyntaxError(f"Instrução inesperada: {token.value} na linha {token.line}")

    def parse_if_stmt(self):
        self.consume('KEYWORD', 'if')
        condition = self.parse_expression()
        self.consume('KEYWORD', 'then')
        then_block = self.parse_block()
        
        else_block = None
        if self.match('KEYWORD', 'else'):
            else_block = self.parse_block()
            
        self.consume('KEYWORD', 'end')
        return IfStmt(condition, then_block, else_block)

    def parse_while_stmt(self):
        self.consume('KEYWORD', 'while')
        condition = self.parse_expression()
        self.consume('KEYWORD', 'do')
        body = self.parse_block()
        self.consume('KEYWORD', 'end')
        return WhileStmt(condition, body)

    def parse_return_stmt(self):
        self.consume('KEYWORD', 'return')
        value = None
        if not self.match('SEMICOLON'):
            value = self.parse_expression()
            self.consume('SEMICOLON')
        return ReturnStmt(value)

    def parse_assign_stmt(self):
        name = self.consume('ID').value
        self.consume('OP_ASSIGN')
        value = self.parse_expression()
        self.consume('SEMICOLON')
        return AssignStmt(name, value)

    def parse_print_stmt(self):
        self.consume('KEYWORD', 'print')
        self.consume('LPAREN')
        value = self.parse_expression()
        self.consume('RPAREN')
        self.consume('SEMICOLON')
        return PrintStmt(value)

    def parse_expression(self):
        return self.parse_logical_or()

    def parse_logical_or(self):
        node = self.parse_logical_and()
        while self.match('KEYWORD', 'or'):
            node = BinaryOp(node, 'or', self.parse_logical_and())
        return node

    def parse_logical_and(self):
        node = self.parse_equality()
        while self.match('KEYWORD', 'and'):
            node = BinaryOp(node, 'and', self.parse_equality())
        return node

    def parse_equality(self):
        node = self.parse_comparison()
        while self.peek() and self.peek().value in ['==', '!=']:
            op = self.consume().value
            node = BinaryOp(node, op, self.parse_comparison())
        return node

    def parse_comparison(self):
        node = self.parse_term()
        while self.peek() and self.peek().value in ['<', '>', '<=', '>=']:
            op = self.consume().value
            node = BinaryOp(node, op, self.parse_term())
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.peek() and self.peek().value in ['+', '-']:
            op = self.consume().value
            node = BinaryOp(node, op, self.parse_factor())
        return node

    def parse_factor(self):
        node = self.parse_unary()
        while self.peek() and self.peek().value in ['*', '/', '%']:
            op = self.consume().value
            node = BinaryOp(node, op, self.parse_unary())
        return node

    def parse_unary(self):
        if self.peek() and (self.peek().value == 'not' or self.peek().value == '-'):
            op = self.consume().value
            return UnaryOp(op, self.parse_unary())
        return self.parse_primary()

    def parse_primary(self):
        token = self.peek()
        if token.type == 'INT':
            self.consume()
            return Literal('int', int(token.value))
        elif token.type == 'FLOAT':
            self.consume()
            return Literal('float', float(token.value))
        elif token.type == 'STRING':
            self.consume()
            return Literal('string', token.value[1:-1])
        elif token.value == 'true':
            self.consume()
            return Literal('bool', True)
        elif token.value == 'false':
            self.consume()
            return Literal('bool', False)
        elif token.type == 'ID':
            name = self.consume().value
            if self.match('LPAREN'):
                args = []
                if not self.match('RPAREN'):
                    args.append(self.parse_expression())
                    while self.match('COMMA'):
                        args.append(self.parse_expression())
                    self.consume('RPAREN')
                return FuncCall(name, args)
            return Identifier(name)
        elif self.match('LPAREN'):
            node = self.parse_expression()
            self.consume('RPAREN')
            return node
        else:
            raise SyntaxError(f"Expressão primária inesperada: {token.value} na linha {token.line}")

def parse(code):
    tokens = tokenize(code)
    parser = Parser(tokens)
    return parser.parse_program()

if __name__ == "__main__":
    sample_code = """
    var x: int = 10;
    func main(): void begin
        print("Olá " + "Mundo");
        if x > 5 then
            print("x é maior que 5");
        end
    end
    """
    try:
        ast = parse(sample_code)
        print("AST construída com sucesso!")
    except SyntaxError as e:
        print(e)
