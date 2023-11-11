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
        self.children = {}
        self.is_word = False


# Сначала сделал через обычное префиксное дерево, а потом перечитал условие и пошел его "сжимать"...
class RadixTree:
    def __init__(self):
        self.__root = Node()

    def add(self, word):
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
        stack = [(self.__root, "")]
        corrections = []

        while stack:
            node, prefix = stack.pop()
            if node.is_word:
                if self.__is_dam_lev_distance_one(word.lower(), prefix):
                    corrections.append(prefix)

            for child_suffix, child_node in node.children.items():
                stack.append((child_node, prefix + child_suffix))

        return corrections

    @staticmethod
    def __is_dam_lev_distance_one(s1, s2):
        len_s1, len_s2 = len(s1), len(s2)

        if abs(len_s1 - len_s2) > 1:
            return False

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
