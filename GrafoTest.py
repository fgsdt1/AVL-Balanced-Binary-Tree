import Grafo

myGrafo = Grafo.Grafo()

myGrafo.addVertice("1")
myGrafo.addVertice("2")
myGrafo.addVertice("3")
myGrafo.addVertice("4")

myGrafo.listaVertices["1"].unirVecino("2", 4)
myGrafo.listaVertices["2"].unirVecino("1", 4)
myGrafo.listaVertices["2"].unirVecino("3", 2)
myGrafo.listaVertices["3"].unirVecino("1", 1)
myGrafo.listaVertices["3"].unirVecino("4", 4)
myGrafo.listaVertices["4"].unirVecino("1", 1)

print(myGrafo)

myGrafo.addArista("4", "1", 6)
myGrafo.addArista("1", "4", 10)

print(myGrafo)

print(myGrafo.listaVertices["3"].devolverVecinos())

