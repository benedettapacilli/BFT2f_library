from .message import Message
from .message_type import MessageType

class NewViewMessage(Message):
    def __init__(self, new_view: int, V: list, O: list):
        """
        Initialize a New View message.

        This constructor initializes a message of type `NEW_VIEW` with a given new view number, set of view-change messages, and set of pre-prepare messages.

        Args:
            new_view (int): The new view number.
            V (list): The set of 2f + 1 valid, non-conflicting view-change messages from other replicas. These view-change messages are used to prove that the previous primary has failed and that enough replicas agree on moving to a new view.
            O (list): The set of pre-prepare messages. These messages correspond to the client requests that were either prepared or in-flight during the view change. They ensure that the operations that were in progress are either committed or re-proposed under the new primary.

        Attributes:
            V (list): The set of 2f + 1 valid, non-conflicting view-change messages from other replicas.
            O (list): The set of pre-prepare messages.
        """
        super().__init__(MessageType.NEW_VIEW, new_view)
        self.V = V
        self.O = O

    def get_V(self) -> list:
        """
        Get the set of 2f + 1 valid, non-conflicting view-change messages from other replicas.

        Returns:
            list: The set of 2f + 1 valid, non-conflicting view-change messages from other replicas.
        """
        return self.V

    def get_O(self) -> list:
        """
        Get the set of pre-prepare messages.

        Returns:
            list: The set of pre-prepare messages.
        """
        return self.O

    def to_string(self):
        """
        Convert the New View message to a string.

        Returns:
            str: A string representation of the New View message.
        """
        return super().to_string() + f"V: {self.V}, O: {self.O}"