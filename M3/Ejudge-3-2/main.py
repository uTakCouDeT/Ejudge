import sys
import re
from math import ceil, log2, log


class BloomFilterError(Exception):
    pass


# class IntBitArray:
#     """
#     Целое число в Python может быть использовано для представления битового массива,
#     поскольку оно эффективно хранит информацию в битах и поддерживает битовые операции.
#     В этом подходе каждый бит в числе представляет один бит в массиве.
#     """
#
#     def __init__(self, size):
#         self.__size = size
#         self.__bit_array = 0
#
#     def set_bit(self, index):
#         """ Устанавливает бит в позиции index в 1 """
#         if index >= self.__size or index < 0:
#             raise IndexError("Index out of range")
#         self.__bit_array |= 1 << index
#
#     def reset_bit(self, index):
#         """ Устанавливает бит в позиции index в 0 """
#         if index >= self.__size or index < 0:
#             raise IndexError("Index out of range")
#         self.__bit_array &= ~(1 << index)
#
#     def get_bit(self, index):
#         """ Возвращает значение бита в позиции index """
#         if index >= self.__size or index < 0:
#             raise IndexError("Index out of range")
#         return (self.__bit_array & (1 << index)) != 0
#
#     def __str__(self):
#         """ Возвращает строковое представление битового массива в правильном порядке """
#         return bin(self.__bit_array)[2:].zfill(self.__size)[::-1]


class ByteBitArray:
    """
    Сначала хотел использовать реализацию с представлением массива через целое число,
    Но потом решил что стандартное представление bitarray через bytearray эффективнее
    """

    def __init__(self, size):
        self.__size = size
        self.__bit_array = bytearray(ceil(size / 8))

    def set_bit(self, index):
        """ Устанавливает бит в позиции index в 1 """
        if index >= self.__size or index < 0:
            raise IndexError("Index out of range")
        byte_index, bit_index = divmod(index, 8)
        self.__bit_array[byte_index] |= 1 << bit_index

    def reset_bit(self, index):
        """ Устанавливает бит в позиции index в 0 """
        if index >= self.__size or index < 0:
            raise IndexError("Index out of range")
        byte_index, bit_index = divmod(index, 8)
        self.__bit_array[byte_index] &= ~(1 << bit_index)

    def get_bit(self, index):
        """ Возвращает значение бита в позиции index """
        if index >= self.__size or index < 0:
            raise IndexError("Index out of range")
        byte_index, bit_index = divmod(index, 8)
        return (self.__bit_array[byte_index] >> bit_index) & 1

    def __str__(self):
        """ Возвращает строковое представление битового массива в правильном порядке """
        bit_string = ''
        for i in range(self.__size):
            bit_string += str(self.get_bit(i))
        return bit_string


class BloomFilter:
    def __init__(self, n, P):
        if n > 0 and 0 < P < 1:
            self.__m = round(-n * log2(P) / log(2))
            self.__k = round(-log2(P))

            if self.__m <= 0 or self.__k <= 0:
                raise BloomFilterError("Incorrect values")

            self.__bit_array = ByteBitArray(self.__m)
            self.__primes = self.__get_primes(self.__k)
            """
            Хранение массива простых чисел позволяет избежать повторных 
            вычислений и повышает общую производительность.
            """
        else:
            raise BloomFilterError("Incorrect values")

    def get_m(self):
        return self.__m

    def get_k(self):
        return self.__k

    def add(self, key):
        for i in range(self.__k):
            index = self.__hash(i, key) % self.__m
            self.__bit_array.set_bit(index)

    def search(self, key):
        for i in range(self.__k):
            index = self.__hash(i, key) % self.__m
            if self.__bit_array.get_bit(index) == 0:
                return False
        return True

    def __hash(self, i, key):
        prime = self.__primes[i]
        return ((i + 1) * key + prime) % 2147483647  # 31-е число Мерсенна

    @staticmethod
    def __get_primes(n):
        """
        Используем решето Эратосфена - один из самых эффективных способов нахождения простых чисел.
        Этот алгоритм хорошо подходит для нахождения всех простых чисел в заданном диапазоне
        """
        if n < 1:
            return []

        # Приблизительная оценка верхней границы для n-го простого числа
        upper_bound = max(int(n * log(n) * 1.5), 10)
        primes = [True] * upper_bound
        primes[0], primes[1] = False, False
        prime_numbers = []

        for p in range(2, upper_bound):
            if primes[p]:
                prime_numbers.append(p)
                if len(prime_numbers) == n:
                    break
                for i in range(p * p, upper_bound, p):
                    primes[i] = False

        return prime_numbers

    def __str__(self):
        return str(self.__bit_array)


def main():
    bloom_filter = None
    command_patterns = [
        re.compile(r'^set (\d+) (\d+\.\d+)$'),
        re.compile(r'^add (\d+)$'),
        re.compile(r'^search (\d+)$'),
        re.compile(r'^print$'),
    ]

    for line in sys.stdin:
        if not line or line == "\n":
            continue
        try:
            for pattern in command_patterns:
                match = pattern.match(line)
                if match:
                    if line.startswith("set") and not bloom_filter:
                        n, P = int(match.group(1)), float(match.group(2))
                        bloom_filter = BloomFilter(n, P)
                        print(f"{bloom_filter.get_m()} {bloom_filter.get_k()}")
                    elif line.startswith("add") and bloom_filter:
                        bloom_filter.add(int(match.group(1)))
                    elif line.startswith("search") and bloom_filter:
                        result = 1 if bloom_filter.search(int(match.group(1))) else 0
                        print(result)
                    elif line.startswith("print") and bloom_filter:
                        print(bloom_filter)
                    else:
                        print("error")
                    break
            else:
                print("error")
        except BloomFilterError as ex:
            print(f"error")


if __name__ == "__main__":
    main()
