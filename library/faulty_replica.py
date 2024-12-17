from .replica import Replica

import socket
import random
import time

class FaultyReplica(Replica):
    """
    A class representing a faulty replica in the BFT2F protocol.
    The faulty replica exhibits Byzantine behavior by sending incorrect or conflicting messages.
    """

    def __init__(self, host, port, f, view=0, clients=[], replicas=[]):
        """
        Initialize a FaultyReplica object.

        This replica intentionally behaves incorrectly to simulate Byzantine faults.
        """
        super().__init__(host, port, f, view, clients, replicas)

    def multicast_message(self, message):
        """
        Override the multicast_message method to simulate faulty behavior.
        This method randomly sends valid, invalid, delayed, or skipped messages to different replicas.
        """

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            for replica in self.replicas:
                faulty_behavior = random.choice(['valid', 'invalid', 'delay', 'skip'])

                if faulty_behavior == 'valid':
                    s.connect((replica.get_host(), replica.get_port()))
                    s.send(message.encode())

                elif faulty_behavior == 'invalid':
                    faulty_message = "INVALID_MESSAGE"
                    s.connect((replica.get_host(), replica.get_port()))
                    s.send(faulty_message.encode())

                elif faulty_behavior == 'delay':
                    delay_time = random.uniform(1, 5)
                    time.sleep(delay_time)
                    s.connect((replica.get_host(), replica.get_port()))
                    s.send(message.encode())

                elif faulty_behavior == 'skip':
                    continue

    def receive_prepare(self, data):
        """
        Override the receive_prepare method to simulate faulty behavior.
        This method ignores valid prepare messages or processes them incorrectly.
        """

    def send_reply(self, client_id, reply_message):
        """
        Override the send_reply method to send incorrect replies to the client.
        """
        faulty_reply = "INCORRECT_REPLY"
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect((self.find_client(client_id).get_host(), self.find_client(client_id).get_port()))
            s.send(faulty_reply.encode())
