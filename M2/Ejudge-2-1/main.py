import re
import sys
from collections import deque


# from memory_profiler import profile


class Node:
    def __init__(self, key, value, parent=None):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = parent  # Без ссылки на родителя тяжко


class SplayTree:
    def __init__(self):
        self.__root = None

    # Повороты можно объединть в один метод,
    # но это наплодит ненужные проверки и дополнительные переменные (а оно нам не надо)
    # Ну и как по мне, сплей в таком случае понятнее выглядит
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
                print("error")  # Ключ уже существует
                self.__splay(node)
                break

    def delete(self, key):
        node_to_delete = self.__search(key)  # Сплей применяется внутри поиска
        if not node_to_delete:
            print("error")
            return

        if node_to_delete.left:
            left_subtree = node_to_delete.left
            left_subtree.parent = None

            if node_to_delete.right:
                right_subtree = node_to_delete.right

                max_node = self.__max(left_subtree)  # И тут тоже

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
            print(f"1 {self.__root.value}")
        else:
            print("0")

    def set(self, key, value):
        node = self.__search(key)
        if node:
            self.__root.value = value
        else:
            print("error")

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
            print(f"{min_node.key} {min_node.value}")
        else:
            print("error")

    def max(self):
        if self.__root:
            max_node = self.__max(self.__root)
            print(f"{max_node.key} {max_node.value}")
        else:
            print("error")

    # @profile
    def print_tree(self):
        if not self.__root:
            print("_")
            return

        print(f"[{self.__root.key} {self.__root.value}]")

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

            # выводить через print("...", end=" ") каждый элемент долго
            # а через " ".join(line) весь слой дорого (хранить массив на 2^24 элементов в 12 тесте не круто)
            # по этому, чтобы, как говорится, и рыбку съесть и тесты пройти, добавим буффер
            # Вершины выводятся небольшими пакетами и после вывода удаляются из памяти
            # Работает быстро, памяти жрёт мало. Красота.
            if join_buffer_count == 1000:                  # 1000 кстати для скорости вполне достаточно
                print(" ".join(line), end=" ")        # Можно его вообще изменять динамически в зависимости от слоя
                join_buffer_count = 0                 # Но я пожалуй лучше пойду остальные задачи доделывать
                line = []

            if count == level_length:
                print(" ".join(line))
                join_buffer_count = 0
                line = []
                level_length *= 2
                count = 0
                if not any(queue):
                    break

    #                   ^
    #                   |       вторая ступень эволюции
    #                   |

    # def _print_tree(self):
    #     if not self._root:
    #         print("_")
    #         return
    #
    #     print(f"[{self._root.key} {self._root.value}]")
    #
    #     level_length = 2
    #     count = 0
    #     queue = deque()
    #     queue.appendleft(self._root.left)
    #     queue.appendleft(self._root.right)
    #     line = []
    #
    #     while True:
    #         node = queue.pop()
    #         count += 1
    #         if node:
    #             line.append(f"[{node.key} {node.value} {node.parent.key}]")
    #             queue.appendleft(node.left)
    #             queue.appendleft(node.right)
    #         else:
    #             line.append("_")
    #             queue.appendleft(None)
    #             queue.appendleft(None)
    #
    #         if count == level_length:
    #             print(" ".join(line))
    #             level_length *= 2
    #             count = 0
    #             line = []
    #             if not any(queue):
    #                 break

    #                   ^
    #                   |       первая ступень эволюции
    #                   |

    # def _print_tree(self):
    #     if not self._root:
    #         print("_")
    #         return
    #
    #     print(f"[{self._root.key} {self._root.value}]")
    #     current_level_nodes = [self._root.left, self._root.right]
    #     while any(current_level_nodes):
    #         next_level_nodes = []
    #         line = []
    #
    #         for node in current_level_nodes:
    #             if node:
    #                 line.append(f"[{node.key} {node.value} {node.parent.key}]")
    #                 next_level_nodes.append(node.left)
    #                 next_level_nodes.append(node.right)
    #             else:
    #                 line.append("_")
    #                 next_level_nodes.append(None)
    #                 next_level_nodes.append(None)
    #         print(" ".join(line))
    #
    #         current_level_nodes = next_level_nodes


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

    # try:
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
    # except KeyboardInterrupt:
    #     return 0


if __name__ == "__main__":
    main()
