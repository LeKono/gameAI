import time

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

            # Iterate over every clean row and add the nodes to the graph.
            for j, column in enumerate(new_row):
                if int(column) == 0:
                    self.graph.add_node((i, j))

                    # Add edge to left node
                    if self.graph.has_node((i-1, j)):
                        self.graph.add_edge((i, j), (i-1, j))

                    # Add edge to above node
                    if self.graph.has_node((i, j-1)):
                        self.graph.add_edge((i, j), (i, j-1))

        map_data.close()

        return map_array

    def print_map(self, grid_map=None, symbols=False):
        """Prints out the array of the map.

        :param grid_map: Grid-Map that should be drawn.
        """
        grid_map = grid_map if grid_map is not None else self.m

        if not symbols:
            for r in grid_map:
                rp = ""
                for c in r:
                    if c == '0':
                        # Unvisited nodes
                        rp += " \033[1;37m\u25AE\033[0m "
                    elif c == '1':
                        # Unaccessible nodes
                        rp += " \u25AE "
                    elif c == 'X':
                        # Start node
                        rp += " \033[1;32m\u25AE\033[0m "
                    elif c == 'Y':
                        # Target node
                        rp += " \033[1;31m\u25AE\033[0m "
                    elif c == '-':
                        # Path node
                        rp += " \033[1;34m\u25AE\033[0m "
                    else:
                        # Visited node
                        rp += " \033[1;35m\u25AE\033[0m "
                print(rp)
        else:
            for row in grid_map:
                print(row)

    def get_dijkstra_path(self, source, target, use_nx=True, print_result=True, symbol_print=True):
        """Uses the NetworkX algorithm for dijkstra path.

        :param source: Source node coordinates (0,0) is bottom left.
        :param target: Target node coordinates (0,0) is bottom left.
        :param use_nx: States if NetworkX implementation of Dijkstra should be used.
        :param print_result: States if the resulting graph (including path should be printed).
        :param symbol_print: States if symbols (0,1, ...) or special characters should be printed.

        :returns: Shortest path
        """
        grid_map = dcp(self.m)
        shortest_path = None

        source = self.map_coordinates(source)
        target = self.map_coordinates(target)

        if use_nx:
            # Use the pre-implemented dijkstra algorithm that ships with NetworkX (no visited information)
            shortest_path = nx.dijkstra_path(self.graph, source, target)

        else:
            # Implementation of Dijkstra Algorithm
            weight = 1

            distance = {node: 100000 if node != source else 0 for node in self.graph.nodes}
            p = {source: -1}
            fringe = list(self.graph.nodes)
            closed = []

            while len(fringe) > 0:
                u = None
                for node in fringe:

                    if u is None:
                        u = node

                    elif distance[node] < distance[u]:
                        u = node

                closed.append(u)
                fringe.remove(u)
                grid_map[u[0]][u[1]] = 'V'

                for neighbor in self.graph.neighbors(u):
                    if neighbor not in closed:
                        if distance[neighbor] > distance[u] + weight:
                            distance[neighbor] = distance[u] + weight
                            p[neighbor] = u

            path = []
            t = target

            while p[t] != -1:
                path.append(t)
                t = p[t]

            path.append(source)
            path.reverse()
            shortest_path = path

        if shortest_path is not None:
            for x, y in shortest_path:
                grid_map[y][x] = '-'
                grid_map[source[1]][source[0]] = 'X'
                grid_map[target[1]][target[0]] = 'Y'

        if print_result:
            self.print_map(grid_map=grid_map, symbols=symbol_print)

        return shortest_path

    def get_astar_path(self, source, target, use_nx=True, print_result=True, symbol_print=True):
        """Uses the NetworkX algorithm for A* path. Using euclidean distance.

        :param source: Source node coordinates (0,0) is bottom left.
        :param target: Target node coordinates (0,0) is bottom left.
        :param use_nx: States if NetworkX implementation of Dijkstra should be used.
        :param print_result: States if the resulting graph (including path should be printed).
        :param symbol_print: States if symbols (0,1, ...) or special characters should be printed.

        :returns: Shortest path
        """
        grid_map = dcp(self.m)
        shortest_path = None
        weight = 1

        source = self.map_coordinates(source)
        target = self.map_coordinates(target)

        # Use euclidean distance calculation that ships with NetworkX
        euclidean_distance = nx.generators.geometric.euclidean

        if use_nx:
            # Use the pre-implemented A* algorithm that ships with NetworkX (no visited information)
            shortest_path = nx.astar_path(self.graph, source, target, euclidean_distance)

        else:
            # Implementation of A* Algorithm
            closed = []
            fringe = [source]
            p = {
                source: -1
            }
            g = {
                source: 0
            }
            f = {
                source: g[source] + euclidean_distance(source, target)
            }

            while len(fringe) > 0:
                u = None
                for node in fringe:
                    if u is None:
                        u = node
                    elif f[node] < f[u]:
                        u = node

                if u == target:
                    break

                closed.append(u)
                fringe.remove(u)
                grid_map[u[0]][u[1]] = 'V'

                for neighbor in self.graph.neighbors(u):
                    if neighbor not in closed:
                        newg = g[u] + weight
                        if neighbor not in fringe or g[neighbor] > newg:
                            g[neighbor] = newg
                            f[neighbor] = g[neighbor] + euclidean_distance(neighbor, target)
                            p[neighbor] = u
                            if neighbor not in fringe:
                                fringe.append(neighbor)

            path = []
            t = target

            while p[t] != -1:
                path.append(t)
                t = p[t]

            path.append(source)
            path.reverse()
            shortest_path = path

        if shortest_path is not None:
            for x, y in shortest_path:
                grid_map[y][x] = '-'
                grid_map[source[1]][source[0]] = 'X'
                grid_map[target[1]][target[0]] = 'Y'

        if print_result:
            self.print_map(grid_map=grid_map, symbols=symbol_print)

        return shortest_path

    def map_coordinates(self, coordinates):
        """Maps the coordinates such that (0,0) is bottom left of the graph.

        :param coordinates: Tuple of coordinates (x, y)
        """
        print(coordinates)
        return coordinates[0], len(self.m)-coordinates[1]-1
