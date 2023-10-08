class Graph:
    def __init__(self):
        self.dependencies = {}

    def add_dependency(self, dependency, libraries):
        self.dependencies[dependency] = libraries

    def find_paths(self, start, end, path=[], visited=set()):
        visited.add(start)
        path.append(start)

        if start == end:
            yield path

        for dependency in self.dependencies.get(start, []):
            if dependency not in visited:
                yield from self.find_paths(dependency, end, path, visited)

        visited.remove(start)
        path.pop()


def find_vulnerable_paths(vulnerable_libraries, project_dependencies):
    graph = Graph()

    # Читаем прямые зависимости проекта
    direct_dependencies = project_dependencies.split()

    # Читаем остальные зависимости
    while True:
        try:
            line = input().strip()
            dependency, libraries = line.split(' ', 1)
            libraries = libraries.split()
            graph.add_dependency(dependency, libraries)
        except EOFError:
            break

    # Находим пути до уязвимых библиотек
    paths = []
    for vulnerable_library in vulnerable_libraries.split():
        for direct_dependency in direct_dependencies:
            paths += list(graph.find_paths(direct_dependency, vulnerable_library))

    # Выводим результат
    for path in paths:
        print(' '.join(path))


def main():
    vulnerable_libraries = input().strip()
    project_dependencies = input().strip()

    find_vulnerable_paths(vulnerable_libraries, project_dependencies)


if __name__ == '__main__':
    main()
