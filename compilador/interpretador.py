
class Interpretador:

    def __init__(self, arq):
        self.C = ''
        self.i = 0
        self.D = []
        self.s = 0
        try:
            with open(arq) as f:
                self.C = f.readlines()
                f.close()
        except IOError as error:
            raise RuntimeError("Could not open file") from error

    def CRCT(self, k):
        self.s += 1
        self.D.append(k)

    def CRVL(self, n):
        self.s += 1
        self.D.append(self.D[n])

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
        if self.D[self.s - 1] < self.D[self.s]:
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
        self.D[n] = self.D[self.s]
        self.D.pop()
        self.s -= 1

    def DSVI(self, p):
        self.i = p

    def DSVF(self, p):
        if self.D[self.s] == 0:
            self.i = p
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
        self.D.append("")
        self.s += m

    def INPP(self):
        self.s = -1

    def PARA(self):
        pass

    def PARAM(self, n):
        self.s += 1
        self.D.append(self.D[n])

    def PUSHER(self, e):
        self.s += 1
        self.D.append(e)

    def CHPR(self, p):
        self.i = p

    def DESM(self, m):
        self.s -= m

    def RTPR(self):
        self.i = self.D[self.s]
        self.D.pop()
        self.s -= 1
