from events import prueba

intento = 0
A= 0
B= 0
C= 0
while intento < 100000:
    intento += 1
    resultado = prueba()
    if resultado == 'A':
        A+= 1 
    elif resultado == 'B':
        B += 1
    elif resultado == 'C':
        C += 1

porcentaje_A = (A / intento) * 100
porcentaje_B = (B / intento) * 100
porcentaje_C = (C / intento) * 100

print(f'Número de intentos: {intento}')
print(f'A = {porcentaje_A:.2f}%')
print(f'B = {porcentaje_B:.2f}%')
print(f'C = {porcentaje_C:.2f}%')    