
class Interpretador:

    def __init__(self, arq):
        self.C = ''
        self.i = 0
        self.D = []
        self.s = -1
        try:
            with open(arq) as f:
                self.C = f.readlines()
                f.close()
        except IOError as error:
            raise RuntimeError("Could not open file") from error

    def interpreter(self):
        self.i = 0
        while True:
            code = self.C[self.i].split()
            op = code[1]
            if op == "CRCT":
                self.CRCT(code[2])
            elif op == "CRVL":
                self.CRVL(code[2])
            elif op == "SOMA":
                self.SOMA()
            elif op == "SUBT":
                self.SUBT()
            elif op == "MULT":
                self.MULT()
            elif op == "DIVI":
                self.DIVI()
            elif op == "INVE":
                self.INVE()
            elif op == "CONJ":
                self.CONJ()
            elif op == "DISJ":
                self.DISJ()
            elif op == "NEGA":
                self.NEGA()
            elif op == "CPME":
                self.CPME()
            elif op == "CPMA":
                self.CPMA()
            elif op == "CPIG":
                self.CPIG()
            elif op == "CDES":
                self.CDES()
            elif op == "CPMI":
                self.CPMI()
            elif op == "CMAI":
                self.CMAI()
            elif op == "ARMZ":
                self.ARMZ(code[2])
            elif op == "DSVI":
                self.DSVI(code[2])
                self.i -= 1
            elif op == "DSVF":
                self.DSVF(code[2])
                self.i -= 1
            elif op == "LEIT":
                self.LEIT()
            elif op == "IMPR":
                self.IMPR()
            elif op == "ALME":
                self.ALME(code[2])
            elif op == "INPP":
                self.INPP()
            elif op == "PARA":
                self.PARA()
                break
            elif op == "PARAM":
                self.PARAM(code[2])
            elif op == "PUSHER":
                self.PUSHER(code[2])
            elif op == "CHPR":
                self.CHPR(code[2])
                self.i -= 1
            elif op == "DESM":
                self.DESM(code[2])
            elif op == "RTPR":
                self.RTPR()
                self.i -= 1
            self.i += 1


    def CRCT(self, k):
        self.s += 1
        self.D.append(float(k))

    def CRVL(self, n):
        self.s += 1
        self.D.append(self.D[int(n)])

    def SOMA(self):
        self.D[self.s - 1] += self.D[self.s]
        self.D.pop()
        self.s -= 1

    def SUBT(self):
        self.D[self.s - 1] -= self.D[self.s]
        self.D.pop()
        self.s -= 1

    def MULT(self):
        self.D[self.s - 1] = self.D[self.s - 1] * self.D[self.s]
        self.D.pop()
        self.s -= 1

    def DIVI(self):
        self.D[self.s - 1] = self.D[self.s - 1] / self.D[self.s]
        self.D.pop()
        self.s -= 1

    def INVE(self):
        self.D[self.s] = -self.D[self.s]

    def CONJ(self):
        if self.D[self.s - 1] == 1 and self.D[self.s] == 1:
            self.D[self.s - 1] = 1
        else:
            self.D[self.s - 1] = 0
        self.D.pop()
        self.s -= 1

    def DISJ(self):
        if self.D[self.s - 1] == 1 or self.D[self.s] == 1:
            self.D[self.s - 1] = 1
        else:
            self.D[self.s - 1] = 0
        self.D.pop()
        self.s -= 1

    def NEGA(self):
        self.D[self.s] = 1 - self.D[self.s]

    def CPME(self):
        if self.D[self.s - 1] < self.D[self.s]:
            self.D[self.s - 1] = 1
        else:
            self.D[self.s - 1] = 0
        self.D.pop()
        self.s -= 1

    def CPMA(self):
        if self.D[self.s - 1] > self.D[self.s]:
            self.D[self.s - 1] = 1
        else:
            self.D[self.s - 1] = 0
        self.D.pop()
        self.s -= 1

    def CPIG(self):
        if self.D[self.s - 1] == self.D[self.s]:
            self.D[self.s - 1] = 1
        else:
            self.D[self.s - 1] = 0
        self.D.pop()
        self.s -= 1

    def CDES(self):
        if self.D[self.s - 1] != self.D[self.s]:
            self.D[self.s - 1] = 1
        else:
            self.D[self.s - 1] = 0
        self.D.pop()
        self.s -= 1

    def CPMI(self):
        if self.D[self.s - 1] <= self.D[self.s]:
            self.D[self.s - 1] = 1
        else:
            self.D[self.s - 1] = 0
        self.D.pop()
        self.s -= 1

    def CMAI(self):
        if self.D[self.s - 1] >= self.D[self.s]:
            self.D[self.s - 1] = 1
        else:
            self.D[self.s - 1] = 0
        self.D.pop()
        self.s -= 1

    def ARMZ(self, n):
        self.D[int(n)] = self.D[self.s]
        self.D.pop()
        self.s -= 1

    def DSVI(self, p):
        self.i = int(p)

    def DSVF(self, p):
        if self.D[self.s] == 0:
            self.i = int(p)
        else:
            self.i += 1
        self.D.pop()
        self.s -= 1

    def LEIT(self):
        self.s += 1
        self.D.append(float(input()))

    def IMPR(self):
        print(self.D[self.s])
        self.D.pop()
        self.s -= 1

    def ALME(self, m):
        self.D.append(0)
        self.s += int(m)

    def INPP(self):
        self.s = -1

    def PARA(self):
        pass

    def PARAM(self, n):
        self.s += 1
        self.D.append(self.D[int(n)])

    def PUSHER(self, e):
        self.s += 1
        self.D.append(int(e))

    def CHPR(self, p):
        self.i = int(p)

    def DESM(self, m):
        self.s -= int(m)

    def RTPR(self):
        self.i = self.D[self.s]
        self.D.pop()
        self.s -= 1
