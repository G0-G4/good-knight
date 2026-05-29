from abc import ABC, abstractmethod


class DetectorStrategy(ABC):
    @abstractmethod
    def is_goodnight(self, text: str) -> bool: ...