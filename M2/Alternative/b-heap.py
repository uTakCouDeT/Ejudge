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

    def __sift_down(self, parent_index):
        while True:
            left, right = (parent_index << 1) + 1, (parent_index << 1) + 2
            smaller_child = parent_index

            if left < len(self.__nodes_list) and self.__nodes_list[left].key < self.__nodes_list[smaller_child].key:
                smaller_child = left
            if right < len(self.__nodes_list) and self.__nodes_list[right].key < self.__nodes_list[smaller_child].key:
                smaller_child = right

            if smaller_child == parent_index:
                break

            self.__swap_nodes(parent_index, smaller_child)
            parent_index = smaller_child

    def __sift_up(self, child_index):
        while child_index > 0:
            parent_index = (child_index - 1) >> 1
            if self.__nodes_list[child_index].key >= self.__nodes_list[parent_index].key:
                break
            self.__swap_nodes(child_index, parent_index)
            child_index = parent_index

    def __swap_nodes(self, first_index, second_index):
        first_node, second_node = self.__nodes_list[first_index], self.__nodes_list[second_index]
        self.__nodes_list[first_index], self.__nodes_list[second_index] = second_node, first_node
        self.__index_dict[first_node.key], self.__index_dict[second_node.key] = second_index, first_index

    def add(self, key, value):
        if key not in self.__index_dict:
            self.__nodes_list.append(Node(key, value))
            self.__index_dict[key] = len(self.__nodes_list) - 1
            self.__sift_up(self.__index_dict[key])
        else:
            raise ValueError("Element already exists")

    def delete(self, key):
        if key in self.__index_dict:
            index = self.__index_dict.pop(key)
            last_index = len(self.__nodes_list) - 1
            if index != last_index:
                self.__nodes_list[index] = self.__nodes_list.pop()
                self.__index_dict[self.__nodes_list[index].key] = index
                if index > 0 and self.__nodes_list[index].key < self.__nodes_list[(index - 1) // 2].key:
                    self.__sift_up(index)
                else:
                    self.__sift_down(index)
            else:
                self.__nodes_list.pop()
        else:
            raise KeyError("No such element")

    def set(self, key, new_value):
        node_index = self.__index_dict.get(key)
        if node_index:
            self.__sift_up(node_index)
            self.__sift_down(node_index)
            self.__nodes_list[node_index].value = new_value
        else:
            raise KeyError("No such element")

    def max(self):
        if self.__nodes_list:
            return max(self.__nodes_list[len(self.__nodes_list) // 2:], key=lambda x: x.key)
        raise ValueError("Heap is empty")

    def min(self):
        if self.__nodes_list:
            return self.__nodes_list[0]
        raise ValueError("Heap is empty")

    def extract(self):
        if self.__nodes_list:
            min_node = self.__nodes_list[0]
            self.delete(min_node.key)
            return min_node
        raise ValueError("Heap is empty")

    def get_index(self, key):
        return self.__index_dict[key] if key in self.__index_dict else None

    def search(self, key):
        index = self.get_index(key)
        return None if index is None else self.__nodes_list[index]

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
