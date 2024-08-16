from bst import build_tree2, search, build_tree, Node, height
from random import randint
from time import time
from red_black import RBTree


test_data1 = [randint(0, 999) for _ in range(10 ** 6)]

tree1 = build_tree2(test_data1)
# tree2 = build_tree2(sorted(test_data1))
tree3 = build_tree(sorted(test_data1))

rbtree = RBTree()
for value in test_data1:
    rbtree.rb_insert(value)
    
rbtree2 = RBTree()
for value in sorted(test_data1):
    rbtree2.rb_insert(value)


def search_time(tree: Node, value: int, case: str) -> None:
    times = []
    for _ in range(10):
        start = time()
        search(tree, value)
        end = time()
        times.append(end-start)
    average = sum(times)/len(times)
    levels = height(tree)
    print(f"{case} time: {average} seconds ({levels} levels)")
    

search_time(tree1, 1000, "Random data, build_tree2")
# search_time(tree2, 1000, "Sorted data, build_tree2")
search_time(tree3, 1000, "Sorted data, build_tree")
search_time(rbtree.root, 1000, "Random data, rb_tree")
search_time(rbtree2.root, 1000, "Sorted data, rb_tree")