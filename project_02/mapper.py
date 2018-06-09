import numpy as np
import networkx as nx

from copy import deepcopy as dcp

class Map:

    def __init__(self, map_file="simpleMap-1-20x20.txt"):
        """Takes a txt file and transforms it into a networkx graph.
        The file contains information about fields that are accessible (0) and
        'wall' information that are not accessible (1).

        :param map_file: Path to map file.
        """
        self.graph = nx.Graph()
        self.m = self.read_map(map_file)
        self.np_matrix = np.matrix(self.m)

    def read_map(self, map_file):
        """Translates information from a given map file into a list of lists.

        :param map_file: Path to map file.
        :return: map_array
        """
        map_data = open(map_file)

        map_array = []

        for i, row in enumerate(map_data.readlines()):
            new_row = row.strip().split(" ")
            map_array.append(new_row)
            for j, column in enumerate(new_row):
                self.graph.add_node((i, j))
                self.graph.nodes[(i, j)]['access'] = int(column)

                # Add edge to left node
                if self.graph.has_node((i-1, j)) and self.graph.nodes[(i-1, j)]['access'] == 0:
                    self.graph.add_edge((i, j), (i-1, j))

                # Add edge to above node
                if self.graph.has_node((i, j-1)) and self.graph.nodes[(i, j-1)]['access'] == 0:
                    self.graph.add_edge((i, j), (i, j-1))

        map_data.close()

        return map_array

    # Translate to networkX

    def show_map(self, grid_map=None):
        """Prints out the array of the map.

        :param grid_map: Grid-Map that should be drawn.
        """
        grid_map = grid_map if grid_map is not None else self.m
        for r in grid_map:
            rp = ""
            for c in r:
                if c == '0':
                    rp += " \033[1;37m\u25AE\033[0m "
                elif c == '1':
                    rp += " \u25AE "
                elif c == 'X':
                    rp += " \033[1;32m\u25AE\033[0m "
                elif c == 'Y':
                    rp += " \033[1;31m\u25AE\033[0m "
                elif c == '-':
                    rp += " \033[1;34m\u25AE\033[0m "
            print(rp)

    def get_dijkstra_path(self, source, target, use_nx=True, print_result=True):
        """Uses the NetworkX algorithm for dijkstra path."""
        grid_map = dcp(self.m)
        if use_nx:
            path = nx.dijkstra_path(self.graph, source, target)
            for x, y in path:
                grid_map[y][x] = '-'
            grid_map[source[1]][source[0]] = 'X'
            grid_map[target[1]][target[0]] = 'Y'

            if print_result:
                self.show_map(grid_map)

    def get_astar_path(self, source, target, use_nx=True, print_result=True):
        """Uses the NetworkX algorithm for A* path. Using euclidean distance."""
        grid_map = dcp(self.m)

        if use_nx:
            path = nx.astar_path(self.graph, source, target, nx.generators.geometric.euclidean)
            for x, y in path:
                grid_map[y][x] = '-'
            grid_map[source[1]][source[0]] = 'X'
            grid_map[target[1]][target[0]] = 'Y'

        if print_result:
            self.show_map(grid_map)

    def mapping(self):
        """Coordinate 0,0 bottom left"""
        pass
