import numpy as np

def event():
    prob = [0.60, 0.25, 0.15]
    sucesos= ['A', 'B', 'C']
    return np.random.choice(sucesos,p = prob)

def launch():
    registro =[]
    example = {}
    equipos = ['Nro 1','Nro 2','Nro 3','Nro 4']
    for i in equipos:
        muestra = event()
        entry = {i: str(muestra)}
        registro.append(entry)
        print(entry)
    return print(registro)
