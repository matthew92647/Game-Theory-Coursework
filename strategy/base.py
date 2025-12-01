from abc import ABC, abstractmethod

class Strategy(ABC):
    @abstractmethod
    def choose_action(self, my_dice, history):
        """Return ("bid", quantity, face) or ("call",)"""
        pass
