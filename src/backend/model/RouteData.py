class RouteData:
    """
       This class contains all the getter an setter methods needed for all the path related data
    """

    def __init__(self):
        self.algo = "Empty"
        self.total_gain = 0
        self.total_drop = 0
        self.path = []
        self.distance = 0.0
        self.start_node = None, None
        self.end_node = None, None

    def set_algo(self, algo):
        """
                This method is used for setting the algorithm name when changed by user.
                Args:
                    algo:

                Returns:
                    None
        """
        self.algo = algo

    def set_total_gain(self, total_gain):
        """
                This method is used for setting the total_gain calculated using any algorithm.
                Args:
                    total_gain:

                Returns:
                    None
        """
        self.total_gain = total_gain

    def set_total_drop(self, total_drop):
        """
                This method is used for setting the total_drop calculated using any algorithm.
                Args:
                    total_drop:

                Returns:
                    None
        """
        self.total_drop = total_drop

    def set_path(self, path):
        """
                This method is used for setting the path calculated using any algorithm.
                Args:
                    path:

                Returns:
                    None
        """
        self.path = path

    def set_distance(self, distance):
        """
                This method is used for setting the total_drop calculated using any algorithm.
                Args:
                    distance:

                Returns:
                    None
        """
        self.distance = distance

    def get_algo(self):
        """
                Getter method for fetching the algorithm name.

                Returns:algorithm name

        """
        return self.algo

    def get_total_gain(self):
        """
                Getter method for fetching the total gain.

                Returns:total_gain

        """
        return self.total_gain

    def get_total_drop(self):
        """
                Getter method for fetching the total drop.

                Returns:total_drop

        """
        return self.total_drop

    def get_path(self):
        """
                Getter method for fetching the path.

                Returns:path

        """
        return self.path

    def get_distance(self):
        """
                Getter method for fetching the distance.

                Returns:distance

        """
        return self.distance

    def set_start_node(self, start_node):
        """
                This method sis used for setting the start node  for the model.

                Args:
                    start_node:

                Returns:
                    None
        """
        self.start_node = start_node

    def get_start_node(self):
        return self.start_node

    def set_end_node(self, end_node):
        """
                This method sis used for setting the start node  for the model.

                Args:
                    end_node:

                Returns:
                    None
        """
        self.end_node = end_node

    def get_end_node(self):
        return self.end_node
