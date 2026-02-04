import compiler.src.visitor.visitor as vs
import compiler.src.lexer.lexer as lx
import compiler.src.semantic.semantic_visitor as sv
from compiler.src.screen.screen import Screen

if __name__ == "__main__":
    screen = Screen(lx.main, vs.main, sv.main)
    screen.executar()
