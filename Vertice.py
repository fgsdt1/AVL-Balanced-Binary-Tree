
# Clase de los vértices que formarán parte de un grafo
class Vertice():

    def __init__(self, clave):

        self.name = clave
        self.aristas = {}

    def unirVecino (self, vecino, ponderacion=0):

        self.aristas[vecino] = ponderacion
        return

    def eliminarVecino (self, vecino):

        return self.aristas.pop(vecino, None)

    def devolverVecinos (self):

        vecinos = []
        for i in self.aristas.keys():
            vecinos.append((i, self.aristas[i]))

        return vecinos

    def __str__(self):

        string = self.name + " conectado a: \n"
        for i in self.aristas.keys():
            string = string + "\t" + i + " -> ponderación -> " + str(self.aristas[i])
            string += "\n"

        return (string)






