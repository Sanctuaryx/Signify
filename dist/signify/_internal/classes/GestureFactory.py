from classes.AbstractGestureFactory import AbstractGestureFactory
import classes.StaticGesture as StaticGesture
import classes.DynamicGesture as DynamicGesture

class GestureFactory(AbstractGestureFactory):
    """
    A factory class for creating different types of gestures.
    """

    def create_static_stored_gesture(self, id, name, left_hand: StaticGesture.Hand, right_hand: StaticGesture.Hand):
        """
        Creates a static stored gesture with the given parameters.

        Args:
            id (int): The ID of the gesture.
            name (str): The name of the gesture.
            left_hand (StaticGesture.Hand): The left hand configuration of the gesture.
            right_hand (StaticGesture.Hand): The right hand configuration of the gesture.

        Returns:
            StaticGesture.StaticGesture: The created static stored gesture.
        """
        return StaticGesture.StaticGesture(left_hand, right_hand, id, name)

    def create_static_gesture(self, left_hand: StaticGesture.Hand, right_hand: StaticGesture.Hand):
        """
        Creates a static gesture with the given parameters.

        Args:
            left_hand (StaticGesture.Hand): The left hand configuration of the gesture.
            right_hand (StaticGesture.Hand): The right hand configuration of the gesture.

        Returns:
            StaticGesture.StaticGesture: The created static gesture.
        """
        return StaticGesture.StaticGesture(left_hand, right_hand)

    def create_dynamic_stored_gesture(self, id, name, left_hand: DynamicGesture.Hand, right_hand: DynamicGesture.Hand):
        """
        Creates a dynamic stored gesture with the given parameters.

        Args:
            id (int): The ID of the gesture.
            name (str): The name of the gesture.
            left_hand (DynamicGesture.Hand): The left hand configuration of the gesture.
            right_hand (DynamicGesture.Hand): The right hand configuration of the gesture.

        Returns:
            DynamicGesture.DynamicGesture: The created dynamic stored gesture.
        """
        return DynamicGesture.DynamicGesture(left_hand, right_hand, id, name)

    def create_dynamic_gesture(self, left_hand: DynamicGesture.Hand, right_hand: DynamicGesture.Hand):
        """
        Creates a dynamic gesture with the given parameters.

        Args:
            left_hand (DynamicGesture.Hand): The left hand configuration of the gesture.
            right_hand (DynamicGesture.Hand): The right hand configuration of the gesture.

        Returns:
            DynamicGesture.DynamicGesture: The created dynamic gesture.
        """
        return DynamicGesture.DynamicGesture(left_hand, right_hand)
