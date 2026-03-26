import sys
from compiler import compile_code
from vm import CVM

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 cobalt.py <arquivo.cobalt>")
        return

    file_path = sys.argv[1]
    try:
        with open(file_path, 'r') as f:
            code = f.read()
        
        functions = compile_code(code)
        vm = CVM(functions)
        
        if 'main' in functions:
            vm.run('main')
        else:
            print("Erro: Função 'main' não encontrada.")
            
    except FileNotFoundError:
        print(f"Erro: Arquivo '{file_path}' não encontrado.")
    except SyntaxError as e:
        print(f"Erro de Sintaxe: {e}")
    except RuntimeError as e:
        print(f"Erro de Execução: {e}")
    except Exception as e:
        print(f"Erro Inesperado: {e}")

if __name__ == "__main__":
    main()
