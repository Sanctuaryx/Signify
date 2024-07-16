class BaseGesture:
    """
    Represents a the formal representation of a base gesture, regardless of movement.

    Attributes:
        _id (int): The ID of the gesture.
        _name (str): The name of the gesture.
    """

    def __init__(self, id, name):
        """
        Initializes a new instance of the BaseGesture class.

        Args:
            id (int): The ID of the gesture.
            name (str): The name of the gesture.
        """
        self._id = id
        self._name = name
    
    @property
    def id(self):
        """
        Gets the ID of the gesture.

        Returns:
            int: The ID of the gesture.
        """
        return self._id
    
    @id.setter
    def id(self, id):
        """
        Sets the ID of the gesture.

        Args:
            id (int): The ID of the gesture.
        """
        self._id = id
    
    @property
    def name(self):
        """
        Gets the name of the gesture.

        Returns:
            str: The name of the gesture.
        """
        return self._name
    
    @name.setter
    def name(self, name):
        """
        Sets the name of the gesture.

        Args:
            name (str): The name of the gesture.
        """
        self._name = name
