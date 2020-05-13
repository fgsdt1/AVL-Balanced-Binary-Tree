
#----------------------------------------------------------------------------------------------------------------------
# Node for the AVL Tree. Value is the key
#----------------------------------------------------------------------------------------------------------------------
class AVLNode:

    def __init__(self, value):

        self.father = None
        self.left = None
        self.right = None
        self.value = value

    def __str__(self):

        if self.father is not None:
            imprimir = "node:" + str (self.value) + ", father:" + str(self.father.value)
        else:
            imprimir = "node:" + str(self.value) + "- It is root"

        return imprimir

#----------------------------------------------------------------------------------------------------------------------
# AVL Balanced Tree Class. Self balanced at insert and delete
#----------------------------------------------------------------------------------------------------------------------
class AVLTree:

    def __init__(self):

        self.top = None
        self.size = 0

    # ------------------------------------------------------------------------------------------------------------------
    # Basic insert method. First call
    def insert(self, nodocp):

        if self.top is None:        # If it is the first element we insert it at the top (root)
            self.top = nodocp
            self.size += 1
        else:
            pointer = self.top      # We go trhough the tree with "pointer" to find the position to insert. Starting at root.
            father = None

            # recursive insert call
            self._insert(father, pointer, nodocp)

    # Recursive insert method. Using pointer, it looks for the location where node value fits. Then inserts and balances
    def _insert(self, father, pointer, nodocp):
        # Params:
        #   fahter: To identify the last visited node before finding the "None" where to insert
        #   pointer: The tree node we are working with at this recursive call
        #   nodocp: The node we want to insert

        if pointer is None:             # If the pointer is None, here we have to insert
            nodocp.father = father      # The parent of the new element is the father node
            if father.value > nodocp.value:
                father.left = nodocp
            else:
                father.right = nodocp
            self.size += 1              # Tree size increases by one

            # For the balancing, we go down-top until the grandfather (father.father) is None, meaning we are at top
            while father.father is not None:
                # We balance with the grandfather as the node to do the calculations
                father = self.nodereBalance(father.father)

        elif pointer.value > nodocp.value:                # We keep looking down the left branch if it is smaller
            self._insert(pointer, pointer.left, nodocp)
        elif pointer.value < nodocp.value:                # We keep looking down the right branch if it is bigger
            self._insert(pointer, pointer.right, nodocp)
        else:
            return

    # ------------------------------------------------------------------------------------------------------------------
    # Main method for value find. We receive the key and return the node object (or None if it does not exist)
    def findnode (self, cp):

        return self._findnode(cp, self.top)    # Call to the recursive method

    # Find recursive method
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
    # Delete method. It receives the node to delete (not the key value)
    def delete(self, node):

        if node is None:
            return 0

        if node.right is None and node.left is None:            # When the node is a leaf (no children)
            if node.father.right == node:                       # The parent is assigned None right or left, depending
                node.father.right = None
            elif node.father.left == node:
                node.father.left = None
            self.size -= 1                                      # Tree size minus one

            # We rebalance down-top until the father of the node is None (root)
            while node.father is not None:
                # The balancing is made starting on the father of the node recently deleted
                node = self.nodereBalance(node.father)

        elif node.right is None:                                # When the node to delete has only one child (left)
            if node.father is None:                             # If the node to delete is at top (no father)
                self.top = node.left                            # Change tree.top to the left branch remaining
                node.left.father = None
            elif node.father.right == node:                     # Else, we assign the left branch to the parent, depending
                node.father.right = node.left
                node.left.father = node.father
            elif node.father.left == node:
                node.father.left = node.left
                node.left.father = node.father

            self.size -= 1                                      # Tree size minus one

            # We rebalance down-top until the father of the node is None (root)
            while node.father is not None:
                # The balancing is made starting on the father of the node recently deleted
                node = self.nodereBalance(node.father)

        elif node.left is None:                                 # When the node to delete has only one child (right)
            if node.father is None:                             # If the node to delete is at top (no father)
                self.top = node.right                           # Change tree.top to the left branch remaining
                node.right.father = None
            elif node.father.right == node:                     # Else, we assign the left branch to the parent, depending
                node.father.right = node.right
                node.right.father = node.father
            elif node.father.left == node:
                node.father.left = node.right
                node.right.father = node.father

            self.size -= 1                                      # Tree size minus one

            # We rebalance down-top until the father of the node is None (root)
            while node.father is not None:
                # The balancing is made starting on the father of the node recently deleted
                node = self.nodereBalance(node.father)

        else:
            lowesthigh  = self.findlowesthigh(node)             # Look for the substitute as the precedent in the tree (the highest of the lower)

            oldfather = lowesthigh.father                       # WE keep the father of the substitute to rebalance from there later

            if lowesthigh.father.left == lowesthigh:            # Depending if the parent of the substitute is right or left
                lowesthigh.father.left = lowesthigh.right       # We assign the children of the substitute as needed
                if lowesthigh.right is not None:                # If children is not None, we can assign them to the new father
                    lowesthigh.right.father = lowesthigh.father # They will only be left children, therwise it would not be precedent
            else:
                lowesthigh.father.right = lowesthigh.right
                if lowesthigh.right is not None:                # If children is not None, we can assign them to the new father
                    lowesthigh.right.father = lowesthigh.father # They will only be left children, therwise it would not be precedent

            if node.father is None:                             # In case the deleted node is the top/root
                self.top = lowesthigh
                lowesthigh.father = None
            else:
                if node.father.right == node:                   # Depending if the parent of the substitute is right or left
                    node.father.right = lowesthigh              # And assign the substitute as the new child
                    lowesthigh.father = node.father
                else:
                    node.father.left = lowesthigh
                    lowesthigh.father = node.father

            # Assign the children of the deleted node to the substitute
            lowesthigh.right = node.right
            if node.right is not None: node.right.father = lowesthigh
            lowesthigh.left = node.left
            if node.left is not None: node.left.father = lowesthigh

            self.size -= 1                                      # Tree size minus one


            # We rebalance down-top until the father of the node is None (root). We start at the father of the substitute
            # prior to being removed
            while oldfather is not None:
                # The balancing is made starting on the father of the node recently deleted
                oldfather = self.nodereBalance(oldfather).father


        return 1

    # ------------------------------------------------------------------------------------------------------------------
    # Main method to find the following node within the tree(the lowest of the higher)
    def findlowesthigh(self, node):

        if node.right is not None:
            return self._findlowesthigh(node.right)
        else:
            return node

    # Recursive method to find the following node
    def _findlowesthigh(self, node):

        if node.left is not None:
            return self._findlowesthigh(node.left)
        else:
            return node

    # ------------------------------------------------------------------------------------------------------------------
    # Method to rebalance (not recursive) for a given node
    # It will be used to do a balancing down-top
    def nodereBalance(self, node=None):

        # We first check the balance of the branches right and left of the node
        nodebalance = self.balanceNum(node)

        if abs(nodebalance) >= 2:                       # If absolute value of balance is equal or greater than two
            if nodebalance <= -2:                       # If the balance is negative (right branch higher)
                son = node.right
                sonbalance = self.balanceNum(son)       # We check the balance of the right child
                if sonbalance == -1:                    # If the balance is -1 we make a left rotation
                    self.rotate (son, "left")
                    return son                          # We return the son so that it can continue balancing up to the top

                elif sonbalance == 1:                   # If the balance is 1 we make a double rotation: right, left
                    pivot = son.left                    # The rotation is made considering the son of the son as pivot
                    self.rotate (pivot, "right")
                    self.rotate (pivot, "left")
                    return pivot                         # We return the pivot so that it can continue balancing up to the top

                else:
                    # This case is a (rare)situation in which both sons hava a 0 balance, but nonetheless one of the
                    # branches is longuer than the other. It is balanced as if it were -1 (though it is 0)
                    # We could include it in the first if, but we put it here for easier understanding
                    self.rotate(son, "left")
                    return son

            elif nodebalance >= 2:                      # If the balance is positive (left branch higher)
                son = node.left
                sonbalance = self.balanceNum(son)       # We check the balance of the left child
                if sonbalance == 1:                     # If the balance is 1 we make a right rotation
                    self.rotate (son, "right")
                    return son                          # We return the son so that it can continue balancing up to the top

                elif sonbalance == -1:                  # If the balance is -11 we make a double rotation: left, right
                    pivot = son.right                   # The rotation is made considering the son of the son as pivot
                    self.rotate (pivot, "left")
                    self.rotate (pivot, "right")
                    return pivot                         # We return the pivot so that it can continue balancing up to the top

                else:
                    # This case is a (rare)situation in which both sons hava a 0 balance, but nonetheless one of the
                    # branches is longuer than the other. It is balanced as if it were +1 (though it is 0)
                    # We could include it in the first if, but we put it here for easier understanding
                    self.rotate (son, "right")
                    return son

        else:

            return node                                 # If it is balanced, we return the node to kepp rebalancing up

    # ------------------------------------------------------------------------------------------------------------------
    # Method to rotate the tree when needs rebalance
    def rotate(self, node, rotation):

        # We need to keep track of the father and gfather of the node to rotate
        gfather = node.father.father
        father = node.father

        # The node new father is now the grandfather
        node.father = gfather

        if rotation == "left":
            if gfather is None:
                self.top = node
            else:
                # The gfather son's is now the node rotated, right or left as corresponds
                if gfather.left == father:
                    gfather.left = node
                else:
                    gfather.right = node

            father.father = node            # The father of the father is now the son/node
            father.right = node.left        # The child by the right of the father is now the former left child of the node
            if node.left is not None:       # The children of the node change father (node) to the father of the node
                node.left.father = father
            node.left = father              # The left children of the node is now the former father

        elif rotation == "right":
            if gfather is None:
                self.top = node
            else:
                # The gfather son's is now the node rotated, right or left as corresponds
                if gfather.left == father:
                    gfather.left = node
                else:
                    gfather.right = node

            father.father = node            # The father of the father is now the son/node
            father.left = node.right        # The child by the left of the father is now the former right child of the node
            if node.right is not None:      # The children of the node change father (node) to the father of the node
                node.right.father = father
            node.right = father             # The right children of the node is now the former father


        else:
            return

        return

    # ------------------------------------------------------------------------------------------------------------------
    # Method to calculate the balance between branches of a node
    def balanceNum(self, node=None):

        if node is None:
            node = self.top

        # It returns the height difference between the right and left branches of the node
        # It will be positive if left branch has more levels, negative on the contrary (or 0 if equal)
        return self._height(node.left) - self._height(node.right)

    # ------------------------------------------------------------------------------------------------------------------
    # Method to check that a given node is balanced between branches
    # Similar to balanceNum but returning Treu or False if balance is between -1 and 1
    def isBalanced(self, node=None):

        if node is None:
            node = self.top

        rightheight = self._height(node.right)
        leftheight = self._height(node.left)

        if abs(leftheight - rightheight) <= 1:
            return True
        else:
            return False

    # ------------------------------------------------------------------------------------------------------------------
    # Main method (node=top/root) to check that a node and all the nodes bellow are correctly balanced
    def isallBalanced(self):

        nodo = self.top
        return self._isallBalanced(nodo)

    # Recursive method to check that a given node and all nodes bellow are correctly balanced
    def _isallBalanced(self, node):

        resultado = False

        rightheight = self._height(node.right)
        leftheight = self._height(node.left)

        if abs(leftheight - rightheight) <= 1:
            resultado = True
        else:
            resultado = False

        if node.left is not None:
            resultado = resultado and self._isallBalanced(node.left)
        if node.right is not None:
            resultado = resultado and self._isallBalanced(node.right)

        return resultado

    # ------------------------------------------------------------------------------------------------------------------
    # Recursive method to calculate the depth (levels to top) of a node
    def depth(self, node):

        if node.father is not None:
            depth = self.depth(node.father)
            depth += 1
            return depth
        else:
            return 1

    # ------------------------------------------------------------------------------------------------------------------
    # Main method to calculate the height (levels to the deepest leaf bellow) of the tree (starting at top) 
    def height(self):

        treeheight = 0
        pointer = self.top
        treeheight += self._height(pointer)
        return treeheight

    # Main method to calculate the height (levels to the deepest leaf bellow) of a given node 
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
    # Main method to calculate the size of a tree (it should actually match the size attribute of the tree)
    def treesize(self):

        pointer = self.top
        treesize=0
        treesize += self._treesize(pointer)
        return treesize

    # Recursive method to calculate the size of a tree bellow a given node
    def _treesize(self, pointer):

        if pointer is not None:
            treesize = 1
            treesize += self._treesize(pointer.left)
            treesize += self._treesize(pointer.right)
            return treesize
        else:
            return 0

    # ------------------------------------------------------------------------------------------------------------------
    # Main method to print the tree from the top. Calls the recursive method
    def __str__(self):

        printing = ""
        pointer = self.top
        printing += self.___str___(pointer, 0, "")
        return printing

    # Recursive method to print the tree down.
    # The level is sent to the method to include it in the printing, but also to include tabs to improve visualization
    def ___str___(self, pointer, level, leftright):

        if pointer is None:
            return ""
        else:
            printing =""
            printing += self.___str___(pointer.right, level + 1, "right")

            # It includes a field (watch) as a check that the tree is correctly balanced
            # It increases the overload of the print. It is not necessary but helps check the class is working ok
            if self.isBalanced(pointer) == False:
                watch = "------------ WARNING ------------"
            else:
                watch = "ok"

            # We use the level to print it on the screen, but also to tab the line as many times as the level (x2)
            # We indicate visually if it is a right or left child with the \ and / signs
            # We also include the height of each branch. It increases overload, but it is also for checking purposes
            if leftright == "left":
                printing += "\t" * 2 * (level) + str(level) + "\\" + str(pointer.value) + watch + str(self._height(pointer.left)) + str(self._height(pointer.right)) + "\n"

            elif leftright == "right":
                printing += "\t" * 2 * (level) + str(level) + "/" + str(pointer.value) + watch + str(self._height(pointer.left)) + str(self._height(pointer.right)) + "\n"

            else:
                printing += "\t" * 2 * (level) + str(level) + str(pointer.value) + watch + str(self._height(pointer.left)) + str(self._height(pointer.right)) + "\n"

            printing += self.___str___(pointer.left, level + 1, "left")

            return printing

