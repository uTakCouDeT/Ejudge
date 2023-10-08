from collections import deque


class Graph:
    def __init__(self):
        self.dependencies = {}
        self.vulnerable_libraries = set()
        self.visited = set()

    def add_dependency(self, dependency, libraries):
        self.dependencies.update({dependency: libraries})
        self.dependencies[dependency] = libraries

    def add_vulnerable_library(self, library):
        self.vulnerable_libraries.add(library)

    def find_paths(self, start_dependency):
        queue = deque([(start_dependency, [start_dependency])])

        while queue:
            current_dependency, current_path = queue.popleft()

            if current_dependency in self.vulnerable_libraries:
                print(" ".join(current_path))

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

    except EOFError:
        return
    except KeyboardInterrupt:
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

        except EOFError:
            break
        except KeyboardInterrupt:
            break

    # Запуск BFS из каждой прямой зависимости
    for dependency in direct_dependencies:
        graph.find_paths(dependency)


if __name__ == '__main__':
    main()
