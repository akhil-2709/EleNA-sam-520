class RouteData:

    def __init__(self):
        self.algo = "Empty"
        self.total_gain = 0
        self.total_drop = 0
        self.path = []
        self.distance = 0.0
        self.start_node = None, None
        self.end_node = None, None

    def set_algo(self, algo):
        self.algo = algo

    def set_total_gain(self, total_gain):
        self.total_gain = total_gain

    def set_total_drop(self, total_drop):
        self.total_drop = total_drop

    def set_path(self, path):
        self.path = path

    def set_distance(self, distance):
        self.distance = distance

    def get_algo(self):
        return self.algo

    def get_total_gain(self):
        return self.total_gain

    def get_total_drop(self):
        return self.total_drop

    def get_path(self):
        return self.path

    def get_distance(self):
        return self.distance

    def set_start_node(self, start_node):
        self.start_node = start_node

    def get_start_node(self):
        return self.start_node

    def set_end_node(self, end_node):
        self.end_node = end_node

    def get_end_node(self):
        return self.end_node
