import unittest
from BFT2F_library.hash_chain_digest import HashChainDigest
from BFT2F_library.checkpoint_message import CheckpointMessage
from BFT2F_library.commit_message import CommitMessage
from BFT2F_library.new_view_message import NewViewMessage
from BFT2F_library.request_message import RequestMessage
from BFT2F_library.version_vector import VersionVector

class TestRequestMessage(unittest.TestCase):
    def setUp(self):
        self.request_message = RequestMessage("Login", 1622337200.0, 1, "Initial State")

    def test_initialization(self):
        """
        Test the initialization of a RequestMessage object.
        """
        self.assertEqual(self.request_message.get_operation(), "Login")
        self.assertEqual(self.request_message.get_timestamp(), 1622337200.0)
        self.assertEqual(self.request_message.get_client_id(), 1)
        self.assertEqual(self.request_message.get_current_system_state(), "Initial State")

    def test_string_representation(self):
        """
        Test the string representation of a RequestMessage object.
        """
        expected_string = "Type: MessageType.REQUEST, View: None, Sequence Number: None, Client ID: 1, Operation: Login, Timestamp: 1622337200.0, Current System State: Initial State"
        self.assertEqual(self.request_message.to_string(), expected_string)

class TestCommitMessage(unittest.TestCase):
    def setUp(self):
        hcd = HashChainDigest()
        self.commit_message = CommitMessage(1, 0, 1, hcd)

    def test_initialization(self):
        """
        Test the initialization of a CommitMessage object.
        """
        self.assertEqual(self.commit_message.get_replica_id(), 1)
        self.assertEqual(self.commit_message.get_view(), 0)
        self.assertEqual(self.commit_message.get_sequence_number(), 1)
        self.assertIsInstance(self.commit_message.get_hcd(), HashChainDigest)

class TestCheckpointMessage(unittest.TestCase):
    def setUp(self):
        vv = VersionVector()
        self.checkpoint_message = CheckpointMessage(1, 10, 5, vv, ['entry1', 'entry2'])

    def test_initialization(self):
        """
        Test the initialization of a CheckpointMessage object.
        """
        self.assertEqual(self.checkpoint_message.get_behind_replica_id(), 1)
        print("print", self.checkpoint_message.get_sequence_number())
        self.assertEqual(self.checkpoint_message.get_sequence_number(), 10)
        self.assertEqual(self.checkpoint_message.get_rcache_n(), 5)
        self.assertIsInstance(self.checkpoint_message.get_version_vector(), VersionVector)
        self.assertEqual(self.checkpoint_message.get_E(), ['entry1', 'entry2'])

class TestNewViewMessage(unittest.TestCase):
    def setUp(self):
        self.new_view_message = NewViewMessage(2, ['view1', 'view2'], ['op1', 'op2'])

    def test_initialization(self):
        """
        Test the initialization of a NewViewMessage object.
        """
        self.assertEqual(self.new_view_message.get_view(), 2)
        self.assertEqual(self.new_view_message.get_V(), ['view1', 'view2'])
        self.assertEqual(self.new_view_message.get_O(), ['op1', 'op2'])

if __name__ == '__main__':
    unittest.main()