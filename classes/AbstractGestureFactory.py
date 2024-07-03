from abc import ABC, abstractmethod

class AbstractGestureFactory(ABC):
    
    @abstractmethod
    def create_static_gesture(self, left_hand, right_hand, id, name):
        pass
    
    @abstractmethod
    def create_static_gesture(self, left_hand, right_hand):
        pass
    
    @abstractmethod
    def create_dynamic_gesture(self, left_hand, right_hand, id, name):
        pass
    
    @abstractmethod
    def create_dynamic_gesture(self, left_hand, right_hand):
        pass
