<h1 align="center">🗄️ CompilerSql</h1>

Um compilador para a linguagem SQL que, além de implementar as etapas léxica, sintática, semântica e geração de assembly também simula a integração com um SGBD (Sistema Gerenciador de Banco de Dados) real, reproduzindo a conversação interna com um banco de dados.

<h1 align="center">📁 Estrutura do projeto</h1>

A estrutura do projeto foi organizada de forma modular, separando claramente cada fase do compilador SQL e seus componentes auxiliares.

```shell
  compiler/
  ├── resources/
  |   ├── databases/ # Bancos (camada física)
  |   ├── MARS/ # Simulador para execução do código (.asm)
  |   ├── output.asm # Resultado da geração de código
  |   ├── transactions.log # Registros das transações realizadas durante a geração de código
  │   └── catalog.json # Catálogo fornecido pelo SGBD adaptado ao escopo do projeto 
  ├── src/
  │   └── assembly/ # Etapa de geração de código
  |   |   ├── __init__.py
  |   |   ├── assembly_visitor.py
  |   |   └── symbol_table_asm.py
  │   └── lexer/ # Etapa léxica
  |   |   ├── __init__.py
  |   |   └── lexer.py
  │   └── parser/ # Etapa sintática
  |   |   ├── __init__.py
  |   |   └── sintatico.py
  │   └── schema/ # Camada responsável por analisar o catálogo e fornecer as informações do schema atual
  |   |   ├── __init__.py
  |   |   └── schema.py
  │   └── screen/ # GUI
  |   |   ├── __init__.py
  |   |   └── screen.py
  │   └── semantic/ # Etapa semântica
  |   |   ├── __init__.py
  |   |   ├── semantic_visitor.py
  |   |   └── symbol_table.py 
  │   └── sintaxe/ # AST
  |   |   ├── __init__.py
  |   |   └── sintaxe_abstrata.py
  |   └── visitor/ # Visitor Pretty Printer
  |   |   ├── __init__.py
  |   |   ├── abstract_visitor.py
  |   |   ├── aux_visitor_print.py
  |   |   └── visitor.py
  |   ├── __init__.py
  |   └── main.py
  ├── test/
  |   └── test.sql # Arquivo padrão de entrada
  └── docs/
      ├── glc.md
      ├── lexico.md
      └── sintatico.md
```

<h1 align="center">모 Visão arquitetural</h1>

<img width="5400" height="3531" alt="Sem título-2025-07-30-1115" src="https://github.com/user-attachments/assets/f3f476a9-d952-4cba-9334-1f15236a6dca" />

<h1 align="center">🎮 Simulador MIPS</h1>

Para executar o assembly MIPS gerado na etapa de geração de código, este projeto utiliza uma versão customizada do **MARS**.
As necessidades do compilador exigiram a manipulação de diretórios e arquivos de dados (CSV), delegando, assim, essas tarefas ao java através de **Syscalls** personalizadas.

* **Projeto Original:** [MARS - MIPS Assembler and Runtime Simulator](https://github.com/dpetersanderson/MARS).
* **Customizações desenvolvidas:** ...
* **Localização no Projeto:** O core modificado reside em `compiler/resources/MARS`.

<h1 align="center">📃 Integração com o SGBD</h1>

Nesta etapa, assume-se que o SGBD fornece ao compilador, por meio do caminho padrão `resources/catalog.json`, as informações necessárias para a análise semântica.
Para este escopo do projeto, o catálogo contém apenas os **schemas**, suas **tabelas** e as
respectivas **colunas**, simulando o catálogo interno de um sistema gerenciador de banco de dados real.
A seguir, um exemplo de catálogo padrão utilizado pelo compilador:

```json
{
    "master": {
        "bindable": "database",
        "dbo": {
            "bindable": "scheme"
        }
    },
    "model": {
        "bindable": "database",
        "dbo": {
            "bindable": "scheme"
        }
    },
    "msdb": {
        "bindable": "database",
        "dbo": {
            "bindable": "scheme"
        }
    },
    "tempdb": {
        "bindable": "database",
        "dbo": {
            "bindable": "scheme"
        }
    },
    "engs_ufs": {
        "bindable": "database",
        "dbo": {
            "bindable": "scheme"
        },
        "biotlab": {
            "bindable": "scheme",
            "funcionario": {
                "bindable": "table",
                "columns": {
                    "id": [
                        "int",
                        "primary key"
                    ],
                    "nome": [
                        "varchar(50)",
                        "not null"
                    ],
                    "cpf": [
                        "varchar(11)",
                        "not null",
                        "unique"
                    ]
                }
            },
            "animal": {
                "bindable": "table",
                "columns": {
                    "id": [
                        "int",
                        "primary key"
                    ],
                    "nome": [
                        "string",
                        "not null"
                    ],
                    "id_bioterio": [
                        "int",
                        "foreign key"
                    ]
                }
            }
        },
        "cuidado": {
            "bindable": "scheme",
            "paciente": {
                "bindable": "table",
                "columns": {
                    "id": [
                        "int",
                        "primary key"
                    ],
                    "nome": [
                        "varchar(50)",
                        "not null"
                    ]
                }
            }
        }
    },
    "nunes": {
        "bindable": "database",
        "dbo": {
            "bindable": "scheme"
        }
    }
}
```


⚠️ Projeto em andamento...
