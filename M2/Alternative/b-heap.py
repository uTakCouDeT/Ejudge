import re
import sys


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class MinHeap:
    def __init__(self):
        self.__nodes_list = []
        self.__index_dict = {}

    def __swap(self, i, j):
        self.__index_dict[self.__nodes_list[i].key], self.__index_dict[self.__nodes_list[j].key] = j, i
        self.__nodes_list[i], self.__nodes_list[j] = self.__nodes_list[j], self.__nodes_list[i]

    def __sift_up(self, index):
        parent = (index - 1) // 2
        while index > 0 and self.__nodes_list[index].key < self.__nodes_list[parent].key:
            self.__swap(index, parent)
            index = parent
            parent = (index - 1) // 2

    def __sift_down(self, index):
        n = len(self.__nodes_list)
        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            smallest = index

            if left < n and self.__nodes_list[left].key < self.__nodes_list[smallest].key:
                smallest = left
            if right < n and self.__nodes_list[right].key < self.__nodes_list[smallest].key:
                smallest = right

            if smallest != index:
                self.__swap(index, smallest)
                index = smallest
            else:
                break

    def add(self, key, value):
        if key in self.__index_dict:
            raise ValueError("Element already exists")
        node = Node(key, value)
        self.__index_dict[key] = len(self.__nodes_list)
        self.__nodes_list.append(node)
        self.__sift_up(len(self.__nodes_list) - 1)

    def set(self, key, value):
        if key not in self.__index_dict:
            raise KeyError("No such element")
        index = self.__index_dict[key]
        self.__nodes_list[index].value = value
        self.__sift_up(index)
        self.__sift_down(index)

    def delete(self, key):
        if key not in self.__index_dict:
            raise KeyError("No such element")
        index = self.__index_dict[key]
        last_node = self.__nodes_list.pop()
        if index < len(self.__nodes_list):
            self.__nodes_list[index] = last_node
            self.__index_dict[last_node.key] = index
            self.__sift_up(index)
            self.__sift_down(index)
        del self.__index_dict[key]

    def get_index(self, key):
        if key in self.__index_dict:
            return self.__index_dict[key]
        return None

    def search(self, key):
        if key in self.__index_dict:
            index = self.__index_dict[key]
            node = self.__nodes_list[index]
            return node
        return None

    def min(self):
        if not self.__nodes_list:
            raise ValueError("Heap is empty")
        return self.__nodes_list[0]

    def max(self):
        if not self.__nodes_list:
            raise ValueError("Heap is empty")
        first_leaf = len(self.__nodes_list) // 2
        return max(self.__nodes_list[first_leaf:], key=lambda x: x.key)

    def extract(self):
        if not self.__nodes_list:
            raise ValueError("Heap is empty")
        root = self.__nodes_list[0]
        self.delete(root.key)
        return root

    def print_heap(self, output_stream=sys.stdout):
        if not self.__nodes_list:
            print("_", file=output_stream)
            return

        print(f"[{self.__nodes_list[0].key} {self.__nodes_list[0].value}]", file=output_stream)

        it = iter(self.__nodes_list)
        next(it)

        level_length = 2
        count = 0
        line = []

        for vertex in it:
            count += 1

            parent_index = (self.__index_dict[vertex.key] - 1) // 2
            line.append(f"[{vertex.key} {vertex.value} {self.__nodes_list[parent_index].key}]")

            if count == level_length:
                print(" ".join(line), file=output_stream)
                line = []
                level_length *= 2
                count = 0

        if count != 0:
            print(" ".join(line), end="", file=output_stream)
            print(" _" * (level_length - count), file=output_stream)


def main():
    min_heap = MinHeap()
    command_patterns = [
        re.compile(r'^add (-?\d+) (\S*)$'),
        re.compile(r'^set (-?\d+) (\S*)$'),
        re.compile(r'^delete (-?\d+)$'),
        re.compile(r'^search (-?\d+)$'),
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
                        node = min_heap.search(int(match.group(1)))
                        if node:
                            index = min_heap.get_index(node.key)
                            print(f"1 {index} {node.value}")
                        else:
                            print("0")
                    elif line.startswith("min"):
                        min_node = min_heap.min()
                        print(f"{min_node.key} 0 {min_node.value}")
                    elif line.startswith("max"):
                        max_node = min_heap.max()
                        index = min_heap.get_index(max_node.key)
                        print(f"{max_node.key} {index} {max_node.value}")
                    elif line.startswith("extract"):
                        node = min_heap.extract()
                        print(f"{node.key} {node.value}")
                    elif line.startswith("print"):
                        min_heap.print_heap()
                    break
            else:
                print("error")
        except KeyError:
            print("error")
        except ValueError:
            print("error")


if __name__ == "__main__":
    main()
