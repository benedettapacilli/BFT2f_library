from .hash_chain_digest import HashChainDigest
from .message import Message
from .message_type import MessageType

class CommitMessage(Message):
    def __init__(self, replica_id: int, view: int, sequence_number: int, hcd : HashChainDigest):
        """
        Initialize a Commit message.

        This constructor initializes a message of type `COMMIT` with a given sequence number, hash chain digest and replica ID.

        Args:
            replica_id (int): The ID of the replica that issued the commit message.
            view (int): The view number.
            sequence_number (int): The sequence number assigned by the primary replica.
            hcd (HashChainDigest): The hash chain digest after n operations.

        Attributes:
            replica_id (int): The ID of the replica that issued the commit message.
            hcd (HashChainDigest): The hash chain digest after n operations.
        """
        super().__init__(MessageType.COMMIT, view, sequence_number)
        self.replica_id = replica_id
        self.hcd = hcd

    def get_replica_id(self) -> int:
        """
        Get the ID of the replica that issued the commit message.

        Returns:
            int: The ID of the replica that issued the commit message.
        """
        return self.replica_id

    def get_view(self) -> int:
        """
        Get the view number.

        Returns:
            int: The view number.
        """
        return self.view

    def get_sequence_number(self) -> int:
        """
        Get the sequence number assigned by the primary replica.

        Returns:
            int: The sequence number assigned by the primary replica.
        """
        return self.sequence_number

    def get_hcd(self) -> HashChainDigest:
        """
        Get the hash chain digest after n operations.

        Returns:
            HashChainDigest: The hash chain digest after n operations.
        """
        return self.hcd

    def to_string(self):
        """
        Convert the Commit message to a string.

        Returns:
            str: The Commit message as a string.
        """
        return super().to_string() + f"Replica ID: {self.replica_id}, HCD: {self.hcd}"