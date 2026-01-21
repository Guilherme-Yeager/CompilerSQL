import tkinter as tk
import compiler.src.visitor.visitor as vs
import compiler.src.lexer.lexer as lx


def executar(opcao_selecionada, texto_sql):
    if opcao_selecionada == 1:
        lx.main(texto_sql.strip())
    else:
        vs.main(texto_sql.strip())


class Screen():

    def __init__(self):
        self.janela = tk.Tk()
        self.opcao_selecionada = tk.IntVar(value=1)
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
        self.add_menu()
        self.add_widgets()

    def add_menu(self):
        self.opcao_selecionada = tk.IntVar(value=1)
        menu = tk.Menu(self.janela)
        sub_menu = tk.Menu(menu, tearoff=0)
        sub_menu.add_radiobutton(
            label="Léxico",
            variable=self.opcao_selecionada,
            value=1
        )
        sub_menu.add_radiobutton(
            label="Sintático",
            variable=self.opcao_selecionada,
            value=2
        )
        menu.add_cascade(label="Menu", menu=sub_menu)
        self.janela.config(menu=menu)

    def add_widgets(self):
        self.caixa_texto = tk.Text(self.janela, width=50,
                                   height=13, font=("Consolas", 14))
        self.caixa_texto.pack(padx=20, pady=(10, 5))

        botao = tk.Button(self.janela, text="Executar", command=lambda: executar(self.opcao_selecionada.get(), self.caixa_texto.get("1.0", tk.END)), font=("Arial", 10),
                          bg="#0400FF", fg="white", width=10, height=1)
        botao.pack(pady=(5, 5))

    def run(self):
        self.janela.mainloop()


if __name__ == "__main__":
    screen = Screen()
    screen.run()
