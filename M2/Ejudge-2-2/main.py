# Сделал вывод "error" в методах кучи через исключения
# Вместо принтов в методах search, min, max, extract теперь возвращается <?>
# Ну и вывод кучи в пользовательский поток

import re
import sys


class MinHeapError(Exception):
    pass


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class MinHeap:
    def __init__(self):
        self.__heap = []
        self.__positions = {}  # хеш-таблица для хранения позиций ключей в куче

    def __swap(self, i, j):
        self.__positions[self.__heap[i].key], self.__positions[self.__heap[j].key] = j, i
        self.__heap[i], self.__heap[j] = self.__heap[j], self.__heap[i]

    def __sift_up(self, index):
        parent = (index - 1) // 2
        while index > 0 and self.__heap[index].key < self.__heap[parent].key:
            self.__swap(index, parent)
            index = parent
            parent = (index - 1) // 2

    def __sift_down(self, index):
        n = len(self.__heap)
        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            smallest = index

            if left < n and self.__heap[left].key < self.__heap[smallest].key:
                smallest = left
            if right < n and self.__heap[right].key < self.__heap[smallest].key:
                smallest = right

            if smallest != index:
                self.__swap(index, smallest)
                index = smallest
            else:
                break

    def add(self, key, value):
        if key in self.__positions:
            raise MinHeapError("Element with this key already exists")
        node = Node(key, value)
        self.__positions[key] = len(self.__heap)
        self.__heap.append(node)
        self.__sift_up(len(self.__heap) - 1)

    def set(self, key, value):
        if key not in self.__positions:
            raise MinHeapError("Element with this key was not found")
        index = self.__positions[key]
        self.__heap[index].value = value
        self.__sift_up(index)
        self.__sift_down(index)

    def delete(self, key):
        if key not in self.__positions:
            raise MinHeapError("Element with this key was not found")
        index = self.__positions[key]
        last_node = self.__heap.pop()
        if index < len(self.__heap):
            self.__heap[index] = last_node
            self.__positions[last_node.key] = index
            self.__sift_up(index)
            self.__sift_down(index)
        del self.__positions[key]

    def search(self, key):
        if key in self.__positions:
            index = self.__positions[key]
            node = self.__heap[index]
            print(f"1 {index} {node.value}")
        else:
            print("0")

    def min(self):
        if not self.__heap:
            raise MinHeapError("Heap is empty")
        min_node = self.__heap[0]
        print(f"{min_node.key} 0 {min_node.value}")

    def max(self):
        if not self.__heap:
            raise MinHeapError("Heap is empty")
        first_leaf = len(self.__heap) // 2
        max_node = max(self.__heap[first_leaf:], key=lambda x: x.key)
        index = self.__positions[max_node.key]
        print(f"{max_node.key} {index} {max_node.value}")

    def extract(self):
        if not self.__heap:
            raise MinHeapError("Heap is empty")
        root = self.__heap[0]
        self.delete(root.key)
        print(f"{root.key} {root.value}")

    def print_heap(self, output_stream=sys.stdout):
        if not self.__heap:
            print("_", file=output_stream)
            return

        print(f"[{self.__heap[0].key} {self.__heap[0].value}]", file=output_stream)

        it = iter(self.__heap)
        next(it)

        level_length = 2
        count = 0
        join_buffer_count = 0
        line = []

        for vertex in it:
            join_buffer_count += 1
            count += 1

            parent_index = (self.__positions[vertex.key] - 1) // 2
            line.append(f"[{vertex.key} {vertex.value} {self.__heap[parent_index].key}]")

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

        if count != 0:
            print(" ".join(line), end="", file=output_stream)
            print(" _" * (level_length - count), file=output_stream)


def main():
    output_stream = sys.stdout
    min_heap = MinHeap()
    command_patterns = [
        re.compile(r'^add ([-+]?\d+) (\S*)$'),
        re.compile(r'^set ([-+]?\d+) (\S*)$'),
        re.compile(r'^delete ([-+]?\d+)$'),
        re.compile(r'^search ([-+]?\d+)$'),
        re.compile(r'^min$'),
        re.compile(r'^max$'),
        re.compile(r'^extract$'),
        re.compile(r'^print$'),
    ]

    for line in sys.stdin:
        if not line or line == "\n":
            continue
        try:
            for pattern in command_patterns:
                match = pattern.match(line)
                if match:
                    if line.startswith("add"):
                        min_heap.add(int(match.group(1)), str(match.group(2)))
                    elif line.startswith("set"):
                        min_heap.set(int(match.group(1)), str(match.group(2)))
                    elif line.startswith("delete"):
                        min_heap.delete(int(match.group(1)))
                    elif line.startswith("search"):
                        min_heap.search(int(match.group(1)))
                    elif line.startswith("min"):
                        min_heap.min()
                    elif line.startswith("max"):
                        min_heap.max()
                    elif line.startswith("extract"):
                        min_heap.extract()
                    elif line.startswith("print"):
                        min_heap.print_heap(output_stream=output_stream)
                    break
            else:
                print("error", file=output_stream)
        except MinHeapError as ex:
            # print(f"Error: {ex}", file=output_stream)
            print("error", file=output_stream)  # Чтобы реализация ошибок не была заточена под вывод


if __name__ == "__main__":
    main()
