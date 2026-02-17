import json


class Schema():

    def __init__(self):
        self.nome_banco_atual = "master"
        self.nome_schema_atual = "dbo"
        self.caminho_catalogo = "compiler/resources/catalog.json"
        self.caminho_log = "compiler/resources/transactions.log"
        self.catalogo = {}
        try:
            with open(self.caminho_catalogo, 'r') as file:
                self.catalogo = json.load(file)
        except FileNotFoundError:
            print(
                f"[Aviso] Catálogo não encontrado, foi adicionado o banco padrão.")
            self.catalogo = {
                "master": {
                    "bindable": "database",
                    "dbo": {
                        "bindable": "scheme"
                    }
                },
            }
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
        if not self.existe_banco(self.nome_banco_atual):
            self.nome_banco_atual = "master"
            self.nome_schema_atual = "dbo"
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

    def existe_tabela_insert(self, nome_tabela):
        nome_tabela = nome_tabela.lower()
        if not self.existe_banco(self.nome_banco_atual):
            return False
        if not self.schema:
            self.carregar_schema()
        return nome_tabela in self.schema and self.schema[nome_tabela].get("bindable", "") == "table"


    def existe_tabela(self, nome_tabela):
        '''
        Verifica se uma tabela existe no schema atual.

        Args:
            nome_tabela (str): O nome da tabela a ser buscada.

        Return:
            bool: True caso a tabela seja encontrada, False caso contrário.
        '''
        nome_tabela = nome_tabela.lower()
        if not self.existe_banco(self.nome_banco_atual):
            return False
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

    def buscar_tipo_coluna(self, nome_tabela, nome_coluna):
        '''
        Busca o tipo de uma coluna.

        Args:
            nome_tabela (str): O nome da tabela que a coluna pode estar.
            nome_coluna (str): O nome da coluna que pode existir na tabela.

        Return:
            str: Tipo da coluna desejada.
            None: Caso a coluna não exista na tabela atual.
        '''
        if self.existe_coluna(nome_tabela, nome_coluna):
            return self.schema[nome_tabela.lower()]["columns"][nome_coluna.lower()][0].lower()
        return None

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

    def drop_database_catalogo(self, nome_banco):
        '''
        Remove um banco do catálogo.

        Args:
            nome_banco (str): O nome do banco a ser removido.
        
        Returns:
            bool: True se o banco foi removido, False caso contrário.
        '''
        nome_banco = nome_banco.lower()
        if nome_banco in ['master', 'tempdb', 'model', 'msdb']:
            return False
        if self.existe_banco(nome_banco):
            self.catalogo.pop(nome_banco, None)
            return True
        return False
    
    def drop_table_catalogo(self, nome_tabela):
        '''
        Remove uma tabela do catálogo.

        Args:
            nome_tabela (str): O nome da tabela a ser removida.

        Returns:
            bool: True se a tabela foi removida, False caso contrário.
        '''
        if self.existe_tabela(nome_tabela):
            self.catalogo[self.nome_banco_atual][self.nome_schema_atual].pop(nome_tabela.lower(), None)
            return True
        return False

    def create_database_catalogo(self, nome_banco):
        '''
        Adiciona um banco ao catálogo.

        Args:
            nome_banco (str): O nome do banco a ser adicionado.

        Returns:
            bool: True se o banco foi adicionado, False caso contrário.
        '''
        nome_banco = nome_banco.lower()
        if not self.existe_banco(nome_banco):
            self.catalogo[nome_banco] = {"bindable": "database", "dbo": {"bindable": "scheme"}}
            return True
        return False

    def atualizar_catalogo(self):
        '''
        Atualiza o catálogo para o estado inicial.
        '''
        self.reseta_catalogo()
        self.carregar_schema()
    
    def reseta_catalogo(self):
        '''
        Atualiza fisicamente o catálogo com as operações de criação e remoção de bancos e tabelas realizadas, 
        lendo o arquivo de log de transações.
        '''
        catalogo = None

        with open(self.caminho_catalogo, 'r') as file:
            catalogo = json.load(file)
        
        self.catalogo = catalogo

        with open(self.caminho_log, 'r') as file:
            linhas = file.readlines()
        
        if not linhas:
            return
        
        for linha in linhas:
            partes = [item.strip() for item in linha.split(',')]
            tipo_operacao, tipo_objeto, caminho = partes[0].lower(), partes[1].lower(), partes[2].lower()
            caminho_partes = caminho.split('/')
            if tipo_operacao == 'd':
                if tipo_objeto == 'database':
                    database = caminho_partes[1]
                    del catalogo[database]
                elif tipo_objeto == 'table':
                    database, schema, table = caminho_partes[1], caminho_partes[3], caminho_partes[5]
                    del catalogo[database][schema][table]
                    
        with open(self.caminho_catalogo, 'w') as file:
            json.dump(self.catalogo, file, indent=4)

        with open(self.caminho_log, 'w') as file:
            pass