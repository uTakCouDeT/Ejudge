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

    # def print_tree(self, node=None, prefix=""):
    #     if node is None:
    #         node = self.__root
    #
    #     for child_suffix, child_node in node.children.items():
    #         current_prefix = prefix + child_suffix
    #         print(f"{' ' * len(prefix)}|- {child_suffix} {'(word)' if child_node.is_word else ''}")
    #         self.print_tree(child_node, current_prefix)

    def add(self, word):
        """
            Сложность: O(m), где m - длина добавляемого слова.
            Пояснение: При добавлении слова в префиксное дерево, алгоритму необходимо пройти по пути,
            соответствующему каждому символу слова. В сжатом префиксном дереве, каждый узел может
            представлять собой целый префикс, что уменьшает количество проверяемых узлов по сравнению
            с обычным префиксным деревом. Но при этом каждый префикс проверяется за время линейно
            зависящее от длины этого префикса. А сумма длин префиксов по пути до конца слова равна длине этого слова.
            Следовательно, количество операций, необходимых для добавления слова, линейно зависит от его длины.
        """
        word = word.lower()
        node = self.__root
        i = 0
        while i < len(word):
            match = False
            for child in node.children.keys():
                common_prefix_length = self.__common_prefix_length(word[i:], child)
                # P.S. сложность этой операции O(common_prefix_length)
                # если common_prefix_length = 0 то сложность его вычисления O(1)
                # таким образом всех детей, у которых длина общего префикса равна 0 мы проверяем за О(1)
                # и только находя в словаре того единственного, мы двигаемся дальше по дереву

                if common_prefix_length > 0:
                    match = True
                    # Если общий префикс совпадает полностью с существующим узлом
                    if common_prefix_length == len(child):
                        node = node.children[child]
                    else:
                        # Разделяем существующий узел
                        existing_node = node.children[child]
                        new_child = child[:common_prefix_length]
                        new_node = Node()

                        # Обновляем детей для нового узла и старого узла
                        node.children[new_child] = new_node
                        new_node.children[child[common_prefix_length:]] = existing_node
                        del node.children[child]

                        node = new_node

                    # А если common_prefix_length > 0
                    # то мы скипаем ровно столько итераций сколько было потрачено на его вычисление
                    i += common_prefix_length
                    break

            if not match:
                new_node = Node()
                new_node.is_word = True
                node.children[word[i:]] = new_node
                break
            elif i == len(word):
                node.is_word = True

    @staticmethod
    def __common_prefix_length(s1, s2):
        """"
            Сложность: O(min(m, n)), где m и n - длины сравниваемых строк.
            Пояснение: Этот метод определяет длину общего префикса двух строк.
            Он проходит по обеим строкам до первого несовпадения или до конца самой короткой строки.
            В худшем случае количество итераций равно длине более короткой строки.
        """
        min_length = min(len(s1), len(s2))
        for i in range(min_length):
            if s1[i] != s2[i]:
                return i
        return min_length

    def search(self, word):
        """
            Сложность: O(m), где m - длина искомого слова.
            Пояснение: Поиск слова в сжатом префиксном дереве также требует прохождения по пути,
            соответствующему каждому символу слова. Соответственно сложность также линейно зависит от длины слова.
        """
        word = word.lower()
        node = self.__root
        i = 0
        while i < len(word):
            found = False
            for child in node.children.keys():
                if word[i:].startswith(child):  # Если первый символ не совпадает - сложность о(1)
                    found = True                # А если совпадет, то в худшем О(min(len(child), len(word)))
                    node = node.children[child]
                    i += len(child)  # Снова скипаем ровно столько итераций сколько затратила проверка
                    break
            if not found:
                return False
        return node.is_word

    def get_corrections(self, word):
        """
            Сложность: O(k * n^2), где k - количество слов в словаре, длина которых по модулю отличается
            от длины проверяемого слова на 1, n - длина проверяемого слова (в худшем случае)

            Пояснение: Алгоритм использует стек для итеративного обхода дерева в глубину.
            Таким образом каждый узел должен быть посщён ровно один раз. Но в данном методе
            не продолжаем поиск в случае, когда длина префикса стала больше чем длина слова.
            Это отсекает большое количество узлов для проверки, но точное количество зависит
            от средней длины префиксов внутри каждого узла и от распределения длин от корня к листьям.
            Более глобально - от количества слов длины больше проверяемого на 1.
            В худшем случае метод get_corrections может обойти все узлы в дереве.

            При этом для каждого слова происходит проверка алгоритмом Дамерау-Левенштейна что расстояние равно 1.
            Эта проверка требует в худшем случае O(m * n), где m и n - длины сравниваемых слов
            (см. описание фунции __is_dam_lev_distance_one)

            В данном методе так же присутствует оптимизация, для того чтобы алгоритм запускался,
            только в том случае, кода сумма длин префиксов достигла длины проверяемого слова минус один,
            это позволяет использовать алгоритмом Дамерау-Левенштейна только в тех случаях,
            когда длина проверяемого слова по модулю отличается от длины слов из словаря не больше чем на один.
            (с учётом остановки при слишком большой длине, которая была описана ранее)

            Таким образом можно утверждать что в контексте данного метода сложность
            алгоритма Дамерау-Левенштейна (в худшем случае) будет равна О(n^2) где n - длина проверяемого слова
            тк слова другого размера (с погрешностью в единицу) проверяться не будут

            Так же стоит учесть, что алгоритм хоть и обходит в худшем случае все узлы, но проверка
            __is_dam_lev_distance_one запускается только в случае если вершина, в которую мы пришли, является концом
            слова. Это означает, что проверка запустится в худшем случае k раз, где k - количество слов в словаре.

            Таким образом, общая сложность метода равна O(k * n^2), где k - количество слов в словаре,
            n - длина проверяемого слова (в худшем случае). Кроме того можно уточнить, что проверка
            запускается только для слов длины, по модулю отличающейся от длины проверяемого на 1.
            И соответственно k можно определить как количество таких слов.
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

            P.S. Оптимизация с проверкой модуля разности длин включена в метод get_corrections,
            тк там она так же влияет на количество вершин по которым будет совершен обход.
            При подсчёте сложности данного метода она не учитывается.

            P.P.S случаи, когда расстояние равно 0 отсекаются ещё раньше, по этому в методе они вообще не учитываются
            (хоть это и не универсально, но в рамках инкапсуляции в этом нет необходимости)

            Сложность в худшем равна O(n * m), например при условии, что расстояние равно 1
            (или когда оно равно 2, но это обнаруживается только в последней строке)
            Но при этом алгоритм оптимизирован для раннего выхода: как только становится ясно,
            что минимальное расстояние в текущем ряду больше одного - алгоритм завершается.

            Если строки отличаются в начале, алгоритм быстро достигнет условия выхода.
            Чаще всего по первым символам уже становится понятно, что расстояние больше чем 1
            Но предположим что это происходит в половине случаев => сложность в среднем будет O(n * m / 2)

            P.P.P.S хотя в реальности вероятность того, что в двух случайно взятых словах
            (только из английского алфавита) первая буква совпадёт равна 0.03846 (остальные случаи - 96,154%)
            это порождает ситуацию в которой минимальное значение в строке становится равно 1
            и каждая неисправимая ошибка приводит к завершению алгоритма. Вероятность что вторые
            буквы совпадут 0.03846 (+ вероятность что не совпадут, но их можно исправить транспозицией 0,001479172).
            В сумме выходит 0,039939172 (обратная ситуация - 96,00%). Вероятность, что первая буква не совпала (около 96%)
            и вместе с этим не совпала вторая буква (тоже около 96%) получается около 92% тк эти ситуации в общем случае
            независимы (вклад транспозиции на порядок меньше). Даже при такой грубой оценке вероятность что алгоритм
            завершится на второй же букве равняется приблизительно 92%. При этом с каждой буквой вероятность раннего
            завершения будет увеличиваться. По этому в среднем данная функция достаточно хорошо оптимизирована.

            Так же транспозиция в данном алгоритме учитывается только там где это необходимо,
            и в большинстве случаев этот этап пропускается. (хотя это скорее микрооптимизация)

            Ну и по памяти полезно хранить не всю матрицу, а только 2 (иногда 3) строки.
        """
        len_s1, len_s2 = len(s1), len(s2)

        prev_prev_row = None
        prev_row = list(range(len_s2 + 1))
        current_row = [0] * (len_s2 + 1)
        # print(prev_row)

        for i in range(1, len_s1 + 1):
            current_row[0] = i
            for j in range(1, len_s2 + 1):
                cost = 0 if s1[i - 1] == s2[j - 1] else 1
                current_row[j] = min(prev_row[j] + 1, current_row[j - 1] + 1, prev_row[j - 1] + cost)

                if prev_prev_row and s1[i - 1] == s2[j - 2] and s1[i - 2] == s2[j - 1]:
                    current_row[j] = min(current_row[j], prev_prev_row[j - 2] + 1)
            # print(current_row)

            # Останавливаем если в матрице все расстояния больше 1
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


