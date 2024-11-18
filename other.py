import numpy as np
import copy
import sys
from itertools import permutations
import os
from collections import deque
import time
import heapq

class Isla:
    def __init__(self, fila, col, isla, valor, puentes):
        self.fila = fila
        self.col = col
        self.isla = isla
        self.valor = valor
        self.puentes = puentes
    def __lt__(self, other):
            return self.valor > other.valor

def buscarResolucion(tablero, jugadasViables):
    jugadas = []
    jugadasErroneas = []
    tableros = []
    for permutacion in permutations(jugadasViables):
        tablero_copia = copy.deepcopy(tablero)
        dequePermutaciones = deque(permutacion)
        for permutacion in dequePermutaciones:
            isla1, isla2 = permutacion
            jugadaBuena = realizoMovimiento(
                tablero_copia, isla1.fila, isla1.col, isla2.fila, isla2.col)
            if jugadaBuena:
                jugadas.append(
                    [isla1.fila, isla1.col, isla2.fila, isla2.col])
            else:
                jugadasErroneas.append((isla1,isla2))
            if ganador_encontrado(tablero_copia):
                return jugadas   
        if jugadasErroneas:
            for isla1,isla2 in jugadasErroneas:
                jugadaValida = realizoMovimiento(
                    tablero_copia, isla1.fila, isla1.col, isla2.fila, isla2.col)
                if jugadaValida:  
                    jugadas.append(
                        [isla1.fila, isla1.col, isla2.fila, isla2.col])
        if ganador_encontrado(tablero_copia):
                return jugadas
        else:
            imprimir_tablero(tablero_copia)
            tableros.append(tablero_copia)
            jugadas.clear()
            sys.exit(0)
    return None

def ganador_encontrado(tablero):
    n, m = tablero.shape
    islas = []
    for i in range(n):
        for j in range(m):
            if tablero[i, j].isla:
                islas.append(tablero[i, j])
    for isla in islas:
        if isla.puentes != isla.valor:
            return False
    print("ganó")
    return True

def crear_tablero(file):
    with open(file, 'r') as f:
        n, m = map(int, f.readline().split(','))
        tablero_aux = []
        for i in range(n):
            fila = []
            valores = list(map(int, f.readline().strip()))
            for j in range(m):
                if valores[j] == 0:
                    fila.append(Isla(i, j, False, ".", 0))
                else:
                    fila.append(Isla(i, j, True, valores[j], 0))
            tablero_aux.append(fila)
    tabla = []
    for i in range(n):
        tabla.append(tablero_aux[i])
        for j in range(m):
            if i < len(tablero_aux) - 1 and tablero_aux[i][j].isla and tablero_aux[i + 1][j].isla:
                lista = []
                for k in range(len(tablero_aux[i])):
                    lista.append(Isla(i, j, False, ".", 0))
                tabla.append(lista)
                break
    for i in range(len(tabla)):
        for j in range(len(tabla[i])):
            if j < len(tabla[i]) - 1 and tabla[i][j].isla and tabla[i][j + 1].isla:
                for k in range(len(tabla)):
                    tabla[k].insert(j + 1, Isla(i, j, False, ".", 0))
                break
    tablero = np.array(tabla)
    posicion_actualizar(tablero)
    return tablero

def conectarIslas(tablero, isla1, isla2):
    if isla1.valor == isla1.puentes:
      if jugador:
        print("Numero maximo de puentes")
        return
      else:
        return
    if isla2.valor == isla2.puentes:
      if jugador:
        print("Numero maximo de puentes")
        return
      else:
        return
    if isla1.fila == isla2.fila:
        if isla1.col < isla2.col:
            if tablero[isla1.fila, isla1.col + 1].puentes == 2:
              if jugador:
                print("Ya hay dos")
                return
              else:
                return
            if tablero[isla1.fila, isla1.col + 1].puentes % 2 == 0:
                for i in range(isla1.col + 1, isla2.col):
                    tablero[isla1.fila, i].puentes = 1
                    tablero[isla1.fila, i].valor = "-"
            else:
                for i in range(isla1.col + 1, isla2.col):
                    tablero[isla1.fila, i].puentes = 2
                    tablero[isla1.fila, i].valor = "="
        else:
            if tablero[isla1.fila, isla1.col - 1].puentes == 2:
              if jugador:
                print("Ya hay dos")
                return
              else:
                return
            if tablero[isla1.fila, isla1.col - 1].puentes % 2 == 0:
                for i in range(isla1.col - 1, isla2.col, -1):
                    tablero[isla1.fila, i].puentes = 1
                    tablero[isla1.fila, i].valor = "-"
            else:
                for i in range(isla1.col - 1, isla2.col, -1):
                    tablero[isla1.fila, i].valor = "="
    if isla1.col == isla2.col:
        if isla1.fila < isla2.fila:
            if tablero[isla1.fila + 1, isla1.col].puentes == 2:
              if jugador:
                print("Ya hay dos")
                return
              else:
                return
            if tablero[isla1.fila + 1, isla1.col].puentes % 2 == 0:
                for i in range(isla1.fila + 1, isla2.fila):
                    tablero[i, isla1.col].puentes = 1
                    tablero[i, isla1.col].valor = "|"
            else:
                for i in range(isla1.fila + 1, isla2.fila):
                    tablero[i, isla1.col].puentes = 2
                    tablero[i, isla1.col].valor = "║"
        else:
            if tablero[isla1.fila - 1, isla1.col].puentes == 2:
              if jugador:
                print("Ya hay dos")
                return
              else:
                return
            if tablero[isla1.fila - 1, isla1.col].puentes % 2 == 0:
                for i in range(isla1.fila - 1, isla2.fila, -1):
                    tablero[i, isla1.col].puentes = 1
                    tablero[i, isla1.col].valor = "|"

            else:
                for i in range(isla1.fila - 1, isla2.fila, -1):
                    tablero[i, isla1.col].puentes = 2
                    tablero[i, isla1.col].valor = "║"
    isla1.puentes += 1
    isla2.puentes += 1

