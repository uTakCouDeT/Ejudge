import sys


# Для того чтобы сразу отбрасывать попытки которые старше 2*B_max, удобнее использовать класс
class BlockTimeCalculator:
    def __init__(self, b_max, current_time):
        self.__b_max = b_max
        self.__current_time = current_time
        self.__login_attempts = []

    def add_login_attempt(self, timestamp):
        """
            Асимптотическая сложность: O(1), т.e. каждая попытка добавляется за константное время.
            Однако, если учитывать, что этот метод вызывается для каждой попытки входа,
            то общая сложность будет O(M), где M - количество попыток входа.
        """
        # при добавлении отбрасываем лишние попытки
        if self.__current_time - timestamp <= 2 * self.__b_max:
            self.__login_attempts.append(timestamp)

    def calculate_block_time(self, n, p, b):
        """
            Асимптотическая сложность: O(N log N), где N - количество сохраненных попыток входа.
            Этот метод сначала сортирует временные метки попыток входа, а затем проверяет условия для блокировки.
            Стандартная сортировка в питоне выполняется за O(N log N). Для каждой попытки входа выполняется проверка,
            укладывается ли она в интервал блокировки. Это требует просмотра каждого элемента в отсортированном списке,
            что даёт сложность O(N). Итак, общая сложность этого метода составляет O(N log N + N) = O(N log N)

            Использование памяти: O(N), где N - количество попыток входа в пределах 2 * B_max от текущего времени.
            Программа хранит временные метки попыток входа в пределах 2 * B_max от текущего времени в списке.
            Сортировка массива производится InPlace. Это означает, что дополнительная память для него не выделяется.
            В худшем случае, когда все попытки входа находятся в пределах 2 * B_max, список может содержать
            все попытки, которые были поданы на вход. Следовательно, в худшем случае, использование
            памяти для данного алгоритма будет O(M), где M - общее количество попыток входа.

            P.S. Вместе с добавлением в массив, общая сложность алгоритма выходит O(N log N + M),
            где N - количество сохранённых попыток входа, а M - общее количество попыток входа.
        """
        # Сортировка попыток по времени (почему вообще попытки поступают не в хронологическом порядке?)
        self.__login_attempts.sort()

        # Инициализация переменных для отслеживания блокировок
        block_duration = b
        last_block_end = 0

        i = n - 1
        while i < len(self.__login_attempts):
            # Проверка, есть ли N неудачных попыток в интервале P
            if self.__login_attempts[i] - self.__login_attempts[i - n + 1] <= p:
                # Расчет времени конца блокировки
                last_block_end = self.__login_attempts[i] + block_duration
                # Удваивание времени блокировки для следующей блокировки, но не более B_max
                block_duration = min(block_duration * 2, self.__b_max)
                i += n
            else:
                i += 1

        # Проверка, истекло ли время последней блокировки
        if last_block_end > self.__current_time:
            return int(last_block_end)
        else:
            return None


def main():
    n, p, b, b_max, current_time = map(int, next(sys.stdin).strip().split())
    block_time_calculator = BlockTimeCalculator(b_max, current_time)

    for line in sys.stdin:
        line = line.rstrip('\n')
        if line:
            block_time_calculator.add_login_attempt(int(line))

    block_time = block_time_calculator.calculate_block_time(n, p, b)
    if block_time:
        print(block_time)
    else:
        print("ok")


if __name__ == "__main__":
    main()
