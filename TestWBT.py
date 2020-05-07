
import WeightBalancedTree as wbt
import random as rd
import time


#--------------------------------------------------------------------------------
# Generación de lista de nodos aleatorios para crear arbol
#--------------------------------------------------------------------------------
lista = []

lista.append(50)
lista.append(62)
lista.append(68)
lista.append(62)
lista.append(68)

n = 150
rd.seed(0)
for i in range(n):
    if i%2 == 0:
        codigo = rd.choice(lista)
    else:
        codigo = rd.randint(0,100)

    lista.append(codigo)

print (lista)
#--------------------------------------------------------------------------------
# Creación del arbol con control tiempo
#--------------------------------------------------------------------------------
starttime = time.time()
miarbol = wbt.WBTree()

for i in range(len(lista)):
    nodovalue = wbt.WBTNode(lista[i])
    miarbol.insert(nodovalue)

print("this is the last-------------------------")

print ("size=", miarbol.size)
print ("weight=", miarbol.weight)

print (miarbol)


print(miarbol.branchweight(miarbol.top))
print ("arbol", miarbol.branchels(miarbol.top))
print ("izquierda", miarbol.branchels(miarbol.top.left))
print ("derecha", miarbol.branchels(miarbol.top.right))

print(miarbol.size, miarbol.treesize())
endtime = time.time()
abb1 = endtime-starttime

print ("execution time abb1 =", abb1)