def revisarIslas(tablero, isla1, isla2):
    if isla1.fila == isla2.fila:
        if isla1.col < isla2.col:
            for i in range(isla1.col + 1, isla2.col):
                if tablero[isla1.fila, i].isla:
                  if jugador:
                    print("Isla en medio")
                    return False
                  else:
                    return False
        else:
            for i in range(isla1.col - 1, isla2.col, -1):
                if tablero[isla1.fila, i].isla:
                  if jugador:
                    print("Isla en medio")
                    return False
                  else:
                    return False
        return True
    if isla1.col == isla2.col:
        if isla1.fila < isla2.fila:
            for i in range(isla1.fila + 1, isla2.fila):
                if tablero[i, isla1.col].isla:
                  if jugador:
                    print("Isla en medio")
                    return False
                  else:
                    return False
        else:
            for i in range(isla1.fila - 1, isla2.fila, -1):
                if tablero[i, isla1.col].isla:
                  if jugador:
                    print("Isla en medio")
                    return False
                  else:
                    return False
        return True
    if jugador:
      print("No se pueden conectar")
      return False
    else:
      return False

def posicion_actualizar(tablero):
    n, m = tablero.shape
    for i in range(n):
        for j in range(m):
            tablero[i, j].fila = i
            tablero[i, j].col = j

def checkPuentes(tablero, isla1, isla2):
    if isla1.fila == isla2.fila:
        if isla1.col < isla2.col:
            camino = tablero[isla1.fila, isla1.col + 1]
            return validarFilaIslaMen(tablero, isla1, isla2, camino.puentes)
        else:
            camino = tablero[isla1.fila, isla1.col - 1]
            return validarFilaIslaMayor(tablero, isla1, isla2, camino.puentes)
    if isla1.col == isla2.col:
        if isla1.fila < isla2.fila:
            camino = tablero[isla1.fila + 1, isla1.col]
            return validarColIslaMen(tablero, isla1, isla2, camino.puentes)
        else:
            camino = tablero[isla1.fila - 1, isla1.col]
            return validarColIslaMayor(tablero, isla1, isla2, camino.puentes)

def imprimir_tablero(tablero):
    os.system('clear')
    n, m = tablero.shape
    for i in range(n):
        for j in range(m):
            if not tablero[i, j].isla:
                print(f"  {tablero[i, j].valor}  ", end="")
            else:
                print(f"  {tablero[i, j].valor}  ", end="")
        print("")
    time.sleep(1)

def validarFilaIslaMen(tablero, isla1, isla2, puente):
    if puente == 0:
        for i in range(isla1.col + 1, isla2.col):
            if tablero[isla1.fila, i].valor != ".":
                return False
    if puente == 1:
        for i in range(isla1.col + 1, isla2.col):
            if tablero[isla1.fila, i].valor != "-":
                return False
    return True

def validarColIslaMayor(tablero, isla1, isla2, puente):
    if puente == 0:
        for i in range(isla1.fila - 1, isla2.fila, -1):
            if tablero[i, isla1.col].valor != ".":
                return False
    if puente == 1:
        for i in range(isla1.fila - 1, isla2.fila, -1):
            if tablero[i, isla1.col].valor != "|":
                return False
    return True

