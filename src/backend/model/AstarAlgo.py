import networkx as nx
import osmnx as ox
import math
from src.backend.model.RouteData import RouteData
from src.util.Util import fetch_path_weight, astar_algorithm
from src.util.logger import get_logger

LOGGER = get_logger(__name__)
ELEVATION_GAIN = "elevation_gain"
ASTAR_ALGORITHM = "AStar"
DISTANCE_FROM_DESTINATION = 'dist_from_dest'

class AstarAlgo:
    def __init__(self, graph, shortest_dist, limiting_percent, mode_of_elevation, start_node, end_node,
                 elevation_gain):
        self.graph = graph
        self.start_node = start_node
        self.end_node = end_node
        self.elevation_path = None
        self.shortest_dist = shortest_dist
        self.limiting_percent = limiting_percent
        self.mode_of_elevation = mode_of_elevation
        self.scale = 100
        self.elevation_distance = None
        self.elevation_gain = elevation_gain
    def dist(self, a, b):
        # This method calculates the distance from the nearest node to the location
        return self.graph.nodes[a][DISTANCE_FROM_DESTINATION] * 1 / self.scale

    def get_shortest_route(self):
        graph = self.graph
        self.elevation_path = nx.shortest_path(graph, source=self.start_node, target=self.end_node,
                                               weight='length')

        # calculating the elevation gain and distance based on user selected min or max gain
        if self.mode_of_elevation == min:
            while self.scale < 10000:
                elevation_path = astar_algorithm(graph,
                                                 source=self.start_node,
                                                 target=self.end_node,
                                                 heuristic=self.dist,
                                                 weight=lambda x, y, d:
                                                 math.exp(1 * d[0]['length'] * (
                                                         d[0]['grade'] + d[0]['grade_abs']) / 2)
                                                 + math.exp(1 / self.scale * (d[0]['length'])))

                elevation_distance = sum(ox.utils_graph.get_route_edge_attributes(graph, elevation_path, 'length'))
                elevation_gain = fetch_path_weight(self.graph, elevation_path, ELEVATION_GAIN)
                if elevation_distance <= (1 + self.limiting_percent) * self.shortest_dist and \
                        1 * elevation_gain <= 1 * self.shortest_path_elevation_gain:
                    self.elevation_path = elevation_path
                    self.shortest_path_elevation_gain = elevation_gain
                self.scale *= 5

        else:
            while self.scale < 10000:
                elevation_path = astar_algorithm(graph,
                                                 source=self.start_node,
                                                 target=self.end_node,
                                                 heuristic=self.dist,
                                                 weight=lambda x, y, d:
                                                 math.exp(-1 * d[0]['length'] * (
                                                         d[0]['grade'] + d[0]['grade_abs']) / 2)
                                                 + math.exp(1 / self.scale * (d[0]['length'])))

                elevation_distance = sum(ox.utils_graph.get_route_edge_attributes(graph, elevation_path, 'length'))
                elevation_gain = fetch_path_weight(self.graph, elevation_path, ELEVATION_GAIN)
                if elevation_distance <= (-1 + self.limiting_percent) * self.shortest_dist and \
                        -1 * elevation_gain <= -1 * self.elevation_gain:
                    self.elevation_path = elevation_path
                    self.elevation_gain = elevation_gain
                self.scale *= 5

        shortest_path = RouteData()
        shortest_path.set_algo(ASTAR_ALGORITHM)
        shortest_path.set_total_gain(fetch_path_weight(self.graph, self.elevation_path, ELEVATION_GAIN))
        shortest_path.set_total_drop(0)
        shortest_path.set_path([[graph.nodes[route_node]['x'], graph.nodes[route_node]['y']]
                                for route_node in self.elevation_path])

        LOGGER.info("Returning the shortest path using the Astar Algorithm")
        LOGGER.info(f"shortest_path: {shortest_path}")
        return shortest_path
