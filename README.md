# Linguagem de Programação Cobalt

**Autor:** Manus AI

## 1. Introdução

Cobalt é uma linguagem de programação compilada em bytecode, projetada para ser simples, segura e eficiente. Ela visa fornecer uma sintaxe clara e concisa, facilitando o desenvolvimento de aplicações robustas e de alto desempenho. A linguagem é fortemente tipada e possui um modelo de execução baseado em uma Máquina Virtual (CVM - Cobalt Virtual Machine).

Este repositório contém a especificação da linguagem, bem como a implementação de referência do Lexer, Parser, Compilador e Máquina Virtual em Python.

## 2. Filosofia e Objetivos

*   **Simplicidade**: Manter a sintaxe e a semântica da linguagem o mais simples possível, reduzindo a curva de aprendizado.
*   **Segurança**: Incorporar recursos que minimizem erros em tempo de execução, como tipagem forte.
*   **Eficiência**: Compilar para bytecode otimizado para uma máquina virtual leve, garantindo bom desempenho.
*   **Portabilidade**: O bytecode gerado deve ser executável em qualquer plataforma que possua uma Máquina Virtual Cobalt (CVM).

## 3. Especificação da Linguagem

### 3.1. Tipos de Dados

Cobalt suporta os seguintes tipos de dados primitivos:

| Tipo de Dado | Descrição                                        | Exemplo          |
| :----------- | :----------------------------------------------- | :--------------- |
| `int`        | Inteiros com sinal                               | `10`, `-5`, `0`  |
| `float`      | Números de ponto flutuante                       | `3.14`, `-0.5`   |
| `bool`       | Valores booleanos                                | `true`, `false`  |
| `string`     | Sequências de caracteres                         | `"Olá, Mundo!"` |
| `void`       | Representa a ausência de valor (para funções)    | N/A              |

### 3.2. Variáveis e Constantes

Variáveis são declaradas usando a palavra-chave `var`, e constantes com `const`.

```cobalt
var idade: int;
var nome: string = "Alice";
const PI: float = 3.14159;
```

### 3.3. Operadores

Cobalt suporta os operadores padrão:
*   **Aritméticos**: `+`, `-`, `*`, `/`, `%`
*   **Relacionais**: `==`, `!=`, `<`, `>`, `<=`, `>=`
*   **Lógicos**: `and`, `or`, `not`
*   **Atribuição**: `=`

### 3.4. Estruturas de Controle de Fluxo

**Condicionais (if/else):**

```cobalt
if idade >= 18 then
    print("Maior de idade");
else
    print("Menor de idade");
end
```

**Laços (while):**

```cobalt
var contador: int = 0;
while contador < 5 do
    print(contador);
    contador = contador + 1;
end
```

### 3.5. Funções

Funções são declaradas com a palavra-chave `func`. O corpo da função é delimitado por `begin` e `end`.

```cobalt
func somar(a: int, b: int): int begin
    return a + b;
end
```

### 3.6. Comentários

*   Linha única: `// comentário`
*   Múltiplas linhas: `/* comentário */`

## 4. Arquitetura do Compilador e VM

A implementação de referência do Cobalt é dividida em quatro componentes principais:

1.  **Lexer (`lexer.py`)**: Converte o código-fonte em uma sequência de tokens.
2.  **Parser (`parser.py`)**: Analisa os tokens e constrói uma Árvore de Sintaxe Abstrata (AST).
3.  **Compilador (`compiler.py`)**: Percorre a AST e gera o bytecode Cobalt.
4.  **Máquina Virtual (`vm.py`)**: Executa o bytecode gerado utilizando uma arquitetura baseada em pilha.

### 4.1. Conjunto de Instruções (Bytecode)

A CVM suporta as seguintes instruções principais:
*   `PUSH_INT`, `PUSH_FLOAT`, `PUSH_STRING`, `PUSH_BOOL`: Empilha literais.
*   `LOAD_VAR`, `STORE_VAR`: Carrega e armazena variáveis locais/globais.
*   `ADD`, `SUB`, `MUL`, `DIV`, `MOD`: Operações aritméticas.
*   `EQ`, `NEQ`, `LT`, `GT`, `LTE`, `GTE`: Operações relacionais.
*   `AND`, `OR`, `NOT`, `NEG`: Operações lógicas e unárias.
*   `JUMP`, `JUMP_IF_FALSE`: Controle de fluxo.
*   `CALL`, `RETURN`: Chamada e retorno de funções.
*   `PRINT`: Imprime o valor no topo da pilha.

## 5. Como Usar

### 5.1. Requisitos

*   Python 3.x

### 5.2. Executando um Programa Cobalt

Você pode executar um arquivo `.cobalt` usando o script principal `cobalt.py`:

```bash
python3 cobalt.py arquivo.cobalt
```

### 5.3. Exemplos

**Fibonacci (`fibonacci.cobalt`):**

```cobalt
func fib(n: int): int begin
    if n <= 1 then
        return n;
    end
    return fib(n - 1) + fib(n - 2);
end

func main(): void begin
    var n: int = 10;
    print("Calculando Fibonacci de:");
    print(n);
    
    var resultado: int = fib(n);
    print("O resultado é:");
    print(resultado);
end
```

**Loop While (`loop_test.cobalt`):**

```cobalt
func main(): void begin
    var i: int = 1;
    var soma: int = 0;
    
    print("Somando números de 1 a 5:");
    
    while i <= 5 do
        print(i);
        soma = soma + i;
        i = i + 1;
    end
    
    print("A soma total é:");
    print(soma);
end
```

## 6. Próximos Passos

A linguagem Cobalt pode ser expandida no futuro com:
*   Estruturas de dados complexas (Arrays, Structs/Classes).
*   Sistema de módulos e importações.
*   Tratamento de exceções.
*   Otimizações no compilador e na VM.
## 7. Realce de Sintaxe (MT Manager)

O arquivo `cobalt.mtsx` fornece realce de sintaxe para o MT Manager. Para instalar, basta abrir o arquivo no MT Manager e seguir as instruções.
