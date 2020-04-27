
# Clase Grafo que constará de un diccionario de vértices (los nodos) y las aristas que son las conexiones entre ellos
# Las aristas se guardarán en una lista asociada al vertice y llevarán una ponderación
import Vertice

class Grafo():

    def __init__(self):

        self.listaVertices = {}
        self.size = 0

    def addVertice(self, nombrevertice):

        # Si no existe el vertice con ese código se crea y se añade, en caso contrario se devuelve Null
        if nombrevertice not in self.listaVertices.keys():
            vertice = Vertice.Vertice(nombrevertice)
            self.listaVertices[vertice.name] = vertice
            self.size += 1
            return vertice
        else:
            return None

    def deleteVertice(self, nombrevertice):

        # Se pregunta si el vertice existe para evitar errores. Si es así se borra
        if nombrevertice in self.listaVertices.keys():
            del self.listaVertices[nombrevertice]
            self.size -=1

        # Se busca cualquier arista que relacione al vertice borrado y se borra
        for ver in self.listaVertices.keys():
            if nombrevertice in self.listaVertices[ver].aristas.keys():
                del self.listaVertices[ver].aristas[nombrevertice]

        return

    def addArista(self, verticede, verticea, ponderacion):

        # Si los vertices "de" o "a" no existen, se crean
        if verticea not in self.listaVertices.keys():
            self.addVertice(verticea)
        if verticede not in self.listaVertices.keys():
            self.addVertice(verticede)

        # Se crea la arista mediante el método de unirVecinos de la clase Vertice
        # Si ya existe, se sobreescribe la nueva ponderación
        self.listaVertices[verticede].unirVecino(verticea, ponderacion)

        return

    def __str__(self):

        string=""
        for nombrevertice in self.listaVertices:
            string = string + str(self.listaVertices[nombrevertice])

        return string