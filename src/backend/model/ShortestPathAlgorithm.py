from src.util.logger import get_logger
import networkx as nx
import osmnx as ox
from src.backend.model.RouteData import RouteData
from src.util.logger import get_logger
from src.util.Util import fetch_path_weight

ELEVATION_GAIN = "elevation_gain"
SHORTEST = "Shortest Route"
LOGGER = get_logger(__name__)

class ShortestPathAlgorithm:
    """
           This class is used to calculate the shortest route without considering the elevation gain
    """

    def __init__(self, graph):
        self.graph = graph
        self.source = None
        self.destination = None
        self.short_path = None
        self.short_distance = None

    def get_shortest_route(self, start, end):
        """
                This method is used to calculate the shortest path without considering any elevation gain like a normal map .
                Args:
                    source_point
                    destination_point

                Returns:
                    shortest_path route
        """

        graph = self.graph
        self.source, self.destination = None, None

        self.source, distance_1 = ox.get_nearest_node(graph, point=start, return_dist=True)
        self.destination, distance_2 = ox.get_nearest_node(graph, point=end, return_dist=True)

        # returns the shortest route from starting node to ending node based on distance
        self.short_path = nx.shortest_path(graph, source=self.source, target=self.destination,
                                           weight='length')

        LOGGER.info("Calculated the shortest path between source and destination with considering elevation")

        shortest_path_info = RouteData()
        shortest_path_info.set_start_node(self.source)
        shortest_path_info.set_end_node(self.destination)
        shortest_path_info.set_algo(SHORTEST)
        shortest_path_info.set_total_gain(fetch_path_weight(self.graph, self.short_path, ELEVATION_GAIN))
        shortest_path_info.set_total_drop(0)
        shortest_path_info.set_path([[graph.nodes[route_node]['x'], graph.nodes[route_node]['y']]
                                     for route_node in self.short_path])
        total_distance = sum(ox.utils_graph.get_route_edge_attributes(graph, self.short_path, 'length'))
        shortest_path_info.set_distance(total_distance)
        return shortest_path_info
