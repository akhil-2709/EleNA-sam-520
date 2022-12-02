from geopy.geocoders import Nominatim
import networkx as nx
from heapq import heappush, heappop
from itertools import count
from networkx.algorithms.shortest_paths.weighted import _weight_function

NORMAL = "normal"
ELEVATION_GAIN = "elevation_gain"
SHORTEST = "Shortest Route"

WEIGHT = 'weight'
ELEVATION = 'elevation'
LENGTH = 'length'

PROPERTIES = "properties"
GEOMETRY = "geometry"
TYPE = "type"
COORDINATES = "coordinates"
FEATURE = "Feature"
LINESTRING = "LineString"


def astar_algorithm(graph, source, target, heuristic, weight):
    if source not in graph or target not in graph:
        print("Graph doesn't contain either source or destination")

    if heuristic is None:
        def heuristic(u, v):
            return 0
    enqueue_dict = {}
    visited_dict = {}
    weight = _weight_function(graph, weight)
    c = count()
    queue = [(0, next(c), source, 0, None)]
    while queue:
        _, __, curr_node, distance, parent = heappop(queue)
        if curr_node == target:
            path = [curr_node]
            node = parent
            while node is not None:
                path.append(node)
                node = visited_dict[node]
            path = path[::-1]
            return path
        if curr_node in visited_dict:
            if visited_dict[curr_node] is None:
                continue
            queue_cost, h = enqueue_dict[curr_node]
            if queue_cost < distance:
                continue
        visited_dict[curr_node] = parent
        for neighbor, node_weight in graph[curr_node].items():
            node_cost = distance + weight(curr_node, neighbor, node_weight)
            if neighbor in enqueue_dict:
                queue_cost, x = enqueue_dict[neighbor]
                if queue_cost <= node_cost:
                    continue
            else:
                x = heuristic(neighbor, target)
            enqueue_dict[neighbor] = node_cost, x
            node_to_push = (node_cost + x, next(c), neighbor, node_cost, curr_node)
            heappush(queue, node_to_push)
    raise nx.NetworkXNoPath(f"{target} node is unreachable from {source}")


def coordinates_to_address(coordinates):
    return Nominatim(user_agent="myGeocoder").reverse(coordinates).address


def fetch_path_weight(graph, path, weight):
    total_weight = 0
    path_length = len(path) - 1
    for i in range(path_length):
        total_weight += fetch_weight(graph, path[i], path[i + 1], weight)
    return total_weight


def fetch_weight(graph, node_1, node_2, weight_type=NORMAL):
    if weight_type == NORMAL:
        try:
            return graph.edges[node_1, node_2, 0][LENGTH]
        except:
            return graph.edges[node_1, node_2][WEIGHT]
    elif weight_type == ELEVATION_GAIN:
        return max(0.0, graph.nodes[node_2][ELEVATION] - graph.nodes[node_1][ELEVATION])

def update_route_json(coordinates):
    route_json = {PROPERTIES: {}, GEOMETRY: {}, TYPE: FEATURE}
    route_json[GEOMETRY][TYPE] = LINESTRING
    route_json[GEOMETRY][COORDINATES] = coordinates
    return route_json