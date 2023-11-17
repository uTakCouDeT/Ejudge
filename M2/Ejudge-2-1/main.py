# Сделал вывод "error" в методах дерева через исключения
# Вместо принтов в методах search, min, max теперь возвращается нода
# Ну и вывод дерева в пользовательский поток

import re
import sys
from collections import deque


# from memory_profiler import profile

class SplayTreeError(Exception):
    pass


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

    def __rotate_left(self, x):
        y = x.right
        x.right = y.left
        if y.left:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.__root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def __rotate_right(self, x):
        y = x.left
        x.left = y.right
        if y.right:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.__root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def __splay(self, node):
        while node.parent:
            # Zig
            if node.parent.parent is None:
                if node == node.parent.left:
                    self.__rotate_right(node.parent)
                else:
                    self.__rotate_left(node.parent)
            # Zig-Zig
            elif node == node.parent.left and node.parent == node.parent.parent.left:
                self.__rotate_right(node.parent.parent)
                self.__rotate_right(node.parent)
            elif node == node.parent.right and node.parent == node.parent.parent.right:
                self.__rotate_left(node.parent.parent)
                self.__rotate_left(node.parent)
            # Zig-Zag
            elif node == node.parent.right and node.parent == node.parent.parent.left:
                self.__rotate_left(node.parent)
                self.__rotate_right(node.parent)
            elif node == node.parent.left and node.parent == node.parent.parent.right:
                self.__rotate_right(node.parent)
                self.__rotate_left(node.parent)
        self.__root = node

    def add(self, key, value):
        if not self.__root:
            self.__root = Node(key, value)
            return
        node = self.__root
        while True:
            if key < node.key:
                if node.left:
                    node = node.left
                else:
                    node.left = Node(key, value, parent=node)
                    self.__splay(node.left)
                    break
            elif key > node.key:
                if node.right:
                    node = node.right
                else:
                    node.right = Node(key, value, parent=node)
                    self.__splay(node.right)
                    break
            else:
                self.__splay(node)
                raise SplayTreeError("error")

    def delete(self, key):
        node_to_delete = self.__search(key)
        if not node_to_delete:
            raise SplayTreeError("error")

        if node_to_delete.left:
            left_subtree = node_to_delete.left
            left_subtree.parent = None

            if node_to_delete.right:
                right_subtree = node_to_delete.right

                max_node = self.__max(left_subtree)

                max_node.right = right_subtree
                right_subtree.parent = max_node

                self.__root = max_node
            else:
                self.__root = left_subtree
        else:
            self.__root = node_to_delete.right
            if self.__root:
                self.__root.parent = None

    def __search(self, key):
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

    def search(self, key):
        node = self.__search(key)
        if node:
            return self.__root  # Хотел возвращать только значение, но исходя из требуемого функционала для min/max
        else:                   # Скорее всего предполагается что тут тоже нужно возвращать ноду
            return None

    def set(self, key, value):
        node = self.__search(key)
        if node:
            self.__root.value = value
        else:
            raise SplayTreeError("error")

    def __min(self, node):
        while node.left is not None:
            node = node.left
        self.__splay(node)
        return node

    def __max(self, node):
        while node.right is not None:
            node = node.right
        self.__splay(node)
        return node

    def min(self):
        if self.__root:
            min_node = self.__min(self.__root)
            return min_node
        raise SplayTreeError("error")

    def max(self):
        if self.__root:
            max_node = self.__max(self.__root)
            return max_node
        raise SplayTreeError("error")

    # @profile
    def print_tree(self, output_stream=sys.stdout):
        if not self.__root:
            print("_", file=output_stream)
            return

        print(f"[{self.__root.key} {self.__root.value}]", file=output_stream)

        level_length = 2
        count = 0
        join_buffer_count = 0
        queue = deque()
        queue.appendleft(self.__root.left)
        queue.appendleft(self.__root.right)
        line = []

        while True:
            node = queue.pop()
            join_buffer_count += 1
            count += 1
            if node:
                line.append(f"[{node.key} {node.value} {node.parent.key}]")
                queue.appendleft(node.left)
                queue.appendleft(node.right)
            else:
                line.append("_")
                queue.appendleft(None)
                queue.appendleft(None)

            if join_buffer_count == 1000:
                print(" ".join(line), end=" ", file=output_stream)
                join_buffer_count = 0
                line = []

            if count == level_length:
                print(" ".join(line), file=output_stream)
                join_buffer_count = 0
                line = []
                level_length *= 2
                count = 0
                if not any(queue):
                    break


def main():
    output_stream = sys.stdout
    splay_tree = SplayTree()
    command_patterns = [
        re.compile(r'^add ([-+]?\d+) (\S*)$'),
        re.compile(r'^set ([-+]?\d+) (\S*)$'),
        re.compile(r'^delete ([-+]?\d+)$'),
        re.compile(r'^search ([-+]?\d+)$'),
        re.compile(r'^min$'),
        re.compile(r'^max$'),
        re.compile(r'^print$'),
    ]

    # try:
    for line in sys.stdin:
        if not line or line == "\n":
            continue
        try:
            for pattern in command_patterns:
                match = pattern.match(line)
                if match:
                    if line.startswith("add"):
                        splay_tree.add(int(match.group(1)), str(match.group(2)))
                    elif line.startswith("set"):
                        splay_tree.set(int(match.group(1)), str(match.group(2)))
                    elif line.startswith("delete"):
                        splay_tree.delete(int(match.group(1)))
                    elif line.startswith("search"):
                        node = splay_tree.search(int(match.group(1)))
                        if node:
                            print(f"1 {node.value}", file=output_stream)
                        else:
                            print("0", file=output_stream)
                    elif line.startswith("min"):
                        node = splay_tree.min()
                        print(node.key, node.value, file=output_stream)
                    elif line.startswith("max"):
                        node = splay_tree.max()
                        print(node.key, node.value, file=output_stream)
                    elif line.startswith("print"):
                        splay_tree.print_tree(output_stream=output_stream)
                    break
            else:
                print("error", file=output_stream)  # Проверка корректности ввода это логика независимая от SplayTree
        except SplayTreeError as ex:
            print(ex, file=output_stream)
    # except KeyboardInterrupt:
    #     return 0


if __name__ == "__main__":
    main()
