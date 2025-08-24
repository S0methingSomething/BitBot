"""Deployment services for BitBot - supports multiple deployment targets."""

import os
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from logging_config import get_logger

logger = get_logger(__name__)


class DeploymentService(ABC):
    """Abstract base class for deployment services."""

    @abstractmethod
    def deploy(self, source_dir: Path) -> dict[str, Any]:
        """Deploy the content to the target platform.

        Args:
            source_dir: Directory containing files to deploy
            **kwargs: Additional deployment parameters

        Returns:
            Dictionary with deployment results including URLs
        """

    @abstractmethod
    def get_deployment_url(self) -> str:
        """Get the deployment URL for this service."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Get the name of this deployment service."""


class GitHubPagesDeployment(DeploymentService):
    """GitHub Pages deployment service."""

    def __init__(self, config: Any):
        """Initialize GitHub Pages deployment service.

        Args:
            config: Configuration object with GitHub Pages settings
        """
        self.config = config
        self.owner = getattr(config, "owner", "")
        self.repo = getattr(config, "repo", "")
        self.branch = getattr(config, "branch", "gh-pages")
        self.token = getattr(config, "token", "")

    def deploy(self, source_dir: Path) -> dict[str, Any]:
        """Deploy to GitHub Pages using GitHub CLI.

        Args:
            source_dir: Directory containing files to deploy

        Returns:
            Dictionary with deployment results
        """
        if not source_dir.exists():
            raise ValueError(f"Source directory does not exist: {source_dir}")

        try:
            # In dry-run mode, just simulate deployment
            if os.environ.get("DRY_RUN", "").lower() in ["true", "1", "yes"]:
                logger.info(f"DRY_RUN: Would deploy to GitHub Pages from {source_dir}")
                return {
                    "success": True,
                    "provider": "github",
                    "url": f"https://{self.owner}.github.io/{self.repo}/",
                    "message": "Dry-run deployment simulation",
                }

            # Real deployment using GitHub CLI
            cmd = [
                "gh",
                "workflow",
                "run",
                "deploy.yml",
                "--repo",
                f"{self.owner}/{self.repo}",
                "-f",
                f"source={source_dir}",
                "-f",
                f"branch={self.branch}",
            ]

            if self.token:
                cmd.extend(["-F", f"token={self.token}"])

            result = subprocess.run(cmd, capture_output=True, text=True, check=True, env=dict(os.environ))

            return {
                "success": True,
                "provider": "github",
                "url": f"https://{self.owner}.github.io/{self.repo}/",
                "message": result.stdout.strip(),
            }
        except subprocess.CalledProcessError as e:
            logger.error(f"GitHub Pages deployment failed: {e.stderr}")
            return {
                "success": False,
                "provider": "github",
                "url": "",
                "error": e.stderr,
            }
        except Exception as e:
            logger.error(f"GitHub Pages deployment failed: {e!s}")
            return {"success": False, "provider": "github", "url": "", "error": str(e)}

    def get_deployment_url(self) -> str:
        """Get the GitHub Pages URL."""
        return f"https://{self.owner}.github.io/{self.repo}/"

    @property
    def name(self) -> str:
        """Get the name of this deployment service."""
        return "GitHub Pages"


class CloudflarePagesDeployment(DeploymentService):
    """Cloudflare Pages deployment service."""

    def __init__(self, config: Any):
        """Initialize Cloudflare Pages deployment service.

        Args:
            config: Configuration object with Cloudflare Pages settings
        """
        self.config = config
        self.account_id = getattr(config, "account_id", "")
        self.project_name = getattr(config, "project_name", "")
        self.api_token = getattr(config, "api_token", "")
        self.branch = getattr(config, "branch", "main")

    def deploy(self, source_dir: Path) -> dict[str, Any]:
        """Deploy to Cloudflare Pages.

        Args:
            source_dir: Directory containing files to deploy
            **kwargs: Additional deployment parameters

        Returns:
            Dictionary with deployment results
        """
        if not source_dir.exists():
            raise ValueError(f"Source directory does not exist: {source_dir}")

        try:
            # In dry-run mode, just simulate deployment
            if os.environ.get("DRY_RUN", "").lower() in ["true", "1", "yes"]:
                logger.info(
                    f"DRY_RUN: Would deploy to Cloudflare Pages from {source_dir}"
                )
                return {
                    "success": True,
                    "provider": "cloudflare",
                    "url": f"https://{self.project_name}.{self.account_id}.cloudflareworkers.com/",
                    "message": "Dry-run deployment simulation",
                }

            # Prepare wrangler command for Cloudflare Pages deployment
            cmd = [
                "wrangler",
                "pages",
                "deploy",
                str(source_dir),
                "--project-name",
                self.project_name,
                "--branch",
                self.branch,
            ]

            if self.api_token:
                env = dict(os.environ)
                env["CLOUDFLARE_API_TOKEN"] = self.api_token
            else:
                env = dict(os.environ)

            result = subprocess.run(
                cmd, capture_output=True, text=True, check=True, env=env
            )

            return {
                "success": True,
                "provider": "cloudflare",
                "url": f"https://{self.project_name}.cloudflareworkers.com/",
                "message": result.stdout.strip(),
            }
        except subprocess.CalledProcessError as e:
            logger.error(f"Cloudflare Pages deployment failed: {e.stderr}")
            return {
                "success": False,
                "provider": "cloudflare",
                "url": "",
                "error": e.stderr,
            }
        except Exception as e:
            logger.error(f"Cloudflare Pages deployment failed: {e!s}")
            return {
                "success": False,
                "provider": "cloudflare",
                "url": "",
                "error": str(e),
            }

    def get_deployment_url(self) -> str:
        """Get the Cloudflare Pages URL."""
        return f"https://{self.project_name}.cloudflareworkers.com/"

    @property
    def name(self) -> str:
        """Get the name of this deployment service."""
        return "Cloudflare Pages"


class DeploymentFactory:
    """Factory for creating deployment services."""

    @staticmethod
    def create_deployment_service(provider: str, config: Any) -> DeploymentService:
        """Create a deployment service based on provider.

        Args:
            provider: Provider name ('github' or 'cloudflare')
            config: Configuration object for the provider

        Returns:
            DeploymentService instance

        Raises:
            ValueError: If provider is not supported
        """
        if provider.lower() == "github":
            return GitHubPagesDeployment(config)
        if provider.lower() == "cloudflare":
            return CloudflarePagesDeployment(config)
        raise ValueError(f"Unsupported deployment provider: {provider}")
