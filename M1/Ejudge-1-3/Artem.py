import sys


# class Graph:
#     def __init__(self, count_of_vertices):
#         self.size_graph = count_of_vertices
#         self.graph = dict()
#
#     def add_edge(self, u, v):
#         if u in self.graph:
#             self.graph[u].append(v)
#         else:
#             self.graph[u] = [v]


class Library:
    def __init__(self, sensitive_lib, depend_lib, graph: dict):
        self.sensitive = sensitive_lib
        self.start_points = depend_lib
        self.all_ways = graph

    def search_from_start_to_end(self, end, path: list, visited: list):
        # print(f'----{end}-----')
        # print(path)
        if end in list(self.all_ways.keys()):
            path.append(end)
            visited.append(end)
            if end in self.start_points:
                print(' '.join(path[::-1]))
            depend_libs = self.all_ways[end]
            for lib in depend_libs:
                if lib not in visited:
                    self.search_from_start_to_end(lib, path, visited)
                else:
                    continue
        else:
            if end in self.start_points:
                path.append(end)
                visited.append(end)
                print(' '.join(path[::-1]))
        if end in path:
            path.pop()
            visited.pop()

    def search_all_way(self):
        for end in self.sensitive:
            if end not in list(self.all_ways.keys()):
                if end in self.start_points:
                    print(end)
                continue
            path = []
            visited = []
            self.search_from_start_to_end(end, path, visited)


def main():
    sensitive_lib = list(set(filter(None, sys.stdin.readline()[:-1].split(' '))))
    dependent_lib = list(set(filter(None, sys.stdin.readline()[:-1].split(' '))))
    raw_graph = sys.stdin.readlines()
    hash_table = dict()
    for line in raw_graph:
        tmp_list_ckecker = []
        if not line:
            exit(0)
        temp_line = list(filter(None, line[:-1].split(' ')))
        if not temp_line:
            continue
        tmp_list_ckecker.append(temp_line[0])
        for lib_index in range(1, len(temp_line)):
            if temp_line[lib_index] not in tmp_list_ckecker:
                tmp_list_ckecker.append(temp_line[lib_index])
                if temp_line[lib_index] not in list(hash_table.keys()):
                    hash_table[temp_line[lib_index]] = [temp_line[0]]
                else:
                    hash_table[temp_line[lib_index]].append(temp_line[0])
            else:
                continue
    print(hash_table)
    library = Library(sensitive_lib, dependent_lib, hash_table)
    if sensitive_lib or dependent_lib:
        library.search_all_way()


if __name__ == "__main__":
    main()

"""
{'console': ['sl4j', 'everything'], 'time': ['sl4j', 'site', 'developer', 'everything'], 'log4j': ['sl4j'], 'junit': ['jupiter', 'everything'], 'void': ['nothing', 'light', 'darkness'], 'developer': ['site', 'everything'], 'coffee': ['site', 'everything'], 'libpoe-component-irc-perl': ['kgb-bot'], 'libpoe-component-server-soap-perl': ['kgb-bot'], 'libpoe-perl': ['kgb-bot'], 'libproc-pid-file-perl': ['kgb-bot'], 'libschedule-ratelimiter-perl': ['kgb-bot'], 'libyaml-perl': ['kgb-bot'], 'lsb-base': ['kgb-bot'], 'perl': ['kgb-bot'], 'food': ['developer', 'everything'], 'water': ['developer', 'everything'], 'sleep': ['developer', 'everything'], 'chocolate': ['developer', 'everything'], 'friends': ['developer', 'everything'], 'wordpress': ['developer', 'everything'], 'love': ['developer', 'everything'], 'english': ['developer', 'everything'], 'fizraToBeStrong': ['developer', 'everything'], 'computer': ['developer', 'everything'], 'stickers': ['developer', 'everything'], 'java': ['junit', 'everything'], 'ant': ['junit', 'everything'], 'nothing': ['somelib'], 'nobody': ['spanishInquisition'], 'everything': ['void'], 'sl4j': ['everything'], 'jupiter': ['everything'], 'site': ['everything'], 'kgb-bot': ['everything']}
hacked
somelib nothing void everything kgb-bot
site developer wordpress
somelib nothing void everything site developer wordpress
somelib nothing void everything developer wordpress
somelib nothing void everything wordpress
sl4j log4j
somelib nothing void everything sl4j log4j
jupiter junit ant
somelib nothing void everything jupiter junit ant
somelib nothing void everything junit ant
somelib nothing void everything ant
"""

"""
{'sl4j': ['console', 'time', 'log4j'], 'jupiter': ['junit'], 'nothing': ['void'], 'site': ['developer', 'time', 'coffee'], 'kgb-bot': ['libpoe-component-irc-perl', 'libpoe-component-server-soap-perl', 'libpoe-perl', 'libproc-pid-file-perl', 'libschedule-ratelimiter-perl', 'libyaml-perl', 'lsb-base', 'perl'], 'developer': ['food', 'water', 'sleep', 'chocolate', 'friends', 'wordpress', 'love', 'time', 'english', 'fizraToBeStrong', 'computer', 'stickers'], 'junit': ['java', 'ant'], 'somelib': ['nothing'], 'light': ['void'], 'darkness': ['void'], 'spanishInquisition': ['nobody'], 'void': ['everything'], 'everything': ['sl4j', 'console', 'jupiter', 'junit', 'site', 'developer', 'time', 'coffee', 'kgb-bot', 'food', 'water', 'sleep', 'chocolate', 'friends', 'wordpress', 'love', 'time', 'english', 'fizraToBeStrong', 'computer', 'stickers', 'java', 'ant']}
jupiter junit ant
sl4j log4j
somelib nothing void everything kgb-bot
somelib nothing void everything wordpress
somelib nothing void everything ant
somelib nothing void everything sl4j log4j
somelib nothing void everything junit ant
somelib nothing void everything developer wordpress
somelib nothing void everything jupiter junit ant
somelib nothing void everything site developer wordpress
site developer wordpress
hacked
"""
