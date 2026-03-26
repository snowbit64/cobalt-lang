class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self, declarations):
        self.declarations = declarations

class VarDecl(ASTNode):
    def __init__(self, name, type_name, initial_value=None):
        self.name = name
        self.type_name = type_name
        self.initial_value = initial_value

class ConstDecl(ASTNode):
    def __init__(self, name, type_name, initial_value):
        self.name = name
        self.type_name = type_name
        self.initial_value = initial_value

class FuncDecl(ASTNode):
    def __init__(self, name, params, return_type, body):
        self.name = name
        self.params = params
        self.return_type = return_type
        self.body = body

class Param(ASTNode):
    def __init__(self, name, type_name):
        self.name = name
        self.type_name = type_name

class Block(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class IfStmt(ASTNode):
    def __init__(self, condition, then_block, else_block=None):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

class WhileStmt(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class ReturnStmt(ASTNode):
    def __init__(self, value=None):
        self.value = value

class AssignStmt(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class PrintStmt(ASTNode):
    def __init__(self, value):
        self.value = value

class BinaryOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class UnaryOp(ASTNode):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

class Literal(ASTNode):
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name

class FuncCall(ASTNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args
