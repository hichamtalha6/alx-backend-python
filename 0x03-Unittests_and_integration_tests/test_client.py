#!/usr/bin/env python3
"""
Unittests for client.GithubOrgClient class.

This module contains test cases for:
- GithubOrgClient.org method
"""
import unittest
from parameterized import parameterized
from unittest.mock import patch
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient class."""

    @patch("client.get_json")
    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    def test_org(self, mock_get_json, org_name):
        """Test that GithubOrgClient.org returns the correct value."""

        expected_payload = {"login": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, expected_payload)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )


if __name__ == "__main__":
    unittest.main()
