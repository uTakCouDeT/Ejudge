import re
import sys


class Node:
    def __init__(self, key, value, parent=None):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = parent  # без ссылки на родителя тяжко


class SplayTree:
    def __init__(self):
        self.root = None

    def _rotate_left(self, x):
        y = x.right
        x.right = y.left
        if y.left:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:  # x был корнем
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _rotate_right(self, x):
        y = x.left
        x.left = y.right
        if y.right:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:  # x был корнем
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def _splay(self, node):
        while node.parent:
            if node.parent.parent is None:
                if node == node.parent.left:
                    self._rotate_right(node.parent)
                else:
                    self._rotate_left(node.parent)
            elif node == node.parent.left and node.parent == node.parent.parent.left:
                self._rotate_right(node.parent.parent)
                self._rotate_right(node.parent)
            elif node == node.parent.right and node.parent == node.parent.parent.right:
                self._rotate_left(node.parent.parent)
                self._rotate_left(node.parent)
            elif node == node.parent.right and node.parent == node.parent.parent.left:
                self._rotate_left(node.parent)
                self._rotate_right(node.parent)
            elif node == node.parent.left and node.parent == node.parent.parent.right:
                self._rotate_right(node.parent)
                self._rotate_left(node.parent)
        self.root = node

    def add(self, key, value):
        if not self.root:
            self.root = Node(key, value)
            return
        node = self.root
        while True:
            if key < node.key:
                if node.left:
                    node = node.left
                else:
                    node.left = Node(key, value, parent=node)
                    self._splay(node.left)
                    break
            elif key > node.key:
                if node.right:
                    node = node.right
                else:
                    node.right = Node(key, value, parent=node)
                    self._splay(node.right)
                    break
            else:
                print("error")  # Ключ уже существует
                self._splay(node)
                break

    def delete(self, key):
        node_to_delete = self._search(key)
        if not node_to_delete:
            print("error")
            return

        if node_to_delete.left:
            left_subtree = node_to_delete.left
            left_subtree.parent = None
            right_subtree = node_to_delete.right

            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right
            self._splay(max_node)

            max_node.right = right_subtree
            if right_subtree:
                right_subtree.parent = max_node

            self.root = max_node
        else:
            self.root = node_to_delete.right
            if self.root:
                self.root.parent = None

    def _search(self, key):
        node = self.root
        while node:
            if key < node.key:
                if node.left is None:
                    self._splay(node)
                    break
                node = node.left
            elif key > node.key:
                if node.right is None:
                    self._splay(node)
                    break
                node = node.right
            else:  # Ключ найден
                self._splay(node)
                return node
        return None

    def search(self, key):
        node = self._search(key)
        if node:
            print(f"1 {self.root.value}")
        else:
            print("0")

    def set(self, key, value):
        node = self._search(key)
        if node:
            self.root.value = value
        else:
            print("error")

    def _min(self, node):
        while node.left is not None:
            node = node.left
        self._splay(node)
        return node

    def _max(self, node):
        while node.right is not None:
            node = node.right
        self._splay(node)
        return node

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

    def _print_tree(self):
        lines = []
        level = 0
        current_level_nodes = [self.root]

        while any(current_level_nodes):
            lines.append([])
            next_level_nodes = []

            for node in current_level_nodes:
                if node:
                    lines[level].append(
                        f"[{node.key} {node.value}]" if node.parent is None else f"[{node.key} {node.value} {node.parent.key}]")
                    next_level_nodes.extend([node.left, node.right])
                else:
                    lines[level].append("_")
                    next_level_nodes.extend([None, None])

            current_level_nodes = next_level_nodes
            level += 1

        return lines

    def print_tree(self):
        if not self.root:
            print("_")
        else:
            lines = self._print_tree()
            for line in lines:
                print(" ".join(line))


def main():
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

    for line in sys.stdin:
        if not line or line == "\n":
            continue

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
                    splay_tree.search(int(match.group(1)))
                elif line.startswith("min"):
                    splay_tree.min()
                elif line.startswith("max"):
                    splay_tree.max()
                elif line.startswith("print"):
                    splay_tree.print_tree()
                break
        else:
            print("error")


if __name__ == "__main__":
    main()
