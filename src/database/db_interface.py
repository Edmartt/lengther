
from abc import abstractmethod, ABC
from typing import Optional


class IDataStorage(ABC):

    @abstractmethod
    def get_db(self) -> Optional[tuple]:
        pass

    @abstractmethod
    def close_db(self, e=None) ->None:
        pass

    @abstractmethod
    def init_db(self) -> None:
        pass