def validarFilaIslaMayor(tablero, isla1, isla2, puente):
    if puente == 0:
        for i in range(isla1.col - 1, isla2.col, -1):
            if tablero[isla1.fila, i].valor != ".":
                return False
    if puente == 1:
        for i in range(isla1.col - 1, isla2.col, -1):
            if tablero[isla1.fila, i].valor != "-":
                return False
    return True

def validarColIslaMen(tablero, isla1, isla2, puente):
    if puente == 0:
        for i in range(isla1.fila + 1, isla2.fila):
            if tablero[i, isla1.col].valor != ".":
                return False
    if puente == 1:
        for i in range(isla1.fila + 1, isla2.fila):
            if tablero[i, isla1.col].valor != "|":
                return False
    return True

def movimiento(tablero, fila1, col1, fila2, col2):
    if tablero[fila1, col1].isla and tablero[fila2, col2].isla:
        if revisarIslas(tablero, tablero[fila1, col1], tablero[fila2, col2]):
            if checkPuentes(tablero, tablero[fila1, col1], tablero[fila2, col2]):
                conectarIslas(tablero, tablero[fila1, col1], tablero[fila2, col2])
    else:
        print("No hay Isla ahi")

def automatico(tablero):
    posiblesJugadas = []
    filas, columnas = tablero.shape
    heapMax = []
    heapq.heapify(heapMax)
    for i in range(filas):
        for j in range(columnas):
            if tablero[i, j].isla:
                islas_horizontales = tablero[i, :]
                parte1_h = islas_horizontales[:j]
                parte2_h = islas_horizontales[j:]
                for k in range(len(parte1_h)-1, -1, -1):
                    if parte1_h[k].isla and not (parte1_h[k].fila == i and parte1_h[k].col == j):
                        posiblesJugadas.append((tablero[i, j], parte1_h[k]))
                        break  
                for aux in parte2_h:
                    if aux.isla and not (aux.fila == i and aux.col == j):
                        posiblesJugadas.append((tablero[i, j], aux))
                        break 
                islas_verticales = tablero[:, j]
                parte1_v = islas_verticales[:i]
                parte2_v = islas_verticales[i:]
                for k in range(len(parte1_v)-1, -1, -1):
                    if parte1_v[k].isla and not (parte1_v[k].fila == i and parte1_v[k].col == j):
                        posiblesJugadas.append((tablero[i, j], parte1_v[k]))
                        break 
                for aux in parte2_v:
                    if aux.isla and not (aux.fila == i and aux.col == j):
                        posiblesJugadas.append((tablero[i, j], aux))
                        break 
    heapq.heapify(posiblesJugadas)
    tablero_copia = copy.deepcopy(tablero)
    return buscarResolucion(tablero_copia, posiblesJugadas)

def realizoMovimiento(tablero, fila1, col1, fila2, col2):
    valida = False
    if tablero[fila1, col1].isla and tablero[fila2, col2].isla:
        if revisarIslas(tablero, tablero[fila1, col1], tablero[fila2, col2]):
            if checkPuentes(tablero, tablero[fila1, col1], tablero[fila2, col2]):
                valida = True
                conectarIslas(tablero, tablero[fila1, col1], tablero[fila2, col2])
    return valida

tablero = crear_tablero("./boards/example.txt")
imprimir_tablero(tablero)
tablero_aux = np.array(tablero)
filas, columnas = tablero_aux.shape
valores = []
jugador = False
print("Automático (1)")
print("Persona (2)")
while True:
    print("Como quiere ejecutar el programa:")
    eleccion = input()
    if eleccion == "1":
        break
    elif eleccion == "2":
        jugador = True
        break
while True:
    valores.clear()
    try:
        if jugador:
            imprimir_tablero(tablero)
            print("Ingrese las coordenadas separadas por coma")
            valores = list(map(int, input().split(',')))
            if len(valores) != 4:
                raise ValueError(
                    "Ingrese 4 números separados por comas")
            if valores[0] > filas-1 or valores[2] > filas-1:
                raise ValueError(
                    "Coordenadas erroneas")
            if valores[1] > columnas-1 or valores[3] > columnas-1:
                raise ValueError("Coordenadas erroneas")
        else:
            valores = automatico(tablero)
        if jugador:
            movimiento(tablero, valores[0], valores[1], valores[2], valores[3])
        else:
            if valores is  not None:
                for valor in valores:
                    imprimir_tablero(tablero)
                    movimiento(tablero, valor[0], valor[1], valor[2], valor[3])
            else:
                print("El tablero no tiene solucion")
    except ValueError as error:
            print(str(error))
    if ganador_encontrado(tablero):
        imprimir_tablero(tablero)
        print("Ganaste")