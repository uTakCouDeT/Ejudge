import sys


# Для того чтобы сразу отбрасывать попытки которые старше 2*B_max, удобнее использовать класс
class BlockTimeCalculator:
    def __init__(self, b_max, current_time):
        self.__b_max = b_max
        self.__current_time = current_time
        self.__login_attempts = []

    def add_login_attempt(self, timestamp):
        # при добавлении отбрасываем лишние попытки
        if self.__current_time - timestamp <= 2 * self.__b_max:
            self.__login_attempts.append(timestamp)

    def calculate_block_time(self, n, p, b):
        # Сортировка попыток по времени
        self.__login_attempts.sort()

        # Инициализация переменных для отслеживания блокировок
        block_duration = b
        last_block_end = None

        for i in range(len(self.__login_attempts)):
            # Проверка, есть ли N неудачных попыток в интервале P
            if i >= n - 1 and self.__login_attempts[i] - self.__login_attempts[i - n + 1] <= p:
                # Расчет начала и конца блокировки
                block_start = self.__login_attempts[i]
                block_end = block_start + block_duration

                # Проверка, не находится ли предыдущая блокировка в этом интервале
                if not last_block_end or block_start > last_block_end:
                    # Удваивание времени блокировки для следующей блокировки, но не более B_max
                    block_duration = min(block_duration * 2, self.__b_max)
                    last_block_end = block_end

        # Проверка, истекло ли время последней блокировки
        if last_block_end and last_block_end > self.__current_time:
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
