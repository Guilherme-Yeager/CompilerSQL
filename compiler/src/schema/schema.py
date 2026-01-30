import json


class Schema():

    def __init__(self):
        self.nome_banco_atual = "master"
        self.nome_schema_atual = "dbo"
        self.caminho_catalogo = "compiler/resources/catalog.json"
        with open(self.caminho_catalogo, 'r') as file:
            self.catalogo = json.load(file)
        self.schema = {}

    def listar_bancos(self):
        '''
        Busca os bancos disponíveis no catálogo.

        Return:
            list[str]: Uma lista contendo os nomes dos bancos.
        '''
        return list(self.catalogo.keys())
        
    def listar_schemas(self):
        '''
        Busca os schemas disponíveis no arquivo de catálogo.

        Return:
            list[str]: Uma lista contendo os nomes dos schemas.
        '''
        return list(self.catalogo[self.nome_banco_atual].keys())[1:]

    def carregar_schema(self):
        '''
        Busca no catálogo os dados de um schema específico com o nome 
        armazenado em 'self.nome_schema_atual' e atribui as informações 
        no atributo 'self.schema'
        '''
        self.schema = self.catalogo[self.nome_banco_atual][self.nome_schema_atual]

    def existe_banco(self, nome_banco):
        '''
        Verifica se um banco existe no catálogo.

        Args:
            nome_banco (str): O nome do banco a ser buscado.

        Return:
            bool: True caso o banco seja encontrado, False caso contrário.
        '''
        nome_banco = nome_banco.lower()
        return nome_banco in self.listar_bancos()
        
    def existe_tabela(self, nome_tabela):
        '''
        Verifica se uma tabela existe no schema atual.

        Args:
            nome_tabela (str): O nome da tabela a ser buscada.

        Return:
            bool: True caso a tabela seja encontrada, False caso contrário.
        '''
        nome_tabela = nome_tabela.lower()
        return nome_tabela in list(self.schema)[1:] and self.schema[nome_tabela].get("bindable", "") == "table"

    def existe_coluna(self, nome_tabela, nome_coluna):
        '''
        Verifica se uma coluna existe no schema atual.

        Args:
            nome_tabela (str): O nome da tabela que a coluna pode estar.
            nome_coluna (str): O nome da coluna a ser buscada.

        Return:
            bool: True caso a coluna seja encontrada, False caso contrário.
        '''
        if self.existe_tabela(nome_tabela):
            return nome_coluna.lower() in self.schema[nome_tabela.lower()]["columns"]
        return False

    def tipo_coluna_compativel(self, nome_tabela, nome_coluna, tipo_esperado):
        '''
        Verifica se o tipo de uma coluna é compatível.

        Args:
            nome_tabela (str): O nome da tabela que a coluna pode estar.
            nome_coluna (str): O nome da coluna que pode existir na tabela.
            tipo_esperado (str): o tipo a ser analisado.

        Return:
            bool: True caso o tipo seja compatível, False caso contrário.
        '''
        if self.existe_coluna(nome_tabela, nome_coluna):
            return tipo_esperado.lower() == self.schema[nome_tabela]["columns"][nome_coluna][0].lower()
        return False

    def buscar_restricao_coluna(self, nome_tabela, nome_coluna):
        '''
        Busca as restrições de uma coluna.

        Args:
            nome_tabela (str): O nome da tabela que a coluna pode estar.
            nome_coluna (str): O nome da coluna que pode existir na tabela.

        Return:
            list (str): Uma lista contendo as restrições da coluna.
        '''
        if self.existe_coluna(nome_tabela, nome_coluna):
            return self.schema[nome_tabela]["columns"][nome_coluna][1:]
        return []

    def definir_banco_atual(self, nome_banco_atual):
        '''
        Define um novo banco para a sessão atual.

        Args:
            nome_banco_atual (str): O nome do banco.
        '''
        self.nome_banco_atual = nome_banco_atual
    
    def definir_nome_schema_atual(self, nome_schema_atual):
        '''
        Define um novo schema para a sessão atual.

        Args:
            nome_schema_atual (str): O nome do schema.
        '''
        self.nome_schema_atual = nome_schema_atual
        self.carregar_schema()