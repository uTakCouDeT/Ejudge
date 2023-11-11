import sys


# class Node:
#     def __init__(self):
#         self.children = {}  # ключ - следующая буква, значение ссылка на её ноду
#         self.is_end_of_word = False
#
#
# class Trie:
#     def __init__(self):
#         self.__root = Node()  # корень - всегда пустое слово, по этому его значение хранить не нужно
#
#     def add(self, word):
#         node = self.__root
#         for char in word.lower():
#             if char not in node.children:
#                 node.children[char] = Node()
#             node = node.children[char]
#         node.is_end_of_word = True
#
#     def search(self, word):
#         node = self.__root
#         for char in word.lower():
#             if char not in node.children:
#                 return None
#             node = node.children[char]
#         return node if node.is_end_of_word else None
#
#     def get_words(self):
#         words = []
#         stack = [(self.__root, "")]
#         while stack:
#             current_node, word = stack.pop()
#             if current_node.is_end_of_word:
#                 words.append(word)
#             for char, next_node in current_node.children.items():
#                 stack.append((next_node, word + char))
#         return words


class Node:
    def __init__(self):
        self.children = {}  # сложность учитывает, что доступ к детям за O(1)
        self.is_word = False


# Сначала сделал через обычное префиксное дерево, а потом перечитал условие и пошел его "сжимать"...
class RadixTree:
    def __init__(self):
        self.__root = Node()

    def add(self, word):
        """
            Сложность: O(m), где m - длина добавляемого слова.
            Пояснение: Для каждого символа слова алгоритм проверяет наличие
            соответствующего дочернего узла и создает новый узел, если он отсутствует.
            Поскольку каждый символ в слове обрабатывается один раз, сложность линейно зависит от длины слова.
        """
        word = word.lower()
        node = self.__root
        i = 0
        while i < len(word):
            match = False
            for child in node.children:
                if word[i:].startswith(child):
                    match = True
                    node = node.children[child]
                    i += len(child)
                    break
            if not match:
                new_node = Node()
                new_node.is_word = True
                node.children[word[i:]] = new_node
                break

    def search(self, word):
        """
            Сложность: O(m), где m - длина искомого слова.
            Пояснение: Аналогично добавлению
        """
        word = word.lower()
        node = self.__root
        i = 0
        while i < len(word):
            found = False
            for child in node.children:
                if word[i:].startswith(child):
                    found = True
                    node = node.children[child]
                    i += len(child)
                    break
            if not found:
                return False
        return node.is_word

    def get_corrections(self, word):
        """
            Сложность: O(k * n^2), где k - количество узлов в дереве, n - длина проверяемого слова (в худшем случае)
            Пояснение: Алгоритм использует стек для итеративного обхода дерева в глубину.
            Таким образом каждый узел должен быть посщён ровно один раз. Но в данном методе
            не продолжаем поиск в случае, когда длина префикса стала больше чем длина слова.
            Это отсекает большое количество узлов для проверки, но точное количество зависит
            от средней длины префиксов внутри каждого узла и от распределения длин от корня к листьям.
            В худшем случае метод get_corrections может обойти все узлы в дереве.

            При этом для каждого слова происходит проверка алгоритмом Дамерау-Левенштейна что расстояние равно 1.
            Эта проверка требует в худшем случае O(m * n), где m и n - длины сравниваемых слов
            (см. описание фунции __is_dam_lev_distance_one)

            В данном методе так же присутствует оптимизация, для того чтобы алгоритм запускался,
            только в том случае, когда слово достигло длины проверяемого слова минус один,
            это позволяет использовать алгоритмом Дамерау-Левенштейна только в тех случаях,
            когда длина проверяемого слова отличается от длины слов в словаре не больше чем на один,
            таким образом можно утверждать что сложность алгоритма Дамерау-Левенштейна (в худшем случае)
            будет равна О(n^2) где n - длина проверяемого слова
            тк слова другого размера (с погрешностью в единицу) проверяться не будут

            Предположим что оптимизация поиска в глубину сократит количество узлов которые необходимо пройти вдвое
            Алгоритм Дамерау-Левенштейна в среднем тоже работает бысрее (из оисания функции __is_dam_lev_distance_one
            предположим что в 2 раза) Следовательно в среднем сложность будет равна:
            O(k * n^2 / 4), где k - количество узлов в дереве, n - длина проверяемого слова
        """
        word = word.lower()
        stack = [(self.__root, "")]
        corrections = []
        word_len = len(word)

        while stack:
            node, prefix = stack.pop()

            # Если префикс слишком длинный дальше не идём
            if len(prefix) > word_len + 1:
                continue

            # Если слово слишком короткое, алгоритм для проверки можно не запускать
            if node.is_word and len(prefix) >= word_len - 1:
                if self.__is_dam_lev_distance_one(word, prefix):
                    corrections.append(prefix)

            for child_suffix, child_node in node.children.items():
                stack.append((child_node, prefix + child_suffix))

        return corrections

    @staticmethod
    def __is_dam_lev_distance_one(s1, s2):
        """
            Сложность: O(m * n), где m и n - длины сравниваемых слов (в худшем случае)
            Пояснение: Алгоритм использует два вложенных цикла, каждый из которых проходит по длине одной из строк.
            В худшем случае это дает сложность O(n * m), где n и m - длины сравниваемых строк.
            Но при этом алгоритм оптимизирован для раннего выхода: как только становится ясно,
            что минимальное расстояние в текущем ряду больше одного - алгоритм завершается.
            Так же транспозиция в данном алгоритме учитывается только там где это необходимо,
            и в большинстве случаев этот этап пропускается. (хотя это скорее микрооптимизация)

            Если строки отличаются в начале, алгоритм быстро достигнет условия выхода.
            Чаще всего по первым символам уже становится понятно, что расстояние больше чем 1
            Но предположим что это происходит в половине случаев => сложность в среднем будет O(n * m / 2)
        """
        len_s1, len_s2 = len(s1), len(s2)

        prev_prev_row = None
        prev_row = list(range(len_s2 + 1))
        current_row = [0] * (len_s2 + 1)

        for i in range(1, len_s1 + 1):
            current_row[0] = i
            for j in range(1, len_s2 + 1):
                cost = 0 if s1[i - 1] == s2[j - 1] else 1
                current_row[j] = min(prev_row[j] + 1, current_row[j - 1] + 1, prev_row[j - 1] + cost)

                if prev_prev_row and s1[i - 1] == s2[j - 2] and s1[i - 2] == s2[j - 1]:
                    current_row[j] = min(current_row[j], prev_prev_row[j - 2] + 1)

            # Останавливаем если в матрицпе все расстояния больше 1
            # тк в следующих строчках оно меньше стать не может
            if min(current_row) > 1:
                return False
            """
                P.S. касательно транспозиции (которая может прыгнуть через строчку):
                если все значения в current_row не меньше 2,
                то в prev_row все значения были не меньше 1
                тк если там есть 0 то минимальное значение для current_row было бы 0 + 1 = 1 (удаление)
                и при транспозиции может получиться минимум 1 + 1 = 2 (что нам, собственно, не подходит)
            """

            # Тут по той же причине можно не сохранять третью строчку если там нет нулей
            prev_prev_row = prev_row.copy() if 0 in prev_row else None
            prev_row, current_row = current_row, [0] * (len_s2 + 1)

        return True if prev_row[len_s2] == 1 else False

        # @staticmethod
        # def __dam_lev_distance(s1, s2):
        #     len_s1, len_s2 = len(s1), len(s2)
        #
        #     d = [[0] * (len_s2 + 1) for _ in range(len_s1 + 1)]
        #
        #     for i in range(len_s1 + 1):
        #         d[i][0] = i
        #     for j in range(len_s2 + 1):
        #         d[0][j] = j
        #
        #     for i in range(1, len_s1 + 1):
        #         for j in range(1, len_s2 + 1):
        #             cost = 0 if s1[i - 1] == s2[j - 1] else 1
        #             d[i][j] = min(d[i - 1][j] + 1,  # удаление
        #                           d[i][j - 1] + 1,  # вставка
        #                           d[i - 1][j - 1] + cost)  # замена
        #
        #             if i > 1 and j > 1 and s1[i - 1] == s2[j - 2] and s1[i - 2] == s2[j - 1]:
        #                 d[i][j] = min(d[i][j], d[i - 2][j - 2] + cost)  # транспозиция
        #
        #     return d[len_s1][len_s2]


class AutoCorrect:
    def __init__(self):
        self.__radix = RadixTree()

    def add_word(self, word):
        self.__radix.add(word)

    def correct_word(self, word):
        if self.__radix.search(word):
            return f"{word} - ok"

        corrections = self.__radix.get_corrections(word)

        if corrections:
            corrections.sort()
            return f"{word} -> {', '.join(corrections)}"
        else:
            return f"{word} -?"


def main():
    ac = AutoCorrect()

    n = int(next(sys.stdin).strip())
    for _ in range(n):
        ac.add_word(next(sys.stdin).rstrip('\n'))

    for line in sys.stdin:
        line = line.rstrip('\n')
        if line:
            print(ac.correct_word(line))


if __name__ == "__main__":
    main()
