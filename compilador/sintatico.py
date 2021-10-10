from compilador import lexico, simbolo

class Sintatico:

    def __init__(self, arq):
        self.lexico = lexico.Lexico(arq)
        #self.simbolo = ''
        self.tabela_simbolo = {}
        self.tipo = ''
        self.temp = 1
        self.codigo = "operador;arg1;arg2;result\n"
        self.linha = 0
        self.linha_temp = 0
        self.i = 0
        self.C = []
        self.s = 0
        self.D = []



    def gera_temp(self, tipo):
        temporario = self.temp
        self.temp += 1
        return simbolo.Simbolo("t" + str(temporario), tipo)

    def code(self, op, arg1, arg2, result):
        self.codigo += str(self.linha) + " - " + op + ";" + arg1 + ";" + arg2 + ";" + result + "\n"
        self.linha += 1

    def gera_linha_temp(self):
        self.linha_temp += 1
        linha = self.linha_temp
        return str(linha) + "X"

    def arruma_linha_temp(self, linha):
        self.codigo = self.codigo.replace(str(self.linha_temp) + "X", str(linha))
        self.linha_temp -= 1

    def obtem_simbolo(self):
        self.simbolo = self.lexico.next_token()

    def verifica_termo(self, termo):
        return (self.simbolo is not None) and (str(self.simbolo.getTermo()) == str(termo))

    def verifica_tipo(self, tipo):
        return (self.simbolo is not None) and (str(self.simbolo.getTipoName()) == str(tipo))

    def verifica_tabela(self, termo):
        return not termo in self.tabela_simbolo.keys()


    def analise(self):
        self.obtem_simbolo()
        self.programa()
        if(self.simbolo is None):
            print("OK")
        else:
            raise RuntimeError(f"Erro sintático esperado no fim de cadeia encontrado: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")

    def programa(self):
        print("programa")
        if self.verifica_termo("program"):
            self.obtem_simbolo()
            if self.verifica_tipo('IDENTIFIER'):
                self.obtem_simbolo()
                self.corpo()
                if self.verifica_termo("."):
                    self.code("PARA", "", "", "")
                    self.obtem_simbolo()
                else:
                    raise RuntimeError(f"Erro sintático. esperado '.' obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")
            else:
                raise RuntimeError(f"Erro sintático. Esperado IDENTIFIER obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")
        else:
            raise RuntimeError(f"Erro sintático. Esperado 'program' obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")

    def corpo(self):
        print("corpo")
        self.dc()
        if self.verifica_termo("begin"):
            self.obtem_simbolo()
            self.comandos()
            if self.verifica_termo("end"):
                self.obtem_simbolo()
            else:
                raise RuntimeError(f"Erro sintático. Esperado 'end' obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")
        else:
            raise RuntimeError(f"Erro sintático. Esperado 'begin' obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")

    def dc(self):
        print("dc")
        if not self.verifica_termo("begin"):
            self.dc_v()
            self.mais_dc()
        else:
            pass

    def dc_v(self):
        print("dc_v")
        tipo_dir = self.tipo_var()
        if self.verifica_termo(":"):
            self.obtem_simbolo()
            self.variaveis(tipo_dir)
        else:
            raise RuntimeError(f"Erro sintático. Esperado ':' obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")

    def tipo_var(self):
        print("tipo_var")
        if self.verifica_termo("integer") or self.verifica_termo("real"):
            if self.simbolo.getTermo() == "integer":
                self.tipo = "INT"
            else:
                self.tipo = "REAL"
            self.obtem_simbolo()
            if self.tipo == "INT":
                return "0"
            else:
                return "0.0"

        else:
            raise RuntimeError(f"Erro sintático. Esperado 'integer' ou 'real' obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")

    def variaveis(self, variaveis_esq):
        print("variaveis")
        if self.verifica_tipo('IDENTIFIER'):
            if self.verifica_tabela(self.simbolo.getTermo()):
                self.tabela_simbolo[self.simbolo.getTermo()] = simbolo.Simbolo(self.simbolo.getTermo(), self.tipo)
            else:
                raise RuntimeError(f"Erro semântico. Identificador '{self.simbolo.getTermo()}' já declarado.")
            self.code("ALME", variaveis_esq, "", self.simbolo.getTermo())
            self.obtem_simbolo()
            self.mais_var(variaveis_esq)
        else:
            raise RuntimeError(f"Erro sintático. Esperado tipo IDENTIFIER obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")

    def mais_var(self, mais_var_esq):
        print("mais_var")
        if self.verifica_termo(","):
            self.obtem_simbolo()
            self.variaveis(mais_var_esq)
        elif self.verifica_termo(";"):
            pass
        else:
            raise RuntimeError(f"Erro sintático. Esperado ',' obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")

    def mais_dc(self):
        print("mais_dc")
        if self.verifica_termo(";"):
            self.obtem_simbolo()
            self.dc()
        elif self.verifica_termo("begin"):
            pass
        else:
            raise RuntimeError(f"Erro sintático. Esperado ';' obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")

    def comandos(self):
        print("comandos")
        self.comando()
        self.mais_comandos()

    def comando(self):
        print("comando")
        if self.verifica_termo("read") or self.verifica_termo("write"):
            op = self.simbolo.getTermo()
            self.obtem_simbolo()
            if self.verifica_termo("("):
                self.obtem_simbolo()
                if self.verifica_tipo("IDENTIFIER"):
                    ident = self.simbolo
                    if ident.getTermo() in self.tabela_simbolo.keys():
                        self.obtem_simbolo()
                    else:
                        raise RuntimeError(f"Erro semântico. identificador '{self.simbolo.getTermo()}' não declarado")
                    if self.verifica_termo(")"):
                        self.obtem_simbolo()
                        if op == "read":
                            self.code(op, "", "", ident.getTermo())
                        else:
                            self.code(op, ident.getTermo(), "", "")
                    else:
                        raise RuntimeError(f"Erro sintático. Esperado ')' obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")
                else:
                    raise RuntimeError(f"Erro sintático. Esperado tipo IDENTIFIER obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")
            else:
                raise RuntimeError(f"Erro sintático. Esperado '(' obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")
        elif self.verifica_tipo("IDENTIFIER"):
            ident = self.simbolo
            if ident.getTermo() in self.tabela_simbolo.keys():
                ident = self.tabela_simbolo[self.simbolo.getTermo()]
                self.obtem_simbolo()
            else:
                raise RuntimeError(f"Erro semântico. identificador '{self.simbolo.getTermo()}' não declarado")
            if self.verifica_termo(":="):
                self.obtem_simbolo()
                expressao_dir = self.expressao()
                if ident.getTipo() == expressao_dir.getTipo():
                    self.code(":=", expressao_dir.getNome(), "", ident.getNome())
                else:
                    raise RuntimeError(f"Erro semântico. '{ident.getNome()}' é {ident.getTipo()}" +
                                       f" e '{expressao_dir.getNome()}' é {expressao_dir.getTipo()}")
            else:
                raise RuntimeError(f"Erro sintático. Esperado ':=' obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")
        elif self.verifica_termo("if"):
            self.obtem_simbolo()
            condicao_dir = self.condicao()
            if self.verifica_termo("then"):
                self.obtem_simbolo()
                self.code("JF", condicao_dir.getNome(), self.gera_linha_temp(), "")
                self.comandos()
                self.pfalsa()
                if self.verifica_termo("$"):
                    self.obtem_simbolo()
                else:
                    raise RuntimeError(f"Erro sintático. Esperado '$' obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")
            else:
                raise RuntimeError(f"Erro sintático. Esperado 'then' obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")
        else:
            raise RuntimeError(f"Erro sintático. Esperado 'read', 'write', tipo IDENTIFIER ou 'if' obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")

    def mais_comandos(self):
        print("mais_comandos")
        if self.verifica_termo(";"):
            self.obtem_simbolo()
            self.comandos()
        elif (self.verifica_termo("end")
                or self.verifica_termo("$")
                or self.verifica_termo("else")):
            pass
        else:
            raise RuntimeError(f"Erro sintático. Esperado ';' obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")

    def expressao(self):
        print("expressao")
        termo_dir = self.termo()
        outros_termos_dir = self.outros_termos(termo_dir)
        return outros_termos_dir

    def termo(self):
        print("termo")
        minus_op = self.op_un()
        fator_dir = self.fator()
        if(minus_op == "-"):
            fator1_dir = self.gera_temp(fator_dir.getTipoName())
            self.code(minus_op, fator_dir.getNome(), "", fator1_dir.getNome())
            mais_fatores_dir = self.mais_fatores(fator1_dir)
            return mais_fatores_dir
        else:
            mais_fatores_dir = self.mais_fatores(fator_dir)
            return mais_fatores_dir

    def op_un(self):
        print("op_un")
        if self.verifica_termo("-"):
            op_un_dir = self.simbolo.getTermo()
            self.obtem_simbolo()
            return op_un_dir
        elif (self.verifica_tipo("IDENTIFIER")
                or self.verifica_tipo("REAL")
                or self.verifica_tipo("INT")
                or self.verifica_termo("(")):
            return ""
        else:
            raise RuntimeError(f"Erro sintático. Esperado '-' ou fator obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")

    def fator(self):
        print("fator")
        if(self.verifica_tipo("IDENTIFIER")):
            if self.simbolo.getTermo() in self.tabela_simbolo.keys():
                ident = self.simbolo
                self.obtem_simbolo()
                return self.tabela_simbolo[ident.getTermo()]
            else:
                raise RuntimeError(f"Erro semântico. identificador '{self.simbolo.getTermo()}' não declarado")
        elif self.verifica_tipo("INT") or self.verifica_tipo("REAL"):
            ident = self.simbolo
            self.obtem_simbolo()
            return simbolo.Simbolo(ident.getTermo(), ident.getTipoName())
        elif self.verifica_termo("("):
            self.obtem_simbolo()
            expressao_dir = self.expressao()
            if self.verifica_termo(")"):
                self.obtem_simbolo()
                return expressao_dir
            else:
                raise RuntimeError(f"Erro sintático. Esperado ')' obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")
        else:
            raise RuntimeError(f"Erro sintático. Esperado '(' ou Tipos INDENTIFER, INT ou REAL obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")

    def mais_fatores(self, mais_fatores_esq):
        print("mais_fatores")
        if self.verifica_termo("*") or self.verifica_termo("/"):
        # if (not self.verifica_termo("+")
        #         and not self.verifica_termo("-")
        #         and not self.verifica_termo(";")
        #         and not self.verifica_termo(")")
        #         and not self.verifica_termo("then")
        #         and not self.verifica_tipo("RELATION")):
            arithmetic_op = self.op_mul()
            fator_dir = self.fator()
            mais_fatores1_dir = self.mais_fatores(fator_dir)
            if mais_fatores_esq.getTipo() == mais_fatores1_dir.getTipo():
                mais_fatores_dir = self.gera_temp(mais_fatores_esq.getTipo())
            else:
                raise RuntimeError(f"Erro semântico. '{mais_fatores_esq.getNome()}' é {mais_fatores_esq.getTipo()}" +
                                   f" e '{mais_fatores1_dir.getNome()}' é {mais_fatores1_dir.getTipo()}")
            self.code(arithmetic_op, mais_fatores_esq.getNome(), mais_fatores1_dir.getNome(), mais_fatores_dir.getNome())
            return mais_fatores_dir
        else:
            return mais_fatores_esq

    def op_mul(self):
        print("op_mul")
        if self.verifica_termo("*") or self.verifica_termo("/"):
            op_mul_dir = self.simbolo.getTermo()
            self.obtem_simbolo()
            return op_mul_dir
        else:
            raise RuntimeError(f"Erro sintático. Esperado '*' ou '/' obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")

    def outros_termos(self, outros_termos_esq):
        print("outros_termos")
        if self.verifica_termo("+") or self.verifica_termo("-"):
        # if(not self.verifica_tipo("RELATION")
        #         and not self.verifica_termo(";")
        #         and not self.verifica_termo("then")
        #         and not self.verifica_termo(")")):
            arithmetic_op = self.op_ad()
            termo_dir = self.termo()
            outros_termos1_dir = self.outros_termos(termo_dir)
            if outros_termos_esq.getTipo() == outros_termos1_dir.getTipo():
                outros_termos_dir = self.gera_temp(outros_termos_esq.getTipo())
            else:
                raise RuntimeError(f"Erro semântico. '{outros_termos_esq.getNome()}' é {outros_termos_esq.getTipo()}" +
                                   f" e '{outros_termos1_dir.getNome()}' é {outros_termos1_dir.getTipo()}")
            self.code(arithmetic_op, outros_termos_esq.getNome(), outros_termos1_dir.getNome(), outros_termos_dir.getNome())
            return outros_termos_dir
        else:
            return outros_termos_esq

    def op_ad(self):
        print("op_ad")
        if self.verifica_termo("+") or self.verifica_termo("-"):
            arithmetic_op = self.simbolo.getTermo()
            self.obtem_simbolo()
            return arithmetic_op
        else:
            raise RuntimeError(f"Erro sintático. Esperado '+' ou '-' obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")

    def condicao(self):
        print("condicao")
        expressao_dir = self.expressao()
        op_relational = self.relacao()
        expressao1_dir = self.expressao()
        if expressao_dir.getTipo() == expressao1_dir.getTipo():
            condicao_dir = self.gera_temp(expressao_dir.getTipo())
        else:
            raise RuntimeError(f"Erro Semântico. {expressao_dir.getNome()} é {expressao_dir.getTipo()}" +
                               f" e {expressao1_dir.getNome()} é {expressao1_dir.getTipo()}")
        self.code(op_relational, expressao_dir.getNome(), expressao1_dir.getNome(), condicao_dir.getNome())
        return condicao_dir

    def relacao(self):
        print("relacao")
        if self.verifica_tipo("RELATION"):
            op_relational = self.simbolo.getTermo()
            self.obtem_simbolo()
            return op_relational
        else:
            raise RuntimeError(f"Erro sintático. Esperado tipo RELATION obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")

    def pfalsa(self):
        print("pfalsa")
        if self.verifica_termo("$"):
            self.arruma_linha_temp(self.linha)
        elif self.verifica_termo("else"):
            self.arruma_linha_temp(str(self.linha+1))
            self.code("goto", self.gera_linha_temp(), "", "")
            self.obtem_simbolo()
            self.comandos()
            self.arruma_linha_temp(self.linha)
        else:
            raise RuntimeError(f"Erro sintático. Esperado 'else' obtido: {self.simbolo.getTermo() if self.simbolo != None else 'NULL'}")

    def CRCT(self, k):
        self.s += 1
        self.D[self.s] = k

    def CRVL(self, n):
        self.s += 1
        self.D[self.s] = self.D[n]

    def SOMA(self):
        self.D[self.s-1] += self.D[self.s]
        self.s -= 1

    def SUBT(self):
        self.D[self.s-1] -= self.D[self.s]
        self.s -= 1

    def MULT(self):
        self.D[self.s-1] = self.D[self.s-1] * self.D[self.s]
        self.s -= 1

    def DIVI(self):
        self.D[self.s - 1] = self.D[self.s - 1] / self.D[self.s]
        self.s -= 1

    def INVE(self):
        self.D[self.s] = -self.D[self.s]

    def CONJ(self):
        if self.D[self.s-1] == 1 and self.D[self.s] == 1:
            self.D[self.s-1] = 1
        else:
            self.D[self.s-1] = 0
        self.s -= 1

    def DISJ(self):
        if self.D[self.s -1] == 1 or self.D[self.s] == 1:
            self.D[self.s-1] = 1
        else:
            self.D[self.s-1] = 0
        self.s -= 1

    def NEGA(self):
        self.D[self.s] = 1 - self.D[self.s]

    def CPME(self):
        if self.D[self.s-1] < self.D[self.s]:
            self.D[self.s-1] = 1
        else:
            self.D[self.s-1] = 0
        self.s -= 1

    def CPMA(self):
        if self.D[self.s-1] < self.D[self.s]:
            self.D[self.s-1] = 1
        else:
            self.D[self.s-1] = 0
        self.s -= 1

    def CPIG(self):
        if self.D[self.s-1] == self.D[self.s]:
            self.D[self.s-1] = 1
        else:
            self.D[self.s-1] = 0
        self.s -= 1

    def CDES(self):
        if self.D[self.s-1] != self.D[self.s]:
            self.D[self.s-1] = 1
        else:
            self.D[self.s-1] = 0
        self.s -= 1

    def CPMI(self):
        if self.D[self.s-1] <= self.D[self.s]:
            self.D[self.s-1] = 1
        else:
            self.D[self.s-1] = 0
        self.s -= 1

    def CMAI(self):
        if self.D[self.s-1] >= self.D[self.s]:
            self.D[self.s-1] = 1
        else:
            self.D[self.s-1] = 0
        self.s -= 1

    def ARMZ(self, n):
        self.D[n] = self.D[self.s]
        self.s -= 1

    def DSVI(self, p):
        self.i = p

    def DSVF(self, p):
        if self.D[self.s] == 0:
            self.i = p
        self.s -= 1             #VERIFICAR SE ESTÁ CERTO

    def LEIT(self):
        self.s += 1
        self.D[self.s] = "valor de entrada"

    def IMPR(self):
        print(self.D[self.s])
        self.s -= 1

    def ALME(self, m):
        self.s += m

    def INPP(self):
        self.s = -1

    def PARA(self):
        pass

    def PARAM(self, n):
        self.s += 1
        self.D[self.s] = self.D[n]

    def PUSHER(self, e):
        self.s += 1
        self.D[self.s] = e

    def CHPR(self, p):
        self.i = p

    def DESM(self, m):
        self.s -= m

    def RTPR(self):
        self.i = self.D[self.s]
        self.s -= 1






