import sys


class KnapsackProblem:
    def __init__(self, approximation, max_weight):
        self.approximation = approximation
        self.max_weight = max_weight
        self.items = []
        self.total_weight = 0
        self.total_value = 0
        self.selected_items = []

    def add_item(self, weight, value):
        self.items.append((weight, value))

    def solve(self):
        self.items.sort(key=lambda x: x[1] / x[0], reverse=True)

        current_weight = 0
        for i, (weight, value) in enumerate(self.items):
            if current_weight + weight <= self.max_weight:
                self.selected_items.append(i + 1)
                current_weight += weight
                self.total_weight += weight
                self.total_value += value

        if self.approximation > 0:
            self._adjust_solution()

    def _adjust_solution(self):
        pass

    def get_solution(self):
        return self.total_weight, self.total_value, self.selected_items


def main():
    approximation = float(next(sys.stdin).strip())
    if not 0 <= approximation <= 1:
        raise ValueError("Approximation coefficient must be between 0 and 1")

    max_weight = int(next(sys.stdin).strip())
    if max_weight < 0:
        raise ValueError("Max weight must be a non-negative integer")

    kp = KnapsackProblem(approximation, max_weight)

    for line in sys.stdin:
        line = line.rstrip('\n')
        if line:
            weight, value = map(int, line.split())
            if weight < 0 or value < 0:
                raise ValueError("Weight and value must be non-negative integers")
            kp.add_item(weight, value)

    kp.solve()
    total_weight, total_value, selected_items = kp.get_solution()
    print(total_weight, total_value)
    for item in selected_items:
        print(item)


if __name__ == "__main__":
    main()
