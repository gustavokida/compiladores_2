#LINK GITHUB: https://github.com/gustavokida/compiladores_1

from compilador import sintatico
from compilador import interpretador

if __name__ == "__main__":
    arq = "correto2.lalg.txt"
    scan = sintatico.Sintatico(arq)
    scan.analise()

    print()
    print(scan.codigo)
    print()

    scan2 = interpretador.Interpretador("compiled_file.txt")
    scan2.interpreter()
