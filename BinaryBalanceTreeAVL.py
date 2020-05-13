
#-------------
# Clase del nodo con el código postal
#-------------
class CodigoPostal:

    def __init__(self, cp):

        self.father = None
        self.left = None
        self.right = None
        self.cp = cp

    def __str__(self):

        if self.father is not None:
            imprimir = "nodo:" + str (self.cp) + ", father:" + str(self.father.cp)
        else:
            imprimir = "nodo:" + str(self.cp) + "- Es el top"

        return imprimir

#-------------
# Clase del arbol binario balanceado de nodos con el código postal. Balanceado automático en insert y delete
# Info de referencia: https://www.cpp.edu/~ftang/courses/CS241/notes/self%20balance%20bst.htm
# Info de referencia: https://towardsdatascience.com/self-balancing-binary-search-trees-101-fc4f51199e1d
#-------------
class ABBCodigoPostal:

    def __init__(self):

        self.top = None
        self.size = 0

    # Método de inserción básica en el arbol
    def insert(self, nodocp):

        if self.top is None:        # Si es el primer elemento simplemente lo añadimos
            self.top = nodocp
            self.size += 1
        else:
            puntero = self.top      # Recorremos el arbol con "puntero" para localizar donde insertar. Empezando en top.
            father = None

            # Llamada a insertar recursivo
            self._insert(father, puntero, nodocp)

    # Método de inserción recursiva. Busca el lugar donde encaja el "puntero", entonces inserta y balancea
    def _insert(self, father, puntero, nodocp):
        # Parametros:
        #   fahter: Para identificar el último nodo por el que hemos pasado antes de encontrar el Null donde insertar
        #   puntero: El nodo del arbol a donde estamos apuntando en ese momento
        #   nodocp: El nodo que queremos insertar

        if puntero is None:             # Si el puntero es None, aquí es donde se debe insertar
            nodocp.father = father      # El padre del nuevo elemento es el padre
            if father.cp > nodocp.cp:
                father.left = nodocp
            else:                       # Si es por la derecha, el hijo derecho del padre es el puntero
                father.right = nodocp
            self.size += 1              # El arbol aumenta en uno el tamaño

            # Si el abuelo no es None: es decir no está en "top" seguimos subiendo
            while father.father is not None:
                # Hacemos un balanceo a partir del abuelo del nodo hacia arriba
                father = self.nodereBalance(father.father)

        elif puntero.cp > nodocp.cp:                # Seguimos buscando donde insertar recursivamente izquierda
            self._insert(puntero, puntero.left, nodocp)
        elif puntero.cp < nodocp.cp:                # Seguimos buscando donde insertar recursivamente derecha
            self._insert(puntero, puntero.right, nodocp)
        else:
            return

    # Metodo principal para encontrar nodo por cp
    def findnode (self, cp):

        return self._findnode(cp, self.top)


    # Metodo recursivo para encontrar nodo por cp
    def _findnode(self, cp, nodo):

        if nodo is None:
            return None
        if nodo.cp == cp:
            return nodo
        elif nodo.cp > cp:
            return self._findnode(cp, nodo.left)
        elif nodo.cp < cp:
            return self._findnode(cp, nodo.right)
        else:
            return None

    # Método de borrado
    def delete(self, nodo):

        if nodo is None:
            return 0

        if nodo.right is None and nodo.left is None:                             # Si el nodo a eliminar no tiene hijos
            if nodo.father.right == nodo:                       # según de donde venga el padre se le asigna None
                nodo.father.right = None
            elif nodo.father.left == nodo:
                nodo.father.left = None
            self.size -= 1                                    # Se resta uno al tamaño del arbol

            # Si el padre del nodo eliminado no es None: es decir no está en "top" seguimos subiendo
            while nodo.father is not None:
                # Hacemos un balanceo a partir del padre del nodo eliminado hacia arriba
                nodo = self.nodereBalance(nodo.father)

        elif nodo.right is None:                                # Si el nodo a eliminar tiene hijos pero solo por la izq
            if nodo.father is None:                             # Si el nodo a eliminar es el top (no padre)
                self.top = nodo.left                            # Cambiamos el "top" a la rama izq
                nodo.left.father = None
            elif nodo.father.right == nodo:                     # Si no asignamos la rama izq al padre según donde sea
                nodo.father.right = nodo.left
                nodo.left.father = nodo.father
            elif nodo.father.left == nodo:
                nodo.father.left = nodo.left
                nodo.left.father = nodo.father

            self.size -= 1                                      # Se resta uno al tamaño del arbol

            # Si el padre del nodo eliminado no es None: es decir no está en "top" seguimos subiendo
            while nodo.father is not None:
                # Hacemos un balanceo a partir del padre del nodo eliminado hacia arriba
                nodo = self.nodereBalance(nodo.father)

        elif nodo.left is None:                                 # Si el nodo a eliminar tiene hijos pero solo por la dcha
            if nodo.father is None:                             # Si el nodo a eliminar es el top (no padre)
                self.top = nodo.right                           # Cambiamos el "top" a la rama dcha
                nodo.right.father = None
            elif nodo.father.right == nodo:                     # Si no asignamos la rama dcha al padre según donde sea
                nodo.father.right = nodo.right
                nodo.right.father = nodo.father
            elif nodo.father.left == nodo:
                nodo.father.left = nodo.right
                nodo.right.father = nodo.father

            self.size -= 1  # Se resta uno al tamaño del arbol

            # Si el padre del nodo eliminado no es None: es decir no está en "top" seguimos subiendo
            while nodo.father is not None:
                # Hacemos un balanceo a partir del padre del nodo eliminado hacia arriba
                nodo = self.nodereBalance(nodo.father)

        else:
            lowesthigh  = self.findlowesthigh(nodo)             # Buscamos el sustituto como el más bajo de los mayores

            oldfather = lowesthigh.father                       # guardamos el nodo padre del sustituto para balancear

            if lowesthigh.father.left == lowesthigh:            # Buscamos si el padre del sustituto es por la izq o dch.
                lowesthigh.father.left = lowesthigh.right       # Y asignamos los hijos del sustituto según corresponda
                if lowesthigh.right is not None:                # Pero con cuidado de que tenga hijos el sustituto (evita error)
                    lowesthigh.right.father = lowesthigh.father # Solo izq, nunca los tendrá por la dch
            else:
                lowesthigh.father.right = lowesthigh.right
                if lowesthigh.right is not None:                # Pero con cuidado de que tenga hijos el sustituto (evita error)
                    lowesthigh.right.father = lowesthigh.father # Solo izq, nunca los tendrá por la dch

            if nodo.father is None:                              # Si el nodo eliminado es el top
                self.top = lowesthigh
                lowesthigh.father = None
            else:
                # Comprobamos si el padre del nodo está en la derecha o en la izquierda
                # Y le asignamos como nuevo hijo el sustituto
                if nodo.father.right == nodo:
                    nodo.father.right = lowesthigh
                    lowesthigh.father = nodo.father
                else:
                    nodo.father.left = lowesthigh
                    lowesthigh.father = nodo.father

            # Asignamos los hijos del nodo al sustituto
            lowesthigh.right = nodo.right
            if nodo.right is not None: nodo.right.father = lowesthigh
            lowesthigh.left = nodo.left
            if nodo.left is not None: nodo.left.father = lowesthigh

            self.size -= 1                                      # Se resta uno al tamaño del arbol

            # Si el padre del sustituto (antes de ser movido) no es None: es decir no está en "top" seguimos subiendo
            while oldfather is not None:
                # Hacemos un balanceo a partir del sustituto y subimos asignandole el padre del nodo resultante
                oldfather = self.nodereBalance(oldfather).father


        return 1

    # Método principal para calcular el siguiente nodo dentro de un arbol (que será el más bajo de los mayores)
    def findlowesthigh(self, nodo):

        if nodo.right is not None:
            return self._findlowesthigh(nodo.right)
        else:
            return nodo

    # Método recursivo para calcular el siguiente nodo dentro de un arbol (que será el más bajo de los mayores)
    def _findlowesthigh(self, nodo):

        if nodo.left is not None:
            return self._findlowesthigh(nodo.left)
        else:
            return nodo

    # Método de balanceo sin recursividad solo para un nodo determinado
    # Se usará para buscar hacia arriba todos los nodos por si estuviesen desbalanceados
    def nodereBalance(self, nodo=None):

        # Se compruba el balance de las ramas del nodo
        nodebalance = self.balanceNum(nodo)

        if abs(nodebalance) >= 2:                       # Si el balance es mayor que dos
            if nodebalance <= -2:                       # Si el balance es negativo (rama derecha más larga)
                son = nodo.right
                sonbalance = self.balanceNum(son)       # Comprobamos el balance del hijo
                if sonbalance == -1:                    # Si el hijo tiene balance -1 rotamos a la izquierda
                    self.rotate (son, "left")
                    return son                          # Se devuelve el hijo para que se siga balanceando hacia arriba

                elif sonbalance == 1:                   # Si el hijo tiene balance 1 rotamos doble: derecha, izquierda
                    pivot = son.left                    # La rotación se hace considerando el "pivot" el hijo del hijo
                    self.rotate (pivot, "right")
                    self.rotate (pivot, "left")
                    return pivot                         # Se devuelve el pivot para que se siga balanceando hacia arriba

                else:
                    # Entonces cubre aquellos casos (raros) en los que ambos hijos tienen balance 0 pero una de las
                    # ramas es más larga que la otra. Se balancea como si fuese -1 (aunque sea 0)
                    # Se podría poner en el primer if, pero así queda más comprenisble el código
                    self.rotate(son, "left")
                    return son

            elif nodebalance >= 2:                      # Si el balance es negativo (rama derecha más larga)
                son = nodo.left
                sonbalance = self.balanceNum(son)       # Comprobamos el balance del hijo
                if sonbalance == 1:                     # Si el hijo tiene balance 1 rotamos a la derecha
                    self.rotate (son, "right")
                    return son                         # Se devuelve True porque el arbol estará balanceado en esta rama

                elif sonbalance == -1:                  # Si el hijo tiene balance -1 rotamos doble: izquierda, derecha
                    pivot = son.right                   # La rotación se hace considerando el "pivot" el hijo del hijo
                    self.rotate (pivot, "left")
                    self.rotate (pivot, "right")
                    return pivot                         # Se devuelve True porque el arbol estará balanceado en esta rama

                else:
                    # Entonces cubre aquellos casos (raros) en los que ambos hijos tienen balance 0 pero una de las
                    # ramas es más larga que la otra. Se balancea como si fuese +1 (aunque sea 0)
                    # Se podría poner en el primer if, pero así queda más comprenisble el código
                    self.rotate (son, "right")
                    return son

        else:

            return nodo            # Si está balanceado devolvemos el propio nodo



    # BORRAR NO NECESARIO------------------------------------------------------------------------------------------------------------------
    # Calculates the expected length of search (ELS) to all the nodes depending on the weight. The lower the better.
    # ELS = depth(node1)*probability(node1) + depth(node2)*probability(node2) + .... + depth (noden)*probability(noden)
    # It is obtained by adding probability of a node times the depth of the node for all the nodes.
    # The probabililty is the weight of the node / weight of the tree (the node and its branches)
    def branchels(self, node=None):

        if node is None: node = self.top
        depth = 1

        els = (1/self.treesize()) * depth

        els += self._branchels(node.right, depth, self.treesize())
        els += self._branchels(node.left, depth, self.treesize())

        return els

    # BORRAR NO NECESARIO------------------------------------------------------------------------------------------------------------------
    # Recursive call for the ELS calculation
    def _branchels(self, node, depth, treesize):

        depth += 1

        if node is not None:

            els = (1 / treesize) * depth

            els += self._branchels(node.right, depth, treesize)
            els += self._branchels(node.left, depth, treesize)

            return els

        else:

            return 0




    # Método para rotar el arbol cuando no está balanceado
    def rotate(self, nodo, rotation):

        # Se necesita saber abuelo y padre del nodo a rotar
        gfather = nodo.father.father
        father = nodo.father

        # Se asigna al nodo como nuevo padre el abuelo
        nodo.father = gfather

        if rotation == "left":
            if gfather is None:
                self.top = nodo
            else:
                # Se asigna al abuelo el nodo como hijo, por la derecha o izquierda según corresponda
                if gfather.left == father:
                    gfather.left = nodo
                else:
                    gfather.right = nodo

            father.father = nodo            # El padre del padre es ahora el hijo (nodo)
            father.right = nodo.left        # Los hijos por la dcha del padre son los hijos que eran del nodo por la izq
            if nodo.left is not None:       # Los hijos del nodo se les asigna el padre del nodo como su nuevo padre
                nodo.left.father = father
            nodo.left = father              # El nodo tiene ahora por la izq a su padre como hijo


        elif rotation == "right":
            if gfather is None:
                self.top = nodo
            else:
                # Se asigna al abuelo el nodo como hijo, por la derecha o izquierda según corresponda
                if gfather.left == father:
                    gfather.left = nodo
                else:
                    gfather.right = nodo

            father.father = nodo            # El padre del padre es ahora el hijo (nodo)
            father.left = nodo.right        # Los hijos por la izq del padre son los hijos que eran del nodo por la dcha
            if nodo.right is not None:      # Los hijos del nodo se les asigna el padre del nodo como su nuevo padre
                nodo.right.father = father
            nodo.right = father             # El nodo tiene ahora por la dcha a su padre como hijo


        else:
            return

        return

    # Método para calcular el balance de un nodo
    def balanceNum(self, nodo=None):

        if nodo is None:
            nodo = self.top

        # Se devuelve la diferencia de niveles entre la rama izquierda y derecha del nodo
        # Será positivo con la rama izquierda con más niveles y negativo si es lo contrario
        return self._height(nodo.left) - self._height(nodo.right)

    # Método para comprobar si un nodo concreto del arbol está balanceado en todos sus nodos
    # Similar al balanceNum pero sólo devolviendo True si es menor o igual a 1 or False
    def isBalanced(self, nodo=None):

        if nodo is None:
            nodo = self.top

        rightheight = self._height(nodo.right)
        leftheight = self._height(nodo.left)

        if abs(leftheight - rightheight) <= 1:
            return True
        else:
            return False

    # Método principal recursivo para comprobar que todos los nodos del arbol están balanceados
    def isallBalanced(self):

        nodo = self.top
        return self._isallBalanced(nodo)

    # Método recursivo a partir de un nodo para comprobar que todas las ramas y nodos están balanceados
    def _isallBalanced(self, nodo):

        resultado = False

        rightheight = self._height(nodo.right)
        leftheight = self._height(nodo.left)

        if abs(leftheight - rightheight) <= 1:
            resultado = True
        else:
            resultado = False

        if nodo.left is not None:
            resultado = resultado and self._isallBalanced(nodo.left)
        if nodo.right is not None:
            resultado = resultado and self._isallBalanced(nodo.right)

        return resultado

    # Metodo recursivo para calcular la profundidad
    def depth(self, nodo):

        if nodo.father is not None:
            depth = self.depth(nodo.father)
            depth += 1
            return depth
        else:
            return 1

    # Método principal para calcular la altura de un arbol
    def height(self):

        treeheight = 0
        puntero = self.top
        treeheight += self._height(puntero)
        return treeheight

    # Método recursivo a partir de un nodo para calcular la altura de las ramas y nodos por debajo
    def _height(self, puntero):

        if puntero is None:
            return 0
        else:
            levelsleft = self._height(puntero.left)
            levelsright = self._height(puntero.right)
            if levelsleft <= levelsright:
                return levelsright+1
            else:
                return levelsleft+1

    # Método principal para calcular el tamaño de un arbol. Debería coincidir con el atributo .size del arbol
    def treesize(self):

        puntero = self.top
        treesize=0
        treesize += self._treesize(puntero)
        return treesize

    # Método recursivo para clacular el tamaño de un arbol a partir de un puntero
    def _treesize(self, puntero):

        if puntero is not None:
            treesize = 1
            treesize += self._treesize(puntero.left)
            treesize += self._treesize(puntero.right)
            return treesize
        else:
            return 0

    # Método principal de impresión del arbol
    def __str__(self):

        impresion = ""
        puntero = self.top
        impresion += self.___str___(puntero, 0, "")
        return impresion

    # Método recursivo de impresión del arbol a partir de un nodo.
    # Se le envía el nivel para incluir tabuladores para mejor visualización
    def ___str___(self, puntero, nivel, leftright):

        if puntero is None:
            return ""
        else:
            impresion =""
            impresion += self.___str___(puntero.right, nivel + 1, "right")

            # Se incluye un campo aviso como comprobación si una rama no estuviese balanceada
            if self.isBalanced(puntero) == False:
                aviso = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
            else:
                aviso = "ok"

            if leftright == "left":
                impresion += "\t"*2*(nivel) + str(nivel) + "\\" + str(puntero.cp) + aviso + str(self._height(puntero.left)) + str(self._height(puntero.right)) + "\n"

            elif leftright == "right":
                impresion += "\t"*2*(nivel) + str(nivel) + "/" + str(puntero.cp) + aviso + str(self._height(puntero.left)) + str(self._height(puntero.right)) + "\n"

            else:
                impresion += "\t"*2*(nivel) + str(nivel) + str(puntero.cp) + aviso + str(self._height(puntero.left)) + str(self._height(puntero.right)) + "\n"

            impresion += self.___str___(puntero.left, nivel+1, "left")
            return impresion




