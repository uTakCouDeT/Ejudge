from collections import deque


class Graph:
    def __init__(self):
        self.dependencies = {}
        self.vulnerable_libraries = set()
        self.direct_dependencies = set()

    def add_dependency(self, dependency, libraries):
        for library in set(libraries):
            if library == dependency:
                continue
            if library in self.dependencies:
                self.dependencies[library].add(dependency)
            else:
                self.dependencies[library] = {dependency}

        # if dependency in self.dependencies:
        #     self.dependencies[dependency].update(set(libraries))
        # else:
        #     self.dependencies[dependency] = set(libraries)
        # self.dependencies[dependency].discard(dependency)

    def add_vulnerable_library(self, library):
        self.vulnerable_libraries.add(library)

    def add_direct_dependency(self, library):
        self.direct_dependencies.add(library)

    def find_paths_from_vertex(self, vertex):
        stack = deque()
        visited = set()
        path = []

        stack.append((vertex, iter(self.dependencies.get(vertex, set()))))

        while stack:
            current_vertex, children = stack[-1]

            try:
                child = next(children)

                for child in self.dependencies.get(current_vertex, set()):
                    if child not in visited:
                        path.append(child)
                        visited.add(child)

                        if child in self.direct_dependencies:
                            print(' '.join(reversed(path)))

                        stack.append((child, iter(self.dependencies.get(child, set()))))
            except StopIteration:
                # All children of current_vertex have been visited
                stack.pop()
                path.pop()
                visited.remove(current_vertex)

    # def find_paths_from_vertex(self, vertex, path, visited):
    #     path.append(vertex)
    #     visited.add(vertex)
    #
    #     if vertex in self.direct_dependencies:
    #         print(' '.join(reversed(path)))
    #
    #     if vertex not in self.dependencies.keys():
    #         path.pop()
    #         visited.remove(vertex)
    #         return
    #
    #     for child in self.dependencies[vertex]:
    #         if child in visited:
    #             continue
    #         self.find_paths_from_vertex(child, path, visited)
    #
    #     path.pop()
    #     visited.remove(vertex)

    def find_paths(self):
        if self.direct_dependencies:
            for library in self.vulnerable_libraries:
                self.find_paths_from_vertex(library)
                # self.find_paths_from_vertex(library, [], set())

        # if self.vulnerable_libraries:
        #     for dependency in self.direct_dependencies:
        #         self.find_paths_from_vertex(dependency)


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
            if len(data) >= 2:
                dependency = data[0]
                dependent_libraries = data[1:]
                graph.add_dependency(dependency, dependent_libraries)

        except (EOFError, KeyboardInterrupt):
            break

    graph.find_paths()


if __name__ == '__main__':
    main()
