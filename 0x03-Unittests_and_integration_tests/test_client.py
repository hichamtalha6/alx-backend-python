#!/usr/bin/env python3
"""
Unittests for client.GithubOrgClient class.

This module tests the following:
- org property
- _public_repos_url property
- public_repos method
"""
import unittest
from parameterized import parameterized
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test GithubOrgClient methods."""

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
                f"https://api.github.com/orgs/{org_name}"
            )

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the correct URL from the org payload."""

        fake_payload = {"repos_url": "https://api.github.com/orgs/google/repos"}
        client = GithubOrgClient("google")

        with patch.object(
            GithubOrgClient,
            "org",
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = fake_payload
            result = client._public_repos_url
            self.assertEqual(result, fake_payload["repos_url"])

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns the correct list of repo names."""

        fake_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = fake_payload

        client = GithubOrgClient("google")

        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/google/repos"

            result = client.public_repos()
            expected = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected)

            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/google/repos"
            )


if __name__ == "__main__":
    unittest.main()

