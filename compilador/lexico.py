from compilador import token

def is_letra(letra) -> bool:
    return((letra >= 'a' and letra <= 'z') or (letra >= 'A' and letra <= 'Z'))
    
def is_digito(letra) -> bool:
    return((letra >= '0' and letra <= '9'))

def is_espaco(letra) -> bool:
    return (letra == ' ' or letra == '\n' or letra == '\t' or letra == '\r')

class Lexico:

    def __init__(self, arq):
        self.conteudo = ''
        self.estado = 0
        self.pos = 0
        try:
            with open(arq) as f:
                self.conteudo = f.read()
                f.close()
        except IOError as error:
            raise RuntimeError("Could not open file") from error




    def is_EOF(self) -> bool:
        return self.pos >= len(self.conteudo)
    
    def next_char(self) -> str:
        if(self.is_EOF()):
            return 0
        char = self.conteudo[self.pos]
        self.pos += 1
        return char

    def back(self):
        self.pos -= 1

    def next_token(self):
        if(self.is_EOF()):
            return None
        
        self.estado = 0
        char = ''
        termo = ''

        while(True):
            if(self.is_EOF()):
                pos = len(self.conteudo) + 1

            char = self.next_char()

            if(self.estado == 0):
                if(is_espaco(char)):
                    self.estado = 0
                elif(char == 0):
                    return None
                elif(is_letra(char)):
                    self.estado = 1
                    termo += char
                elif(is_digito(char)):
                    self.estado = 3
                    termo += char
                else:
                    if(char == ":"):
                        self.estado = 5
                        termo += char
                    elif(char == "<"):
                        self.estado = 6
                        termo += char
                    elif(char == ">"):
                        self.estado = 7
                        termo += char
                    elif(char == "="):
                        termo += char
                        return token.Token(token.Type.RELATION, termo)
                    else:
                        termo += char
                        return token.Token(token.Type.SYMBOL, termo)
            elif(self.estado == 1):
                if char == 0:
                    if termo in token.reserved_keys:
                        return token.Token(token.Type.RESERVED_KEY, termo)
                    else:
                        return token.Token(token.Type.IDENTIFIER, termo)
                elif(is_digito(char) or is_letra(char)):
                    self.estado = 1
                    termo += char
                elif(termo in token.reserved_keys):
                    self.back()
                    return token.Token(token.Type.RESERVED_KEY, termo)
                else:
                    self.back()
                    return token.Token(token.Type.IDENTIFIER, termo)
            elif(self.estado == 3):
                if char == 0:
                    return token.Token(token.Type.INT, termo)
                elif(is_digito(char)):
                    self.estado = 3
                elif(char == "."):
                    self.estado = 4
                    termo += char
                elif(is_letra(char)):
                    raise RuntimeError("Número não reconhecido")
                else:
                    self.back()
                    return token.Token(token.Type.INT, termo)
            elif(self.estado == 4):
                if char == 0:
                    return token.Token(token.Type.REAL, termo)
                elif(is_digito(char)):
                    self.estado = 4
                    termo += char
                else:
                    self.back()
                    return token.Token(token.Type.REAL, termo)
            elif(self.estado == 5):
                if char == 0:
                    return token.Token(token.Type.SYMBOL, termo)
                elif(char ==  "="):
                    termo += char
                    return token.Token(token.Type.SYMBOL, termo)
                else:
                    self.back()
                    return token.Token(token.Type.SYMBOL, termo)
            elif(self.estado == 6):
                if char == 0:
                    return token.Token(token.Type.RELATION, termo)
                elif(char == ">" or char == "="):
                    termo += char
                    return token.Token(token.Type.RELATION, termo)
                else:
                    self.back()
                    return token.Token(token.Type.RELATION, termo)
            elif(self.estado == 7):
                if char == 0:
                    return token.Token(token.Type.RELATION, termo)
                if(char == "="):
                    termo += char
                    return token.Token(token.Type.RELATION, termo)
                else:
                    self.back()
                    return token.Token(token.Type.RELATION, termo)



