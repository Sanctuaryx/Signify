from abc import ABC, abstractmethod

class AbstractGestureFactory(ABC):
    """
    An abstract base class for creating gesture objects.
    """

    @abstractmethod
    def create_static_gesture(self, left_hand, right_hand, id, name):
        """
        Creates a static gesture object with the given left and right hand data, id, and name.

        Args:
            left_hand (Hand): The left hand data for the gesture.
            right_hand (Hand): The right hand data for the gesture.
            id (int): The ID of the gesture.
            name (str): The name of the gesture.

        Returns:
            StaticGesture: The created static gesture object.
        """
        pass
    
    @abstractmethod
    def create_static_gesture(self, left_hand, right_hand):
        """
        Creates a static gesture object with the given left and right hand data.

        Args:
            left_hand (Hand): The left hand data for the gesture.
            right_hand (Hand): The right hand data for the gesture.

        Returns:
            StaticGesture: The created static gesture object.
        """
        pass
    
    @abstractmethod
    def create_dynamic_gesture(self, left_hand, right_hand, id, name):
        """
        Creates a dynamic gesture object with the given left and right hand data, id, and name.

        Args:
            left_hand (Hand): The left hand data for the gesture.
            right_hand (Hand): The right hand data for the gesture.
            id (int): The ID of the gesture.
            name (str): The name of the gesture.

        Returns:
            DynamicGesture: The created dynamic gesture object.
        """
        pass
    
    @abstractmethod
    def create_dynamic_gesture(self, left_hand, right_hand):
        """
        Creates a dynamic gesture object with the given left and right hand data.

        Args:
            left_hand (Hand): The left hand data for the gesture.
            right_hand (Hand): The right hand data for the gesture.

        Returns:
            DynamicGesture: The created dynamic gesture object.
        """
        pass
