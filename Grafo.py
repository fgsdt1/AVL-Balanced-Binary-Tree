
# Clase Grafo que constará de un diccionario de vértices (los nodos) y las aristas que son las conexiones entre ellos
# Las aristas se guardarán en una lista asociada al vertice y llevarán una ponderación
import Vertice
import math

class Grafo():

    def __init__(self):

        self.listaVertices = {}
        self.size = 0

    # Añade un vértice al grafo
    def addVertice(self, nombrevertice):

        # Si no existe el vertice con ese código se crea y se añade, en caso contrario se devuelve Null
        if nombrevertice not in self.listaVertices.keys():
            vertice = Vertice.Vertice(nombrevertice)
            self.listaVertices[vertice.name] = vertice
            self.size += 1
            return vertice
        else:
            return None

    # Borra un vértice y todas las aristas relacionadas
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

    # Añade una arista entre dos vértices
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

    # Calcula el camino menos costoso (más corto) para ir de un punto a todos los demás verices usando el agoritmo Dijkstra
    def shortestMap (self, verticede):

        # Creamos un diccionario de vertices (tablaVertices) con doble valor:
        #       El tamaño del camino (inicializado a infinito) y el camino optimo para llegar ("")
        #  y también creamos un diccionario de vértices (visitaVertices) que no se han visitado
        tablaVertices = {}
        visitaVertices = {}
        for ver in self.listaVertices.keys():
            tablaVertices[ver]=[math.inf, ""]
            visitaVertices[ver]=False

        # Aplicamos valores iniciales al vector origen
        tablaVertices[verticede] = [0, verticede]
        # Repetimos el proceso mientras que queden vertices por analizar (VistaVertices)
        while len(visitaVertices) > 0:
            # Fijamos el puntero en el nodo con menor distnacia y que este en la lista de vertices por visitar (visitaVertices)
            # Para ello recorremos el diccionario. La primera vez será el nodo verticede, que es el único con valor 0
            minVertice = ""
            for ver in visitaVertices.keys():
                if minVertice == "":
                    minVertice = ver
                else:
                    if tablaVertices[ver][0] < tablaVertices[minVertice][0]:
                        minVertice = ver

            # borramos el puntero de la lista de visita
            del visitaVertices[minVertice]

            # Buscamos todas las aristas asociadas al mínimo vértice
            for ari in self.listaVertices[minVertice].aristas.keys():
                # Procesamos aquellas que no han sido procesadas todavía (están en a lista de visita)
                if ari in visitaVertices.keys():
                    # Calculamos las distancias. Distancia actual al nodo puntero más la ponderación de la arista
                    distancia = tablaVertices[minVertice][0] + self.listaVertices[minVertice].aristas[ari]
                    # Si la distancia es menor que la registrada en la tabla de vertices la actualizamos,
                    if distancia < tablaVertices[ari][0]:
                        tablaVertices[ari][0] = distancia
                        # y actualizamos también el camino
                        tablaVertices[ari][1] = tablaVertices[minVertice][1] + ari

        # Salimos del bucle cuando están ya todos los nodos visitados. Se habrá actualizado la tabla de Vertices
        # Devolvemos la tabla de vertices completa con el camino
        return tablaVertices

    # Calcula el camino menos costos (más corto) para ir de un punto a otro concreto usando el agoritmo Dijkstra
    def shortestPath (self, verticede, verticea):

        tablaVertices = self.shortestMap(verticede)
        return tablaVertices[verticea]

    # Se implementa un algoritmo "Depth First Traversal" para recorrer el grafo completo
    # Método principal
    def dfsRoute (self, verticede=""):

        # Si no se envía el vertice origen se considera el primero incluido en el diccionario
        if verticede=="": verticede = list(self.listaVertices.keys())[0]

        #Se crea una pila de vertices recorridos y se le incorpora el primer valor
        recorridos = []
        recorridos.append (verticede)
        # se llama a algoritmo recursivo dfs para crear el camino
        path = self._dfsRoute (verticede, recorridos)

        return path

    # Método iterativo de la implementación del algoritmo "Depth First Traversal", complemento de "dfsRoute"
    def _dfsRoute (self, vertice, recorridos):

        path = vertice
        for ari in self.listaVertices[vertice].aristas.keys():
            if ari not in recorridos:
                recorridos.append(ari)
                path = path + self._dfsRoute(ari, recorridos)

        return path

    # Generación de grafo a partir de una matriz de doble entrada con distanicas/ponderaciones
    # y una lista con los nombres de los nodos
    def matrixintoGraph (self, matriz, listanodos):
        #
        # Si es el propio nodo, la distancia en la matriz ha de ser 0
        # Si no hay conexión entre los nodos, la distancia ha de ser math.inf
        #
        # Ejemplo:
        #       N=math.inf
        #       vertices = ["A", "B", "C", "D"]
        #       matriz = [[0,1,3,N],
        #                 [1,0,N,2],
        #                 [3,N,0,1],
        #                 [N,2,1,0]]

        for i in range(len(listanodos)):
            self.addVertice(str(listanodos[i])) # Se convierte a string por si acaso se envía el nombre del nodo como número

        for row in range(len(matriz)):
            for col in range(len(matriz[row])):
                if 0 < matriz[row][col] < math.inf:
                    self.addArista(listanodos[row], listanodos[col], matriz[row][col])

        return

    def __str__(self):

        string=""
        for nombrevertice in self.listaVertices:
            string = string + str(self.listaVertices[nombrevertice])

        return string