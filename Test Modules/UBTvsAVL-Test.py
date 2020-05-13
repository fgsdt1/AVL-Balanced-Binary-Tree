import BinaryBalanceTreeAVL as avl
import UsageBalancedTree as ubt
import random as rd
import cProfile

# --------------------------------------------------------------------------------
# Function to test performance of WBT vs AVL bulk data access with cProfile
# --------------------------------------------------------------------------------
def findtest(listaprueba, tree):

    for ele in range(len(listaprueba)):
        tree.findnode(listaprueba[ele])

# --------------------------------------------------------------------------------
# Function to test performance of AVL insert function with cProfile
# --------------------------------------------------------------------------------
def testinsertAVL(listanodos, tree):

    for ele in range(len(listanodos)):
        tree.insert(listanodos[ele])

# --------------------------------------------------------------------------------
# Random node list generation for tree creation
# --------------------------------------------------------------------------------
lista = []

n = 10000
rd.seed(14)
for i in range(n):
    code = rd.randint(0,2000)
    lista.append(code)

# --------------------------------------------------------------------------------
# AVL and WBT Tree Creation... with time performance check for AVL
# --------------------------------------------------------------------------------
mytree = ubt.UBTree()
mytreeAVL = avl.AVLTree()

listanodos=[]
for i in range(len(lista)):
    listanodos.append(avl.AVLNode(lista[i]))

cProfile.run("testinsertAVL(listanodos, mytreeAVL)")

for i in range(len(lista)):

    nodovalue = ubt.UBTNode(lista[i])
    mytree.insert(nodovalue)

# --------------------------------------------------------------------------------
# WBT - ELS (Expected Length of Search)
# --------------------------------------------------------------------------------
# Just after tree creation, without rebalance
print(mytree.branchweight(mytree.top))
print ("tree ELS:", mytree.branchels(mytree.top))
print ("left ELS", mytree.branchels(mytree.top.left))
print ("right ELS:", mytree.branchels(mytree.top.right))

# We choose a number of nodes (n). Those will be accessed a random number of times.
# This will increase the weight of those nodes
n = 200  # 10% of the nodes
for i in range(200):
    b = rd.choice(lista)
    for i in range(rd.randint(10,100)):
        mytree.findnode(b)

# and we rebalance the tree with the new weights and print the new ELS
mytree.rebalance()

print(mytree.branchweight(mytree.top))
print ("tree ELS", mytree.branchels(mytree.top))
print ("left ELS", mytree.branchels(mytree.top.left))
print ("right ELS", mytree.branchels(mytree.top.right))

# --------------------------------------------------------------------------------
# Preparing the final test data randomly
# --------------------------------------------------------------------------------
listatree = mytree.treetolist()
listatest = []
for i in range(len(listatree)):
    nodo = mytree.findnode(rd.choice(lista))
    #
    # To get a more accurate result of the performance test WBT vs AVL (improved performance of WBT) the list of
    # elements should be evaluated in regards with the weight of each node (more entries for the "heaviest" nodes)
    # For that, we process the initial list data and generate as many requests as random(0,5 - 1,5) times the weight
    # The next two sentences could do the trick when preparing the data set:
    numqueries = 1-rd.randint(-80, 80)/100
    for i in range(int(5*nodo.weight*numqueries)): listatest.append(nodo.value)
    #
    # Alternatively we have done a even distribution of loads, which should benefit AVL performance vs WBT
    # for i in range(40): listatest.append(nodo.value)

rd.shuffle(listatest)

# For performance reference we calculate the cumulative depth of all the nodes accessed.
# Idealy the lowest total depth (WBT vs AVL) should get the best performance
# The different would be the number of times in excess the find method is accessed
dep = 0
depavl = 0

for i in range(len(listatest)):
    noda=mytree.findnode(listatest[i])
    deptmp = mytree.depth(noda)
    dep+=deptmp

    nodo = mytreeAVL.findnode(listatest[i])
    depabbtmp = mytreeAVL.depth(nodo)
    depavl += depabbtmp

print ("Cumulative heights AVL", depavl)
print ("Cumulative heights UBT", dep)


# Final bulk find execition for performance test
cProfile.run("findtest(listatest,mytree)")
cProfile.run("findtest(listatest,mytreeAVL)")









