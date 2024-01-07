import sys


class Node:
    def __init__(self):
        self.children = {}
        self.end_of_word = False


class Trie:
    def __init__(self):
        self.__root = Node()

    def add(self, word):
        """
            Сложность: O(n), где n - длина слова, добавляемого в дерево.
            Это связано с тем, что основная операция в методе — это последовательное прохождение по каждому
            символу слова для его вставки в дерево. На каждом шаге алгоритма проверяется наличие соответствующего
            префикса среди дочерних узлов текущего узла. Если необходимо, выполняется разделение или добавление узлов.
            Эти операции зависят только от количества символов в слове, а не от общего количества слов
            или узлов в дереве. Следовательно, общее время выполнения метода прямо пропорционально длине
            добавляемого слова, что и определяет линейную сложность O(n).
        """
        word = word.lower()
        current = self.__root

        index = 0
        while index < len(word):
            found = False
            # Итерация по существующим дочерним узлам
            for child_key in list(current.children):

                # Нахождение общего префикса
                left_word = word[index:]
                right_word = child_key
                prefix_len = min(len(left_word), len(right_word))
                for current_len in range(prefix_len):
                    if left_word[current_len] != right_word[current_len]:
                        prefix_len = current_len
                        break

                if prefix_len > 0:
                    found = True
                    if prefix_len < len(child_key):
                        # Разделение существующего узла
                        existing_child = current.children.pop(child_key)
                        split_node = Node()
                        current.children[word[index:index + prefix_len]] = split_node
                        split_node.children[child_key[prefix_len:]] = existing_child
                        current = split_node
                    else:
                        current = current.children[child_key]
                    index += prefix_len
                    break

            if not found:
                # Создание нового узла
                new_node = Node()
                new_node.end_of_word = index == len(word) - 1
                current.children[word[index:]] = new_node
                current = new_node
                index += len(word) - index

        current.end_of_word = True

    def search(self, word):
        """
            Сложность: O(n), где где n - длина искомого слова.
            Это связано с тем, что алгоритм проходит через каждый символ слова ровно один раз.
            В процессе поиска, метод последовательно проверяет совпадение сегментов слова с ключами дочерних
            узлов в дереве, причём каждый символ слова рассматривается только один раз. Таким образом,
            общее время выполнения метода тоже прямо линейно зависит от количества символов в слове.

        """
        word = word.lower()
        current_node = self.__root
        word_index = 0

        while word_index < len(word):
            matched = False
            # Перебор дочерних узлов текущего узла
            for child_key, child_node in current_node.children.items():
                if word.startswith(child_key, word_index):
                    # Смещение индекса на длину совпавшего префикса
                    word_index += len(child_key)
                    current_node = child_node
                    matched = True
                    break

            if not matched:
                return False

            if word_index == len(word):
                return current_node.end_of_word

        return False

    def get_corrections(self, word):
        """
            Сложность: O(k * n^2), где k - количество слов в словаре, длина которых по модулю отличается
            от длины проверяемого слова на 1, n - длина проверяемого слова (в худшем случае)
        """
        word = word.lower()
        stack = [(self.__root, "")]
        corrections = []
        word_len = len(word)

        while stack:
            node, prefix = stack.pop()

            if len(prefix) > word_len + 1:
                continue

            if node.end_of_word and len(prefix) >= word_len - 1:
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

            if min(current_row) > 1:
                return False

            prev_prev_row = prev_row.copy() if 0 in prev_row else None
            prev_row, current_row = current_row, [0] * (len_s2 + 1)

        return True if prev_row[len_s2] == 1 else False


class AutoCorrect:
    def __init__(self):
        self.__radix = Trie()

    def add_word(self, word):
        self.__radix.add(word)

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


if __name__ == "__main__":
    main()
