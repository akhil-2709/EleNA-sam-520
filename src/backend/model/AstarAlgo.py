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
