import sys


class library:
    def __init__(self):
        self.__vertexes = dict()
        self.__vuls = set()
        self.__directs = set()

    def parse_vuls(self, line: str):
        vuls = line.split(' ')
        for vul in vuls:
            self.__vuls.add(vul)

    def parse_directs(self, line: str):
        dirs = line.split(' ')
        for dir in dirs:
            self.__directs.add(dir)

    def parse_neighbours(self, line: str):
        input_list = line.split(' ')
        if not input_list[0] in self.__vertexes.keys():
            self.__vertexes[input_list[0]] = set(input_list[1:])
        else:
            self.__vertexes[input_list[0]].update(set(input_list[1:]))

    def find_ways(self, dir: str, visited: list, repeats: set):
        if dir in repeats:
            return

        visited.append(dir)
        repeats.add(dir)

        if dir in self.__vuls:
            print(' '.join(visited))

        if not dir in self.__vertexes.keys():
            visited.pop()
            repeats.remove(dir)
            return

        for neighbour in self.__vertexes[dir]:
            self.find_ways(neighbour, visited, repeats)

        visited.pop()
        repeats.remove(dir)

    def print_all_ways(self):
        for dir in self.__directs:
            visited = []
            repeats = set()
            self.find_ways(dir, visited, repeats)


def __main__():
    lib = library()

    try:
        line = input()
    except EOFError:
        return
    if not line:
        return
    lib.parse_vuls(line)

    try:
        line = input()
    except EOFError:
        return
    if not line:
        return
    lib.parse_directs(line)

    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line:
            continue
        lib.parse_neighbours(line)

    lib.print_all_ways()


if __name__ == "__main__":
    __main__()
