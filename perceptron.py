import numpy as np
import csv


def obtener_pesos(archivo):
    x = [] #caracteristicas
    pesos = [] #etiquetas

    with open(archivo, 'r') as file:
        reader = csv.reader(file)

        for row in reader:
            row = row[0].split(';')
            row_len = len(row)
            row_x = []
            for i in range(row_len - 1):
                row_x.append(float(row[i]))
            x.append(row_x)
            pesos.append(int(row[row_len - 1]))

    return x, pesos


def funcion_activacion(w, x, b): #Calcula el producto punto entre los pesos (w) y las características (x) y suma el sesgo (b).
    z = w * x
    if z.sum() + b > 0:
        return 1
    else:
        return 0


def execute(archivo, tasa_aprendizaje, error, iteraciones): #Esta función realiza el entrenamiento del perceptrón utilizando el algoritmo de aprendizaje del perceptrón.
    x, yd = obtener_pesos(archivo)
    pesos = np.random.uniform(-2, 2, size=3)
    b = 1

    pesos_iteracion = []
    errores_iteracion = []

    for i in range(iteraciones):
        errors_number = 0
        for j in range(len(x)):
            yc = funcion_activacion(pesos, x[j], b)
            error = yd[j] - yc
            errors_number += error ** 2
            pesos[0] += tasa_aprendizaje * x[j][0] * error
            pesos[1] += tasa_aprendizaje * x[j][1] * error
            pesos[2] += tasa_aprendizaje * x[j][2] * error

        pesos_this = [pesos[0], pesos[1], pesos[2]]
        pesos_iteracion.append(pesos_this)
        errores_iteracion.append(errors_number)

        if errors_number <= float(error):
            break

    return pesos_iteracion, errores_iteracion
