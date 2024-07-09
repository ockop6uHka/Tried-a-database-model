from avl_tree import AVLTree
from red_black_tree import RedBlackTree
from btree import BTree

class ContainerFactory:
    @staticmethod
    def create_container(container_type):
        if container_type == "AVL":
            return AVLTree()
        elif container_type == "RedBlack":
            return RedBlackTree()
        elif container_type == "BTREE":
            return BTree()
        else:
            raise ValueError("Unsupported container type")
