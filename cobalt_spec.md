# Especificação da Linguagem Cobalt

## 1. Introdução

Cobalt é uma linguagem de programação compilada em bytecode, projetada para ser simples, segura e eficiente. Ela visa fornecer uma sintaxe clara e concisa, facilitando o desenvolvimento de aplicações robustas e de alto desempenho. A linguagem será fortemente tipada e terá um modelo de memória gerenciado para evitar erros comuns de programação.

## 2. Filosofia e Objetivos

*   **Simplicidade**: Manter a sintaxe e a semântica da linguagem o mais simples possível, reduzindo a curva de aprendizado.
*   **Segurança**: Incorporar recursos que minimizem erros em tempo de execução, como tipagem forte e gerenciamento automático de memória.
*   **Eficiência**: Compilar para bytecode otimizado para uma máquina virtual leve, garantindo bom desempenho.
*   **Portabilidade**: O bytecode gerado deve ser executável em qualquer plataforma que possua uma Máquina Virtual Cobalt (CVM).
*   **Concorrência**: Suporte a modelos de concorrência simples e seguros (a ser definido em fases posteriores).

## 3. Tipos de Dados

Cobalt suportará os seguintes tipos de dados primitivos:

| Tipo de Dado | Descrição                                        | Exemplo          |
| :----------- | :----------------------------------------------- | :--------------- |
| `int`        | Inteiros de 64 bits com sinal                    | `10`, `-5`, `0`  |
| `float`      | Números de ponto flutuante de 64 bits (IEEE 754) | `3.14`, `-0.5`   |
| `bool`       | Valores booleanos                                | `true`, `false`  |
| `string`     | Sequências de caracteres Unicode                 | `"Olá, Mundo!"` |
| `void`       | Representa a ausência de valor (para funções)    | N/A              |

## 4. Variáveis e Constantes

### 4.1. Declaração de Variáveis

Variáveis são declaradas usando a palavra-chave `var`, seguida pelo nome da variável, um dois pontos (`:`) e o tipo de dado. A inicialização é opcional.

```cobalt
var idade: int;
var nome: string = "Alice";
var is_active: bool = true;
```

### 4.2. Declaração de Constantes

Constantes são declaradas usando a palavra-chave `const`, seguida pelo nome da constante, um dois pontos (`:`) e o tipo de dado. A inicialização é obrigatória.

```cobalt
const PI: float = 3.14159;
const MAX_USERS: int = 1000;
```

## 5. Operadores

Cobalt suportará operadores aritméticos, relacionais, lógicos e de atribuição.

### 5.1. Operadores Aritméticos

| Operador | Descrição        | Exemplo      |
| :------- | :--------------- | :----------- |
| `+`      | Adição           | `a + b`      |
| `-`      | Subtração        | `a - b`      |
| `*`      | Multiplicação    | `a * b`      |
| `/`      | Divisão          | `a / b`      |
| `%`      | Módulo           | `a % b`      |

### 5.2. Operadores Relacionais

| Operador | Descrição             | Exemplo      |
| :------- | :-------------------- | :----------- |
| `==`     | Igual a               | `a == b`     |
| `!=`     | Diferente de          | `a != b`     |
| `<`      | Menor que             | `a < b`      |
| `>`      | Maior que             | `a > b`      |
| `<=`     | Menor ou igual a      | `a <= b`     |
| `>=`     | Maior ou igual a      | `a >= b`     |

### 5.3. Operadores Lógicos

| Operador | Descrição | Exemplo         |
| :------- | :-------- | :-------------- |
| `and`    | E lógico  | `a and b`       |
| `or`     | Ou lógico | `a or b`        |
| `not`    | Não lógico| `not a`         |

### 5.4. Operadores de Atribuição

| Operador | Descrição  | Exemplo      |
| :------- | :--------- | :----------- |
| `=`      | Atribuição | `x = 10`     |

## 6. Estruturas de Controle de Fluxo

### 6.1. Condicionais (if/else)

```cobalt
if idade >= 18 then
    print("Maior de idade");
else
    print("Menor de idade");
end
```

### 6.2. Laços (while)

```cobalt
var contador: int = 0;
while contador < 5 do
    print(contador);
    contador = contador + 1;
end
```

## 7. Funções

Funções são declaradas usando a palavra-chave `func`, seguida pelo nome da função, uma lista de parâmetros entre parênteses, um dois pontos (`:`) e o tipo de retorno. O corpo da função é delimitado por `begin` e `end`.

```cobalt
func somar(a: int, b: int): int begin
    return a + b;
end

func saudacao(nome: string): void begin
    print("Olá, " + nome + "!");
end

var resultado: int = somar(10, 20);
saudacao("Mundo");
```

## 8. Comentários

Comentários de linha única começam com `//`.

```cobalt
// Este é um comentário de linha única
var x: int = 10; // Atribui 10 a x
```

Comentários de múltiplas linhas são delimitados por `/*` e `*/`.

```cobalt
/*
Este é um comentário
de múltiplas linhas.
*/
func foo(): void begin
    // ...
end
```

## 9. Palavras-chave Reservadas

As seguintes palavras-chave são reservadas e não podem ser usadas como identificadores:

`var`, `const`, `func`, `if`, `then`, `else`, `end`, `while`, `do`, `return`, `true`, `false`, `and`, `or`, `not`, `int`, `float`, `bool`, `string`, `void`, `print`.

## 10. Funções Built-in (Inicial)

*   `print(value: any): void`: Imprime o valor para a saída padrão.

## 11. Estrutura do Programa

Um programa Cobalt consiste em uma sequência de declarações de variáveis, constantes e funções. A execução começa na função principal (a ser definida, possivelmente `main`).

```cobalt
// Exemplo de programa Cobalt

func main(): void begin
    var mensagem: string = "Bem-vindo ao Cobalt!";
    print(mensagem);

    var num1: int = 5;
    var num2: int = 3;
    var soma: int = somar(num1, num2);
    print("A soma é: " + soma);

    if soma > 10 then
        print("Soma maior que 10");
    else
        print("Soma menor ou igual a 10");
    end
end

func somar(a: int, b: int): int begin
    return a + b;
end
```

## 12. Próximos Passos

Esta especificação inicial será expandida para incluir detalhes sobre:

*   Estruturas de dados mais complexas (arrays, structs/objetos).
*   Módulos e importação.
*   Tratamento de erros e exceções.
*   Modelo de concorrência.
*   Especificação do formato do bytecode.
*   Detalhes da Máquina Virtual Cobalt (CVM).