class AutoCorrect:
    def __init__(self):
        self.__radix = RadixTree()

    def add_word(self, word):
        self.__radix.add(word)
        # self.__radix.print_tree()

    def is_correct(self, word):
        return self.__radix.search(word)

    def get_corrections(self, word):
        return self.__radix.get_corrections(word)


def print_corrections(word, is_correct, corrections, output_stream=sys.stdout):
    if is_correct:
        print(f"{word} - ok", file=output_stream)
        return

    if corrections:
        corrections.sort()
        print(f"{word} -> {', '.join(corrections)}", file=output_stream)
    else:
        print(f"{word} -?", file=output_stream)


def main():
    ac = AutoCorrect()

    n = int(next(sys.stdin).strip())
    for _ in range(n):
        ac.add_word(next(sys.stdin).rstrip('\n'))

    for line in sys.stdin:
        line = line.rstrip('\n')
        if line:
            is_correct = ac.is_correct(line)
            corrections = ac.get_corrections(line)
            print_corrections(line, is_correct, corrections)

# class AutoCorrect:
#     def __init__(self):
#         self.__radix = RadixTree()
#
#     def add_word(self, word):
#         self.__radix.add(word)
#         # self.__radix.print_tree()
#
#     def is_correct(self, word):
#         return self.__radix.search(word)
#
#     def get_corrections(self, word):
#         return self.__radix.get_corrections(word)
if __name__ == "__main__":
    main()
