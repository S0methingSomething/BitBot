"""Tests for the deployment system."""
import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.deployment import (
    CloudflarePagesDeployment,
    DeploymentFactory,
    GitHubPagesDeployment,
)


class TestDeploymentSystem:
    """Test cases for the deployment system."""

    def test_github_pages_deployment_initialization(self):
        """Test GitHub Pages deployment initialization."""
        class MockConfig:
            def __init__(self):
                self.owner = "test_owner"
                self.repo = "test_repo"
                self.branch = "gh-pages"
                self.token = "test_token"

        config = MockConfig()
        deployment = GitHubPagesDeployment(config)

        assert deployment.owner == "test_owner"
        assert deployment.repo == "test_repo"
        assert deployment.branch == "gh-pages"
        assert deployment.token == "test_token"
        assert deployment.name == "GitHub Pages"

    def test_cloudflare_pages_deployment_initialization(self):
        """Test Cloudflare Pages deployment initialization."""
        class MockConfig:
            def __init__(self):
                self.account_id = "test_account"
                self.project_name = "test_project"
                self.api_token = "test_token"
                self.branch = "main"

        config = MockConfig()
        deployment = CloudflarePagesDeployment(config)

        assert deployment.account_id == "test_account"
        assert deployment.project_name == "test_project"
        assert deployment.api_token == "test_token"
        assert deployment.branch == "main"
        assert deployment.name == "Cloudflare Pages"

    def test_github_pages_get_deployment_url(self):
        """Test GitHub Pages deployment URL generation."""
        class MockConfig:
            def __init__(self):
                self.owner = "test_owner"
                self.repo = "test_repo"
                self.branch = "gh-pages"
                self.token = ""

        config = MockConfig()
        deployment = GitHubPagesDeployment(config)
        url = deployment.get_deployment_url()

        assert url == "https://test_owner.github.io/test_repo/"

    def test_cloudflare_pages_get_deployment_url(self):
        """Test Cloudflare Pages deployment URL generation."""
        class MockConfig:
            def __init__(self):
                self.account_id = "test_account"
                self.project_name = "test_project"
                self.api_token = ""
                self.branch = "main"

        config = MockConfig()
        deployment = CloudflarePagesDeployment(config)
        url = deployment.get_deployment_url()

        assert url == "https://test_project.test_account.pages.dev/"

    @patch("src.deployment.subprocess.run")
    def test_github_pages_dry_run_deployment(self, mock_run):
        """Test GitHub Pages dry-run deployment."""
        class MockConfig:
            def __init__(self):
                self.owner = "test_owner"
                self.repo = "test_repo"
                self.branch = "gh-pages"
                self.token = ""

        # Set dry-run environment variable
        os.environ["DRY_RUN"] = "true"

        config = MockConfig()
        deployment = GitHubPagesDeployment(config)

        with tempfile.TemporaryDirectory() as tmp_dir:
            source_path = Path(tmp_dir)
            result = deployment.deploy(source_path)

            assert result["success"] is True
            assert result["provider"] == "github"
            assert result["url"] == "https://test_owner.github.io/test_repo/"
            assert "Dry-run deployment simulation" in result["message"]

            # Verify subprocess was not called
            mock_run.assert_not_called()

        # Clean up environment variable
        del os.environ["DRY_RUN"]

    @patch("src.deployment.subprocess.run")
    def test_cloudflare_pages_dry_run_deployment(self, mock_run):
        """Test Cloudflare Pages dry-run deployment."""
        class MockConfig:
            def __init__(self):
                self.account_id = "test_account"
                self.project_name = "test_project"
                self.api_token = ""
                self.branch = "main"

        # Set dry-run environment variable
        os.environ["DRY_RUN"] = "true"

        config = MockConfig()
        deployment = CloudflarePagesDeployment(config)

        with tempfile.TemporaryDirectory() as tmp_dir:
            source_path = Path(tmp_dir)
            result = deployment.deploy(source_path)

            assert result["success"] is True
            assert result["provider"] == "cloudflare"
            assert result["url"] == "https://test_project.test_account.pages.dev/"
            assert "Dry-run deployment simulation" in result["message"]

            # Verify subprocess was not called
            mock_run.assert_not_called()

        # Clean up environment variable
        del os.environ["DRY_RUN"]

    def test_github_pages_deployment_nonexistent_source(self):
        """Test GitHub Pages deployment with nonexistent source directory."""
        class MockConfig:
            def __init__(self):
                self.owner = "test_owner"
                self.repo = "test_repo"
                self.branch = "gh-pages"
                self.token = ""

        config = MockConfig()
        deployment = GitHubPagesDeployment(config)

        # Try to deploy from a nonexistent directory
        nonexistent_path = Path("/nonexistent/directory")
        with pytest.raises(ValueError, match="does not exist"):
            deployment.deploy(nonexistent_path)

    def test_cloudflare_pages_deployment_nonexistent_source(self):
        """Test Cloudflare Pages deployment with nonexistent source directory."""
        class MockConfig:
            def __init__(self):
                self.account_id = "test_account"
                self.project_name = "test_project"
                self.api_token = ""
                self.branch = "main"

        config = MockConfig()
        deployment = CloudflarePagesDeployment(config)

        # Try to deploy from a nonexistent directory
        nonexistent_path = Path("/nonexistent/directory")
        with pytest.raises(ValueError, match="does not exist"):
            deployment.deploy(nonexistent_path)

    @patch("src.deployment.subprocess.run")
    def test_cloudflare_pages_missing_wrangler(self, mock_run):
        """Test Cloudflare Pages deployment with missing wrangler."""
        # Mock subprocess.run to raise FileNotFoundError for wrangler --version
        mock_run.side_effect = FileNotFoundError()

        class MockConfig:
            def __init__(self):
                self.account_id = "test_account"
                self.project_name = "test_project"
                self.api_token = "test_token"
                self.branch = "main"

        config = MockConfig()
        deployment = CloudflarePagesDeployment(config)

        with tempfile.TemporaryDirectory() as tmp_dir:
            source_path = Path(tmp_dir)
            result = deployment.deploy(source_path)

            assert result["success"] is False
            assert result["provider"] == "cloudflare"
            assert "Wrangler CLI is not installed" in result["error"]

    def test_deployment_factory_create_github_service(self):
        """Test deployment factory creating GitHub service."""
        class MockConfig:
            def __init__(self):
                self.owner = "test_owner"
                self.repo = "test_repo"
                self.branch = "gh-pages"
                self.token = ""

        config = MockConfig()
        deployment = DeploymentFactory.create_deployment_service("github", config)

        assert isinstance(deployment, GitHubPagesDeployment)
        assert deployment.name == "GitHub Pages"

    def test_deployment_factory_create_cloudflare_service(self):
        """Test deployment factory creating Cloudflare service."""
        class MockConfig:
            def __init__(self):
                self.account_id = "test_account"
                self.project_name = "test_project"
                self.api_token = ""
                self.branch = "main"

        config = MockConfig()
        deployment = DeploymentFactory.create_deployment_service("cloudflare", config)

        assert isinstance(deployment, CloudflarePagesDeployment)
        assert deployment.name == "Cloudflare Pages"

    def test_deployment_factory_invalid_provider(self):
        """Test deployment factory with invalid provider."""
        class MockConfig:
            pass

        config = MockConfig()

        with pytest.raises(ValueError, match="Unsupported deployment provider"):
            DeploymentFactory.create_deployment_service("invalid_provider", config)
