import re
import sys


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


class SplayTree:
    def __init__(self):
        self.root = None

    # Вспомогательная функция для левого поворота узла x.
    def _rotate_left(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        return y

    # Вспомогательная функция для правого поворота узла x.
    def _rotate_right(self, x):
        y = x.left
        x.left = y.right
        y.right = x
        return y

    # Основная функция, реализующая операцию splay.
    def _splay(self, root, key):
        if root is None or root.key == key:
            return root

        if root.key > key:
            if root.left is None:
                return root
            if root.left.key > key:
                # Zig-Zig или Zig
                root.left.left = self._splay(root.left.left, key)
                root = self._rotate_right(root)
            elif root.left.key < key:
                # Zig-Zag
                root.left.right = self._splay(root.left.right, key)
                if root.left.right:
                    root.left = self._rotate_left(root.left)
            return root if root.left is None else self._rotate_right(root)
        else:
            if root.right is None:
                return root
            if root.right.key > key:
                # Zig-Zag
                root.right.left = self._splay(root.right.left, key)
                if root.right.left:
                    root.right = self._rotate_right(root.right)
            elif root.right.key < key:
                # Zig-Zig или Zig
                root.right.right = self._splay(root.right.right, key)
                root = self._rotate_left(root)
            return root if root.right is None else self._rotate_left(root)

    # Метод для добавления узла с ключом key и значением value.
    def add(self, key, value):
        new_node = Node(key, value)
        if self.root is None:
            self.root = new_node
        else:
            self.root = self._insert(self.root, new_node)
        self.root = self._splay(self.root, key)

    # Метод для добавления узла в обыкновенное ДДП.
    def _insert(self, root, new_node):
        if root is None:
            return new_node

        if new_node.key < root.key:
            root.left = self._insert(root.left, new_node)
        elif new_node.key > root.key:
            root.right = self._insert(root.right, new_node)

        return root

    # Метод для обновления значения узла с ключом key на новое значение value.
    def set(self, key, value):
        self.root = self._splay(self.root, key)
        if self.root and self.root.key == key:
            self.root.value = value
        else:
            print("error")

    # Метод для удаления узла с ключом key.
    def delete(self, key):
        self.root = self._splay(self.root, key)
        if self.root and self.root.key == key:
            if self.root.left is None:
                self.root = self.root.right
            elif self.root.right is None:
                self.root = self.root.left
            else:
                left_subtree = self.root.left
                right_subtree = self.root.right
                self.root = self._splay(left_subtree, left_subtree._max.key)
                self.root.right = right_subtree
        else:
            print("error")

    # Метод для поиска узла с ключом key.
    def search(self, key):
        self.root = self._splay(self.root, key)
        if self.root and self.root.key == key:
            print(f"1 {self.root.value}")
        else:
            print("0")

    # Метод для поиска минимального узла в дереве.
    def min(self):
        if self.root:
            min_node = self._min(self.root)
            print(f"{min_node.key} {min_node.value}")
        else:
            print("error")

    # Метод для поиска максимального узла в дереве.
    def max(self):
        if self.root:
            max_node = self._max(self.root)
            print(f"{max_node.key} {max_node.value}")
        else:
            print("error")

    # Вспомогательная функция для поиска минимального узла в поддереве.
    def _min(self, root):
        while root.left:
            root = root.left
        return root

    # Вспомогательная функция для поиска максимального узла в поддереве.
    def _max(self, root):
        while root.right:
            root = root.right
        return root

    # Вспомогательная функция для печати дерева.
    def _print_tree(self, root, level, parent_key, lines):
        if level == len(lines):
            lines.append([])
        if root:
            if root == self.root:
                lines[level].append(f"[{root.key} {root.value}]")
            else:
                lines[level].append(f"[{root.key} {root.value} {parent_key}]")
            self._print_tree(root.left, level + 1, root.key, lines)
            self._print_tree(root.right, level + 1, root.key, lines)
        else:
            lines[level].append("_")

    # Метод для печати дерева.
    def print_tree(self):
        if self.root:
            lines = []
            self._print_tree(self.root, 0, '_', lines)
            for line in lines[:-1] if all(i == "_" for i in lines[-1]) else lines:
                print(" ".join(line))
        else:
            print("_")


def main():
    splay_tree = SplayTree()
    command_patterns = [
        re.compile(r'^add (\d+) (\S+)$'),
        re.compile(r'^set (\d+) (\S+)$'),
        re.compile(r'^delete (\d+)$'),
        re.compile(r'^search (\d+)$'),
        re.compile(r'^min$'),
        re.compile(r'^max$'),
        re.compile(r'^print$'),
    ]

    for line in sys.stdin:
        command = line.strip()
        if not command:
            continue

        for pattern in command_patterns:
            match = pattern.match(command)
            if match:
                if command.startswith("add"):
                    splay_tree.add(int(match.group(1)), match.group(2))
                elif command.startswith("set"):
                    splay_tree.set(int(match.group(1)), match.group(2))
                elif command.startswith("delete"):
                    splay_tree.delete(int(match.group(1)))
                elif command.startswith("search"):
                    splay_tree.search(int(match.group(1)))
                elif command.startswith("min"):
                    splay_tree.min()
                elif command.startswith("max"):
                    splay_tree.max()
                elif command.startswith("print"):
                    splay_tree.print_tree()
                break
        else:
            print("error")


if __name__ == "__main__":
    main()
