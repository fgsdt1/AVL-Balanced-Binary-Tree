
#-----------------------------------------------------------------------------------------------------------------------
# Node Class with Value (in this case numeric) and the weight
#-----------------------------------------------------------------------------------------------------------------------
class WBTNode:

    def __init__(self, value, weight=1):

        self.father = None
        self.left = None
        self.right = None
        self.value = value
        self.weight = weight

    def __str__(self):

        if self.father is not None:
            show = "node:" + str (self.value) + "/" + str (self.weight) + "father:" + str(self.father.value)
        else:
            show = "node:" + str(self.value) + "/" + str (self.weight) + "- Is Root"

        return show

#-----------------------------------------------------------------------------------------------------------------------
# Class for the weight balanced tree.
# The size of the tree will be the add up of the different weights
# It is thought for a tree with intensive access, and each access is registered in the weight.
# Balancing the tree in every access would be resource consuming with little effect on the performance of the tree
# For this reason it is more efficient to balance the tree with an specific method used periodically
#-----------------------------------------------------------------------------------------------------------------------
class WBTree:

    def __init__(self):

        self.top = None
        self.size = 0
        self.weight = 0

    # ------------------------------------------------------------------------------------------------------------------
    # Basic tree insert method (calls the recursive one)
    def insert(self, node):

        if self.top is None:        # If it is the first element in the tree
            self.top = node
            self.size += 1
            self.weight += 1
        else:
            pointer = self.top      # We go trough the tree nodes with "pointer" to locate where to insert. Starting at top.
            father = None

            # Recursive insert call
            self._insert(father, pointer, node)

    # ------------------------------------------------------------------------------------------------------------------
    # Recursive tree insert method. Looks for the place to insert a new node
    # An insert (if its weight is 1 as should be in a first insert) will not unbalance the tree significantly,
    # thus no automatic rebalance is necessary
    def _insert(self, father, pointer, node):
        # Parameters:
        #   fahter: to identify the last node we inspected before finding the right place to insert
        #   pointer: The node of the tree where we are pointing at the moment
        #   node: The node to insert

        if pointer is None:                         # If the pointer is None, here is where we have to insert
            node.father = father                    # The father of the new element is the father we sent to the method
            if father.value > node.value:           # If the father is greater, the left son of the father is the pointer
                father.left = node
            else:                                   # else, it will be the right son
                father.right = node
            self.weight += node.weight              # The weight of the tree increases by the weight of the node
            self.size += 1                          # The size of the tree increases by 1
        elif pointer.value > node.value:             # Keep searching where to insert recursively in the left
            self._insert(pointer, pointer.left, node)
        elif pointer.value < node.value:                # Keep searching where to insert recursively in the left
            self._insert(pointer, pointer.right, node)
        else:
            pointer.weight += node.weight           # The weight of tree and node increases by the weight of the node
            self.weight += node.weight

        return

    # ------------------------------------------------------------------------------------------------------------------
    # Basic tree search method by value. Calls the recursive method
    def findnode (self, value):
        if self.top.value == value:
            return self.top
        else:
            return self._findnode(value, self.top)

    # ------------------------------------------------------------------------------------------------------------------
    # Recursive tree search method by value
    def _findnode(self, value, node):
        if node is None:
            return None
        if node.value == value:
            return node
        elif node.value > value:
            return self._findnode(value, node.left)
        elif node.value < value:
            return self._findnode(value, node.right)
        else:
            return None

    # ------------------------------------------------------------------------------------------------------------------
    # Node deletion method by node. To delete by value first we have to call the findnode method which returns the node
    def delete(self, node):

        if node is None:
            return 0

        if self._height(node) == 1:                     # If the node to delete has no children
            if node.father.right == node:               # Depending on the branch of the father of the node to delete
                node.father.right = None
            elif node.father.left == node:
                node.father.left = None
            self.size -= node.weight                    # The weight of the node is subtracted from the total

        elif node.right is None:                        # if the node to delete has children, but only by the left
            if node.father is None:                     # if the node to delete is the root
                self.top = node.left                    # we change "top" (root) to the left branch of the node
                node.left.father = None
            elif node.father.right == node:             # else we assign the left branch where it should be
                node.father.right = node.left
                node.left.father = node.father
            elif node.father.left == node:
                node.father.left = node.left
                node.left.father = node.father
            self.size -= node.weight                    # The weight of the node is subtracted  from the total

        elif node.left is None:                         # if the node to delete has children, but only by the right
            if node.father is None:                     # if the node to delete is the root
                self.top = node.right                   # we change "top" (root) to the right branch of the node
                node.right.father = None
            elif node.father.right == node:             # else we assign the right branch where it should be
                node.father.right = node.right
                node.right.father = node.father
            elif node.father.left == node:
                node.father.left = node.right
                node.right.father = node.father
            self.size -= node.weight                    # The weight of the node is subtracted  from the total
        else:
# Pendiente____________________
            return 1

        return 1


    # ------------------------------------------------------------------------------------------------------------------
    # Calculates the total weight of a node and all its branches together with the number of nodes (Size) and height
    def branchweight(self, node):

        branch = {}

        if node is not None:

            branch["weight"] = node.weight
            branch["size"] = 1
            branch["height"] = 1

            branchleft = self.branchweight(node.left)
            branchright = self.branchweight(node.right)
            branch["weight"] += (branchleft["weight"] + branchright["weight"])
            branch["size"] += (branchleft["size"] + branchright["size"])

            if branchleft["height"] >= branchright["height"]:
                branch["height"]+=branchleft["height"]
            else:
                branch["height"]+=branchright["height"]

        else:
            branch["weight"] = 0
            branch["size"] = 0
            branch["height"] = 0

        return branch

    # ------------------------------------------------------------------------------------------------------------------
    # Calculates the expected length of search (ELS) to all the nodes depending on the weight
    # ELS = depth(node1)*probability(node1) + depth(node2)*probability(node2) + .... + depth (noden)*probability(noden)
    # It is obtained by adding probability of a node times the depth of the node for all the nodes.
    # The probabililty is the weight of the node / weight of the tree (the node and its branches)
    def branchels(self, node=None):

        if node is None: node = self.top
        depth = 1

        branchweight = self.branchweight(node)["weight"]
        els = (node.weight/branchweight) * depth

        els += self._branchels(node.right, depth, branchweight)
        els += self._branchels(node.left, depth, branchweight)

        return els

    def _branchels(self, node, depth, branchweight):

        depth += 1

        if node is not None:

            els = (node.weight / branchweight) * depth

            els += self._branchels(node.right, depth, branchweight)
            els += self._branchels(node.left, depth, branchweight)

            return els

        else:

            return 0

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
            #if self.isBalanced(puntero) == False:
            #    aviso = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
            #else:
            aviso = "ok"

            if leftright == "left":
                impresion += "\t"*2*(nivel) + str(nivel) + "\\" + str(puntero.value) + aviso + str(puntero.weight) + "\n"

            elif leftright == "right":
                impresion += "\t"*2*(nivel) + str(nivel) + "/" + str(puntero.value) + aviso + str(puntero.weight) + "\n"

            else:
                impresion += "\t"*2*(nivel) + str(nivel) + str(puntero.value) + aviso + str(puntero.weight) + "\n"

            impresion += self.___str___(puntero.left, nivel+1, "left")
            return impresion




