symbolTable = []

INT = 'int'
STRING = 'string'
BINDABLE = 'bindable'
DATABASE = 'database'
TABLE = 'table'
VALUES = 'values'
CLAUSES = 'clauses'
COLUMNS = 'columns'
SCOPE = 'scope'
OFFSET = 'offset'
SP = 'sp' 
TYPE = 'type'

DEBUG = -1

def beginScope(nameScope):
    global symbolTable
    symbolTable.append({})
    symbolTable[-1][SP] = 0
    contador = len(symbolTable)
    symbolTable[-1][SCOPE] = f'{nameScope}_{contador}'

def endScope():
    global symbolTable
    if len(symbolTable) > 0:
        symbolTable.pop()

def addCommand(name, database=None, table=None, columns=None, values=None, clauses=None, size=4):
    global symbolTable
    if size % 4 != 0:
        size += (4 - (size % 4))
    symbolTable[-1][SP] -= size
    contador_comandos = len(symbolTable[-1])
    nome_comando = f'{name}_{contador_comandos}'
    symbolTable[-1][nome_comando] = {
        BINDABLE: name,
        DATABASE: database,
        TABLE: table,
        COLUMNS: columns,
        VALUES: values,
        CLAUSES: clauses,
        OFFSET: symbolTable[-1][SP],
        TYPE: STRING if name == 'select' else INT
    }

def getSP():
    return symbolTable[-1][SP]

def getBindable(bindableName):
    for i in reversed(range(len(symbolTable))):
        if bindableName in symbolTable[i]:
            return symbolTable[i][bindableName]
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
