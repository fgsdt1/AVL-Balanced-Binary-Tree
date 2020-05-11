
import BinaryBalanceTreeAVL as avl
import random as rd
import time

#--------------------------------------------------------------------------------
# Generación de lista de nodos aleatorios para crear arbol
#--------------------------------------------------------------------------------
lista = []
n = 1200
rd.seed(0)
for i in range(n):
    codigo = rd.randint(0,52900)
    lista.append(codigo)

#--------------------------------------------------------------------------------
# Creación del arbol con control tiempo
#--------------------------------------------------------------------------------
starttime = time.time()
miarbol = avl.ABBCodigoPostal()

for i in range(len(lista)):
    nodocp = avl.CodigoPostal(lista[i])
    miarbol.insert(nodocp)

print("this is the last-------------------------")
print(miarbol.height())
print(miarbol._height(miarbol.top.left))
print(miarbol._height(miarbol.top.right))
print(miarbol.size, miarbol.treesize())
endtime = time.time()
abb1 = endtime-starttime

print ("execution time abb1 =", abb1)


#--------------------------------------------------------------------------------
#Test de borrado
#--------------------------------------------------------------------------------

# Editar lista de elementos a borrar
borrar = []
borrar.append(28760)
nb = 29550
for i in range(nb):
    rand = rd.randint(0, 52000)
    #if mytree.findnode(rand) is not None:
    borrar.append(rand)


print ("Lista creada --------------------")
print(borrar)
print ("size:", miarbol.size, "-", miarbol.treesize())
print ("balanceado total:", miarbol.isallBalanced())
noexiste=0
borrados=0
for i in range(len(borrar)):
    nodo = miarbol.findnode(borrar[i])
    if nodo is not None:
        print ("borrar:-----------------------------------------------------", nodo, "--------------------------------------------------")
        print("balanceado total:", miarbol.isallBalanced())
        miarbol.delete(nodo)
        borrados +=1
    else:
        noexiste+=1
print ("no existieron:", noexiste)
print ("borrados:", borrados)
print ("size:", miarbol.size, "-", miarbol.treesize())
print ("balanceado total:", miarbol.isallBalanced())

print (miarbol)
