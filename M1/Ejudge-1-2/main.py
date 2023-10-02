import re


class Deque:
    def __init__(self, max_size):
        if max_size >= 0:
            self.max_size = max_size
            self.deque = [None] * max_size
            self.front = 0
            self.rear = 0
            self.size = 0
        else:
            print("error")

    def pushf(self, value):
        if self.size < self.max_size:
            self.front = (self.front - 1) % self.max_size
            self.deque[self.front] = value
            self.size += 1
        else:
            print("overflow")

    def pushb(self, value):
        if self.size < self.max_size:
            self.deque[self.rear] = value
            self.rear = (self.rear + 1) % self.max_size
            self.size += 1
        else:
            print("overflow")

    def popf(self):
        if self.size > 0:
            value = self.deque[self.front]
            self.front = (self.front + 1) % self.max_size
            self.size -= 1
            return value
        else:
            return "underflow"

    def popb(self):
        if self.size > 0:
            self.rear = (self.rear - 1) % self.max_size
            value = self.deque[self.rear]
            self.size -= 1
            return value
        else:
            return "underflow"

    def print_deque(self):
        if self.size == 0:
            return "empty"
        else:
            return " ".join(str(self.deque[(self.front + i) % self.max_size]) for i in range(self.size))


max_size = 0
deque = None

while True:
    try:
        command = input().strip()
        if not command:
            continue

        if re.match(r'^set_size \d+$', command):
            _, max_size_str = command.split()
            max_size = int(max_size_str)
            deque = Deque(max_size)
            continue

        if deque is None:
            print("error")
            continue

        if re.match(r'^pushf \S+$', command):
            _, value = command.split()
            deque.pushf(value)

        elif re.match(r'^pushb \S+$', command):
            _, value = command.split()
            deque.pushb(value)

        elif command == "popf":
            result = deque.popf()
            print(result)

        elif command == "popb":
            result = deque.popb()
            print(result)

        elif command == "print":
            result = deque.print_deque()
            print(result)

        else:
            print("error")

    except EOFError:
        break
