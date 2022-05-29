""" AVL Tree implemented on top of the standard BST. """

__author__ = 'Alexey Ignatiev'
__docformat__ = 'reStructuredText'

from bst import BinarySearchTree
from typing import TypeVar, Generic
from node import AVLTreeNode

K = TypeVar('K')
I = TypeVar('I')


class AVLTree(BinarySearchTree, Generic[K, I]):
    """ Self-balancing binary search tree using rebalancing by sub-tree
        rotations of Adelson-Velsky and Landis (AVL).
    """

    def __init__(self) -> None:
        """
            Initialises an empty Binary Search Tree
            :complexity: O(1)
        """
        BinarySearchTree.__init__(self)

    def __setitem__(self, key: K, item: I) -> None:
        self.root = self.insert_aux(self.root, key, item)
        #self.print_tree()

    def insert_aux(self, current: AVLTreeNode, key: K, item: I) -> AVLTreeNode:
        """
            Attempts to insert an item into the tree, it uses the Key to insert
            it. After insertion, performs sub-tree rotation whenever it becomes
            unbalanced.
            returns the new root of the subtree.
        """
        if current is None:  # base case: at the leaf
            current = AVLTreeNode(key, item)
            self.length += 1
            return current
        elif key < current.key:
            current.left = self.insert_aux(current.left, key, item)
        elif key > current.key:
            current.right = self.insert_aux(current.right, key, item)
        else:  # key == current.key. Duplication should cause error
            raise ValueError('Inserting duplicate item')

        # Finally, update heights rebalance current root after insertion completed (postorder processing)
        current.height = max(self.get_height(current.left), self.get_height(current.right)) + 1
        return self.rebalance(current)  # return new root of rebalanced tree

    def get_height(self, current: AVLTreeNode) -> int:
        """
            Get the height of a node. Return current.height if current is 
            not None. Otherwise, return 0.
            :complexity: O(1)
        """

        if current is not None:
            return current.height
        return 0

    def get_balance(self, current: AVLTreeNode) -> int:
        """
            Compute the balance factor for the current sub-tree as the value
            (right.height - left.height). If current is None, return 0.
            :complexity: O(1)
        """

        if current is None:
            return 0
        return self.get_height(current.right) - self.get_height(current.left)

    def delete_aux(self, current: AVLTreeNode, key: K) -> AVLTreeNode:
        """

            :param current: root node of tree or sub-tree to search through for deletion
            :param key: key of node to be deleted
            :pre:
            :post:
            :raises ValueError:
            :complexity:
            :returns:
        """
        if current is None:  # key not found
            raise ValueError('Deleting non-existent item')
        elif key < current.key:
            current.left = self.delete_aux(current.left, key)
        elif key > current.key:
            current.right = self.delete_aux(current.right, key)
        else:  # we found our key => do actual deletion
            if self.is_leaf(current):
                self.length -= 1
                return None
            elif current.left is None:
                self.length -= 1
                return current.right
            elif current.right is None:
                self.length -= 1
                return current.left

            # general case => find a successor
            succ = self.get_successor(current)
            current.key  = succ.key
            current.item = succ.item
            current.right = self.delete_aux(current.right, succ.key)

        current.height = max(self.get_height(current.left), self.get_height(current.right)) + 1
        return self.rebalance(current)

    def left_rotate(self, current: AVLTreeNode) -> AVLTreeNode:
        """
            Perform left rotation of the sub-tree.
            Right child of the current node, i.e. of the root of the target
            sub-tree, should become the new root of the sub-tree.
            returns the new root of the subtree.
            Example:

                 current                                       child
                /       \                                      /   \
            l-tree     child           -------->        current     r-tree
                      /     \                           /     \
                 center     r-tree                 l-tree     center

            :complexity: O(1)
        """
        child = current.right
        center = child.left
        child.left = current
        current.right = center
        current.height = 1 + max(self.get_height(current.left), self.get_height(current.right))
        child.height = 1 + max(self.get_height(child.left), self.get_height(child.right))

        return child

    def right_rotate(self, current: AVLTreeNode) -> AVLTreeNode:
        """
            Perform right rotation of the sub-tree.
            Left child of the current node, i.e. of the root of the target
            sub-tree, should become the new root of the sub-tree.
            returns the new root of the subtree.
            Example:

                       current                                child
                      /       \                              /     \
                  child       r-tree     --------->     l-tree     current
                 /     \                                           /     \
            l-tree     center                                 center     r-tree

            :complexity: O(1)
        """
        child = current.left
        center = child.right
        child.right = current
        current.left = center
        current.height = 1 + max(self.get_height(current.left), self.get_height(current.right))
        child.height = 1 + max(self.get_height(child.left), self.get_height(child.right))

        return child

    def rebalance(self, current: AVLTreeNode) -> AVLTreeNode:
        """ Compute the balance of the current node.
            Do rebalancing of the sub-tree of this node if necessary.
            Rebalancing should be done either by:
            - one left rotate
            - one right rotate
            - a combination of left + right rotate
            - a combination of right + left rotate
            returns the new root of the subtree.
        """
        if self.get_balance(current) >= 2:
            child = current.right
            if self.get_height(child.left) > self.get_height(child.right):
                current.right = self.right_rotate(child)
            return self.left_rotate(current)

        if self.get_balance(current) <= -2:
            child = current.left
            if self.get_height(child.right) > self.get_height(child.left):
                current.left = self.left_rotate(child)
            return self.right_rotate(current)

        self.root = current
        return current

    def kth_largest(self, k: int) -> AVLTreeNode:
        """
        Returns the kth largest element in the tree.
        k=1 would return the largest.
        """
        current = self.root
        largest = None

        # count variable to keep count of visited Nodes
        count = 0

        while (current != None):
            # if right child is None
            if (current.right == None):
                # first increment count and
                # check if count = k
                count += 1
                if (count == k):
                    largest = current
                # otherwise move to the left child
                current = current.left
            else:
                # find inorder successor of
                # current Node
                succ = current.right
                while (succ.left != None and
                       succ.left != current):
                    succ = succ.left

                if (succ.left == None):
                    # set left child of successor
                    # to the current Node
                    succ.left = current
                    # move current to its right
                    current = current.right

                # restoring the tree back to
                # original binary search tree
                # removing threaded links
                else:
                    succ.left = None
                    count += 1
                    if (count == k):
                        largest = current
                    # move current to its left child
                    current = current.left

        return largest


if __name__ == '__main__':
    b = AVLTree()
    b[15] = "A"
    b[10] = "B"
    b[20] = "C"
    b[17] = "D"
    b[5] = "E"
    b[3] = "F"
    b[4] = "G"
    b[22] = "H"