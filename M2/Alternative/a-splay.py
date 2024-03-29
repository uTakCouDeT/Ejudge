from collections import deque
import sys
import re


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

    def __splay(self, current_node):
        while current_node.parent:
            # Один поворот (Zig)
            if current_node.parent.parent is None:
                if current_node == current_node.parent.left:
                    self.__rotate(current_node.parent, left=False)
                else:
                    self.__rotate(current_node.parent, left=True)
            # Два поворота (Zig-Zig)
            elif current_node == current_node.parent.left and current_node.parent == current_node.parent.parent.left:
                self.__rotate(current_node.parent.parent, left=False)
                self.__rotate(current_node.parent, left=False)
            elif current_node == current_node.parent.right and current_node.parent == current_node.parent.parent.right:
                self.__rotate(current_node.parent.parent, left=True)
                self.__rotate(current_node.parent, left=True)
            # Два поворота (Zig-Zag)
            elif current_node == current_node.parent.right and current_node.parent == current_node.parent.parent.left:
                self.__rotate(current_node.parent, left=True)
                self.__rotate(current_node.parent, left=False)
            elif current_node == current_node.parent.left and current_node.parent == current_node.parent.parent.right:
                self.__rotate(current_node.parent, left=False)
                self.__rotate(current_node.parent, left=True)
        self.__root = current_node

    def add(self, key, value):
        current_node = self.__root
        parent = None

        while current_node:
            parent = current_node
            if key == current_node.key:
                self.__splay(current_node)
                raise ValueError("Element already exists")
            elif key < current_node.key:
                current_node = current_node.left
            else:
                current_node = current_node.right

        new_node = Node(key, value, parent)
        if parent is None:
            self.__root = new_node
        elif key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        self.__splay(new_node)

    def search(self, key):
        current_node = self.__root
        while current_node:
            if key > current_node.key:
                if not current_node.right:
                    self.__splay(current_node)
                    break
                current_node = current_node.right
            elif key < current_node.key:
                if not current_node.left:
                    self.__splay(current_node)
                    break
                current_node = current_node.left
            else:
                self.__splay(current_node)
                return current_node
        return None

    def delete(self, key):
        deletion_node = self.search(key)
        if deletion_node is None:
            raise KeyError("No such element")

        if deletion_node.left:
            left_tree = deletion_node.left
            left_tree.parent = None

            if deletion_node.right:
                right_tree = deletion_node.right

                max_node_left = left_tree
                while max_node_left.right:
                    max_node_left = max_node_left.right
                self.__splay(max_node_left)

                max_node_left.right = right_tree
                right_tree.parent = max_node_left

                self.__root = max_node_left
            else:
                self.__root = left_tree
        else:
            self.__root = deletion_node.right
            if self.__root:
                self.__root.parent = None

    def set(self, key, value):
        found_node = self.search(key)
        if found_node:
            found_node.value = value
        else:
            raise KeyError("No such element")

    def max(self):
        if not self.__root:
            raise ValueError("Tree is empty")

        current_node = self.__root
        while current_node.right is not None:
            current_node = current_node.right
        self.__splay(current_node)
        return current_node

    def min(self):
        if not self.__root:
            raise ValueError("Tree is empty")

        current_node = self.__root
        while current_node.left is not None:
            current_node = current_node.left
        self.__splay(current_node)
        return current_node

    def print_tree(self, stream=sys.stdout):
        current_node = self.__root
        if not current_node:
            print('_', file=stream)
            return
        print(f'[{current_node.key} {current_node.value}]', file=stream)

        current_level_nodes = {}
        if current_node.left:
            current_level_nodes[0] = current_node.left
        if current_node.right:
            current_level_nodes[1] = current_node.right

        next_level_nodes = {}
        level_width = 2

        while current_level_nodes:
            previous_index = -1
            for current_index, current_node in current_level_nodes.items():
                if current_index == 0:
                    print(f'[{current_node.key} {current_node.value} {current_node.parent.key}]', end='', file=stream)
                else:
                    if previous_index == -1:
                        print((current_index - 1) * '_ ', end='_', file=stream)
                    else:
                        print((current_index - previous_index - 1) * ' _', end='', file=stream)
                    print(f' [{current_node.key} {current_node.value} {current_node.parent.key}]', end='', file=stream)
                if current_node.left:
                    next_level_nodes[2 * current_index] = current_node.left
                if current_node.right:
                    next_level_nodes[2 * current_index + 1] = current_node.right
                previous_index = current_index

            if previous_index < level_width - 1:
                print((level_width - previous_index - 1) * ' _', end='', file=stream)
            print(file=stream)

            current_level_nodes = next_level_nodes
            next_level_nodes = {}
            level_width *= 2


def main():
    splay_tree = SplayTree()

    for line in sys.stdin:
        line = line.rstrip("\n")
        if line:
            try:
                if re.match(r'^add (-?\d+) (\S*)$', line):
                    key, value = re.match(r'^add (-?\d+) (\S*)$', line).groups()
                    splay_tree.add(int(key), value)

                elif re.match(r'^set (-?\d+) (\S*)$', line):
                    key, value = re.match(r'^set (-?\d+) (\S*)$', line).groups()
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
