from BFT2F_library.replica import Replica
from BFT2F_library.client import Client

f = 0
clients = []

client = Client("localhost", 6000, f)
clients.append(client)
replica0 = Replica("localhost", 5000, f, clients=clients)
replica1 = Replica("localhost", 5001, f, clients=clients)

replica0.add_replica(replica0)
replica0.add_replica(replica1)
replica1.add_replica(replica0)
replica1.add_replica(replica1)

client.add_replica(replica0)
client.add_replica(replica1)

client.make_request('log in')