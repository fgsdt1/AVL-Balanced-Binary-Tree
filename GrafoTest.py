import Grafo
import math

# -------------------------------
# Pruebas básicas
# -------------------------------

myGrafo = Grafo.Grafo()

myGrafo.addVertice("A")
myGrafo.addVertice("B")
myGrafo.addVertice("C")
myGrafo.addVertice("D")
myGrafo.addVertice("E")

myGrafo.listaVertices["A"].unirVecino("B", 3)
myGrafo.listaVertices["A"].unirVecino("C", 1)
myGrafo.listaVertices["B"].unirVecino("C", 7)
myGrafo.listaVertices["B"].unirVecino("D", 5)
myGrafo.listaVertices["B"].unirVecino("E", 1)
myGrafo.listaVertices["C"].unirVecino("A", 1)
myGrafo.listaVertices["C"].unirVecino("B", 7)
myGrafo.listaVertices["C"].unirVecino("D", 2)
myGrafo.listaVertices["D"].unirVecino("B", 5)
myGrafo.listaVertices["D"].unirVecino("C", 2)
myGrafo.listaVertices["D"].unirVecino("E", 7)

print(myGrafo)

print(myGrafo.shortestMap("B"))
print(myGrafo.shortestPath("A", "B"))
print(myGrafo.shortestPath("B", "A"))

print(myGrafo.dfsRoute("C"))

# -------------------------------
# Prueba creación desde matriz
# -------------------------------


myGrafo = Grafo.Grafo()
N=math.inf
vertices = ["1", "2", "3", "4", "5", "6", "7"]
matriz = [[0,8,1,N,N,N,N],
          [8,0,5,2,N,N,N],
          [1,5,0,7,5,N,N],
          [N,2,7,0,N,N,N],
          [N,N,5,N,0,9,3],
          [N,N,N,N,9,0,N],
          [N,N,N,N,3,N,0]]

myGrafo.matrixintoGraph(matriz, vertices)

print(myGrafo)

print(myGrafo.shortestMap("2"))
print(myGrafo.shortestPath("1", "5"))
print(myGrafo.shortestPath("3", "1"))
print(myGrafo.shortestPath("3", "7"))


# -------------------------------
# Prueba creación desde matriz 2
# -------------------------------


myGrafo = Grafo.Grafo()
N=math.inf
vertices = ["A", "B", "C", "D", "E", "F", "G", "H"]
matriz = [[ 0, 7,10, 4, N, N, N, N],
          [ N, 0, 6, N, 5, N, N, N],
          [10, 6, 0,14, N,12, N, N],
          [ 4, N,14, 0, N, N, 1, N],
          [ N, 5, N, N, 0, 8, N,20],
          [ N, N,12, N, 8, 0,18, 9],
          [ N, N, N, 1, N,18, 0,26],
          [ N, N, N, N,20, 9,26, 0]]

myGrafo.matrixintoGraph(matriz, vertices)

print(myGrafo)

print(myGrafo.shortestMap("A"))
print(myGrafo.shortestPath("B", "F"))
print("A->H", myGrafo.shortestPath("A", "H"))
print("H->A", myGrafo.shortestPath("H", "A"))
print(myGrafo.shortestPath("F", "C"))
