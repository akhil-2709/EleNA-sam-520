from src.backend.controller.Controller import *
from src.backend.model.AstarAlgo import *
"""
   This controller is implements Astar Algorithm which gives the shortest path between source and destination taking 
   elevation into consideration
"""
class AstarController(Controller):

    def __init__(self):
        super().__init__()
        self.data_model = None
        self.observer = None
        self.mode_of_elevation = None
        self.source = None
        self.destination = None
        self.limiting_percent = None

    def set_data_model(self, data_model):
        self.data_model = data_model

    def set_source_point(self, source):
        self.source = source

    def set_destination_point(self, destination):
        self.destination = destination

    def set_mode_of_elevation(self, mode_of_elevation):
        self.mode_of_elevation = mode_of_elevation

    def set_limiting_percent(self, limiting_percent):
        self.limiting_percent = limiting_percent

    def manipulate_data_model(self):
        self.data_model.set_algorithm(AstarAlgo)
        self.data_model.generate_paths(self.source, self.destination, self.limiting_percent, self.mode_of_elevation)