import numpy as np

class Calculator:
    def __init__(self, Vo, Vr,Irms):
        self.Vo = Vo
        self.Vr = Vr
        self.Irms = Irms
    
    def aparente(self):
        S =self.Vo * self.Irms
        return S

    def activa(self):
        P= self.Vr *  self.Irms
        return P
    def factor(self):
        f = self.activa() / self.aparente()
        return f
    def reactiva(self):
        Q = np.sqrt(self.aparente()**2 - self.activa() ** 2)
        return Q

