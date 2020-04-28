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
vertices = ["A", "B", "C", "D", "E"]
matriz = [[0,1,3,N,3],
          [N,0,N,2,2],
          [N,N,0,1,N],
          [N,2,1,0,N],
          [N,2,N,N,0]]

myGrafo.matrixintoGraph(matriz, vertices)

print(myGrafo)

print(myGrafo.shortestMap("B"))
print(myGrafo.shortestPath("A", "E"))
print(myGrafo.shortestPath("E", "A"))
print(myGrafo.shortestPath("C", "E"))
