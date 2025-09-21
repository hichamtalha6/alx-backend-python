#!/usr/bin/env python3
"""
Unittests for client.GithubOrgClient class.
"""
import unittest
from unittest.mock import patch
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test GithubOrgClient methods."""

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the correct URL."""

        fake_payload = {"repos_url": "https://api.github.com/orgs/google/repos"}
        client = GithubOrgClient("google")

        with patch.object(
            GithubOrgClient,
            "org",
            new_callable=property
        ) as mock_org:
            mock_org.return_value = fake_payload
            result = client._public_repos_url
            self.assertEqual(result, fake_payload["repos_url"])
