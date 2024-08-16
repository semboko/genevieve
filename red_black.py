from typing import Optional
from bst import Node, build_tree, search


class ColoredNode(Node):
    def __init__(self, value) -> None:
        super().__init__(value)
        self.color = True


class RBTree:
    def __init__(self) -> None:
        self.root: Optional[ColoredNode] = None

    def left_rotate(self, x: ColoredNode) -> None:
        y = x.right
        x.right = y.left
        if y.left is not None:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y
    
    def right_rotate(self, y: ColoredNode) -> None:
        x = y.left
        y.left = x.right
        if x.right is not None:
            x.right.parent = y
        x.parent = y.parent
        if y.parent is None:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        x.right = y
        y.parent = x


    def rb_insert_fixup(self, z: ColoredNode) -> None:
        while z.parent is not None and z.parent.color:
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y is not None and y.color:
                    z.parent.color = False
                    y.color = False
                    z.parent.parent.color = True
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self.left_rotate(z)
                    z.parent.color = False
                    z.parent.parent.color = True
                    self.right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y is not None and y.color:
                    z.parent.color = False
                    y.color = False
                    z.parent.parent.color = True
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.right_rotate(z)
                    z.parent.color = False
                    z.parent.parent.color = True
                    self.left_rotate(z.parent.parent)
                    
        self.root.color = False

    def rb_insert(self, value: int) -> None:
        z = ColoredNode(value)
        y = None
        x = self.root
        while x is not None:
            y = x
            if z.value < x.value:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if y == None:
            self.root = z
        elif z.value < y.value:
            y.left = z
        else:
            y.right = z
        self.rb_insert_fixup(z)
    
    
if __name__ == "__main__":
    tree = RBTree()

    test_values = [2, 14, 1, 7, 5, 8, 9]
    for v in test_values:
        tree.rb_insert(v)
    print(tree)