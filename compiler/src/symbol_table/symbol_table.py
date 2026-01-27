import json

#Dicionario que representa a tabela de simbolos.
symbolTable = []
INT = 'int'
FLOAT = 'float'
BOOL = 'boolean'
TYPE = 'type'
PARAMS = 'params'
BINDABLE = 'bindable'
FUNCTION = 'fun'
VARIABLE = 'var'
SCOPE = 'scope'
OFFSET = 'offset'
SP = 'sp'

OBJECTS = 'objects'
SCHEMA = 'schema'
TABLE = 'table'
COLUMNS = 'columns'


# Se DEBUG = -1, imprime conteudo da tabela de símbolos após cada mudança
DEBUG = 0
Number = [INT, FLOAT]

curoffset = 0
def printTable():
    global DEBUG
    if DEBUG == -1:
        print(json.dumps(symbolTable, indent=4))


def load_scope_global():
    global symbolTable

    with open('compiler/test/global_scope.json', 'r', encoding='utf-8') as f:
        catalog = json.load(f)


    symbolTable.append({
        SCOPE: "global",
        OBJECTS: {}
    })

    global_objects = symbolTable[-1][OBJECTS]

    for schema_name, schema_data in catalog.items():
        global_objects[schema_name] = {
            BINDABLE: SCHEMA,
            OBJECTS: {}
        }

        for obj_name, obj_data in schema_data.items():
            if obj_name == BINDABLE:
                continue

            if obj_data[BINDABLE] == TABLE:
                global_objects[schema_name][OBJECTS][obj_name] = {
                    BINDABLE: TABLE,
                    COLUMNS: obj_data[COLUMNS]
                }
    printTable()

def beginScope(nameScope):
    global symbolTable
    symbolTable.append({})
    symbolTable[-1][SCOPE] = nameScope
    printTable()

def endScope():
    global symbolTable
    symbolTable = symbolTable[0:-1]
    printTable()

def addVar(name, type, offset = None):
    global symbolTable
    symbolTable[-1][name] = {BINDABLE: VARIABLE, TYPE : type, OFFSET: offset}
    printTable()

def addFunction(name, params, returnType):
    global symbolTable
    symbolTable[-1][name] = {BINDABLE: FUNCTION, PARAMS: params, TYPE : returnType}
    printTable()

def getBindable(bindableName):
    global symbolTable
    for i in reversed(range(len(symbolTable))):
        if (bindableName in symbolTable[i].keys()):
            return symbolTable[i][bindableName]
    return None

def getScope(bindableName):
    global symbolTable
    for i in reversed(range(len(symbolTable))):
        if (bindableName in symbolTable[i].keys()):
            return symbolTable[i][SCOPE]
    return None

def main():
    global DEBUG
    DEBUG = -1
    print('\n# Carregando escopo global')
    load_scope_global()
    

if __name__ == "__main__":
    main()