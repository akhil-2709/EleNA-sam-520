from abc import ABC, abstractmethod
"""
    This class is an abstract controller and has methods to be implemented by children classes
"""
class Controller(ABC):

    def __init__(self):
        self.data_model = None
        self.observer = None
        self.elevation_strategy = None

    @abstractmethod
    def set_data_model(self, data_model):
        pass

    @abstractmethod
    def set_mode_of_elevation(self, mode_of_elevation):
        pass

    @abstractmethod
    def manipulate_data_model(self):
        pass
