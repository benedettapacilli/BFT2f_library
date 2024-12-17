from enum import Enum

class MessageType(Enum):
    """
    Enum for message types.

    This enum is used to represent the different types of messages that are sent/received in Replica-Replica communication or Replica-Client communication, in the BFT2F protocol. Each message type corresponds to a specific step in the protocol's consensus process.

    PRE_PREPARE (0):
        Sent by the primary replica to propose a client request for execution.

    PREPARE (1):
        Sent by replicas upon receiving a valid PRE_PREPARE message. This message indicates that the replica is ready to commit the proposed operation after agreement from other replicas.

    COMMIT (2):
        Sent by replicas after receiving enough PREPARE messages. It signals that the replica is ready to execute the operation, ensuring that at least 2f + 1 replicas agree on the operation.

    REPLY (3):
        Sent by replicas to the client after an operation is committed and executed. The client waits for replies from at least 2f + 1 replicas before accepting the result.

    REQUEST (4):
        Sent by clients to request an operation from the replicas.

    VIEW_CHANGE (5):
        Sent by replicas when they detect that the current primary is faulty or slow. This message initiates the process of electing a new primary and switching to a new view.

    PRIMARY_NOT_DOMINANT (6):
        Sent when a replica detects that the current primary is not performing correctly, signaling that a view change may be necessary.

    OPERATIONS_DICTIONARY (7):
        Contains a digest of all operations committed by a replica. This message ensures that replicas can synchronize their states by sharing this information in case some replicas lag behind.

    NEW_VIEW (8):
        Sent by the new primary after a view change. This message contains the state of the system and ensures that all replicas in the new view are synchronized.

    CHECKPOINT (9):
        Sent periodically by replicas to mark stable points in the operation history. This message allows replicas to garbage collect old logs and ensures that all replicas have a consistent state up to a certain sequence number.
    """
    PRE_PREPARE = 0
    PREPARE = 1
    COMMIT = 2
    REPLY = 3
    REQUEST = 4
    VIEW_CHANGE = 5
    PRIMARY_NOT_DOMINANT = 6
    OPERATIONS_DICTIONARY = 7
    NEW_VIEW = 8
    CHECKPOINT = 9