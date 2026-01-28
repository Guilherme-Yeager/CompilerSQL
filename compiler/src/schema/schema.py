import json

class Schema():

    def __init__(self, schema_atual):
        self.schema_atual = schema_atual
        self.caminho_catalogo = "compiler/resources/catalog.json"
        self.objetos = self.carregar_catalogo()

    def carregar_catalogo(self):
        with open(self.caminho_catalogo, 'r') as file:
            return json.load(file).get(self.schema_atual, {})

    def existe_tabela(self, nome_tabela):
        return nome_tabela in self.objetos

    def existe_coluna(self, nome_tabela, nome_coluna):
        tabela = self.objetos.get(nome_tabela, {})
        return nome_coluna in tabela.get("columns", {})
    
    def tipo_coluna_compativel(self, nome_tabela, nome_coluna, tipo_esperado):
        tabela = self.objetos.get(nome_tabela, {})
        colunas = tabela.get("columns", {})
        info_coluna = colunas.get(nome_coluna)
        if info_coluna:
            tipo_real = info_coluna[0]
            return tipo_real == tipo_esperado
        return False
    
    def buscar_restricao_coluna(self, nome_tabela, nome_coluna):
        tabela = self.objetos.get(nome_tabela, {})
        colunas = tabela.get("columns", {})
        info_coluna = colunas.get(nome_coluna)
        if info_coluna:
            return info_coluna[1:]
        return []
    
