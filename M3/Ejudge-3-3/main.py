import sys


class Node:
    """ Для повышения читаемости кода """

    def __init__(self, weight, cost, scaled_cost):
        self.weight = weight
        self.cost = cost
        self.scaled_cost = scaled_cost


class Solution:
    """ Чтобы программа не была заточена под вывод """

    def __init__(self, total_weight, total_cost, selected_items):
        self.total_weight = total_weight
        self.total_cost = total_cost
        self.selected_items = selected_items


class KnapsackProblem:
    def __init__(self, approximation, max_weight):
        if not 0 <= approximation <= 1:
            raise ValueError("Approximation coefficient must be between 0 and 1")
        if max_weight < 0:
            raise ValueError("Max weight must be a non-negative integer")
        self.approximation = approximation
        self.max_weight = max_weight
        self.items = []
        self.max_cost = 0

    def add_item(self, weight, cost):
        if weight < 0 or cost < 0:
            raise ValueError("Weight and value must be non-negative integers")
        if weight <= self.max_weight:
            self.items.append(Node(weight, cost, 0))
            self.max_cost = max(self.max_cost, cost)

    def __calculate_scaled_costs(self):
        scale = self.approximation * self.max_cost / len(self.items)
        for item in self.items:
            item.scaled_cost = int(item.cost / scale)

    def __find_best_combination(self):
        self.__calculate_scaled_costs()
        dp = {0: (0, [])}
        for i, item in enumerate(self.items):
            new_dp = dp.copy()
            for total_cost, (total_weight, selected_items) in dp.items():
                new_weight = total_weight + item.weight
                new_cost = total_cost + item.scaled_cost
                if new_weight <= self.max_weight and (new_cost not in new_dp or new_dp[new_cost][0] > new_weight):
                    new_dp[new_cost] = (new_weight, selected_items + [i])
            dp = new_dp
        best_cost = max(dp.keys())
        return dp[best_cost]

    def get_solution(self):
        best_weight, selected_items = self.__find_best_combination()
        total_cost = sum(self.items[i].cost for i in selected_items)
        return Solution(best_weight, total_cost, [i + 1 for i in selected_items])


def main():
    approximation = float(next(sys.stdin).strip())
    max_weight = int(next(sys.stdin).strip())

    kp = KnapsackProblem(approximation, max_weight)

    for line in sys.stdin:
        line = line.rstrip('\n')
        if line:
            weight, cost = map(int, line.split())
            kp.add_item(weight, cost)

    solution = kp.get_solution()
    print(solution.total_weight, solution.total_cost)
    for item in solution.selected_items:
        print(item)


if __name__ == "__main__":
    main()
