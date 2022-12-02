import os
import pickle as pkl
import osmnx as ox
from haversine import haversine, Unit
from src.util.logger import get_logger

LOGGER = get_logger(__name__)

DESTINATION_FROM_DISTANCE = 'dist_from_dest'

class NetworkGenerator:

    def __init__(self):
        self.graph = None
        self.google_map_api_key = "AIzaSyBmQKnCAXug20yc7pj4ZO_kLbZuPLAkwxs"
        # Centre point is the location of UMass Amherst
        self.middle_point = (42.3867637, -72.5322402)
        self.location_on_offline_map = "../../openstreetmapoffline.p"

    def download_map(self):
        # This method fetched the map from OSMNX and adds elevation attributes
        LOGGER.info("Downloading the Map from OSMNX successfully")
        self.graph = ox.graph_from_point(self.middle_point, dist=15000, network_type='walk')
        # After creating the graph, add the elevation attributes
        self.graph = ox.add_node_elevations(self.graph, api_key=self.google_map_api_key)

        # Saving the graph which had been created.
        pkl.dump(self.graph, open(self.location_on_offline_map, "wb"))
        LOGGER.info("Saved the graph successfully")

    def generate_graph_to_end_point(self, dest_node):
        # Updates the graph with distance from end point and returns it.
        print("Trying to load offline map....", self.location_on_offline_map)
        try:
            self.graph = pkl.load(open("src/openstreetmapoffline.p", "rb"))
            LOGGER.info("Offline map successfully loaded 1!")
            self.graph = ox.add_edge_grades(self.graph)
        except:
            if os.path.exists("../../openstreetmapoffline.p"):
                self.graph = pkl.load(open(self.location_on_offline_map, "rb"))
                LOGGER.info("Offline map successfully loaded 2!")
                self.graph = ox.add_edge_grades(self.graph)
            else:
                LOGGER.info("Failed to download offline map")
                self.download_map()

        # Graph is updated with Distance from all nodes in the graph to the final destination
        end_node = self.graph.nodes[ox.get_nearest_node(self.graph, point=dest_node)]
        for node, data in self.graph.nodes(data=True):
            end_x = end_node['x']
            end_y = end_node['y']
            node_x = self.graph.nodes[node]['x']
            node_y = self.graph.nodes[node]['y']
            data[DESTINATION_FROM_DISTANCE] = haversine((end_x, end_y), (node_x, node_y), unit=Unit.METERS)
        return self.graph
