class DijkstraAlgorithm:
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
