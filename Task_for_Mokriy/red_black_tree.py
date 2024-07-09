from associative_container import AssociativeContainer


# red_black_tree.py

class RedBlackTreeNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.color = "RED"
        self.left = None
        self.right = None
        self.parent = None


class RedBlackTree(AssociativeContainer):
    def __init__(self):
        super().__init__()
        self.NIL_LEAF = RedBlackTreeNode(None, None)
        self.root = self.NIL_LEAF

    def add(self, key, value):
        new_node = RedBlackTreeNode(key, value)
        self._insert_node(new_node)

    def _insert_node(self, new_node):
        current = self.root
        parent = None

        while current != self.NIL_LEAF:
            parent = current
            if new_node.key < current.key:
                current = current.left
            else:
                current = current.right

        new_node.parent = parent
        if parent is None:
            self.root = new_node
        elif new_node.key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        new_node.left = self.NIL_LEAF
        new_node.right = self.NIL_LEAF
        new_node.color = "RED"

        self._fix_insert(new_node)

    def get(self, key):
        return self._get(self.root, key)

    def _get(self, node, key):
        while node != self.NIL_LEAF and key != node.key:
            if key < node.key:
                node = node.left
            else:
                node = node.right
        if node == self.NIL_LEAF:
            return None
        return node.value

    def update(self, key, value):
        node = self._get_node(key)
        if node:
            node.value = value
        else:
            raise KeyError(f"Key '{key}' not found.")

    def delete(self, key):
        node = self._get_node(key)
        if node:
            self._delete_node(node)
        else:
            raise KeyError(f"Key '{key}' not found.")

    def _get_node(self, key):
        current = self.root
        while current != self.NIL_LEAF and key != current.key:
            if key < current.key:
                current = current.left
            else:
                current = current.right
        if current == self.NIL_LEAF:
            return None
        return current

    def _delete_node(self, node):
        y = node
        y_original_color = y.color
        if node.left == self.NIL_LEAF:
            x = node.right
            self._transplant(node, node.right)
        elif node.right == self.NIL_LEAF:
            x = node.left
            self._transplant(node, node.left)
        else:
            y = self._find_min(node.right)
            y_original_color = y.color
            x = y.right
            if y.parent == node:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = node.right
                y.right.parent = y
            self._transplant(node, y)
            y.left = node.left
            y.left.parent = y
            y.color = node.color
        if y_original_color == "BLACK":
            self._fix_delete(x)

    def _fix_delete(self, x):
        while x != self.root and x.color == "BLACK":
            if x == x.parent.left:
                sibling = x.parent.right
                if sibling.color == "RED":
                    sibling.color = "BLACK"
                    x.parent.color = "RED"
                    self._rotate_left(x.parent)
                    sibling = x.parent.right
                if sibling.left.color == "BLACK" and sibling.right.color == "BLACK":
                    sibling.color = "RED"
                    x = x.parent
                else:
                    if sibling.right.color == "BLACK":
                        sibling.left.color = "BLACK"
                        sibling.color = "RED"
                        self._rotate_right(sibling)
                        sibling = x.parent.right
                    sibling.color = x.parent.color
                    x.parent.color = "BLACK"
                    sibling.right.color = "BLACK"
                    self._rotate_left(x.parent)
                    x = self.root
            else:
                sibling = x.parent.left
                if sibling.color == "RED":
                    sibling.color = "BLACK"
                    x.parent.color = "RED"
                    self._rotate_right(x.parent)
                    sibling = x.parent.left
                if sibling.right.color == "BLACK" and sibling.left.color == "BLACK":
                    sibling.color = "RED"
                    x = x.parent
                else:
                    if sibling.left.color == "BLACK":
                        sibling.right.color = "BLACK"
                        sibling.color = "RED"
                        self._rotate_left(sibling)
                        sibling = x.parent.left
                    sibling.color = x.parent.color
                    x.parent.color = "BLACK"
                    sibling.left.color = "BLACK"
                    self._rotate_right(x.parent)
                    x = self.root
        x.color = "BLACK"

    def _transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _rotate_left(self, z):
        y = z.right
        z.right = y.left
        if y.left != self.NIL_LEAF:
            y.left.parent = z

        y.parent = z.parent
        if z.parent is None:
            self.root = y
        elif z == z.parent.left:
            z.parent.left = y
        else:
            z.parent.right = y

        y.left = z
        z.parent = y

    def _rotate_right(self, z):
        y = z.left
        z.left = y.right
        if y.right != self.NIL_LEAF:
            y.right.parent = z

        y.parent = z.parent
        if z.parent is None:
            self.root = y
        elif z == z.parent.right:
            z.parent.right = y
        else:
            z.parent.left = y

        y.right = z
        z.parent = y

    def _find_min(self, node):
        current = node
        while current.left != self.NIL_LEAF:
            current = current.left
        return current


    def _fix_insert(self, new_node):
        while new_node.parent.color == "RED":
            if new_node.parent == new_node.parent.parent.left:
                uncle = new_node.parent.parent.right
                if uncle.color == "RED":
                    new_node.parent.color = "BLACK"
                    uncle.color = "BLACK"
                    new_node.parent.parent.color = "RED"
                    new_node = new_node.parent.parent
                else:
                    if new_node == new_node.parent.right:
                        new_node = new_node.parent
                        self._rotate_left(new_node)
                    new_node.parent.color = "BLACK"
                    new_node.parent.parent.color = "RED"
                    self._rotate_right(new_node.parent.parent)
            else:
                uncle = new_node.parent.parent.left
                if uncle.color == "RED":
                    new_node.parent.color = "BLACK"
                    uncle.color = "BLACK"
                    new_node.parent.parent.color = "RED"
                    new_node = new_node.parent.parent
                else:
                    if new_node == new_node.parent.left:
                        new_node = new_node.parent
                        self._rotate_right(new_node)
                    new_node.parent.color = "BLACK"
                    new_node.parent.parent.color = "RED"
                    self._rotate_left(new_node.parent.parent)

        self.root.color = "BLACK"


