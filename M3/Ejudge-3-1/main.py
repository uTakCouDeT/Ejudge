import sys
from datetime import datetime, timedelta


def calculate_block_time(attempts, N, P, B, B_max, current_time):
    # Преобразование текущего времени в объект datetime для удобства
    current_datetime = datetime.fromtimestamp(current_time)
    max_block_datetime = current_datetime - timedelta(seconds=2 * B_max)

    # Фильтрация попыток, которые старше 2*B_max
    filtered_attempts = [datetime.fromtimestamp(attempt) for attempt in attempts if
                         datetime.fromtimestamp(attempt) >= max_block_datetime]

    # Сортировка отфильтрованных попыток по времени
    filtered_attempts.sort()

    # Инициализация переменных для отслеживания блокировок
    block_duration = timedelta(seconds=B)
    last_block_end = None

    for i in range(len(filtered_attempts)):
        # Проверка, есть ли N неудачных попыток в интервале P
        if i >= N - 1 and filtered_attempts[i] - filtered_attempts[i - N + 1] <= timedelta(seconds=P):
            # Расчет начала и конца блокировки
            block_start = filtered_attempts[i]
            block_end = block_start + block_duration

            # Проверка, не находится ли предыдущая блокировка в этом интервале
            if not last_block_end or block_start > last_block_end:
                # Удваивание времени блокировки для следующей блокировки, но не более B_max
                block_duration = min(block_duration * 2, timedelta(seconds=B_max))
                last_block_end = block_end

    # Проверка, истекло ли время последней блокировки
    if last_block_end and last_block_end > current_datetime:
        return int(last_block_end.timestamp())
    else:
        return "ok"


def main():
    N, P, B, B_max, current_time = map(int, next(sys.stdin).strip().split())
    test_attempts = []

    for line in sys.stdin:
        line = line.rstrip('\n')
        if line:
            test_attempts.append(int(line))

    print(calculate_block_time(test_attempts, N, P, B, B_max, current_time))


if __name__ == "__main__":
    main()
