import tkinter as tk


class Screen():
    def __init__(self, executar_lexico, executar_sintatico, executar_semantico, schema):
        self.executar_lexico = executar_lexico
        self.executar_sintatico = executar_sintatico
        self.executar_semantico = executar_semantico
        self.schema = schema

        self.janela = tk.Tk()
        self.opcao_analisador = tk.IntVar(value=1)
        self.opcao_analisador.trace_add("write", self.gerenciar_menu_schema)
        self.opcao_saida = tk.IntVar(value=1)
        self.nome_schema_atual = tk.StringVar()
        self.nome_schema_atual.trace_add("write", self.gerenciar_nome_schema)
        self.caixa_texto = None
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
        self.gerenciar_menu_schema()

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

        opcoes = self.schema.listar_schemas()

        if opcoes:
            self.nome_schema_atual.set(opcoes[0])
            self.schema.definir_nome_schema_atual(opcoes[0])

        self.menu_schemas = tk.OptionMenu(
            frame_superior, 
            self.nome_schema_atual, 
            *opcoes
        )
        self.menu_schemas = tk.OptionMenu(
            frame_superior, self.nome_schema_atual, *opcoes)
        self.menu_schemas.config(width=12)
        self.menu_schemas.pack(side="right", padx=(5, 0))
        tk.Label(frame_superior, text="Schema:", font=(
            "Monospace", 10)).pack(side="right")

        self.caixa_texto = tk.Text(self.janela, font=("Monospace", 12))
        self.caixa_texto.pack(padx=20, pady=10, fill="both", expand=True)

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

    def gerenciar_menu_schema(self, *args):
        if self.opcao_analisador.get() == 3:
            self.menu_schemas.config(state="normal")
        else:
            self.menu_schemas.config(state="disabled")

    def gerenciar_nome_schema(self, *args):
        self.schema.definir_nome_schema_atual(self.nome_schema_atual.get())

    def executar_analisador(self, opcao_analisador, texto_sql, mode_output):
        if opcao_analisador == 1:
            self.executar_lexico(texto_sql.strip(), mode_output)
        elif opcao_analisador == 2:
            self.executar_sintatico(texto_sql.strip(), mode_output)
        elif opcao_analisador == 3:
            pass
            
    def executar(self):
        self.janela.mainloop()
