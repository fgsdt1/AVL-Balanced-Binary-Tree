
import BinaryBalanceTreeAVL as avl
import random as rd
import time

print ("Insert Test --------------------")
#--------------------------------------------------------------------------------
# Preparing a list of random nodes to create the tree
#--------------------------------------------------------------------------------
lista = []
n = 1200
rd.seed(10)
for i in range(n):
    value = rd.randint(0,52900)
    lista.append(value)

#--------------------------------------------------------------------------------
# Tree creation with time control
#--------------------------------------------------------------------------------
starttime = time.time()
mytree = avl.AVLTree()

for i in range(len(lista)):
    nodocp = avl.AVLNode(lista[i])
    mytree.insert(nodocp)

print("height", mytree.height())
print("size", mytree.size)
print ("balanceado total:", mytree.isallBalanced())
endtime = time.time()
abb1 = endtime-starttime

print ("execution time abb1 =", abb1)

#--------------------------------------------------------------------------------
# Deletion test
#--------------------------------------------------------------------------------

print ("Deletion Test --------------------")

# We create a list of elements to delete chosen randomly. Many might not actually exist in the tree
todelete = []
todelete.append(28760)
nb = 29550
for i in range(nb):
    rand = rd.randint(0, 52900)
    todelete.append(rand)

notexisting=0
deleted=0
for i in range(len(todelete)):
    nodo = mytree.findnode(todelete[i])
    if nodo is not None:
        mytree.delete(nodo)
        deleted +=1
    else:
        notexisting+=1

print ("deleted:", deleted)
print ("remaining size:", mytree.size)
print ("balanceado total:", mytree.isallBalanced())

print (mytree)
