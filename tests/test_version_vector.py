import unittest
from BFT2F_library.request_message import RequestMessage
from BFT2F_library.version_vector import VersionVector, VersionVectorEntry
from BFT2F_library.hash_chain_digest import HashChainDigest

class TestVersionVectorEntry(unittest.TestCase):
    def setUp(self):
        hcd = HashChainDigest()
        hcd.add_block("data", 1)
        self.entry = VersionVectorEntry(1, 1, 1, hcd)

    def test_entry_initialization(self):
        """
        Test that the entry is initialized correctly
        """
        self.assertEqual(self.entry.get_replica_id(), 1)
        self.assertEqual(self.entry.get_view(), 1)
        self.assertEqual(self.entry.get_sequence_number(), 1)
        self.assertIsNotNone(self.entry.get_hcd())

class TestVersionVector(unittest.TestCase):
    def setUp(self):
        self.common_hcd = HashChainDigest()
        self.common_hcd.add_block(RequestMessage("Operation", 123456.789, 1, "state1"), 1)
        self.common_hcd.add_block(RequestMessage("Operation", 123457.789, 2, "state2"), 2)

        self.vector = VersionVector()

    def test_update_and_retrieve_entry(self):
        """
        Test that an entry can be updated and retrieved from the version vector and that it is correct.
        """
        self.vector.update_entry(1, 1, 1, 1, self.common_hcd)
        self.vector.update_entry(2, 2, 1, 1, self.common_hcd)
        self.vector.update_entry(3, 3, 1, 1, self.common_hcd)

        entry1 = self.vector.get_entry(1, 0)
        entry2 = self.vector.get_entry(2, 0)
        entry3 = self.vector.get_entry(3, 0)

        self.assertEqual(entry1.get_hcd(), self.common_hcd)
        self.assertEqual(entry2.get_hcd(), self.common_hcd)
        self.assertEqual(entry3.get_hcd(), self.common_hcd)
        self.assertEqual(entry1.get_hcd(), entry2.get_hcd())
        self.assertEqual(entry2.get_hcd(), entry3.get_hcd())

    def test_current_system_state(self):
        """
        Test that the current system state can be retrieved from the version vector and that it is correct.
        """
        for i in range(1, 4):
            self.vector.update_entry(i, i, 2, 2, self.common_hcd)

        current_state = self.vector.get_current_system_state(1)
        self.assertEqual(current_state.get_sequence_number(), 2)
        self.assertEqual(current_state.get_view(), 2)
        self.assertEqual(current_state.get_hcd(), self.common_hcd)

if __name__ == '__main__':
    unittest.main()