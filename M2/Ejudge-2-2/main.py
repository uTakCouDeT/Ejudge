import heapq


class HeapNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class BinaryMinHeap:
    def __init__(self):
        self.heap = []
        self.key_to_index = {}
        self.next_index = 0  # Для генерации уникальных индексов

    def add(self, key, value):
        if key in self.key_to_index:
            # Update the value if the key already exists
            index = self.key_to_index[key]
            self.heap[index] = HeapNode(key, value)
            self._heapify_up(index)
        else:
            # Add a new key-value pair
            node = HeapNode(key, value)
            self.heap.append(node)
            self.key_to_index[key] = self.next_index
            self._heapify_up(self.next_index)
            self.next_index += 1

    def set(self, key, value):
        if key in self.key_to_index:
            index = self.key_to_index[key]
            self.heap[index].value = value
            self._heapify_up(index)
        else:
            # If the key doesn't exist, add it
            self.add(key, value)

    def delete(self, key):
        if key in self.key_to_index:
            index = self.key_to_index[key]
            last_node = self.heap.pop()
            if index < len(self.heap):
                self.heap[index] = last_node
                self.key_to_index[last_node.key] = index
                self._heapify_up(index)
                self._heapify_down(index)
            del self.key_to_index[key]

    def search(self, key):
        if key in self.key_to_index:
            index = self.key_to_index[key]
            value = self.heap[index].value
            return f"1 {index} {value}"
        return "0"

    def min(self):
        if self.heap:
            min_node = self.heap[0]
            return f"{min_node.key} 0 {min_node.value}"
        return "error"

    def extract(self):
        if self.heap:
            min_node = self.heap[0]
            del self.key_to_index[min_node.key]
            last_node = self.heap.pop()
            if self.heap:
                self.heap[0] = last_node
                self.key_to_index[last_node.key] = 0
                self._heapify_down(0)
            return f"{min_node.key} {min_node.value}"
        return "error"

    def print_heap(self):
        if self.heap:
            levels = []
            current_level = [0]
            while current_level:
                next_level = []
                level_output = []
                for index in current_level:
                    if index < len(self.heap):
                        node = self.heap[index]
                        level_output.append(f"[{node.key} {node.value}]")
                        left_child = 2 * index + 1
                        right_child = 2 * index + 2
                        next_level.extend([left_child, right_child])
                    else:
                        level_output.append("_")
                        next_level.extend([None, None])
                levels.append(" ".join(level_output))
                current_level = [i for i in next_level if i is not None]
            for level in levels:
                print(level)
        else:
            print("_")

    def _heapify_up(self, index):
        while index > 0:
            parent_index = (index - 1) // 2
            if self.heap[parent_index].key > self.heap[index].key:
                self.heap[parent_index], self.heap[index] = self.heap[index], self.heap[parent_index]
                self.key_to_index[self.heap[parent_index].key] = parent_index
                self.key_to_index[self.heap[index].key] = index
                index = parent_index
            else:
                break

    def _heapify_down(self, index):
        while True:
            left_child_index = 2 * index + 1
            right_child_index = 2 * index + 2
            smallest = index

            if left_child_index < len(self.heap) and self.heap[left_child_index].key < self.heap[smallest].key:
                smallest = left_child_index

            if right_child_index < len(self.heap) and self.heap[right_child_index].key < self.heap[smallest].key:
                smallest = right_child_index

            if smallest != index:
                self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
                self.key_to_index[self.heap[index].key] = index
                self.key_to_index[self.heap[smallest].key] = smallest
                index = smallest
            else:
                break


def parse_command(command, heap):
    parts = command.split()
    if parts[0] == 'add':
        key, value = int(parts[1]), parts[2]
        heap.add(key, value)
    elif parts[0] == 'set':
        key, value = int(parts[1]), parts[2]
        heap.set(key, value)
    elif parts[0] == 'delete':
        key = int(parts[1])
        heap.delete(key)
    elif parts[0] == 'search':
        key = int(parts[1])
        result = heap.search(key)
        print(result)
    elif parts[0] == 'min':
        result = heap.min()
        print(result)
    elif parts[0] == 'max':
        result = heap.max()
        print(result)
    elif parts[0] == 'extract':
        result = heap.extract()
        print(result)
    elif parts[0] == 'print':
        heap.print_heap()


if __name__ == "__main__":
    heap = BinaryMinHeap()
    while True:
        try:
            command = input()
            if not command:
                continue
            parse_command(command, heap)
        except EOFError:
            break
