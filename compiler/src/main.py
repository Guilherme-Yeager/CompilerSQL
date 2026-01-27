import tkinter as tk
import compiler.src.visitor.visitor as vs
import compiler.src.lexer.lexer as lx


def executar(opcao_analisador, texto_sql, mode_output):
    if opcao_analisador == 1:
        lx.main(texto_sql.strip(), mode_output)
    else:
        vs.main(texto_sql.strip(), mode_output)


class Screen:

    def __init__(self):
        self.janela = tk.Tk()
        self.opcao_analisador = tk.IntVar(value=1)
        self.opcao_saida = tk.IntVar(value=1)
        self.caixa_texto = None
        self.setup_screen()

    def setup_screen(self):
        self.janela.title("CompilerSql")
        largura = self.janela.winfo_screenwidth()
        altura = self.janela.winfo_screenheight()
        pos_x = (largura - 500) // 2
        pos_y = (altura - 350) // 2
        self.janela.geometry(f"{500}x{350}+{pos_x}+{pos_y}")
        self.janela.resizable(False, False)
        self.janela.columnconfigure(0, weight=1)
        self.janela.rowconfigure(0, weight=1)
        self.add_menu()
        self.add_widgets()

    def add_menu(self):
        self.opcao_analisador = tk.IntVar(value=1)
        menu = tk.Menu(self.janela)
        menu_analisador = tk.Menu(menu, tearoff=0)
        menu_analisador.add_radiobutton(
            label="Léxico", variable=self.opcao_analisador, value=1
        )
        menu_analisador.add_radiobutton(
            label="Sintático", variable=self.opcao_analisador, value=2
        )
        menu.add_cascade(label="Analisador", menu=menu_analisador)

        menu_saida = tk.Menu(menu, tearoff=0)
        menu_saida.add_radiobutton(label="SQL", variable=self.opcao_saida, value=1)
        menu_saida.add_radiobutton(label="XML", variable=self.opcao_saida, value=2)
        menu.add_cascade(label="Saída", menu=menu_saida)
        self.janela.config(menu=menu)

    def add_widgets(self):
        self.caixa_texto = tk.Text(self.janela, font=("Monospace", 12))
        self.caixa_texto.grid(row=0, column=0, padx=20, pady=(10, 5), sticky="nsew")

        botao = tk.Button(
            self.janela,
            text="Executar",
            command=lambda: executar(
                self.opcao_analisador.get(),
                self.caixa_texto.get("1.0", tk.END),
                self.opcao_saida.get(),
            ),
            bg="#0400FF",
            fg="white",
            activebackground="#0400FF",
            activeforeground="white",
        )
        botao.grid(row=1, column=0, pady=(5, 10))

    def run(self):
        self.janela.mainloop()


if __name__ == "__main__":
    screen = Screen()
    screen.run()
