#!/usr/bin/env python3
"""
Unittests for client.GithubOrgClient class.
"""
import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test GithubOrgClient methods."""

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns the correct list of repos."""

        # Fake data returned by get_json
        fake_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = fake_payload

        client = GithubOrgClient("google")
        # Patch the _public_repos_url property
        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/google/repos"

            result = client.public_repos()

            # The list of repo names should match the payload
            expected = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected)

            # Check that both the property and get_json were called once
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/google/repos"
            )
