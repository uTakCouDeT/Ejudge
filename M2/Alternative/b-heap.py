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

    def __format_node(self, node, parent_index=None):
        if parent_index is None:
            return f'[{node.key} {node.value}]'
        return f'[{node.key} {node.value} {self.__nodes_list[parent_index].key}]'

    def __get_layer_nodes(self, start, end, layer_size):
        nodes = []
        for i in range(start, min(end, len(self.__nodes_list))):
            parent_index = (i - 1) // 2 if i != 0 else None
            nodes.append(self.__format_node(self.__nodes_list[i], parent_index))
        nodes.extend(['_'] * (layer_size - len(nodes)))
        return nodes

    def print_heap(self, output_stream=sys.stdout):
        if not self.__nodes_list:
            print("_", file=output_stream)
            return

        layer, index = 1, 0
        while index < len(self.__nodes_list):
            layer_end = index + layer
            print(' '.join(self.__get_layer_nodes(index, layer_end, layer)), file=output_stream)
            index = layer_end
            layer *= 2


def main():
    min_heap = MinHeap()

    for line in sys.stdin:
        line = line.rstrip("\n")
        if line:
            try:
                if re.match(r'^add (-?\d+) (\S*)$', line):
                    key, value = re.match(r'^add (-?\d+) (\S*)$', line).groups()
                    min_heap.add(int(key), value)

                elif re.match(r'^set (-?\d+) (\S*)$', line):
                    key, value = re.match(r'^set (-?\d+) (\S*)$', line).groups()
                    min_heap.set(int(key), value)

                elif re.match(r'^delete (-?\d+)$', line):
                    key = re.match(r'^delete (-?\d+)$', line).group(1)
                    min_heap.delete(int(key))

                elif re.match(r'^search (-?\d+)$', line):
                    key = re.match(r'^search (-?\d+)$', line).group(1)
                    node = min_heap.search(int(key))
                    if node:
                        index = min_heap.get_index(node.key)
                        print(f"1 {index} {node.value}")
                    else:
                        print("0")

                elif re.match(r'^min$', line):
                    min_node = min_heap.min()
                    print(f"{min_node.key} 0 {min_node.value}")

                elif re.match(r'^max$', line):
                    max_node = min_heap.max()
                    index = min_heap.get_index(max_node.key)
                    print(f"{max_node.key} {index} {max_node.value}")

                elif re.match(r'^extract$', line):
                    node = min_heap.extract()
                    print(f"{node.key} {node.value}")

                elif re.match(r'^print$', line):
                    min_heap.print_heap()

                else:
                    print("error")

            except ValueError:
                print("error")
            except KeyError:
                print("error")


if __name__ == "__main__":
    main()
