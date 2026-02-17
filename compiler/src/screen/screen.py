import tkinter as tk
import subprocess
import os
import compiler.src.assembly.assembly_visitor as av
from compiler.src.schema.schema import Schema


class Screen():
    def __init__(self, executar_lexico, executar_sintatico, executar_semantico):
        self.executar_lexico = executar_lexico
        self.executar_sintatico = executar_sintatico
        self.executar_semantico = executar_semantico
        self.schema = Schema()

        self.janela = tk.Tk()
        self.opcao_analisador = tk.IntVar(value=1)
        self.opcao_saida = tk.IntVar(value=1)
        self.nome_schema_atual = tk.StringVar()
        self.nome_banco_atual = tk.StringVar()
        self.nome_banco_atual.trace_add("write", self.gerenciar_nome_banco)
        self.nome_schema_atual.trace_add("write", self.gerenciar_nome_schema)
        self.menu_schemas = None
        self.caixa_texto = None
        self.schema.atualizar_catalogo()
        self.setup_screen()

    def setup_screen(self):
        self.janela.title("CompilerSql")
        largura, altura = 800, 600
        pos_x = (self.janela.winfo_screenwidth() - largura) // 2
        pos_y = (self.janela.winfo_screenheight() - altura) // 2
        self.janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")
        self.janela.resizable(False, False)
        self.add_menu()
        self.add_widgets()

    def add_menu(self):
        menu = tk.Menu(self.janela)
        menu_analisador = tk.Menu(menu, tearoff=0)
        menu_analisador.add_radiobutton(
            label="Léxico", variable=self.opcao_analisador, value=1)
        menu_analisador.add_radiobutton(
            label="Sintático", variable=self.opcao_analisador, value=2)
        menu_analisador.add_radiobutton(
            label="Semântico", variable=self.opcao_analisador, value=3)
        menu.add_cascade(label="Analisador", menu=menu_analisador)
        menu_gerador_assembly = tk.Menu(menu, tearoff=0)
        menu_gerador_assembly.add_command(
            label="Gerar MIPS (.asm)",
            command=lambda: self.gerar_assembly(self.nome_banco_atual.get(), self.nome_schema_atual.get(
            ), self.schema, self.caixa_texto.get("1.0", tk.END))
        )
        menu.add_cascade(label="Assembly", menu=menu_gerador_assembly)
        menu_simulador = tk.Menu(menu, tearoff=0)
        menu_simulador.add_command(
            label="MARS", 
            command=self.abrir_mars
        )
        menu.add_cascade(label="Simulador", menu=menu_simulador)
        menu_saida = tk.Menu(menu, tearoff=0)
        menu_saida.add_radiobutton(
            label="SQL", variable=self.opcao_saida, value=1)
        menu_saida.add_radiobutton(
            label="XML", variable=self.opcao_saida, value=2)
        menu.add_cascade(label="Saída", menu=menu_saida)
        self.janela.config(menu=menu)
        

    def add_widgets(self):
        frame_superior = tk.Frame(self.janela)
        frame_superior.pack(side="top", fill="x", padx=20, pady=(10, 0))
        tk.Label(frame_superior, text="Entrada:",
                 font=("Monospace", 10)).pack(side="left")

        opcoes_db = self.schema.listar_bancos()
        if opcoes_db:
            self.nome_banco_atual.set(self.schema.nome_banco_atual)
        opcoes_schema = self.schema.listar_schemas()
        if opcoes_schema:
            self.nome_schema_atual.set(self.schema.nome_schema_atual)
        self.menu_schemas = tk.OptionMenu(
            frame_superior, self.nome_schema_atual, *opcoes_schema)
        self.menu_schemas.config(width=12)
        self.menu_schemas.pack(side="right")

        tk.Label(frame_superior, text="Schema:", font=(
            "Monospace", 10)).pack(side="right", padx=(5, 0))

        self.menu_databases = tk.OptionMenu(
            frame_superior, self.nome_banco_atual, *opcoes_db)
        self.menu_databases.config(width=12)
        self.menu_databases.pack(side="right")

        tk.Label(frame_superior, text="Banco:", font=(
            "Monospace", 10)).pack(side="right")

        frame_inferior = tk.Frame(self.janela)
        frame_inferior.pack(side="bottom", pady=(0, 10))
        botao = tk.Button(
            frame_inferior,
            text="Executar",
            command=lambda: self.executar_analisador(
                self.opcao_analisador.get(),
                self.caixa_texto.get("1.0", tk.END),
                self.opcao_saida.get()
            ),
            bg="#0400FF", fg="white", width=12
        )
        botao.pack()

        self.caixa_texto = tk.Text(self.janela, font=("Monospace", 12))
        self.caixa_texto.pack(padx=20, pady=10, fill="both", expand=True)

    def atualizar_menus_interface(self):
        bancos = self.schema.listar_bancos()
        menu_db = self.menu_databases["menu"]
        menu_db.delete(0, "end")

        for banco in bancos:
            menu_db.add_command(label=banco, command=lambda b=banco: self.nome_banco_atual.set(b))
        
        if self.nome_banco_atual.get() not in bancos:
            self.nome_banco_atual.set("master")

        self.gerenciar_nome_banco()

    def gerenciar_nome_schema(self, *args):
        self.schema.definir_nome_schema_atual(self.nome_schema_atual.get())

    def gerenciar_nome_banco(self, *args):
        if self.menu_schemas is None:
            return
        self.schema.nome_banco_atual = self.nome_banco_atual.get()

        lista_schemas = self.schema.listar_schemas()
        menu = self.menu_schemas["menu"]
        menu.delete(0, "end")

        if lista_schemas:
            self.nome_schema_atual.set(self.schema.nome_schema_atual)
            for schema in lista_schemas:
                menu.add_command(
                    label=schema,
                    command=lambda s=schema: self.nome_schema_atual.set(s)
                )
        self.schema.definir_banco_atual(self.nome_banco_atual.get())

    def abrir_mars(self):
        caminho_mars = os.path.join("compiler", "resources")
        try:
            subprocess.Popen(
                ["java", "-cp", "MARS/.", "Mars"], 
                cwd=caminho_mars
            )
        except Exception as e:
            print(f"Erro ao abrir o MARS: {e}")

    def executar_analisador(self, opcao_analisador, texto_sql, mode_output):
        if opcao_analisador == 1:
            self.executar_lexico(texto_sql.strip())
        elif opcao_analisador == 2:
            self.executar_sintatico(texto_sql.strip(), mode_output)
        elif opcao_analisador == 3:
            self.schema.atualizar_catalogo()
            self.executar_semantico(
                texto_sql.strip(), self.schema, mode_output)
            self.schema.atualizar_catalogo()
            self.atualizar_menus_interface()

    def gerar_assembly(self, nome_banco, nome_schema, schema, texto_sql):
        self.schema.atualizar_catalogo()
        av.main(nome_banco, nome_schema, schema, texto_sql.strip())
        self.schema.atualizar_catalogo()
        self.atualizar_menus_interface()

    def executar(self):
        self.janela.mainloop()
