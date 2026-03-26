from ast_nodes import *

class Compiler:
    def __init__(self):
        self.bytecode = []
        self.functions = {} # name -> (num_params, bytecode)
        self.current_bytecode = []

    def emit(self, opcode, *args):
        self.current_bytecode.append((opcode, *args))

    def compile_program(self, program):
        # Primeiro, compilar declarações globais (variáveis/constantes)
        # Por enquanto, vamos focar em funções.
        for decl in program.declarations:
            if isinstance(decl, FuncDecl):
                self.compile_func_decl(decl)
            elif isinstance(decl, (VarDecl, ConstDecl)):
                # Declarações globais (serão tratadas na inicialização)
                self.compile_global_decl(decl)
        
        return self.functions

    def compile_global_decl(self, decl):
        # Por enquanto, apenas emite instruções para inicialização
        if decl.initial_value:
            self.compile_expression(decl.initial_value)
            self.emit('STORE_VAR', decl.name)

    def compile_func_decl(self, func_decl):
        old_bytecode = self.current_bytecode
        self.current_bytecode = []
        
        # Parâmetros são passados na pilha. 
        # O último argumento está no topo da pilha.
        # Então devemos desempilhar na ordem inversa.
        for param in reversed(func_decl.params):
            self.emit('STORE_VAR', param.name)
            
        # O corpo da função
        self.compile_block(func_decl.body)
        
        # Garantir que toda função termine com RETURN
        if not self.current_bytecode or self.current_bytecode[-1][0] != 'RETURN':
            self.emit('PUSH_BOOL', False) # Default return value
            self.emit('RETURN')
            
        self.functions[func_decl.name] = (len(func_decl.params), self.current_bytecode)
        self.current_bytecode = old_bytecode

    def compile_block(self, block):
        for stmt in block.statements:
            self.compile_statement(stmt)

    def compile_statement(self, stmt):
        if isinstance(stmt, IfStmt):
            self.compile_if_stmt(stmt)
        elif isinstance(stmt, WhileStmt):
            self.compile_while_stmt(stmt)
        elif isinstance(stmt, ReturnStmt):
            self.compile_return_stmt(stmt)
        elif isinstance(stmt, AssignStmt):
            self.compile_assign_stmt(stmt)
        elif isinstance(stmt, PrintStmt):
            self.compile_print_stmt(stmt)
        elif isinstance(stmt, FuncCall):
            self.compile_func_call(stmt)
            self.emit('POP') # Descartar o valor de retorno de chamadas de função como instrução
        elif isinstance(stmt, VarDecl):
            self.compile_var_decl(stmt)
        elif isinstance(stmt, ConstDecl):
            self.compile_const_decl(stmt)

    def compile_var_decl(self, decl):
        if decl.initial_value:
            self.compile_expression(decl.initial_value)
        else:
            # Default values
            if decl.type_name == 'int': self.emit('PUSH_INT', 0)
            elif decl.type_name == 'float': self.emit('PUSH_FLOAT', 0.0)
            elif decl.type_name == 'bool': self.emit('PUSH_BOOL', False)
            elif decl.type_name == 'string': self.emit('PUSH_STRING', "")
            else: self.emit('PUSH_BOOL', False)
        self.emit('STORE_VAR', decl.name)

    def compile_const_decl(self, decl):
        self.compile_expression(decl.initial_value)
        self.emit('STORE_VAR', decl.name)

    def compile_if_stmt(self, stmt):
        self.compile_expression(stmt.condition)
        
        jump_if_false_idx = len(self.current_bytecode)
        self.emit('JUMP_IF_FALSE', 0) # Placeholder
        
        self.compile_block(stmt.then_block)
        
        if stmt.else_block:
            jump_idx = len(self.current_bytecode)
            self.emit('JUMP', 0) # Placeholder para pular o else
            
            # Atualizar JUMP_IF_FALSE para o início do else
            self.current_bytecode[jump_if_false_idx] = ('JUMP_IF_FALSE', len(self.current_bytecode))
            
            self.compile_block(stmt.else_block)
            
            # Atualizar JUMP para o fim do else
            self.current_bytecode[jump_idx] = ('JUMP', len(self.current_bytecode))
        else:
            # Atualizar JUMP_IF_FALSE para o fim do if
            self.current_bytecode[jump_if_false_idx] = ('JUMP_IF_FALSE', len(self.current_bytecode))

    def compile_while_stmt(self, stmt):
        start_idx = len(self.current_bytecode)
        self.compile_expression(stmt.condition)
        
        jump_if_false_idx = len(self.current_bytecode)
        self.emit('JUMP_IF_FALSE', 0) # Placeholder
        
        self.compile_block(stmt.body)
        
        self.emit('JUMP', start_idx)
        self.current_bytecode[jump_if_false_idx] = ('JUMP_IF_FALSE', len(self.current_bytecode))

    def compile_return_stmt(self, stmt):
        if stmt.value:
            self.compile_expression(stmt.value)
        else:
            self.emit('PUSH_BOOL', False)
        self.emit('RETURN')

    def compile_assign_stmt(self, stmt):
        self.compile_expression(stmt.value)
        self.emit('STORE_VAR', stmt.name)

    def compile_print_stmt(self, stmt):
        self.compile_expression(stmt.value)
        self.emit('PRINT')

    def compile_expression(self, expr):
        if isinstance(expr, Literal):
            if expr.type == 'int':
                self.emit('PUSH_INT', expr.value)
            elif expr.type == 'float':
                self.emit('PUSH_FLOAT', expr.value)
            elif expr.type == 'string':
                self.emit('PUSH_STRING', expr.value)
            elif expr.type == 'bool':
                self.emit('PUSH_BOOL', expr.value)
        elif isinstance(expr, Identifier):
            self.emit('LOAD_VAR', expr.name)
        elif isinstance(expr, BinaryOp):
            self.compile_expression(expr.left)
            self.compile_expression(expr.right)
            op_map = {
                '+': 'ADD', '-': 'SUB', '*': 'MUL', '/': 'DIV', '%': 'MOD',
                '==': 'EQ', '!=': 'NEQ', '<': 'LT', '>': 'GT', '<=': 'LTE', '>=': 'GTE',
                'and': 'AND', 'or': 'OR'
            }
            self.emit(op_map[expr.op])
        elif isinstance(expr, UnaryOp):
            self.compile_expression(expr.operand)
            if expr.op == '-':
                self.emit('NEG')
            elif expr.op == 'not':
                self.emit('NOT')
        elif isinstance(expr, FuncCall):
            self.compile_func_call(expr)

    def compile_func_call(self, expr):
        for arg in expr.args:
            self.compile_expression(arg)
        self.emit('CALL', expr.name, len(expr.args))

def compile_code(code):
    from parser import parse
    ast = parse(code)
    compiler = Compiler()
    return compiler.compile_program(ast)

if __name__ == "__main__":
    sample_code = """
    func main(): void begin
        var x: int = 10;
        print(x + 5);
    end
    """
    functions = compile_code(sample_code)
    for name, (nparams, bytecode) in functions.items():
        print(f"Function {name}({nparams} params):")
        for i, inst in enumerate(bytecode):
            print(f"  {i:04d}: {inst}")
