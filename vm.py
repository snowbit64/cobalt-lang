class CVM:
    def __init__(self, functions):
        self.functions = functions # name -> (num_params, bytecode)
        self.stack = []
        self.call_stack = []
        self.globals = {}
        self.locals = [{}] # Stack of local environments

    def push(self, val):
        self.stack.append(val)

    def pop(self):
        if not self.stack:
            raise RuntimeError("Pilha vazia")
        return self.stack.pop()

    def run(self, function_name, args=[]):
        if function_name not in self.functions:
            raise RuntimeError(f"Função {function_name} não encontrada")
        
        num_params, bytecode = self.functions[function_name]
        if len(args) != num_params:
            raise RuntimeError(f"Função {function_name} espera {num_params} argumentos, mas recebeu {len(args)}")
        
        # Preparar ambiente local
        local_env = {}
        # Em Cobalt, os parâmetros são carregados no ambiente local
        # No entanto, na nossa implementação de CALL, os argumentos já estão na pilha.
        # Mas para a chamada inicial 'run', passamos os args diretamente.
        
        # Se for a chamada inicial, vamos simular a pilha
        for arg in args:
            self.push(arg)
            
        return self.execute(function_name)

    def execute(self, function_name):
        num_params, bytecode = self.functions[function_name]
        
        # Criar novo frame
        local_env = {}
        # Pop argumentos da pilha e colocar no local_env (na ordem inversa)
        # No entanto, para facilitar, vamos assumir que os argumentos são passados via pilha
        # e o compilador gera LOAD_VAR para acessá-los.
        # Mas precisamos saber os nomes dos parâmetros!
        # Vamos ajustar o compilador para emitir STORE_VAR para cada parâmetro no início da função.
        
        # Por enquanto, vamos manter simples.
        self.locals.append(local_env)
        
        ip = 0
        while ip < len(bytecode):
            inst = bytecode[ip]
            opcode = inst[0]
            args = inst[1:]
            
            if opcode == 'PUSH_INT' or opcode == 'PUSH_FLOAT' or opcode == 'PUSH_STRING' or opcode == 'PUSH_BOOL':
                self.push(args[0])
            elif opcode == 'LOAD_VAR':
                name = args[0]
                if name in self.locals[-1]:
                    self.push(self.locals[-1][name])
                elif name in self.globals:
                    self.push(self.globals[name])
                else:
                    raise RuntimeError(f"Variável {name} não definida")
            elif opcode == 'STORE_VAR':
                name = args[0]
                val = self.pop()
                self.locals[-1][name] = val
                # Se for no nível global (futuro), atualizar globals
            elif opcode == 'ADD':
                b = self.pop()
                a = self.pop()
                self.push(a + b)
            elif opcode == 'SUB':
                b = self.pop()
                a = self.pop()
                self.push(a - b)
            elif opcode == 'MUL':
                b = self.pop()
                a = self.pop()
                self.push(a * b)
            elif opcode == 'DIV':
                b = self.pop()
                a = self.pop()
                self.push(a / b)
            elif opcode == 'MOD':
                b = self.pop()
                a = self.pop()
                self.push(a % b)
            elif opcode == 'EQ':
                b = self.pop()
                a = self.pop()
                self.push(a == b)
            elif opcode == 'NEQ':
                b = self.pop()
                a = self.pop()
                self.push(a != b)
            elif opcode == 'LT':
                b = self.pop()
                a = self.pop()
                self.push(a < b)
            elif opcode == 'GT':
                b = self.pop()
                a = self.pop()
                self.push(a > b)
            elif opcode == 'LTE':
                b = self.pop()
                a = self.pop()
                self.push(a <= b)
            elif opcode == 'GTE':
                b = self.pop()
                a = self.pop()
                self.push(a >= b)
            elif opcode == 'AND':
                b = self.pop()
                a = self.pop()
                self.push(a and b)
            elif opcode == 'OR':
                b = self.pop()
                a = self.pop()
                self.push(a or b)
            elif opcode == 'NOT':
                a = self.pop()
                self.push(not a)
            elif opcode == 'NEG':
                a = self.pop()
                self.push(-a)
            elif opcode == 'PRINT':
                val = self.pop()
                print(val)
            elif opcode == 'JUMP':
                ip = args[0]
                continue
            elif opcode == 'JUMP_IF_FALSE':
                val = self.pop()
                if not val:
                    ip = args[0]
                    continue
            elif opcode == 'CALL':
                func_name = args[0]
                num_args = args[1]
                # Os argumentos já estão na pilha.
                # Chamada recursiva da execução
                result = self.execute(func_name)
                self.push(result)
            elif opcode == 'RETURN':
                result = self.pop()
                self.locals.pop()
                return result
            elif opcode == 'POP':
                self.pop()
            
            ip += 1
        
        self.locals.pop()
        return None

if __name__ == "__main__":
    from compiler import compile_code
    sample_code = """
    func main(): void begin
        var x: int = 10;
        if x > 5 then
            print("x é maior que 5");
        else
            print("x é menor ou igual a 5");
        end
        
        print("Soma de 10 + 20:");
        print(somar(10, 20));
    end

    func somar(a: int, b: int): int begin
        return a + b;
    end
    """
    functions = compile_code(sample_code)
    vm = CVM(functions)
    vm.run('main')
