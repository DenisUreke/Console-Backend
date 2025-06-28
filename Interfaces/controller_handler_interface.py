from abc import ABC, abstractmethod

class InputHandler(ABC):
    @abstractmethod
    def extract(self, payload: dict):
        pass
