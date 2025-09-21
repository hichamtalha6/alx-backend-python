#!/usr/bin/env python3
"""
Unittests for client.GithubOrgClient class.

This module contains test cases for:
- GithubOrgClient.org method
- GithubOrgClient._public_repos_url property
"""
import unittest
from parameterized import parameterized
from unittest.mock import patch
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    def test_org(self, org_name):
        """Test that GithubOrgClient.org returns the correct value."""

        expected_payload = {"login": org_name}

        with patch("client.get_json") as mock_get_json:
            mock_get_json.return_value = expected_payload

            client = GithubOrgClient(org_name)
            result = client.org

            self.assertEqual(result, expected_payload)
            mock_get_json.assert_called_once_with(
                f"https
