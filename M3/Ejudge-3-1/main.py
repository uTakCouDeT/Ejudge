from collections import deque
import sys

"""
Асимптотическая сложность и использование памяти

    Временная сложность: O(M), где M - количество попыток входа в пределах 2*B_max. 
    Каждая попытка обрабатывается за постоянное время.
    Пространственная сложность: O(M), так как хранятся только попытки в течение 2*B_max. 
    Очередь filtered_attempts содержит максимум M элементов.
    
"""


def calculate_block_time(attempts, N, P, B, B_max, current_time):
    # Инициализация переменных
    block_time = B
    last_block_end_time = 0
    filtered_attempts = deque()

    # Фильтрация попыток за последние 2*B_max секунд
    for attempt_time in attempts:
        if current_time - attempt_time <= 2 * B_max:
            filtered_attempts.append(attempt_time)

    for attempt_time in filtered_attempts:
        # Удаление старых попыток
        while filtered_attempts and filtered_attempts[0] < attempt_time - P:
            filtered_attempts.popleft()

        # Проверка количества попыток и блокировка если требуется
        if len(filtered_attempts) >= N:
            # Удвоение времени блокировки, если предыдущая блокировка недавно закончилась
            if last_block_end_time and attempt_time <= last_block_end_time:
                block_time = min(block_time * 2, B_max)
            last_block_end_time = attempt_time + block_time
            filtered_attempts.clear()  # Очистка после блокировки

    return last_block_end_time if last_block_end_time and last_block_end_time > current_time else "ok"


# Чтение данных из стандартного ввода
params = input().split()
attempts = [int(input()) for _ in range(len(params) - 5)]
N, P, B, B_max, current_time = map(int, params[:5])

# Вычисление времени окончания блокировки
result = calculate_block_time(attempts, N, P, B, B_max, current_time)
print(result)
