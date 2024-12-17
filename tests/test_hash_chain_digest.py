import unittest
from BFT2F_library.request_message import RequestMessage
from BFT2F_library.hash_chain_digest import HashChainBlock, HashChainDigest

class TestHashChainBlock(unittest.TestCase):
    def test_initialization(self):
        """
        Test if the block is initialized correctly.
        """
        request = RequestMessage("Operation X", 123456.789, 1, "state1")
        block = HashChainBlock(request, 1, "0")
        self.assertEqual(block.get_data().get_operation(), "Operation X")
        self.assertEqual(block.get_data().get_timestamp(), 123456.789)
        self.assertEqual(block.get_data().get_client_id(), 1)
        self.assertEqual(block.get_data().get_current_system_state(), "state1")
        self.assertIsNotNone(block.get_hash())

    def test_hash_consistency(self):
        """
        Test if the hash is consistent among blocks with the same data.
        """
        request = RequestMessage("Test Data", 123456.0, 1, "state1")
        block1 = HashChainBlock(request, 1, "0")
        block2 = HashChainBlock(request, 1, "0")
        self.assertEqual(block1.get_hash(), block2.get_hash())

class TestHashChainDigest(unittest.TestCase):
    def test_chain_integrity(self):
        """
        Test if the chain is maintained correctly.
        """
        chain = HashChainDigest()
        request1 = RequestMessage("Login", 123456.0, 101, "state1")
        request2 = RequestMessage("Logout", 123457.0, 102, "state2")
        chain.add_block(request1, 1)
        chain.add_block(request2, 2)

        self.assertEqual(len(chain.get_chain()), 2)
        self.assertEqual(chain.get_chain()[0].get_data().get_operation(), "Login")
        self.assertEqual(chain.get_chain()[1].get_data().get_operation(), "Logout")
        self.assertEqual(chain.get_chain()[1].get_previous_hash(), chain.get_chain()[0].get_hash())

    def test_chain_growth(self):
        """
        Test if the chain grows correctly.
        """
        chain = HashChainDigest()
        request1 = RequestMessage("Operation A", 123450.789, 1, "stateA")
        request2 = RequestMessage("Operation B", 123451.789, 2, "stateB")
        request3 = RequestMessage("Operation C", 123452.789, 3, "stateC")
        chain.add_block(request1, 1)
        chain.add_block(request2, 2)
        chain.add_block(request3, 3)

        self.assertEqual(len(chain.get_chain()), 3)
        self.assertEqual(chain.get_chain()[0].get_data().get_operation(), "Operation A")
        self.assertEqual(chain.get_chain()[1].get_data().get_operation(), "Operation B")
        self.assertEqual(chain.get_chain()[2].get_data().get_operation(), "Operation C")
        self.assertNotEqual(chain.get_chain()[0].get_hash(), chain.get_chain()[1].get_hash())
        self.assertNotEqual(chain.get_chain()[1].get_hash(), chain.get_chain()[2].get_hash())
        self.assertEqual(chain.get_chain()[2].get_previous_hash(), chain.get_chain()[1].get_hash())

    def test_last_block_retrieval(self):
        """
        Test if the last block is retrieved correctly.
        """
        chain = HashChainDigest()
        request1 = RequestMessage("Start Session", 123460.789, 10, "initialState")
        request2 = RequestMessage("End Session", 123461.789, 11, "finalState")
        chain.add_block(request1, 1)
        chain.add_block(request2, 2)

        last_block = chain.get_last_block()
        self.assertEqual(last_block.get_data().get_operation(), "End Session")
        self.assertEqual(last_block.get_sequence_number(), 2)
        self.assertEqual(last_block.get_data().get_client_id(), 11)
        self.assertEqual(last_block.get_data().get_current_system_state(), "finalState")

if __name__ == '__main__':
    unittest.main()