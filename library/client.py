import sys
import time
import socket
from .reply_message import ReplyMessage
from .version_vector import VersionVector
from .hash_chain_digest import HashChainDigest
from .request_message import RequestMessage
from .message_type import MessageType
from threading import Lock, Thread

class Client():
    """
    The Client class represents a client in the BFT2F system.
    """
    _id_counter = 0
    def __init__(self, host, port, f, replicas = []):
        """
        Initialize a Client object and start listening for incoming messages.

        Args:
            host (str): The host address of the client.
            port (int): The port number of the client.
            f (int): The fault tolerance level of the system. The system can tolerate f faulty replicas.
            replicas (list): A list of Replica objects representing the replicas in the system.

        Attributes:
            host (str): The host address of the client.
            port (int): The port number of the client.
            lock (Lock): A threading lock
            client_id (int): The ID of the client.
            hcd (HashChainDigest): The hash chain digest after n operations.
            version_vector (VersionVector): The version vector of the client.
            f (int): The fault tolerance level of the system. The system can tolerate f faulty replicas.
            received_replies (list): A list of received replies.
            pending_requests (list): A list of pending requests.
            replicas (list): A list of Replica objects representing the replicas in the system.
        """
        self.host = host
        self.port = port
        self.lock =Lock()
        self.client_id = Client._id_counter
        Client._id_counter += 1
        self.hcd = HashChainDigest()
        self.version_vector = VersionVector()
        self.f = f
        self.received_replies = []
        self.pending_requests = []
        self.replicas = replicas

        self.listen()

    def get_client_id(self):
        """
        Get the ID of the client.

        Returns:
            int: The ID of the client.
        """
        return self.client_id

    def get_host(self):
        """
        Get the host address of the client.

        Returns:
            str: The host address of the client.
        """
        return self.host

    def get_port(self):
        """
        Get the port number of the client.

        Returns:
            int: The port number of the client.
        """
        return self.port

    def get_num_received_replies(self):
        """
        Get the number of received replies.

        Returns:
            int: The number of received replies.
        """
        return len(self.received_replies)

    def get_version_vector(self):
        """
        Get the version vector of the client.

        Returns:
            VersionVector: The version vector of the client.
        """
        return self.version_vector

    def add_replica(self, replica):
        """
        Add a replica to the list of replicas.

        Args:
            replica (Replica): The replica to be added.
        """
        if replica not in self.replicas:
            self.replicas.append(replica)

    def listen(self):
        """
        Start listening for incoming messages.
        """
        listen_thread = Thread(target=self._listen_thread)
        listen_thread.daemon = False
        listen_thread.start()

    def _listen_thread(self):
        """
        The thread that listens for incoming messages.

        This method listens for incoming messages on the client's host and port.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            try:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((self.host, self.port))
            except OSError as e:
                print(f"Failed to bind to {self.host}:{self.port} with error: {e}")
            while True:
                data, addr = s.recvfrom(1024)
                msg = data.decode()
                if not data:
                    break
                msg = self.deserialize_message(msg)
                if isinstance(msg, Exception):
                    continue
                if msg.get_message_type() == MessageType.REPLY:
                    self.handle_reply(msg)

    def make_request(self, operation):
        """
        Make a request to the system.

        This method creates a request message with the given operation and multicasts it to the replicas in the system.

        Args:
            operation (str): The operation to be performed.
        """
        timestamp = time.time()
        current_system_state = self.version_vector.get_current_system_state(f = 0)
        request = RequestMessage(operation, timestamp, self.client_id, current_system_state)
        self.pending_requests.append(request)
        self.multicast_request(request)

    def multicast_request(self, request: RequestMessage):
        """
        Multicast a request message to the replicas in the system.

        This method sends the request message to the multicast group address and port of each replica in the system.

        Args:
            request (RequestMessage): The request message to be multicasted.
        """

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            try:
                for replica in self.replicas:
                    multicast_group = (replica.get_host(), replica.get_port())
                    s.sendto(request.encode(), multicast_group)
            finally:
                s.close()

    def handle_reply(self, reply_message: ReplyMessage):
        """
        Handle a reply message received by the client.

        This method processes the reply message received by the client and updates the version vector accordingly.

        Args:
            reply_message (ReplyMessage): The reply message to be processed.

        Returns:
            bool: True if consensus is reached, False otherwise.
        """

        if reply_message not in self.received_replies:
            self.received_replies.append(reply_message)
        total = 0
        for pending_request in self.pending_requests:
            if pending_request.get_timestamp() == reply_message.get_timestamp():
                founded_request = pending_request
                for received_reply in self.received_replies:
                    if received_reply.get_timestamp() == reply_message.get_timestamp() and received_reply.get_client_id() == reply_message.get_client_id() and received_reply.get_result() == reply_message.get_result() and received_reply.get_entry() == reply_message.get_entry():
                        total += 1
        if total >= ((2 * self.f) + 1):
            self.pending_requests.remove(founded_request)
            for received_reply in self.received_replies:
                self.version_vector.update_entry(self.client_id, received_reply.get_entry().get_replica_id(), received_reply.get_entry().get_view(), received_reply.get_entry().get_sequence_number(), received_reply.get_entry().get_hcd())
            if (self.version_vector.get_current_system_state(self.f).get_hcd() == reply_message.get_entry().get_hcd()):
                print("Consensus reached")
                sys.exit()
                # print(f"Client {self.client_id} received {len(self.received_replies)} matching replies with {len(self.replicas)} replicas and fault tolerance of {self.f}") # to be printed once only
                return True
        else:
            return False

    def deserialize_message(self, msg):
        """
        Deserialize a message from a string. When a message is received, it is serialized as a string. This method deserializes the message string into a Message object. More specifically, it into a ReplyMessage object.

        Args:
            msg (str): The message to be deserialized.

        Returns:
            Message: The deserialized message.

        Throws:
            Exception: If the message type is invalid.
        """
        try:
            components = msg.split(', ')
            if components[0].split(': ')[1] == 'MessageType.REPLY':
                return ReplyMessage(
                    int(components[3].split(': ')[1]), float(components[4].split(': ')[1]),
                    components[5].split(': ')[1], int(components[6].split(': ')[2]),
                    int(components[7].split(': ')[1]), int(components[8].split(': ')[1]),
                    components[9].split(': ')[1]
                )
            else:
                raise Exception("Invalid message type")
        except Exception as e:
            return Exception("Invalid message")