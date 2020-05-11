
import UsageBalancedTree as ubt
import random as rd
import cProfile

# --------------------------------------------------------------------------------
# Function to test performance of WBT bulk data access with cProfile
# --------------------------------------------------------------------------------
def findtest(listaprueba, tree):

    for ele in range(len(listaprueba)):
        tree.findnode(listaprueba[ele])


# --------------------------------------------------------------------------------
# Random node list generation for tree creation
# --------------------------------------------------------------------------------
lista = []

n = 10000
rd.seed(543)
for i in range(n):
    code = rd.randint(0,2000)
    lista.append(code)

print (lista)

# --------------------------------------------------------------------------------
# WBT Tree Creation
# --------------------------------------------------------------------------------
mytree = ubt.WBTree()

for i in range(len(lista)):

    nodovalue = ubt.WBTNode(lista[i])
    mytree.insert(nodovalue)

print ("---")
print (mytree)
# --------------------------------------------------------------------------------
# WBT - ELS (Expected Length of Search)
# --------------------------------------------------------------------------------
# Just after tree creation, without rebalance
print(mytree.branchweight(mytree.top))
print ("tree ELS:", mytree.branchels(mytree.top))
print ("left ELS", mytree.branchels(mytree.top.left))
print ("right ELS:", mytree.branchels(mytree.top.right))

# We increase the weight of the nodes by randomly access the tree to search for nodes several times
for i in range(10000):
    mytree.findnode(rd.choice(lista))

# and we rebalance the tree with the new weights and print the new ELS
mytree.rebalance(False)

print(mytree.branchweight(mytree.top))
print ("tree ELS", mytree.branchels(mytree.top))
print ("left ELS", mytree.branchels(mytree.top.left))
print ("right ELS", mytree.branchels(mytree.top.right))

print("\n_____________\n")

# --------------------------------------------------------------------------------
# Preparing the final test data randomly
# --------------------------------------------------------------------------------
listatree = mytree.treetolist()

listatest = []
for i in range(len(listatree)):
    nodo = mytree.findnode(rd.choice(lista))
    #
    # To get a more accurate result of the performance test the list of elements should be evaluated in regards with
    # the weight of each node (more entries for the "heaviest" nodes).
    # For that, we process the initial list data and generate as many requests as random(0,5 - 1,5) times the weight
    # The next two sentences could do the trick when preparing the data set:
    numqueries = 1-rd.randint(-80, 80)/100
    for i in range(int(5*nodo.weight*numqueries)): listatest.append(nodo.value)


rd.shuffle(listatest)


# Final bulk find execition for performance test
cProfile.run("findtest(listatest,mytree)")



