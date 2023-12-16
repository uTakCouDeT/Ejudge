import sys
import re
from math import log2, log


class BloomFilterError(Exception):
    pass


class BloomFilter:
    def __init__(self, n, P):
        if n > 0 and 0 < P < 1:
            self.__m = round(-n * log2(P) / log(2))
            self.__k = round(-log2(P))
            self.__bit_array = [0] * self.__m
            self.__M = 2147483647  # 31-е число Мерсенна
        else:
            raise BloomFilterError("Incorrect values")

    def get_m(self):
        return self.__m

    def get_k(self):
        return self.__k

    def add(self, key):
        for i in range(self.__k):
            index = self.__hash(i, key) % self.__m
            self.__bit_array[index] = 1

    def search(self, key):
        for i in range(self.__k):
            index = self.__hash(i, key) % self.__m
            if self.__bit_array[index] == 0:
                return False
        return True

    def __hash(self, i, key):
        prime = self.__get_prime(i + 1)
        return ((i + 1) * key + prime) % self.__M

    @staticmethod
    def __get_prime(n):
        if n == 1:
            return 2

        upper_bound = max(int(n * log(n) * 1.5), 10)
        primes = [True] * upper_bound
        primes[0], primes[1] = False, False
        p, count = 2, 0

        while count < n:
            if primes[p]:
                count += 1
                for i in range(p * p, upper_bound, p):
                    if i < upper_bound:
                        primes[i] = False
            p += 1
            if p >= upper_bound:
                extra_bound = int(upper_bound * 1.5)
                primes.extend([True] * (extra_bound - upper_bound))
                upper_bound = extra_bound

        return p - 1

    def print_state(self, output_stream=sys.stdout):
        print(''.join(map(str, self.__bit_array)), file=output_stream)


def main():
    output_stream = sys.stdout
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
                    if line.startswith("set"):
                        if bloom_filter:
                            print("error")
                        else:
                            n, P = int(match.group(1)), float(match.group(2))
                            bloom_filter = BloomFilter(n, P)
                            print(f"{bloom_filter.get_m()} {bloom_filter.get_k()}", file=output_stream)
                    elif line.startswith("add"):
                        if bloom_filter:
                            bloom_filter.add(int(match.group(1)))
                    elif line.startswith("search"):
                        if bloom_filter:
                            result = 1 if bloom_filter.search(int(match.group(1))) else 0
                            print(result, file=output_stream)
                    elif line.startswith("print"):
                        if bloom_filter:
                            bloom_filter.print_state(output_stream=output_stream)
                    break
            else:
                print("error", file=output_stream)
        except BloomFilterError as ex:
            print(f"error", file=output_stream)


if __name__ == "__main__":
    main()
