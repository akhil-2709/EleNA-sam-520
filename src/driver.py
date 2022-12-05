import json

import googlemaps
from flask import Flask, request, render_template
from backend.controller.AstarController import *
from backend.controller.DijkstraController import *
from backend.model.DataModel import *
from src.view.View import View

ACCESS_KEY = 'pk.eyJ1IjoibXRhayIsImEiOiJja25wNmdyMTMxYm9tMm5wZTlha2lhcmFnIn0.JsFh89MfCIDr32o-1OHmdA'
GOOGLE_MAP_API_KEY = 'AIzaSyBmQKnCAXug20yc7pj4ZO_kLbZuPLAkwxs'
gmaps = googlemaps.Client(key=GOOGLE_MAP_API_KEY)
static_folder = "./view/static"
template_folder = "./view/templates"
static_url_path = ''
app = Flask(__name__, static_folder=static_folder, template_folder=template_folder, static_url_path=static_url_path)
app.config.from_object(__name__)
app.config.from_envvar('APP_CONFIG_FILE', silent=True)

SOURCE_CORDINATES = 'source_coordinates'
DESTINATION_CORDINATES = 'destination_coordinates'
ALGORITHM = 'algo'
MIN_MAX = 'minimum_maximum'
LIMITING_PERCENT = 'limiting_percent'
LATITUDE = 'lat'
LONGITUDE = 'lng'
MANUAL_SOURCE_ADDRESS = 'manual_source_address'
MANUAL_DESTINATION_ADDRESS = 'manual_destination_address'
DIJKSTRA_ALGO = 'DijkstraAlgorithm'

@app.route('/view')
def client():
    return render_template(
        'view.html',
        ACCESS_KEY=ACCESS_KEY
    )


def get_controller_obj(algo):
    if algo == "DijkstraAlgorithm":
        controller = DijkstraController()
    else:
        controller = AstarController()
    return controller


@app.route('/path_via_pointers', methods=['POST'])
def get_route():
    json_output = request.get_json(force=True)
    LOGGER.info(f"Request: {json_output}")
    source_coords = json.loads(json_output[SOURCE_CORDINATES])
    destination_coords = json.loads(json_output[DESTINATION_CORDINATES])
    source_point = (source_coords[LATITUDE], source_coords[LONGITUDE])
    destination_point = (destination_coords[LATITUDE], destination_coords[LONGITUDE])
    path_limit = float(json_output[LIMITING_PERCENT])
    mode_of_elevation = json_output[MIN_MAX]
    algorithm = json_output[ALGORITHM]
    data_model = DataModel()
    view = View()
    data_model.register_observer(view)
    controller = get_controller_obj("DIJKSTRA_ALGO")
    controller.set_data_model(data_model)
    controller.set_source_point(source_point)
    controller.set_destination_point(destination_point)
    controller.set_limiting_percent(path_limit)
    controller.set_mode_of_elevation(mode_of_elevation)
    controller.manipulate_data_model()
    return view.fetch_json_output()


def convert_address_to_coordinates(location_name):
    geocode_result = gmaps.geocode(location_name)
    return geocode_result[0]['geometry']['location'][LATITUDE], geocode_result[0]['geometry']['location'][LONGITUDE]


@app.route('/path_via_address', methods=['POST'])
def get_routes_via_address():
    json_output = request.get_json(force=True)
    LOGGER.info(f"Request: {json_output}")
    start_address = json_output[MANUAL_SOURCE_ADDRESS]

    LOGGER.info("HELLO= ====================")
    end_address = json_output[MANUAL_DESTINATION_ADDRESS]

    geocode_result = gmaps.geocode(start_address)
    print("geocode result",geocode_result)
    source_point = geocode_result[0]['geometry']['location'][LATITUDE], geocode_result[0]['geometry']['location'][LONGITUDE]
    geocode_result = gmaps.geocode(end_address)
    destination_point = geocode_result[0]['geometry']['location'][LATITUDE], geocode_result[0]['geometry']['location'][LONGITUDE]
    LOGGER.info(f"Souce: {source_point}")
    LOGGER.info(f"Destination: {destination_point}")

    path_limit = float(json_output[LIMITING_PERCENT])
    elevation_strategy = json_output[MIN_MAX]
    algorithm = json_output[ALGORITHM]
    data_model = DataModel()
    view = View()
    data_model.register_observer(view)
    controller = get_controller_obj("DIJKSTRA_ALGO")
    controller.set_data_model(data_model)
    controller.set_limiting_percent(path_limit)
    controller.set_mode_of_elevation(elevation_strategy)
    controller.set_source_point(source_point)
    controller.set_destination_point(destination_point)
    controller.manipulate_data_model()
    output = view.fetch_json_output()
    return output
