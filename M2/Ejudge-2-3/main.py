import sys


class Node:
    def __init__(self):
        self.children = {}  # ключ - следующая буква, значение ссылка на её ноду
        self.is_end_of_word = False


class Trie:
    def __init__(self):
        self.__root = Node()  # корень пустое слово, по этому значение хранить не нужно

    def add(self, word):
        node = self.__root
        for char in word.lower():
            if char not in node.children:
                node.children[char] = Node()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word):
        node = self.__root
        for char in word.lower():
            if char not in node.children:
                return None
            node = node.children[char]
        return node if node.is_end_of_word else None

    def get_words(self):
        words = []
        stack = [(self.__root, "")]
        while stack:
            current_node, word = stack.pop()
            if current_node.is_end_of_word:
                words.append(word)
            for char, next_node in current_node.children.items():
                stack.append((next_node, word + char))
        return words


class AutoCorrect:
    def __init__(self):
        self.__trie = Trie()

    def add_word(self, word):
        self.__trie.add(word)

    def correct_word(self, word):
        lower_word = word.lower()
        if self.__trie.search(lower_word):
            return f"{word} - ok"

        corrections = []
        for dict_word in self.__trie.get_words():
            if self.__is_dam_lev_distance(lower_word, dict_word):
                corrections.append(dict_word)

        if corrections:
            corrections.sort()
            return f"{word} -> {', '.join(corrections)}"
        else:
            return f"{word} -?"

    @staticmethod
    def __is_dam_lev_distance(s1, s2):
        len_s1 = len(s1)
        len_s2 = len(s2)

        # Раннее прерывание, если разница в длине больше 1
        if abs(len_s1 - len_s2) > 1:
            return False

        d = [[0] * (len_s2 + 1) for _ in range(len_s1 + 1)]

        for i in range(len_s1 + 1):
            d[i][0] = i
        for j in range(len_s2 + 1):
            d[0][j] = j

        for i in range(1, len_s1 + 1):
            for j in range(1, len_s2 + 1):
                cost = 0 if s1[i - 1] == s2[j - 1] else 1
                d[i][j] = min(d[i - 1][j] + 1,  # удаление
                              d[i][j - 1] + 1,  # вставка
                              d[i - 1][j - 1] + cost)  # замена

                if i > 1 and j > 1 and s1[i - 1] == s2[j - 2] and s1[i - 2] == s2[j - 1]:
                    d[i][j] = min(d[i][j], d[i - 2][j - 2] + cost)  # транспозиция

            # Раннее прерывание, если минимальное расстояние уже больше 1
            if min(d[i]) > 1:
                return False

        return True if d[len_s1][len_s2] == 1 else False

    # @staticmethod
    # def __dam_lev_distance(s1, s2):
    #
    #     len_s1 = len(s1)
    #     len_s2 = len(s2)
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
