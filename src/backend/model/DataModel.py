from src.backend.model.NetworkGenerator import NetworkGenerator
from src.backend.model.ShortestPathAlgorithm import ShortestPathAlgorithm
from src.util.Util import coordinates_to_address
from src.util.logger import get_logger

LOGGER = get_logger(__name__)


class DataModel:
    """
        This class initializes critical parameters such the graph,the algorithm,the path_limit  etc.It contains methods to register the
        observer,set the algorithm,set the algorithm object,print the route information etc and also it notifies the observers.
    """
    def __init__(self):
        self.map_api_key = None
        self.graph = None
        self.shortest_route_obj = None
        self.shortest_path_info = None
        self.elevation_route_obj = None
        self.elevation_path_info = None
        self.observer = None
        self.algorithm = None
        self.algorithm_obj = None
        self.limiting_percent = None
        self.mode_of_elevation = None

    def register_observer(self, observer):
        self.observer = observer

    def set_algorithm(self, algorithm):
        self.algorithm = algorithm

    def get_mapbox_api(self):
        return self.map_api_key

    def set_mapbox_api(self, api_key):
        self.map_api_key = api_key

    def set_algorithm_obj(self):
        self.algorithm_obj = self.algorithm(self.graph,
                                            self.shortest_path_info.get_distance(),
                                            self.limiting_percent,
                                            self.mode_of_elevation,
                                            self.shortest_path_info.get_start_node(),
                                            self.shortest_path_info.get_end_node(),
                                            self.shortest_path_info.get_total_gain())

    def set_shortest_route_obj(self, start_coordinate, end_coordinate):
        self.graph = NetworkGenerator().generate_graph_to_end_point(end_coordinate)
        self.shortest_route_obj = ShortestPathAlgorithm(self.graph)
        self.shortest_path_info = self.shortest_route_obj.get_shortest_route(start_coordinate, end_coordinate)

    def get_algorithm_obj(self):
        return self.algorithm_obj

    def print_route_details(self, route):
        LOGGER.info("#")
        LOGGER.info(f"Algorithm Strategy: {route.get_algo()}")
        LOGGER.info(f"Total Distance: {str(route.get_distance())}")
        LOGGER.info(f"Elevation Gain: {str(route.get_total_gain())}")
        LOGGER.info("#")

    def generate_paths(self, origin, destination, limiting_percent, mode_of_elevation):
        self.set_shortest_route_obj(origin, destination)
        self.print_route_details(self.shortest_path_info)
        if limiting_percent == 0:
            self.observer.update_notifier(self.shortest_path_info,
                                          self.shortest_path_info,
                                          coordinates_to_address(origin),
                                          coordinates_to_address(destination))
            return

        self.limiting_percent = limiting_percent / 100.0
        self.mode_of_elevation = mode_of_elevation

        self.set_algorithm_obj()
        LOGGER.info(f"Algorithm information: {self.get_algorithm_obj()}")
        self.elevation_path_info = self.get_algorithm_obj().get_shortest_route()

        self.print_route_details(self.elevation_path_info)

        self.observer.update_notifier(self.shortest_path_info,
                                      self.elevation_path_info,
                                      coordinates_to_address(origin),
                                      coordinates_to_address(destination))
