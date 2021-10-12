class Simbolo:

    def __init__(self, nome, tipo):
        self.nome = nome
        self.tipo = tipo
        self.end_rel = -1

    def getNome(self):
        return self.nome

    def setNome(self, nome):
        self.nome = nome

    def getTipo(self):
        return self.tipo

    def setTipo(self, tipo):
        self.tipo = tipo

    def getEnd_rel(self):
        return self.end_rel

    def setEnd_rel(self, end_rel):
        self.end_rel = end_rel