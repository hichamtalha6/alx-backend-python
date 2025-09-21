#!/usr/bin/env python3
"""
Unittests for utils.py module.

This module contains test cases for:
- access_nested_map function
- memoize decorator
"""
import unittest
from parameterized import parameterized
from unittest.mock import patch
from utils import access_nested_map, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map returns correct values."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    def test_access_nested_map_exception(self):
        """Test that KeyError is raised with the correct message."""
        with self.assertRaises(KeyError) as cm:
            access_nested_map({}, ("a",))
        self.assertEqual(str(cm.exception), "'a'")

        with self.assertRaises(KeyError) as cm:
            access_nested_map({"a": 1}, ("a", "b"))
        self.assertEqual(str(cm.exception), "'b'")


class TestMemoize(unittest.TestCase):
    """Test cases for the memoize decorator."""

    def test_memoize(self):
        """Test that memoize caches the result of a method."""

        class TestClass:
            """Helper class to test memoization."""

            def a_method(self):
                """Simple method returning a fixed value."""
                return 42

            @memoize
            def a_property(self):
                """Memoized property calling a_method."""
                return self.a_method()

        with patch.object(
            TestClass,
            "a_method",
            return_value=42
        ) as mock_method:
            obj = TestClass()

            # First call: should call a_method
            result1 = obj.a_property
            # Second call: should use cached value, not call a_method again
            result2 = obj.a_property

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
