# Dicionario que representa a tabela de simbolos.
symbolTable = []

INT = 'int'
STRING = 'string'
TYPE = 'type'
BINDABLE = 'bindable'
COLUMNS = 'columns'
TABLE = 'table'
VALUES = 'values'
SCOPE = 'scope'

# Se DEBUG = -1, imprime conteudo da tabela de símbolos após cada mudança
DEBUG = 0


def printTable():
    global DEBUG
    if DEBUG == -1:
        print('Tabela:', symbolTable)


def beginScope(nameScope):
    global symbolTable
    symbolTable.append({})
    contador_escopos = len(symbolTable)
    symbolTable[-1][SCOPE] = f'{nameScope}_{contador_escopos}'
    printTable()


def endScope():
    global symbolTable
    symbolTable = symbolTable[0:-1]
    printTable()


def addCommand(name, table=None, columns=None, values=None):
    global symbolTable
    contador_comandos = len(symbolTable[-1])
    symbolTable[-1][f'{name}_{contador_comandos}'] = {
        BINDABLE: name,
        TABLE: table,
        COLUMNS: columns,
        VALUES: values
    }
    printTable()


def getBindable(bindableName):
    global symbolTable
    for i in reversed(range(len(symbolTable))):
        if (bindableName in symbolTable[i].keys()):
            return symbolTable[i].get(bindableName, 'Bindable Desconhecido')
    return None


def getScope(bindableName):
    global symbolTable
    for i in reversed(range(len(symbolTable))):
        if (bindableName in symbolTable[i].keys()):
            return symbolTable[i].get(SCOPE, 'Escopo Desconhecido')
    return None


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
    addCommand('select', 'empresa', ['id_organizacao'])
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
