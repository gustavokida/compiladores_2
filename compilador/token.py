from enum import Enum

reserved_keys = ["program",
                 "begin",
                 "end",
                 "real",
                 "integer",
                 "read",
                 "write",
                 "if",
                 "then",
                 "else"]

class Type(Enum):
    IDENTIFIER = 0
    INT = 1
    REAL = 2
    SYMBOL = 3
    RESERVED_KEY = 4
    RELATION = 5

class Token:

    def __init__(self, tipo, termo):
        self.tipo = tipo
        self.termo = termo
    
    def getTipo(self):
        return self.tipo

    def getTipoValue(self):
        return self.tipo.value

    def getTipoName(self):
        return self.tipo.name
    
    def setTipo(self, tipo):
        self.tipo = tipo

    def getTermo(self):
        return self.termo
    
    def setTermo(self, termo):
        self.termo = termo
        
    def toString(self):
        return ("Token [" + str(self.tipo.name) + ", " + self.termo + "]")