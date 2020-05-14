
#-----------------------------------------------------------------------------------------------------------------------
# Node Class with Value (in this case numeric) and the weight
#-----------------------------------------------------------------------------------------------------------------------
class UBTNode:

    def __init__(self, value, weight=1, father=None, left=None, right=None):

        self.father = father
        self.left = left
        self.right = right
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
class UBTree:

    def __init__(self):

        self.top = None
        self.size = 0

    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # Methods to insert, delete and find nodes in the tree
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
            self.size -= 1

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
            self.size -= 1

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
            self.size -= 1

        else:
            previous = self.findprevious(node.left)
            next = self.findnext(node.right)

            depthprevious = self.depth(previous)
            depthnext = self.depth(next)

            treeweight = self.treeweight()
            elsprevious = (previous.weight / treeweight) * depthprevious
            elsnext = (next.weight / treeweight) * depthnext

            if elsnext >= elsprevious:

                node.value = next.value
                node.weight = next.weight

                self.delete(next)

            else:

                node.value = previous.value
                node.weight = previous.weight

                self.delete(previous)


        return 1

    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # Methods to calculate the Expected Legth of Search - ELS
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

        #branchweight = self.branchweight(node)["weight"]
        branchweight = self._treeweight(node)
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
    # Methods to rebalance and adjust the tree (treetolist and listtotree)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # Rebalance the tree
    #       - adjust, default True, makes fine adjustments to slightly improve the ELS of the tree
    def rebalance(self, adjust=True):

        # We convert the tree in an ordered list of nodes
        treelist = self.treetolist()

        # we transform back the list into a tree considering the weight of the nodes
        self.top = self.listtotree(treelist)
        self.top.father = None

        # If wanted it makes fine adjustments to the balancing of the nodes
        if adjust:
            self.nodeadjust(self.top)

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
    # Recursive method. Create back the tree, optimal weight balance, from the list
    def listtotree(self, treelist):

        # We are going to prepare a "frequency table" of the node values based on their weight
        frequency = 0
        branchweight = 0
        node = None

        # The weight of the branch is the addition of all the weights
        for i in range(len(treelist)): branchweight += treelist[i].weight

        for i in range(len(treelist)):

            # The frequency of a node will be the weight of the node / the total weight of the elements in the tree
            frequency += treelist[i].weight / branchweight

            # When the cumulative frequency >= .50 (half the weight) we split the tree in two
            if frequency >= 0.50:

                treelist[i].left = self.listtotree(treelist[:i])               # recursive for the left remaining nodes
                if treelist[i].left is not None: treelist[i].left.father = treelist[i]

                treelist[i].right = self.listtotree(treelist[i + 1:])          # recursive for right remaining nodes
                if treelist[i].right is not None: treelist[i].right.father = treelist[i]

                node = treelist[i]
                break

        return node

    # ------------------------------------------------------------------------------------------------------------------
    # Recursive method to adjust nodes if possible, comparing each node with the precedent (previous) or following (next)
    # ones to see if switching places improves the total ELS.
    def nodeadjust(self, pointer):

        if pointer is not None and (pointer.left is not None or pointer.right is not None):

            # Calculate the depth of the node (pointer) and the weight of the tree for later calculations
            depthpointer = self.depth(pointer)
            treeweight = self.treeweight()

            # We look for the previous and next node to see if it is worth to swap
            if pointer.left is not None:
                previous = self.findprevious(pointer.left)
                depthprevious = self.depth(previous)
                # The relative weight of the previous is the weight of the node / total weight of the tree times its depth
                elsprevious = (previous.weight / treeweight) * depthprevious
            else:
                previous = None
                depthprevious = depthpointer
                elsprevious = 0

            if pointer.right is not None:
                next = self.findnext(pointer.right)
                depthnext = self.depth(next)
                # The relative weight of the next is the weight of the node / total weight of the tree times its depth
                elsnext = (next.weight / treeweight) * depthnext
            else:
                next = None
                depthnext = depthpointer
                elsnext = 0

            # We choose to work with the node (previous or next) that can provide better improvement (higher ELS)
            if elsnext >= elsprevious:
                # The improvement is the weight of the node to "upgrade" (next), times the number of levels upgraded
                # plus the addition of the weights of the right branch, that will go up one level if next is removed
                improvement = next.weight*(depthnext-depthpointer) + self._treeweight(next.right)

                # If the possible improvement is greater than the pointer relative weight increase when downgraded...
                # calculated as the weight of the pointer times the difference of depths with its new position, which
                # would be that of a son of the previous
                if improvement > pointer.weight*(depthprevious-depthpointer+1):

                    # Create a new node with the pointer value/weight that will be placed as right son of previous
                    newnode = UBTNode(pointer.value, pointer.weight)

                    # Assign to the pointer node the value/weight of the next
                    pointer.value = next.value
                    pointer.weight = next.weight

                    # Place the new node (pointer values) under the previous node
                    if previous is not None:
                        previous.right = newnode
                        previous.right.father = previous
                    else:
                        pointer.left = newnode
                        pointer.left.father = pointer

                    # delete the next node, placed now where the pointer used to be
                    self.delete(next)


            elif elsprevious > elsnext:
                # The improvement is the weight of the node to "upgrade" (previous), times the number of levels upgraded
                # plus the addition of the weights of the left branch, that will go up one level if previous is removed
                improvement = previous.weight*(depthprevious-depthpointer) + self._treeweight(previous.left)

                # If the possible improvement is greater than the pointer relative weight increase when downgraded...
                # calculated as the weight of the pointer times the difference of depths with its new position, which
                # would be that of a son of the next
                if improvement > pointer.weight*(depthnext - depthpointer + 1):

                    # Create a new node with the pointer value/weight that will be placed as left son of next
                    newnode = UBTNode(pointer.value, pointer.weight)

                    # Assign to the pointer node the value/weight of the previous
                    pointer.value = previous.value
                    pointer.weight = previous.weight

                    # Place the new node (pointer values) under the next node
                    if next is not None:
                        next.left = newnode
                        next.left.father = next
                    else:
                        pointer.right = newnode
                        pointer.right.father = pointer

                    # delete the previous node, placed now where the pointer used to be
                    self.delete(previous)

            self.nodeadjust(pointer.left)
            self.nodeadjust(pointer.right)

    # ------------------------------------------------------------------------------------------------------------------
    # Recursive method to find the next (following) node of a given node within a tree
    def findnext(self, nodo):

        if nodo.left is not None:
            return self.findnext(nodo.left)
        else:
            return nodo

    # Recursive method to find the previous (precedent) node of a given node within a tree
    def findprevious(self, nodo):

        if nodo.right is not None:
            return self.findprevious(nodo.right)
        else:
            return nodo

    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # Depth calculation for a node and Height calculation for a node or the whole tree
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # Recursive method to calculate the depth (levels up to the top) from a node
    def depth(self, nodo):

        if nodo.father is not None:
            depth = self.depth(nodo.father)
            depth +=1
            return depth
        else:
            return 1

    # ------------------------------------------------------------------------------------------------------------------
    # Main method to calculate the height of the tree. Calls the recursive method
    def height(self):

        treeheight = self._height(self.top)
        return treeheight

    # ------------------------------------------------------------------------------------------------------------------
    # Recursive method to calcuulate the height of a given node
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
    # Calculations for size (treesiza) and weight(treeweight) of the tree
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # Main method to calculate the size of the tree. It calls the recursive method. It should match the .size attribute
    def treesize(self):

        pointer = self.top
        treesize=0
        treesize += self._treesize(pointer)
        return treesize

    # ------------------------------------------------------------------------------------------------------------------
    # Recursive method to calculate the size of the tree (from a given node)
    def _treesize(self, pointer):

        if pointer is not None:
            treesize = 1
            treesize += self._treesize(pointer.left)
            treesize += self._treesize(pointer.right)
            return treesize
        else:
            return 0

    # ------------------------------------------------------------------------------------------------------------------
    # Main method to calculate the total weight of the tree. It calls the recursive method.
    def treeweight(self):

        treeweight = self._treeweight(self.top)
        return treeweight

    # ------------------------------------------------------------------------------------------------------------------
    # Recursive method to calculate the total weight of the tree from a given point down
    def _treeweight(self, pointer):

        if pointer is not None:
            treeweight = pointer.weight
            treeweight += self._treeweight(pointer.left)
            treeweight += self._treeweight(pointer.right)
            return treeweight
        else:
            return 0

    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # Printing methods
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # Main printing method for the tree
    def __str__(self):

        impresion = ""
        puntero = self.top
        impresion += self.___str___(puntero, 0, "")
        return impresion

    # ------------------------------------------------------------------------------------------------------------------
    # Recursive method to print the tree down.
    # The level is sent to the method to include it in the printing, but also to include tabs to improve visualization
    def ___str___(self, puntero, nivel, leftright):

        if puntero is None:
            return ""
        else:
            impresion =""
            impresion += self.___str___(puntero.right, nivel + 1, "right")

            # We use the level to print it on the screen, but also to tab the line as many times as the level (x2)
            # We indicate visually if it is a right or left child with the \ and / signs
            # We also include the height of each branch. It increases overload, but it is also for checking purposes
            if leftright == "left":
                impresion += "\t"*2*(nivel) + str(nivel) + "\\" + str(puntero.value) + "-" + str(puntero.weight) + "\n"

            elif leftright == "right":
                impresion += "\t"*2*(nivel) + str(nivel) + "/" + str(puntero.value) + "-" + str(puntero.weight) + "\n"

            else:
                impresion += "\t"*2*(nivel) + str(nivel) + "|->" + str(puntero.value) + "-" + str(puntero.weight) + "\n"

            impresion += self.___str___(puntero.left, nivel+1, "left")
            return impresion




