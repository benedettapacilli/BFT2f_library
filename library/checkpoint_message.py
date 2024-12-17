from .message import Message
from .message_type import MessageType
from .version_vector import VersionVector

class CheckpointMessage(Message):
    def __init__(self, behind_replica_id: int, sequence_number: int, rcache_n: int, version_vector: VersionVector, E: list):
        """
        Initialize a Checkpoint message.

        This constructor initializes a message of type `CHECKPOINT` with a given sequence number and additional data specific to a replica that is behind.

        Args:
            behind_replica_id (int): The ID of the replica that is behind.
            sequence_number (int): The sequence number for the checkpoint.
            rcache_n (int): The number of entries in the replica cache.
            version_vector (VersionVectore): The version vector representing the state of each replica.
            E (list): The 'E' element associated with the checkpoint.

        Attributes:
            behind_replica_id (int): The ID of the replica that is behind.
            rcache_n (int): The number of entries in the replica cache.
            version_vector (VersionVector): The version vector representing the state of each replica.
            E (list): The 'E' element associated with the checkpoint.
        """
        super().__init__(MessageType.CHECKPOINT, sequence_number = sequence_number)
        self.behind_replica_id = behind_replica_id
        self.rcache_n = rcache_n
        self.version_vector = version_vector
        self.E = E

    def get_behind_replica_id(self):
        """
        Get the ID of the replica that is behind.

        Returns:
        int: The ID of the replica that is behind.
        """
        return self.behind_replica_id

    def get_rcache_n(self):
        """
        Get the number of entries in the replica cache.

        Returns:
        int: The number of entries in the replica cache.
        """
        return self.rcache_n

    def get_version_vector(self):
        """
        Get the version vector representing the state of each replica.

        Returns:
        VersionVector: The version vector representing the state of each replica.
        """
        return self.version_vector

    def get_E(self):
        """
        Get the 'E' element used associated with the checkpoint.

        The 'E' element is a set of older version vector entries for replicas where the sequence number `n` is less than or equal to `n - 2I`. The function helps ensure consistency in a fork* consistent system by including older, signed version vector entries, allowing for recovery from fork sets and consistency validation.

        Returns:
        list: The 'E' element associated with the checkpoint.
        """
        return self.E