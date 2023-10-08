from collections import deque


class Graph:
    def __init__(self):
        self.dependencies = {}
        self.vulnerable_libraries = set()
        self.direct_dependencies = set()

    def add_dependency(self, dependency, libraries):
        if dependency not in self.dependencies:
            self.dependencies[dependency] = libraries

    def add_vulnerable_library(self, library):
        self.vulnerable_libraries.add(library)

    def add_direct_dependency(self, library):
        self.direct_dependencies.add(library)

    def BFS_find_paths(self):
        for dependency in self.direct_dependencies:
            queue = deque([(dependency, [dependency])])
            visited_paths = set()  # Хранит уже посещенные пути

            while queue:
                current_dependency, current_path = queue.popleft()

                if current_dependency in self.vulnerable_libraries:
                    path_str = " ".join(current_path)
                    if path_str not in visited_paths:
                        visited_paths.add(path_str)
                        print(path_str)

                if current_dependency in self.dependencies:
                    for dependency in self.dependencies[current_dependency]:
                        if dependency not in current_path:
                            new_path = current_path + [dependency]
                            queue.append((dependency, new_path))


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
            if dependency not in dependent_libraries:
                graph.add_dependency(dependency, dependent_libraries)

        except (EOFError, KeyboardInterrupt):
            break

    graph.BFS_find_paths()


if __name__ == '__main__':
    main()
