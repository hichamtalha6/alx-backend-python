import unittest
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for access_nested_map"""

    @parameterized.expand([
        ({}, ("a",), "'a'"),
        ({"a": 1}, ("a", "b"), "'b'"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_message):
        """Test that KeyError is raised with the correct message"""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)

        # Check that the exception message matches the expected message
        self.assertEqual(str(cm.exception), expected_message)
