import sys


class LoginBlocker:
    def __init__(self, n, p, b, b_max, current_time):
        self.__n = n
        self.__p = p
        self.__b_min = b
        self.__b_max = b_max
        self.__current_time = current_time
        self.__login_attempts = []

    def add_login_attempt(self, timestamp):
        # Очищаем попытки, которые уже не важны
        self.__login_attempts = [t for t in self.__login_attempts if self.__current_time - t <= 2 * self.__b_max]
        self.__login_attempts.append(timestamp)

    def __compute_block_duration(self):
        # Проверяем попытки входа и вычисляем время блокировки
        self.__login_attempts.sort()
        block_duration = self.__b_min
        last_block_end = 0

        for i in range(len(self.__login_attempts) - self.__n + 1):
            window = self.__login_attempts[i:i + self.__n]
            if window[-1] - window[0] <= self.__p:
                if last_block_end >= window[0]:
                    block_duration = min(block_duration * 2, self.__b_max)
                last_block_end = window[-1] + block_duration
                i += self.__n - 1  # Пропускаем проверяемое окно

        return last_block_end

    def unlock_time(self):
        block_end = self.__compute_block_duration()
        if block_end > self.__current_time:
            return block_end
        else:
            return None


def main():
    n, p, b, b_max, current_time = map(int, next(sys.stdin).strip().split())
    blocker = LoginBlocker(n, p, b, b_max, current_time)

    for line in sys.stdin:
        line = line.rstrip('\n')
        if line:
            timestamp = int(line)
            blocker.add_login_attempt(timestamp)

    unlock_time = blocker.unlock_time()
    if unlock_time:
        print(unlock_time)
    else:
        print("ok")


if __name__ == "__main__":
    main()
