import sys


class Node:
    def __init__(self):
        self.children = {}
        self.end_of_word = False


class Trie:
    def __init__(self):
        self.__root = Node()

    def add(self, word):
        word = word.lower()
        node = self.__root
        i = 0
        while i < len(word):
            match = False
            for child in node.children.keys():
                common_prefix_length = self.__common_prefix_length(word[i:], child)

                if common_prefix_length > 0:
                    match = True

                    if common_prefix_length == len(child):
                        node = node.children[child]
                    else:
                        existing_node = node.children[child]
                        new_child = child[:common_prefix_length]
                        new_node = Node()

                        node.children[new_child] = new_node
                        new_node.children[child[common_prefix_length:]] = existing_node
                        del node.children[child]

                        node = new_node

                    i += common_prefix_length
                    break

            if not match:
                new_node = Node()
                new_node.end_of_word = True
                node.children[word[i:]] = new_node
                break
            elif i == len(word):
                node.end_of_word = True

    @staticmethod
    def __common_prefix_length(s1, s2):
        min_length = min(len(s1), len(s2))
        for i in range(min_length):
            if s1[i] != s2[i]:
                return i
        return min_length

    def search(self, word):
        word = word.lower()
        node = self.__root
        i = 0
        while i < len(word):
            found = False
            for child in node.children.keys():
                if word[i:].startswith(child):
                    found = True
                    node = node.children[child]
                    i += len(child)
                    break
            if not found:
                return False
        return node.end_of_word

    def get_corrections(self, word):
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
