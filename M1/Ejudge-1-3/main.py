class Graph:
    def __init__(self):
        self.dependencies = {}
        self.vulnerable_libraries = set()
        self.visited = set()

    def add_dependency(self, dependency, libraries):
        self.dependencies[dependency] = libraries

    def add_vulnerable_library(self, library):
        self.vulnerable_libraries.add(library)

    def find_paths(self, start_dependency, current_path):
        current_path.append(start_dependency)

        if start_dependency in self.vulnerable_libraries:
            print(" ".join(current_path))

        if start_dependency in self.dependencies:
            for dependency in self.dependencies[start_dependency]:
                if dependency not in current_path:
                    self.find_paths(dependency, current_path)

        current_path.pop()


if __name__ == "__main__":
    graph = Graph()

    # Чтение входных данных
    vulnerable_libraries = input().split()
    dependencies = input().split()

    while True:
        try:
            line = input().split()
            dependency = line[0]
            libraries = line[1:]
            graph.add_dependency(dependency, libraries)
        except EOFError:
            break

    for library in vulnerable_libraries:
        graph.add_vulnerable_library(library)

    # Запуск DFS из каждой прямой зависимости
    for dependency in dependencies:
        if dependency not in graph.visited:
            graph.find_paths(dependency, [])
