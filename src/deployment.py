"""Deployment services for BitBot - supports multiple deployment targets."""

import json
import os
import re
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

    def _check_project_exists(self) -> bool:
        """Check if the Cloudflare Pages project exists.

        Returns:
            True if project exists, False otherwise
        """
        try:
            # Use curl to check if project exists
            cmd = [
                "curl",
                "-s",
                "-H", f"Authorization: Bearer {self.api_token}",
                "-H", "Content-Type: application/json",
                f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/pages/projects/{self.project_name}"
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            response = json.loads(result.stdout)
            return bool(response.get("success", False))
        except (subprocess.CalledProcessError, json.JSONDecodeError, Exception) as e:
            logger.debug(f"Error checking project existence: {e}")
            return False

    def _create_project(self) -> bool:
        """Create a new Cloudflare Pages project.

        Returns:
            True if project was created successfully, False otherwise
        """
        try:
            # Prepare project creation data
            data = {
                "name": self.project_name,
                "production_branch": self.branch
            }

            # Use curl to create the project
            cmd = [
                "curl",
                "-s",
                "-X", "POST",
                "-H", f"Authorization: Bearer {self.api_token}",
                "-H", "Content-Type: application/json",
                "-d", json.dumps(data),
                f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/pages/projects"
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            response = json.loads(result.stdout)
            return bool(response.get("success", False))
        except (subprocess.CalledProcessError, json.JSONDecodeError, Exception) as e:
            logger.error(f"Error creating project: {e}")
            return False

    def deploy(self, source_dir: Path) -> dict[str, Any]:
        """Deploy to Cloudflare Pages with automatic project creation.

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
                logger.info(
                    f"DRY_RUN: Would deploy to Cloudflare Pages from {source_dir}"
                )
                # Use the correct default Cloudflare Pages URL format
                return {
                    "success": True,
                    "provider": "cloudflare",
                    "url": f"https://{self.project_name}.{self.account_id}.pages.dev/",
                    "message": "Dry-run deployment simulation",
                }

            # Check if wrangler is installed
            try:
                subprocess.run(["/usr/bin/npx", "wrangler", "--version"], capture_output=True, check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                logger.error("Wrangler CLI is not installed. Please install it with: npm install -g wrangler")
                return {
                    "success": False,
                    "provider": "cloudflare",
                    "url": "",
                    "error": "Wrangler CLI is not installed. Please install it with: npm install -g wrangler",
                }

            # Check if project exists, create if it doesn't
            if not self._check_project_exists():
                logger.info(f"Project {self.project_name} does not exist. Creating...")
                if not self._create_project():
                    logger.error(f"Failed to create project {self.project_name}")
                    return {
                        "success": False,
                        "provider": "cloudflare",
                        "url": "",
                        "error": f"Failed to create project {self.project_name}",
                    }
                logger.info(f"Successfully created project {self.project_name}")

            # Prepare wrangler command for Cloudflare Pages deployment
            cmd = [
                "/usr/bin/npx",
                "wrangler",
                "pages",
                "deploy",
                str(source_dir),
                "--project-name",
                self.project_name,
                "--branch",
                self.branch,
            ]

            # Set environment variables
            env = dict(os.environ)
            if self.api_token:
                env["CLOUDFLARE_API_TOKEN"] = self.api_token

            result = subprocess.run(
                cmd, capture_output=True, text=True, check=True, env=env
            )

            # Parse the URL from the wrangler output
            # The output contains a line like:
            # "✨ Deployment complete! Take a peek over at https://0a550b22.bitedit.pages.dev"
            output = result.stdout.strip()
            url = f"https://{self.project_name}.{self.account_id}.pages.dev/"

            # Extract the actual deployment URL from wrangler output
            url_match = re.search(r"https://[^\s]+\.pages\.dev", output)
            if url_match:
                url = url_match.group(0)

            return {
                "success": True,
                "provider": "cloudflare",
                "url": url,
                "message": output,
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
        return f"https://{self.project_name}.{self.account_id}.pages.dev/"

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
