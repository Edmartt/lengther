from abc import ABC, abstractmethod

from src.locations.models.model import Location

class IDataAccess(ABC):

    @abstractmethod
    def save_data(self) -> str:
        pass

    @abstractmethod
    def read_locations(self) -> list:
        pass

    @abstractmethod
    def read_location(self, location_id: str) -> Location | None:
        pass
