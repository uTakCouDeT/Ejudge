from collections import deque


class Graph:
    def __init__(self):
        self.dependencies = {}
        self.vulnerable_libraries = set()
        self.direct_dependencies = set()

    def add_dependency(self, dependency, libraries):
        if dependency in self.dependencies:
            self.dependencies[dependency].update(set(libraries))
        else:
            self.dependencies[dependency] = set(libraries)
        self.dependencies[dependency].discard(dependency)

    def add_vulnerable_library(self, library):
        self.vulnerable_libraries.add(library)

    def add_direct_dependency(self, library):
        self.direct_dependencies.add(library)

    def find_paths_from_vertex(self, vertex):
        queue = deque([(vertex, [])])

        while queue:
            current_vertex, current_path = queue.popleft()

            if current_vertex in self.vulnerable_libraries:
                for lib in current_path:
                    print(lib, end=' ')
                print(current_vertex)

            for child in self.dependencies.get(current_vertex, []):
                if child in current_path:  # Хотел использовать сет, для поиска за O(1)
                    continue  # Но его копирование на каждой итерации всё равно будет O(n)
                queue.append((child, current_path + [current_vertex]))

    def find_paths(self):
        for dependency in self.direct_dependencies:
            self.find_paths_from_vertex(dependency)


def main():
    graph = Graph()

    try:
        vulnerable_libraries = input().split()
        for library in vulnerable_libraries:
            graph.add_vulnerable_library(library)

        direct_dependencies = input().split()
        for library in direct_dependencies:
            graph.add_direct_dependency(library)

    except (EOFError, KeyboardInterrupt):
        return

    while True:
        try:
            line = input()
            if not line:
                continue

            data = line.split()
            dependency = data[0]
            dependent_libraries = data[1:]
            graph.add_dependency(dependency, dependent_libraries)

        except (EOFError, KeyboardInterrupt):
            break

    graph.find_paths()


if __name__ == '__main__':
    main()
