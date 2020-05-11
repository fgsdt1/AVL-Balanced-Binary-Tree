
#-----------------------------------------------------------------------------------------------------------------------
# Node Class with Value (in this case numeric) and the weight
#-----------------------------------------------------------------------------------------------------------------------
class WBTNode:

    def __init__(self, value, weight=1, father=None, left=None, right=None):

        self.father = father
        self.left = left
        self.right = right
        self.value = value
        self.weight = weight

    def copynode(self):

        return WBTNode(self.value, self.weight, self.father, self.left, self.right)

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

    # todo: optimizar código de listtotree para que si el primero tiene poco peso mandarlo abajo
    # todo: delete ubt

    def __init__(self):

        self.top = None
        self.size = 0

    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # Metodos para insertar, borrar y encontrar un nodo en el arbol
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # Basic tree insert method (calls the recursive one)
    def insert(self, node):

        if self.top is None:        # If it is the first element in the tree
            self.top = node
            self.size += 1
        else:
            pointer = self.top      # We go trough the tree nodes with "pointer" to locate where to insert. Starting at top.
            father = None

            # Recursive insert call
            self._insert(father, pointer, node)

    # ------------------------------------------------------------------------------------------------------------------
    # Recursive tree insert method. Looks for the place to insert a new node
    # An insert (if its weight is 1 as should be in a first insert) will not unbalance the tree significantly,
    def _insert(self, father, pointer, node):
        if pointer is None:                         # If the pointer is None, here is where we have to insert
            node.father = father                    # The father of the new element is the father we sent to the method
            if father.value > node.value:           # If the father is greater, the left son of the father is the pointer
                father.left = node
            else:                                   # else, it will be the right son
                father.right = node
            self.size += 1                          # The size of the tree increases by 1
        elif pointer.value > node.value:             # Keep searching where to insert recursively in the left
            self._insert(pointer, pointer.left, node)
        elif pointer.value < node.value:                # Keep searching where to insert recursively in the left
            self._insert(pointer, pointer.right, node)
        else:
            pointer.weight += node.weight           # The weight of tree and node increases by the weight of the node

        return

    # ------------------------------------------------------------------------------------------------------------------
    # Bassic tree search method by value. Calls the recursive method.
    def findnode (self, value):

        return self._findnode(value, self.top)

    # ------------------------------------------------------------------------------------------------------------------
    # Recursive tree search method by value. When found adds 1 to the weight of the node.
    def _findnode(self, value, node):

        if node is None:
            return None
        if node.value == value:
            node.weight += 1
            return node
        elif node.value > value:
            return self._findnode(value, node.left)
        else:
            return self._findnode(value, node.right)

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
    # ------------------------------------------------------------------------------------------------------------------
    # Metodos para calcular el Expected Legth of Search - ELS
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # Calculates the expected length of search (ELS) to all the nodes depending on the weight. The lower the better.
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

    # ------------------------------------------------------------------------------------------------------------------
    # Recursive call for the ELS calculation
    def _branchels(self, node, depth, branchweight):

        depth += 1

        if node is not None:

            els = (node.weight / branchweight) * depth
            els += self._branchels(node.right, depth, branchweight)
            els += self._branchels(node.left, depth, branchweight)
            return els

        else:

            return 0

    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # Metodos de rebalanceo del arbol treetolist and listtotree
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # Rebalance the tree
    def rebalance(self):

        treelist = self.treetolist()
        self.listtotree(treelist)

    # ------------------------------------------------------------------------------------------------------------------
    # Create a list from the tree to rebalance it later
    def treetolist(self):

        treelist = []
        self._treetolist(self.top, treelist)
        return treelist

    # ------------------------------------------------------------------------------------------------------------------
    # Recursive to create the list from the tree
    def _treetolist(self, nodo, treelist):

        if nodo is not None:
            self._treetolist(nodo.left,treelist)
            treelist.append(nodo)
            self._treetolist(nodo.right,treelist)

    # ------------------------------------------------------------------------------------------------------------------
    # Main method. Create back the tree, optimal, from the list
    def listtotree(self, treelist):

        frequency = 0
        treeweight = self.treeweight()

        for i in range(len(treelist)):
            frequency += treelist[i].weight/treeweight
            if frequency >= 0.50:
                self.top = treelist[i]
                self.top.father = None
                self.top.left = self._listtotree(treelist[:i])
                if self.top.left is not None: self.top.left.father = self.top
                self.top.right = self._listtotree(treelist[i+1:])
                if self.top.right is not None: self.top.right.father = self.top
                break

    # ------------------------------------------------------------------------------------------------------------------
    # Recursive method. Create back the tree, optimal, from the list
    def _listtotree(self, treelist):

        frequency = 0
        branchweight = 0
        node = None
        for i in range(len(treelist)): branchweight += treelist[i].weight

        for i in range(len(treelist)):
            frequency += treelist[i].weight / branchweight
            if frequency >= 0.50:

                treelist[i].left = self._listtotree(treelist[:i])
                if treelist[i].left is not None: treelist[i].left.father = treelist[i]

                treelist[i].right = self._listtotree(treelist[i + 1:])
                if treelist[i].right is not None: treelist[i].right.father = treelist[i]

                node = treelist[i]
                break

        return node

    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # Cáluclos de profundidad (depth) de un nodo y altura (height) del arbol o un nodo
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # Metodo recursivo para calcular la profundidad
    def depth(self, nodo):

        if nodo.father is not None:
            depth = self.depth(nodo.father)
            depth +=1
            return depth
        else:
            return 1

    # ------------------------------------------------------------------------------------------------------------------
    # Método principal para calcular la altura de un arbol
    def height(self):

        treeheight = self._height(self.top)
        return treeheight

    # ------------------------------------------------------------------------------------------------------------------
    # Método recursivo a partir de un nodo para calcular la altura de las ramas y nodos por debajo
    def _height(self, pointer):

        if pointer is None:
            return 0
        else:
            levelsleft = self._height(pointer.left)
            levelsright = self._height(pointer.right)
            if levelsleft <= levelsright:
                return levelsright+1
            else:
                return levelsleft+1

    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # Cáluclos de tamaño (treesiza) y peso (treeweight) del arbol
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # Método principal para calcular el tamaño de un arbol. Debería coincidir con el atributo .size del arbol
    def treesize(self):

        pointer = self.top
        treesize=0
        treesize += self._treesize(pointer)
        return treesize

    # ------------------------------------------------------------------------------------------------------------------
    # Método recursivo para clacular el tamaño de un arbol a partir de un puntero
    def _treesize(self, pointer):

        if pointer is not None:
            treesize = 1
            treesize += self._treesize(pointer.left)
            treesize += self._treesize(pointer.right)
            return treesize
        else:
            return 0

    # ------------------------------------------------------------------------------------------------------------------
    # Método principal para calcular el peso de un arbol.
    def treeweight(self):

        treeweight = self._treeweight(self.top)
        return treeweight

    # ------------------------------------------------------------------------------------------------------------------
    # Método recursivo para clacular el tamaño de un arbol a partir de un puntero
    def _treeweight(self, pointer):

        if pointer is not None:
            treeweight = pointer.weight
            treeweight += self._treeweight(pointer.left)
            treeweight += self._treeweight(pointer.right)
            return treeweight
        else:
            return 0

    # ------------------------------------------------------------------------------------------------------------------
    # Calculates the total weight of a node and all its branches together with the number of nodes (Size) and height
    # Provides more information than treeweight and treesize but it is more complex / resource consuming
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
    # ------------------------------------------------------------------------------------------------------------------
    # Métodos de impresión
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # Método principal de impresión del arbol
    def __str__(self):

        impresion = ""
        puntero = self.top
        impresion += self.___str___(puntero, 0, "")
        return impresion

    # ------------------------------------------------------------------------------------------------------------------
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




