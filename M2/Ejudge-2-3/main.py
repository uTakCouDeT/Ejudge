from collections import defaultdict


class TrieNode:
    def __init__(self):
        self.children = defaultdict(TrieNode)
        self.word = None


class SpellingCorrector:
    def __init__(self):
        self.root = TrieNode()
        self.corrections = {}

    def insert_word(self, word):
        node = self.root
        for char in word:
            node = node.children[char]
        node.word = word

    def build_dictionary(self, dictionary):
        for word in dictionary:
            self.insert_word(word.lower())  # Приводим слова к нижнему регистру

    def get_corrections(self, word):
        self.corrections = {}
        self.find_corrections(self.root, word, '', 0)
        return self.corrections

    def find_corrections(self, node, word, current_word, errors):
        if errors > 1:
            return

        if not word:
            if node.word:
                self.corrections[current_word] = node.word
            if errors == 1:
                for child_char, child_node in node.children.items():
                    self.find_corrections(child_node, word, current_word + child_char, errors + 1)
        else:
            char = word[0]
            for child_char, child_node in node.children.items():
                if char == child_char:
                    self.find_corrections(child_node, word[1:], current_word + char, errors)
                else:
                    self.find_corrections(child_node, word[1:], current_word + child_char, errors + 1)


if __name__ == "__main__":
    n = int(input())
    dictionary = [input().strip().lower() for _ in range(n)]

    corrector = SpellingCorrector()
    corrector.build_dictionary(dictionary)

    while True:
        try:
            word = input().strip().lower()
            if not word:
                continue

            if word in dictionary:
                print(f"{word} - ok")
            else:
                corrections = corrector.get_corrections(word)
                if not corrections:
                    print(f"{word} -?")
                else:
                    sorted_corrections = sorted(corrections.values())
                    print(f"{word} -> {', '.join(sorted_corrections)}")
        except EOFError:
            break
