class Node:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.value = None


class Trie:
    def __init__(self):
        self.root = Node()

    def add(self, word, value):
        node = self.root
        for char in word.lower():
            if char not in node.children:
                node.children[char] = Node()
            node = node.children[char]
        node.is_end_of_word = True
        node.value = value

    def search(self, word):
        node = self.root
        for char in word.lower():
            if char not in node.children:
                return None
            node = node.children[char]
        return node if node.is_end_of_word else None

    def get_words(self):
        # Метод для получения всех слов в Trie
        words = []
        self._get_words_helper(self.root, "", words)
        return words

    def _get_words_helper(self, node, current_word, words):
        if node.is_end_of_word:
            words.append(current_word)
        for char, next_node in node.children.items():
            self._get_words_helper(next_node, current_word + char, words)


class AutoCorrect:
    def __init__(self):
        self.trie = Trie()

    def add_word(self, word, value=None):
        self.trie.add(word, value)

    def correct_word(self, word):
        lower_word = word.lower()
        if self.trie.search(lower_word):
            return f"{word} - ok"

        corrections = []
        for dict_word in self.trie.get_words():
            if abs(len(lower_word) - len(dict_word)) <= 1:
                if dam_lev_distance(lower_word, dict_word) == 1:
                    corrections.append(dict_word)

        if corrections:
            corrections.sort()
            return f"{word} -> {', '.join(corrections)}"
        else:
            return f"{word} -?"


def dam_lev_distance(s1, s2):
    """
    Рассчитывает расстояние Дамерау-Левенштейна между двумя строками.
    """
    len_s1 = len(s1)
    len_s2 = len(s2)

    d = [[0 for _ in range(len_s2 + 1)] for _ in range(len_s1 + 1)]

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

    return d[len_s1][len_s2]


def main():
    ac = AutoCorrect()
    n = int(input().strip())
    for _ in range(n):
        word = input().strip().lower()
        ac.add_word(word)

    try:
        while True:
            word = input()
            if word:
                print(ac.correct_word(word))
    except EOFError:
        pass


if __name__ == "__main__":
    main()
