# Dicionario que representa a tabela de simbolos.
symbolTableSemantic = []

INT = 'int'
STRING = 'string'
TYPE = 'type'
BINDABLE = 'bindable'
COLUMNS = 'columns'
TABLE = 'table'
VALUES = 'values'
CLAUSES = 'clauses'
DATABASE = 'database'
SCOPE = 'scope'

# Se DEBUG = -1, imprime conteudo da tabela de símbolos após cada mudança
DEBUG = 0


def printTable():
    global DEBUG
    if DEBUG == -1:
        print('Tabela:', symbolTableSemantic)


def beginScope(nameScope):
    global symbolTableSemantic
    symbolTableSemantic.append({})
    contador_escopos = len(symbolTableSemantic)
    symbolTableSemantic[-1][SCOPE] = f'{nameScope}_{contador_escopos}'
    printTable()


def endScope():
    global symbolTableSemantic
    symbolTableSemantic = symbolTableSemantic[0:-1]
    printTable()

def addCommand(name, database=None, table=None, columns=None, values=None, clauses=None):
    global symbolTableSemantic
    contador_comandos = len(symbolTableSemantic[-1])
    nome_comando = f'{name}_{contador_comandos}'
    symbolTableSemantic[-1][nome_comando] = {
        BINDABLE: name,
        DATABASE: database,
        TABLE: table,
        COLUMNS: columns,
        VALUES: values,
        CLAUSES: clauses
    }
    printTable()


def getBindable(bindableName):
    global symbolTableSemantic
    for i in reversed(range(len(symbolTableSemantic))):
        if (bindableName in symbolTableSemantic[i].keys()):
            return symbolTableSemantic[i].get(bindableName, 'Bindable Desconhecido')
    return None


def getScope(bindableName):
    global symbolTableSemantic
    for i in reversed(range(len(symbolTableSemantic))):
        if (bindableName in symbolTableSemantic[i].keys()):
            return symbolTableSemantic[i].get(SCOPE, 'Escopo Desconhecido')
    return None

def clearSymbolTable():
    global symbolTableSemantic
    symbolTableSemantic = []

def main():
    global DEBUG
    DEBUG = -1
    print('\n# Criando escopo select')
    beginScope('select')
    print('\n# Adicionando comando select')
    addCommand('select', 'funcionario', ['nome'])
    print('\n# Criando escopo subconsulta')
    beginScope('subconsulta')
    print('\n# Adicionando comando de subconsulta')
    addCommand('select', 'empresa', ['id_organizacao'], clauses=['where', 'ord'])
    print('\n# Removendo escopo subconsulta')
    endScope()
    print('\n# Removendo escopo select')
    endScope()
    print('\n# Criando escopo truncate')
    beginScope('truncate')
    print('\n# Adicionando comando truncate')
    addCommand('truncate', 'funcionario')
    print('\n# Removendo escopo truncate')
    endScope()

if __name__ == "__main__":
    main()
