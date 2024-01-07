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

    def get_words_with_similar_length(self, length):
        """
        Сложность: O(m + n), где m - длина префикса, а n - общее количество символов в поддереве,
                                                              начинающемся с узла этого префикса.
        Метод исследует поддерево для сбора слов, имеющих схожую длину с префиксом,
        и зависит от длины префикса и количества символов в этом поддереве.
        """
        words = []
        stack = [(self.__root, "")]  # Стек для хранения пар (node, current_word)

        while stack:
            node, current_word = stack.pop()
            if abs(len(current_word) - length) <= 1 and node.end_of_word:
                words.append(current_word)

            for char, next_node in node.children.items():
                stack.append((next_node, current_word + char))

        return words


class AutoCorrection:
    def __init__(self):
        self.__dictionary = Trie()

    def add_word_in_dictionary(self, word):
        self.__dictionary.add(word)

    def correctness_check(self, word):
        return self.__dictionary.search(word)

    @staticmethod
    def __calculate_edit_distance(left_word, right_word):
        """
        Вычисляет, является ли расстояние редактирования между двумя строками равным 1.
        Это метод алгоритма Дамерау-Левенштейна с ограниченной сложностью O(m * n).

            Сложность: O(m * n), где m и n - длины двух строк.
            Это обусловлено использованием двух вложенных циклов, каждый из которых проходит от 1 до длины
            соответствующей строки. Основная операция внутри вложенного цикла выполняется за константное время.

            * Выполненные Оптимизации:

            Оптимизация По Памяти:
                Вместо хранения всей матрицы редактирования алгоритм хранит только три строки одновременно
                (текущую, предыдущую и "пред-предыдущую" строку). Это значительно снижает использование
                памяти по сравнению с классическим подходом, где требуется хранить всю матрицу.

            Ранний Выход:
                Алгоритм реализует ранний выход из текущей итерации, если минимальное значение в текущей
                строке матрицы превышает 1. Это уменьшает количество ненужных вычислений, так как если
                минимальное расстояние уже больше 1, то дальнейшие проверки не изменят общий результат.

            Оптимизация Транспозиции:
                Учет операции транспозиции (обмен местами двух соседних символов) реализован только в том случае,
                если текущий символ i и j предшествуют друг другу в обоих строках. Это улучшает эффективность,
                так как операция транспозиции проверяется только тогда, когда это действительно необходимо.
        """
        left_word_len, right_word_len = len(left_word), len(right_word)

        # Инициализация матрицы редактирования
        previous_row = [i for i in range(right_word_len + 1)]
        current_row = [0] * (right_word_len + 1)
        two_rows_ago = None

        for i in range(1, left_word_len + 1):
            current_row[0] = i
            for j in range(1, right_word_len + 1):
                substitution_cost = 0 if left_word[i - 1] == right_word[j - 1] else 1
                current_row[j] = min(
                    previous_row[j] + 1,  # удаление
                    current_row[j - 1] + 1,  # вставка
                    previous_row[j - 1] + substitution_cost  # замена
                )

                if two_rows_ago is not None and i > 1 and j > 1 \
                        and left_word[i - 1] == right_word[j - 2] and left_word[i - 2] == right_word[j - 1]:
                    current_row[j] = min(current_row[j], two_rows_ago[j - 2] + 1)  # транспозиция

            if min(current_row) > 1:
                return False

            two_rows_ago = previous_row.copy() if 0 in previous_row else None
            previous_row, current_row = current_row, [0] * (right_word_len + 1)

        return previous_row[right_word_len] == 1

    def get_corrections_array(self, word):
        """
        Сложность: O(k * n^2), где k - количество слов в словаре, длина которых отличается
        от длины проверяемого слова на 1 символ, n - длина проверяемого слова.

        Метод использует стек для итеративного обхода дерева в глубину. Каждый узел
        посещается только один раз. Обход останавливается, если длина текущего префикса в словаре
        становится больше длины проверяемого слова. Если длина слова из словаря отличается от длины
        проверяемого более чем на 1 символ, то алгоритм Дамерау-Левенштейна не применяется.

        Для каждого слова из словаря, длина которого отличается от длины проверяемого слова на 1 символ,
        выполняется проверка расстояния редактирования Дамерау-Левенштейна. В худшем случае
        выполнение этой проверки требует времени O(n^2), где n - длина проверяемого слова.

        Таким образом, общая временная сложность метода составляет O(k * n^2), где k - количество слов
        в словаре, длина которых отличается от длины проверяемого слова на 1 символ, n - длина проверяемого слова
        (в худшем случае).
        """
        word = word.lower()
        corrections = set()
        similar_length_words = self.__dictionary.get_words_with_similar_length(len(word))
        for candidate in similar_length_words:
            if self.__calculate_edit_distance(word, candidate):
                corrections.add(candidate)
        return list(corrections)


def corrections_handler(word, is_correct, corrections_array, stream=sys.stdout):
    if is_correct:
        stream.write(f"{word} - ok\n")
    else:
        if corrections_array:
            corrections_array.sort()
            stream.write(f"{word} -> {', '.join(corrections_array)}\n")
        else:
            stream.write(f"{word} -?\n")


def main():
    auto_correction = AutoCorrection()

    for i in range(int(next(sys.stdin).strip())):
        auto_correction.add_word_in_dictionary(next(sys.stdin).rstrip('\n'))

    for line in sys.stdin:
        line = line.rstrip('\n')
        if line:
            is_correct = auto_correction.correctness_check(line)
            corrections_array = auto_correction.get_corrections_array(line)
            corrections_handler(line, is_correct, corrections_array)


if __name__ == "__main__":
    main()
