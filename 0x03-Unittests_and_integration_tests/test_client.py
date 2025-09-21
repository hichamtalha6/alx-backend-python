@patch("client.get_json")
def test_public_repos(self, mock_get_json):
    """Test that public_repos returns the correct list of repo names."""

    # Payload returned by get_json
    fake_payload = [{"name": "repo1"}, {"name": "repo2"}]
    mock_get_json.return_value = fake_payload

    client = GithubOrgClient("google")

    # Mock the _public_repos_url property
    with patch.object(
        GithubOrgClient,
        "_public_repos_url",
        new_callable=PropertyMock
    ) as mock_url:
        mock_url.return_value = "https://api.github.com/orgs/google/repos"

        result = client.public_repos()
        expected = ["repo1", "repo2"]

        self.assertEqual(result, expected)
        mock_url.assert_called_once()
        mock_get_json.assert_called_once_with(
            "https://api.github.com/orgs/google/repos"
        )
