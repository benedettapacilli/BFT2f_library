from .message_type import MessageType

class Message:
    def __init__(self, message_type : MessageType, view : int = None, sequence_number : int = None):
        """
        Initialize a message.

        This constructor initializes a message with a given message type, view number, and sequence number. View and sequence number values are common to most message types, they can be set to None if not applicable.

        Args:
            message_type (MessageType): The type of the message.
            view (int): The view number.
            sequence_number (int): The sequence number assigned by the primary replica.

        Attributes:
            message_type (MessageType): The type of the message.
            view (int): The view number.
            sequence_number (int): The sequence number assigned by the primary replica.
        """
        self.message_type = message_type
        self.view = view
        self.sequence_number = sequence_number

    def get_message_type(self):
        """
        Get the type of the message.

        Returns:
            MessageType: The type of the message.
        """
        return self.message_type

    def get_view(self):
        """
        Get the view number.

        Returns:
            int: The view number.
        """
        return self.view

    def get_sequence_number(self):
        """
        Get the sequence number assigned by the primary replica.

        Returns:
            int: The sequence number assigned by the primary replica.
        """
        return self.sequence_number

    def to_string(self):
        """
        Convert the message to a string.

        Returns:
            str: A string representation of the message.
        """
        return f"Type: {self.message_type}, View: {self.view}, Sequence Number: {self.sequence_number}, "

    def encode(self):
        """
        Encode the message as a byte string.

        Returns:
            bytes: The message encoded as a byte string.
        """
        return self.to_string().encode('utf-8')