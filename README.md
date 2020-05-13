# Usage-Balanced-Binary-Tree in Python
Usage Balanced Binary Tree is an implementation of binary search trees with **better performance than AVL** when the access to the nodes is not exactly proportional, that is, when some nodes are accessed more than others

This is the implementation of a **Usage Balanced Binary Tree (UBT)** class with inserts, deletes and balancing methods. The difference with an AVL is that each node of the tree has a weight that represents the number of times the node has been accessed. The balancing is made based on these wheights, keeping the most used nodes up in the tree, while the less used ones are on deeper in the tree structure. 

This is incompatible with a completly AVL-type balanced tree, but performance is much better, reaching **improvements of up to 20%** in bulk access times.

There are several .py files for unit, tree and benchmarking tests and a word document explaining the tree together with a benchmark with AVL
