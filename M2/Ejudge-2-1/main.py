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

    def _rotate_left(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def _rotate_right(self, x):
        y = x.left
        x.left = y.right
        y.right = x
        return y

    def _splay(self, root, key):
        if root is None or root.key == key:
            return root

        if root.key > key:
            if root.left is None:
                return root
            if root.left.key > key:
                root.left.left = self._splay(root.left.left, key)
                root = self._rotate_right(root)
            elif root.left.key < key:
                root.left.right = self._splay(root.left.right, key)
                if root.left.right:
                    root.left = self._rotate_left(root.left)
            return root if root.left is None else self._rotate_right(root)
        else:
            if root.right is None:
                return root
            if root.right.key > key:
                root.right.left = self._splay(root.right.left, key)
                if root.right.left:
                    root.right = self._rotate_right(root.right)
            elif root.right.key < key:
                root.right.right = self._splay(root.right.right, key)
                root = self._rotate_left(root)
            return root if root.right is None else self._rotate_left(root)

    def add(self, key, value):
        if self.root is None:
            self.root = Node(key, value)
        else:
            self.root = self._splay(self.root, key)
            if self.root.key == key:
                self.root.value = value
            elif self.root.key > key:
                new_node = Node(key, value)
                new_node.left = self.root.left
                new_node.right = self.root
                self.root.left = None
                self.root = new_node
            else:
                new_node = Node(key, value)
                new_node.right = self.root.right
                new_node.left = self.root
                self.root.right = None
                self.root = new_node

    def set(self, key, value):
        self.root = self._splay(self.root, key)
        if self.root and self.root.key == key:
            self.root.value = value
        else:
            print("error")

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
                self.root = self._splay(left_subtree, key)
                self.root.right = right_subtree
        else:
            print("error")

    def search(self, key):
        self.root = self._splay(self.root, key)
        if self.root and self.root.key == key:
            print(f"1 {self.root.value}")
        else:
            print("0")

    def min(self):
        if self.root:
            min_node = self._min(self.root)
            print(f"{min_node.key} {min_node.value}")
        else:
            print("error")

    def max(self):
        if self.root:
            max_node = self._max(self.root)
            print(f"{max_node.key} {max_node.value}")
        else:
            print("error")

    def _min(self, root):
        while root.left:
            root = root.left
        return root

    def _max(self, root):
        while root.right:
            root = root.right
        return root

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

    def print_tree(self):
        if self.root:
            lines = []
            self._print_tree(self.root, 0, '_', lines)
            for line in lines[:-1] if lines[-1] == ["_", "_"] else lines:
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
