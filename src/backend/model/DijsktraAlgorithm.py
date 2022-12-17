import logging
import networkx as nx
import osmnx as ox

import math
from src.backend.model.RouteData import RouteData
from src.util.Util import fetch_path_weight, astar_algorithm

from src.util.logger import get_logger

LOGGER = get_logger(__name__)
ELEVATION_GAIN = "elevation_gain"
ASTAR_ALGORITHM = "AStar"

class DijkstraAlgorithm:
    """
       This class is used to calculate the shortest route using the Dijkstra's Algorithm and also considering the elevation gain.
    """
    def __init__(self, graph, shortest_dist, limiting_percent, elevation_mode, start_node, end_node,
                 elevation_gain):
        self.graph = graph
        self.start_node = start_node
        self.end_node = end_node
        self.elevation_route = None
        self.shortest_dist = shortest_dist
        self.limiting_percent = limiting_percent
        self.elevation_mode = elevation_mode
        self.scale = 100
        self.elevation_distance = None
        self.elevation_gain = elevation_gain
    def get_shortest_route(self):
        """
                This method takes into consideration the weights and elevation gain into account and calculates the shortest route.

                Returns:
                ShortestPath route
        """
        graph = self.graph

        self.elevation_route = nx.shortest_path(graph, source=self.start_node, target=self.end_node,
                                                weight='length')

        # calculating the elevation gain and distance based on user selected min or max gain
        if self.elevation_mode == min:
            while self.scale < 10000:
                # Dijkstra is a special case of AStar algorithm when the heuristic is set to None
                elevation_route = astar_algorithm(graph,
                                                  source=self.start_node,
                                                  target=self.end_node,
                                                  heuristic=None,
                                                  weight=lambda u, v, d:
                                                  math.exp(1 * d[0]['length'] * (
                                                          d[0]['grade'] + d[0]['grade_abs']) / 2)
                                                  + math.exp(1 / self.scale * (d[0]['length'])))

                elevation_distance = sum(ox.utils_graph.get_route_edge_attributes(graph, elevation_route, 'length'))
                elevation_gain_1 = fetch_path_weight(self.graph, elevation_route, ELEVATION_GAIN)
                if elevation_distance <= (1 + self.limiting_percent) * self.shortest_dist and \
                        1 * elevation_gain_1 <= 1 * self.elevation_gain:
                    self.elevation_route = elevation_route
                    self.elevation_gain = elevation_gain_1
                self.scale *= 5

        else:
            while self.scale < 10000:
                # Dijkstra is a special case of AStar algorithm when the heuristic is set to None
                elevation_route = astar_algorithm(graph,
                                                  source=self.start_node,
                                                  target=self.end_node,
                                                  heuristic=None,
                                                  weight=lambda u, v, d:
                                                  math.exp(-1 * d[0]['length'] * (
                                                          d[0]['grade'] + d[0]['grade_abs']) / 2)
                                                  + math.exp(1 / self.scale * (d[0]['length'])))

                elevation_distance = sum(ox.utils_graph.get_route_edge_attributes(graph, elevation_route, 'length'))
                elevation_gain_1 = fetch_path_weight(self.graph, elevation_route, ELEVATION_GAIN)
                if elevation_distance <= (1 + self.limiting_percent) * self.shortest_dist and \
                        -1 * elevation_gain_1 <= -1 * self.elevation_gain:
                    self.elevation_route = elevation_route
                    self.elevation_gain = elevation_gain_1
                self.scale *= 5

        shortest_path = RouteData()
        shortest_path.set_algo(ASTAR_ALGORITHM)
        shortest_path.set_total_gain(fetch_path_weight(self.graph, self.elevation_route, ELEVATION_GAIN))
        shortest_path.set_total_drop(0)
        shortest_path.set_path([[graph.nodes[route_node]['x'], graph.nodes[route_node]['y']]
                                for route_node in self.elevation_route])
        shortest_path.set_distance(
            sum(ox.utils_graph.get_route_edge_attributes(graph, self.elevation_route, 'length')))

        LOGGER.info("Returning the shortest path using the Astar Algorithm")
        LOGGER.info(f"shortest_path: {shortest_path}")
        return shortest_path

