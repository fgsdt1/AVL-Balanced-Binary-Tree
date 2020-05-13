
import UsageBalancedTree as ubt
import random as rd
import cProfile

# --------------------------------------------------------------------------------
# Function to test performance of WBT bulk data access with cProfile
# --------------------------------------------------------------------------------
def findtest(listaprueba, tree):

    for ele in listaprueba:
        tree.findnode(ele.value)


# --------------------------------------------------------------------------------
# Random node list generation for tree creation
# --------------------------------------------------------------------------------
lista = []

n = 100
rd.seed(23)
for i in range(n):
    code = rd.randint(0,10)
    lista.append(code)

# --------------------------------------------------------------------------------
# WBT Tree Creation
# --------------------------------------------------------------------------------
mytree = ubt.UBTree()

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

# We increase the weight of the nodes by randomly access the tree to search for nodes several times
for i in range(100):
    mytree.findnode(rd.choice(lista))

# and we rebalance the tree with the new weights and print the new ELS

# --------------------------------------------------------------------------------
# Preparing the final test data randomly
# --------------------------------------------------------------------------------
listatree = mytree.treetolist()

rd.shuffle(listatree)

print(mytree)

print("\n_____________\n")

mytree.rebalance()
print(mytree.branchweight(mytree.top))
print ("tree ELS", mytree.branchels(mytree.top))
print ("left ELS", mytree.branchels(mytree.top.left))
print ("right ELS", mytree.branchels(mytree.top.right))

print("\n_____________\n")

cProfile.run("findtest(listatree,mytree)")


mytree.delete(mytree.findnode(7))
mytree.delete(mytree.findnode(9))
print(mytree)




