import re
import sys
from collections import deque


class Node:
    def __init__(self, key, value, parent=None):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = parent


class SplayTree:
    def __init__(self):
        self.__root = None

    def __rotate(self, x, left):
        y = x.right if left else x.left
        if y:
            setattr(x, 'right' if left else 'left', getattr(y, 'left' if left else 'right'))
            if getattr(y, 'left' if left else 'right'):
                setattr(getattr(y, 'left' if left else 'right'), 'parent', x)

        y.parent = x.parent
        if not x.parent:
            self.__root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        setattr(y, 'left' if left else 'right', x)
        x.parent = y

    def __splay(self, node):
        while node.parent:
            is_left_child = node == node.parent.left
            is_parent_left_child = node.parent == node.parent.parent.left if node.parent.parent else False

            if node.parent.parent is None:
                # Zig
                self.__rotate(node.parent, left=is_left_child)
            elif is_left_child == is_parent_left_child:
                # Zig-Zig
                self.__rotate(node.parent.parent, left=is_left_child)
                self.__rotate(node.parent, left=is_left_child)
            else:
                # Zig-Zag
                self.__rotate(node.parent, left=is_left_child)
                self.__rotate(node.parent, left=not is_left_child)

        self.__root = node

    def add(self, key, value):
        node = self.__root
        parent = None

        while node:
            parent = node
            if key == node.key:
                self.__splay(node)
                raise ValueError("Element already exists")
            elif key < node.key:
                node = node.left
            else:
                node = node.right

        new_node = Node(key, value, parent)
        if parent is None:
            self.__root = new_node
        elif key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        self.__splay(new_node)

    def delete(self, key):
        node_to_delete = self.search(key)
        if not node_to_delete:
            raise KeyError("Element was not found")

        if node_to_delete.left:
            left_subtree = node_to_delete.left
            left_subtree.parent = None

            if node_to_delete.right:
                right_subtree = node_to_delete.right

                max_node = left_subtree
                while max_node.right is not None:
                    max_node = max_node.right
                self.__splay(max_node)

                max_node.right = right_subtree
                right_subtree.parent = max_node

                self.__root = max_node
            else:
                self.__root = left_subtree
        else:
            self.__root = node_to_delete.right
            if self.__root:
                self.__root.parent = None

    def search(self, key):
        node = self.__root
        while node:
            if key < node.key:
                if node.left is None:
                    self.__splay(node)
                    break
                node = node.left
            elif key > node.key:
                if node.right is None:
                    self.__splay(node)
                    break
                node = node.right
            else:
                self.__splay(node)
                return node
        return None

    def set(self, key, value):
        node = self.search(key)
        if node:
            self.__root.value = value
        else:
            raise KeyError("Element was not found")

    def min(self):
        if self.__root:
            node = self.__root
        else:
            raise ValueError("Tree is empty")

        while node.left is not None:
            node = node.left
        self.__splay(node)
        return node

    def max(self):
        if self.__root:
            node = self.__root
        else:
            raise ValueError("Tree is empty")

        while node.right is not None:
            node = node.right
        self.__splay(node)
        return node

    def print_tree(self, output_stream=sys.stdout):
        if not self.__root:
            print("_", file=output_stream)
            return

        print(f"[{self.__root.key} {self.__root.value}]", file=output_stream)

        level_length = 2
        count = 0
        queue = deque()
        queue.appendleft(self.__root.left)
        queue.appendleft(self.__root.right)
        line = []

        while True:
            node = queue.pop()
            count += 1
            if node:
                line.append(f"[{node.key} {node.value} {node.parent.key}]")
                queue.appendleft(node.left)
                queue.appendleft(node.right)
            else:
                line.append("_")
                queue.appendleft(None)
                queue.appendleft(None)

            if count == level_length:
                print(" ".join(line), file=output_stream)
                line = []
                level_length *= 2
                count = 0
                if not any(queue):
                    break


def main():
    splay_tree = SplayTree()

    for line in sys.stdin:
        line = line.strip()
        if line:
            try:
                if re.match(r'^add (-?\d+) (\S+)$', line):
                    key, value = re.match(r'^add (-?\d+) (\S+)$', line).groups()
                    splay_tree.add(int(key), value)

                elif re.match(r'^set (-?\d+) (\S+)$', line):
                    key, value = re.match(r'^set (-?\d+) (\S+)$', line).groups()
                    splay_tree.set(int(key), value)

                elif re.match(r'^delete (-?\d+)$', line):
                    key = re.match(r'^delete (-?\d+)$', line).group(1)
                    splay_tree.delete(int(key))

                elif re.match(r'^search (-?\d+)$', line):
                    key = re.match(r'^search (-?\d+)$', line).group(1)
                    node = splay_tree.search(int(key))
                    print(f"1 {node.value}" if node else "0")

                elif re.match(r'^min$', line):
                    node = splay_tree.min()
                    print(node.key, node.value)

                elif re.match(r'^max$', line):
                    node = splay_tree.max()
                    print(node.key, node.value)

                elif re.match(r'^print$', line):
                    splay_tree.print_tree()

                else:
                    print("error")

            except ValueError:
                print("error")
            except KeyError:
                print("error")


if __name__ == "__main__":
    main()
