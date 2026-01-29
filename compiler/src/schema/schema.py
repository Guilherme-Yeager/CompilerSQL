import json


class Schema():

    def __init__(self):
        self.nome_schema_atual = ""
        self.objetos = {}
        self.caminho_catalogo = "compiler/resources/catalog.json"

    def listar_schemas(self):
        '''
        Busca os schemas disponíveis no arquivo de catálogo.

        Return:
            list[str]: Uma lista contendo os nomes dos schemas.
        '''
        with open(self.caminho_catalogo, 'r') as file:
            return list(json.load(file).keys())

    def carregar_schema(self):
        '''
        Busca no arquivo de catálogo os dados de um schema específico
        com o nome armazenado em 'self.nome_schema_atual' e atribui as informações 
        no atributo 'self.objetos'
        '''
        with open(self.caminho_catalogo, 'r') as file:
            self.objetos = json.load(file).get(self.nome_schema_atual, {})

    def existe_tabela(self, nome_tabela):
        '''
        Verifica se uma tabela existe no schema atual.

        Args:
            nome_tabela (str): O nome da tabela a ser buscada.

        Return:
            bool: True caso a tabela seja encontrada, False caso contrário.
        '''
        nome_tabela = nome_tabela.lower()
        return nome_tabela in self.objetos and self.objetos[nome_tabela].get("bindable", "") == "table"

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
            return nome_coluna.lower() in self.objetos[nome_tabela.lower()]["columns"]
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
            return tipo_esperado.lower() == self.objetos[nome_tabela]["columns"][nome_coluna][0].lower()
        return False

    def buscar_restricao_coluna(self, nome_tabela, nome_coluna):
        '''
        Busca as restrições de uma coluna

        Args:
            nome_tabela (str): O nome da tabela que a coluna pode estar.
            nome_coluna (str): O nome da coluna que pode existir na tabela.

        Return:
            list (str): Uma lista contendo as restrições da coluna.
        '''
        if self.existe_coluna(nome_tabela, nome_coluna):
            return self.objetos[nome_tabela]["columns"][nome_coluna][1:]
        return []

    def definir_nome_schema_atual(self, nome_schema_atual):
        '''
        Define um novo schema para a sessão atual.

        Args:
            nome_schema_atual (str): O nome do schema.
        '''
        self.nome_schema_atual = nome_schema_atual
        self.carregar_schema()
