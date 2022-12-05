import json

from src.util.Util import update_route_json

SHORTEST_PATH_DIST = "shortDist"
SHORTEST_PATH_GAIN = "gainShort"
SHORTEST_PATH_DROP = "dropShort"
SHORTEST_PATH_ROUTE = "shortest_route"

ELEV_PATH_DIST = "elev_path_dist"
ELEV_PATH_GAIN = "elev_path_gain"
ELEV_PATH_DROP = "elev_path_drop"
ELEV_PATH_ROUTE = "elev_path_route"

ORIGIN = "start"
DESTINATION = "end"
FEATURE = "Feature"
LINESTRING = "LineString"
PROPERTIES = "properties"
GEOMETRY = "geometry"
TYPE = "type"
COORDINATES = "coordinates"
BOOL_POP = "bool_pop"


class View:
    def __init__(self):
        self.output_json = {}

    def update_notifier(self, shortest_route=None, elevation_route=None, starting_point=None, ending_point=None):
        self.output_json = {ELEV_PATH_ROUTE: update_route_json(elevation_route.get_path()),
                            SHORTEST_PATH_ROUTE: update_route_json(shortest_route.get_path()),
                            SHORTEST_PATH_DIST: shortest_route.get_distance(),
                            SHORTEST_PATH_GAIN: shortest_route.get_total_gain(),
                            SHORTEST_PATH_DROP: shortest_route.get_total_drop(),
                            ORIGIN: starting_point,
                            DESTINATION: ending_point,
                            ELEV_PATH_DIST: elevation_route.get_distance(),
                            ELEV_PATH_GAIN: elevation_route.get_total_gain(),
                            ELEV_PATH_DROP: elevation_route.get_total_drop()}

        if len(elevation_route.get_path()) == 0:
            self.output_json[BOOL_POP] = 1
        else:
            self.output_json[BOOL_POP] = 2

    def fetch_json_output(self):

        print('Sending output - ', self.output_json)
        return json.dumps(self.output_json)
