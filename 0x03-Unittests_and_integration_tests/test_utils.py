#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for access_nested_map"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map returns correct values"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    def test_access_nested_map_exception(self):
        """Test that KeyError is raised with the correct message"""
        with self.assertRaises(KeyError) as cm:
            access_nested_map({}, ("a",))
        self.assertEqual(str(cm.exception), "'a'")

        with self.assertRaises(KeyError) as cm:
            access_nested_map({"a": 1}, ("a", "b"))
        self.assertEqual(str(cm.exception), "'b'")


if __name__ == "__main__":
    unittest.main()
