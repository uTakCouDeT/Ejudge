import sys


class Node:
    """ Для повышения читаемости кода запишем все предметы в объекты отдельного класса """

    def __init__(self, index, weight, cost, scaled_cost):
        self.index = index  # Индекс, чтобы сохранить порядок
        self.weight = weight
        self.cost = cost
        self.scaled_cost = scaled_cost  # Для приближенного решения задачи
        # Записываем scaled_cost в отдельную переменную, тк исходные стоимости будут нужны при формировании ответа


class Solution:
    """ Класс, возвращаемый при решении задачи: Чтобы программа не была заточена под вывод """

    def __init__(self, total_weight, total_cost, selected_items):
        self.total_weight = total_weight
        self.total_cost = total_cost
        self.selected_items = selected_items


class KnapsackProblem:
    def __init__(self, approximation, max_weight):
        # Проверки на валидность входных данных (на всякий случай)
        if not 0 <= approximation <= 1:
            raise ValueError("Approximation coefficient must be between 0 and 1")
        if max_weight < 0:
            raise ValueError("Max weight must be a non-negative integer")
        self.approximation = approximation
        self.max_weight = max_weight
        self.items = []
        self.max_cost = 0
        self.counter = 1  # Счётчик предметов, чтобы сохранить порядок в ответе
        # Потратил 4 попытки, чтобы понять, что без него порядок сбивался :(

    def add_item(self, weight, cost):
        # Ну и тут тоже можно
        if weight < 0 or cost < 0:
            raise ValueError("Weight and value must be non-negative integers")
        # Предметы, которые очевидно не влезут, можно не учитывать
        if weight <= self.max_weight:
            self.items.append(Node(self.counter, weight, cost, 0))
            self.max_cost = max(self.max_cost, cost)
        self.counter += 1

    def __calculate_scaled_costs(self):
        """ Масштабируем стоимости предметов для приближенного решения """
        scale = self.approximation * self.max_cost / (len(self.items) * (1 + self.approximation))
        for item in self.items:
            item.scaled_cost = int(item.cost / scale)

    def __find_best_combination(self):
        """ Находим лучшую комбинацию предметов, используя динамическое программирование (с учётом масштабирования) """
        self.__calculate_scaled_costs()
        dp = {0: (0, [])}
        for item in self.items:
            for total_cost, (total_weight, selected_items) in list(dp.items()):
                new_weight = total_weight + item.weight
                new_cost = total_cost + item.scaled_cost
                if new_weight <= self.max_weight and (new_cost not in dp or dp[new_cost][0] > new_weight):
                    dp[new_cost] = (new_weight, selected_items + [item.index])
        best_cost = max(dp.keys())
        return dp[best_cost]

    def get_solution(self):
        # Если предметов нет, возвращаем пустое решение
        if not self.items:
            return Solution(0, 0, [])
        # В остальных случаях считаем лучшую комбинацию
        best_weight, selected_items = self.__find_best_combination()
        total_cost = sum(item.cost for item in self.items if item.index in selected_items)
        return Solution(best_weight, total_cost, selected_items)


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
