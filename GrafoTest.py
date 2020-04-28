import Grafo


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
#myGrafo.listaVertices["C"].unirVecino("A", 1)
myGrafo.listaVertices["C"].unirVecino("B", 7)
myGrafo.listaVertices["C"].unirVecino("D", 2)
myGrafo.listaVertices["D"].unirVecino("B", 5)
myGrafo.listaVertices["D"].unirVecino("C", 2)
myGrafo.listaVertices["D"].unirVecino("E", 7)


print(myGrafo)

print(myGrafo.shortestGrid("B"))
print(myGrafo.shortestPath("A", "B"))
print(myGrafo.shortestPath("B", "A"))



