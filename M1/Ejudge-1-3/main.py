import sys


def find_vulnerable_paths(vulnerable_libs, direct_deps, dependencies):
    def dfs(node, path):
        if node in vulnerable_libs:
            paths.append(path)

        visited.add(node)

        for dep in dependencies.get(node, []):
            if dep not in visited:
                dfs(dep, path + [dep])

    paths = []
    visited = set()

    for direct_dep in direct_deps:
        dfs(direct_dep, [direct_dep])

    return paths


if __name__ == "__main__":
    vulnerable_libs = input().strip().split()
    direct_deps = input().strip().split()
    dependencies = {}

    for line in sys.stdin:
        parts = line.strip().split()
        dependency = parts[0]
        libs = parts[1:]

        dependencies[dependency] = libs

    paths = find_vulnerable_paths(vulnerable_libs, direct_deps, dependencies)

    for path in paths:
        print(" ".join(path))
