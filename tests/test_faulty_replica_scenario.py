from BFT2F_library.client import Client
from BFT2F_library.faulty_replica import FaultyReplica
from BFT2F_library.replica import Replica

f = 1
clients = []

client = Client("localhost", 6000, f)
clients.append(client)

replica0 = Replica("localhost", 5000, f, clients=clients)
replica1 = Replica("localhost", 5001, f, clients=clients)
faulty_replica = FaultyReplica("localhost", 5002, f, clients=clients)

replica0.add_replica(replica1)
replica0.add_replica(faulty_replica)

replica1.add_replica(replica0)
replica1.add_replica(faulty_replica)

faulty_replica.add_replica(replica0)
faulty_replica.add_replica(replica1)

client.add_replica(replica0)
client.add_replica(replica1)
client.add_replica(faulty_replica)

client.make_request('log in')