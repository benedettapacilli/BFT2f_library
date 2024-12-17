import hashlib
import time

from .request_message import RequestMessage

class HashChainBlock:
    """A class to represent a hash chain block. Blocks are used to create a hash chain."""
    def __init__(self, data: RequestMessage, sequence_number: int, previous_hash: str):
        """
        Initialize a hash chain block.

        This constructor initializes a block with a given data field, sequence number, and the hash of the previous block in the chain.

        Args:
            data (RequestMessage): The data field of the block.
            sequence_number (int): The sequence number of the block.
            previous_hash (str): The hash of the previous block in the chain.

        Attributes:
            data (RequestMessage): The data field of the block.
            sequence_number (int): The sequence number of the block.
            timestamp (float): The timestamp of the block which represents the time the block was created.
            previous_hash (str): The hash of the previous block in the chain.
            hash (str): The hash of the block.
        """
        self.data = data # msg'n
        self.sequence_number = sequence_number
        self.timestamp = time.time()
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """Calculates the hash of the block.

        Returns:
            str: The hash of the block.
        """
        block_str = str(self.data) + str(self.previous_hash)
        return hashlib.sha256(block_str.encode()).hexdigest()

    def get_data(self) -> RequestMessage:
        """
        Get the data field of the block.

        Returns:
            RequestMessage: The data field of the block.
        """
        return self.data

    def get_sequence_number(self) -> int:
        """
        Get the sequence number of the block.

        Returns:
            int: The sequence number of the block.
        """
        return self.sequence_number

    def get_timestamp(self) -> float:
        """
        Get the timestamp of the block.

        Returns:
            float: The timestamp of the block which represents the time the block was created.
        """
        return self.timestamp

    def get_previous_hash(self) -> str:
        """
        Get the hash of the previous block in the chain.

        Returns:
            str: The hash of the previous block in the chain.
        """
        return self.previous_hash

    def get_hash(self) -> str:
        return self.hash

class HashChainDigest:
    """A class to represent a hash chain. A hash chain is a sequence of blocks, where each block contains a data field and a hash field."""
    def __init__(self):
        """
        Initialize a hash chain.

        This constructor initializes an empty hash chain, as a list of blocks.

        Attributes:
            chain (list): The hash chain as a list of blocks.
        """
        self.chain = []

    def add_block(self, block_data: RequestMessage, sequence_number: int):
        """Adds a block to the hash chain. The block is created with the given data and sequence number, and appended to the chain.

        Args:
            block_data (RequestMessage): The data field of the block.
            sequence_number (int): The sequence number of the block
        """
        if len(self.chain) == 0:
            previous_hash = "0"
        else:
            previous_hash = self.chain[-1].get_hash()

        block = HashChainBlock(block_data, sequence_number, previous_hash)

        self.chain.append(block)

    def get_chain(self):
        """Get the hash chain.

        Returns:
            list: The hash chain as a list of blocks.
        """
        return self.chain

    def get_last_block(self) -> HashChainBlock:
        """
        Get the last block in the hash chain.

        Returns:
            HashChainBlock: The last block in the hash chain.
        """
        if len(self.chain) > 0:
            return self.chain[-1]