from associative_container import AssociativeContainer



class BTreeNode:
    def __init__(self, t, leaf=False):
        self.t = t  # Минимальная степень (t)
        self.leaf = leaf
        self.keys = []
        self.values = []
        self.children = []

    def __str__(self):
        return f"Keys: {self.keys}, Values: {self.values}, Leaf: {self.leaf}"


class BTree(AssociativeContainer):
    def __init__(self, degree):
        super().__init__()
        self.root = BTreeNode(degree, True)
        self.t = degree

    def add(self, key, value):
        root = self.root
        if len(root.keys) == (2 * self.t) - 1:
            temp = BTreeNode(self.t, False)
            temp.children.insert(0, self.root)
            self.split_child(temp, 0)
            self.root = temp
        self._insert_non_full(self.root, key, value)

    def _insert_non_full(self, node, key, value):
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append(None)
            node.values.append(None)
            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                node.values[i + 1] = node.values[i]
                i -= 1
            node.keys[i + 1] = key
            node.values[i + 1] = value
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == (2 * self.t) - 1:
                self.split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], key, value)

    def split_child(self, parent, index):
        t = self.t
        y = parent.children[index]
        z = BTreeNode(t, y.leaf)
        parent.children.insert(index + 1, z)
        parent.keys.insert(index, y.keys[t - 1])
        parent.values.insert(index, y.values[t - 1])

        z.keys = y.keys[t: (2 * t) - 1]
        z.values = y.values[t: (2 * t) - 1]
        y.keys = y.keys[0: t - 1]
        y.values = y.values[0: t - 1]

        if not y.leaf:
            z.children = y.children[t: (2 * t)]
            y.children = y.children[0: t]

    def get(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        if i < len(node.keys) and key == node.keys[i]:
            return node.values[i]
        elif node.leaf:
            return None
        else:
            return self._search(node.children[i], key)

    def update(self, key, value):
        node = self.root
        while node:
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            if i < len(node.keys) and key == node.keys[i]:
                node.values[i] = value
                return True
            elif node.leaf:
                return False
            else:
                node = node.children[i]
        return False

    def delete(self, key):
        self._delete(self.root, key)
        if len(self.root.keys) == 0:
            if not self.root.leaf:
                self.root = self.root.children[0]
            else:
                self.root = BTreeNode(self.t, True)

    def _delete(self, node, key):
        t = self.t
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        if i < len(node.keys) and key == node.keys[i]:
            if node.leaf:
                del node.keys[i]
                del node.values[i]
            else:
                if len(node.children[i].keys) >= t:
                    pred_key, pred_value = self._get_predecessor(node, i)
                    node.keys[i] = pred_key
                    node.values[i] = pred_value
                    self._delete(node.children[i], pred_key)
                elif len(node.children[i + 1].keys) >= t:
                    succ_key, succ_value = self._get_successor(node, i)
                    node.keys[i] = succ_key
                    node.values[i] = succ_value
                    self._delete(node.children[i + 1], succ_key)
                else:
                    self._merge(node, i)
                    self._delete(node.children[i], key)
        elif not node.leaf:
            if len(node.children[i].keys) < t:
                if i != 0 and len(node.children[i - 1].keys) >= t:
                    self._borrow_from_prev(node, i)
                elif i != len(node.keys) and len(node.children[i + 1].keys) >= t:
                    self._borrow_from_next(node, i)
                else:
                    if i != len(node.keys):
                        self._merge(node, i)
                    else:
                        self._merge(node, i - 1)
            self._delete(node.children[i], key)

    def _get_predecessor(self, node, index):
        current = node.children[index]
        while not current.leaf:
            current = current.children[len(current.keys)]
        return current.keys[-1], current.values[-1]

    def _get_successor(self, node, index):
        current = node.children[index + 1]
        while not current.leaf:
            current = current.children[0]
        return current.keys[0], current.values[0]

    def _merge(self, node, index):
        child = node.children[index]
        sibling = node.children[index + 1]
        t = self.t
        child.keys.append(node.keys[index])
        child.values.append(node.values[index])

        child.keys.extend(sibling.keys)
        child.values.extend(sibling.values)

        if not child.leaf:
            child.children.extend(sibling.children)

        node.keys.pop(index)
        node.values.pop(index)
        node.children.pop(index + 1)

    def _borrow_from_prev(self, node, index):
        child = node.children[index]
        sibling = node.children[index - 1]

        child.keys.insert(0, node.keys[index - 1])
        child.values.insert(0, node.values[index - 1])

        if not child.leaf:
            child.children.insert(0, sibling.children.pop())

        node.keys[index - 1] = sibling.keys.pop()
        node.values[index - 1] = sibling.values.pop()

    def _borrow_from_next(self, node, index):
        child = node.children[index]
        sibling = node.children[index + 1]

        child.keys.append(node.keys[index])
        child.values.append(node.values[index])

        if not child.leaf:
            child.children.append(sibling.children.pop(0))

        node.keys[index] = sibling.keys.pop(0)
        node.values[index] = sibling.values.pop(0)
