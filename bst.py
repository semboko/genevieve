from typing import List, Optional
from random import randint

class Node:
    def __init__(self, value) -> None:
        self.value = value
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None
        self.parent: Optional[Node] = None
        
    def __str__(self):
        return f"""Node: {self.value}
            Left: {self.left}
            Right: {self.right}
        """


def build_tree(
    numbers: List[int], 
    parent: Optional[Node] = None,
) -> Optional[Node]:
    if not numbers:
        return None
    mid = len(numbers) // 2
    root = Node(numbers[mid])
    root.parent = parent
    root.left = build_tree(numbers[:mid], root)
    root.right = build_tree(numbers[mid+1:], root)
    return root
    

test_data1 = [0, 25, 50, 75, 100]
test_tree1 = build_tree(test_data1)

def search(tree: Node, value: int) -> Optional[Node]:
    if tree is None:
        return None
    if tree.value == value:
        return tree
    if value > tree.value:
        return search(tree.right, value)
    if value < tree.value:
        return search(tree.left, value)
    
test_data2 = sorted([randint(0, 99) for _ in range(10 ** 5)])
test_tree2 = build_tree(test_data2)
node = search(test_tree2, 50)


def add_node(tree: Node, value: int) -> None:
    if tree.value > value:
        if tree.left is None:
            tree.left = Node(value)
            tree.left.parent = tree
            return
        add_node(tree.left, value)
        return
    
    if tree.value < value:
        if tree.right is None:
            tree.right = Node(value)
            tree.right.parent = tree
            return
        add_node(tree.right, value)
        
root = Node(50)
add_node(root, 100)
add_node(root, 25)
add_node(root, 0)


def build_tree2(numbers: List[int]) -> Node:
    root = Node(numbers[0])
    for n in numbers:
        add_node(root, n)
    return root

test_data3 = [randint(0, 9) for i in range(10)]
root3 = build_tree2(test_data3)


def transplant(root: Node, u: Node, v: Node) -> None:
    if u.parent.left == u:
        u.parent.left = v
    if u.parent.right == u:
        u.parent.right = v
    if v is not None:
        v.parent = u.parent


def tree_minimum(root: Node):
    result = root
    while result.left is not None:
        result = result.left
    return result
        

def tree_delete(root: Node,  value: int) -> None:
    z = search(root, value)
    if z is None:
        return
    if z.left is None:
        transplant(root, z, z.right)
    elif z.right is None:
        transplant(root, z, z.left)
    else:
        y = tree_minimum(z.right)
        if y.parent is not z:
            transplant(root, y, y.right)
            y.right = z.right
            y.right.p = y
        transplant(root, z, y)
        y.left = z.left
        y.left.parent = y
        

test_data4 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
root4 = build_tree(test_data4)
tree_delete(root4, 4)
print(root4)


def height(root: Optional[Node]) -> int:
    if root is None:
        return 0
    queue = [(root, 1)]
    lowest = 1
    while queue:
        current_node, current_level = queue.pop()
        if current_level > lowest:
            lowest = current_level
        if current_node.left is not None:
            queue.append((current_node.left, current_level + 1))
        if current_node.right is not None:
            queue.append((current_node.right, current_level + 1))
    return lowest
    
root = Node(10)
root.right = Node(12)
root.left = Node(5)
root.left.left = Node(1)
assert height(root) == 3