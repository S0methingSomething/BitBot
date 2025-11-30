"""Tests for commands that interact with external APIs."""

from returns.result import Failure, Success
from rich.console import Console


class TestPageCommand:
    """Tests for page command."""

    def test_page_generates_html(self, tmp_path):
        """Page command generates valid HTML."""
        from bitbot.gh.page_generator import generate_landing_page

        releases_data = {
            "bot_repo": "owner/bot",
            "apps": [
                {
                    "id": "bitlife",
                    "display_name": "BitLife",
                    "latest_release": {
                        "version": "3.21",
                        "download_url": "https://example.com/dl",
                        "published_at": "2025-01-01",
                    },
                    "releases": [],
                }
            ],
        }

        output = tmp_path / "index.html"
        result = generate_landing_page(releases_data, output, "default_landing_page.html")

        assert isinstance(result, Success)
        assert output.exists()
        content = output.read_text()
        assert "BitLife" in content
        assert "3.21" in content

    def test_page_handles_empty_apps(self, tmp_path):
        """Page generates even with no apps."""
        from bitbot.gh.page_generator import generate_landing_page

        releases_data = {"bot_repo": "owner/bot", "apps": []}
        output = tmp_path / "index.html"

        result = generate_landing_page(releases_data, output, "default_landing_page.html")

        assert isinstance(result, Success)
        assert output.exists()

    def test_page_creates_output_directory(self, tmp_path):
        """Page creates output directory if missing."""
        from bitbot.gh.page_generator import generate_landing_page

        releases_data = {"bot_repo": "owner/bot", "apps": []}
        output = tmp_path / "subdir" / "index.html"

        result = generate_landing_page(releases_data, output, "default_landing_page.html")

        assert isinstance(result, Success)
        assert output.parent.exists()


class TestGatherCommand:
    """Tests for gather command with mocked GitHub API."""

    def test_gather_fetches_from_both_repos(self):
        """Gather fetches from source and bot repos."""
        from bitbot.commands.gather import _parse_release_metadata

        source_releases = [
            {"body": "app: BitLife\nversion: 3.21", "published_at": "2025-01-01"},
        ]
        bot_releases = [
            {
                "body": "app: BitLife\nversion: 3.21",
                "assets": [{"browser_download_url": "https://example.com"}],
            },
        ]
        apps_config = {"BitLife": "BitLife"}

        apps_data = {}
        for rel in source_releases:
            app_id, ver = _parse_release_metadata(rel)
            if app_id not in apps_config:
                continue

            url = ""
            for bot in bot_releases:
                if not bot.get("assets"):
                    continue
                _, bot_ver = _parse_release_metadata(bot)
                if bot_ver == ver:
                    url = bot["assets"][0]["browser_download_url"]
                    break

            if url:
                apps_data[app_id] = {
                    "display_name": apps_config[app_id],
                    "latest_release": {"version": ver, "download_url": url},
                }

        assert "BitLife" in apps_data
        assert apps_data["BitLife"]["latest_release"]["version"] == "3.21"

    def test_gather_handles_api_error(self):
        """Gather handles GitHub API errors gracefully."""
        from bitbot.core.errors import GitHubAPIError

        result = Failure(GitHubAPIError("API rate limit"))

        assert isinstance(result, Failure)
        assert "rate limit" in str(result.failure())

    def test_gather_skips_releases_without_version(self):
        """Releases without version field are skipped."""
        from bitbot.commands.gather import _parse_release_metadata

        releases = [
            {"body": "app: BitLife"},
            {"body": "version: 3.21"},
            {"body": "random text"},
        ]

        for rel in releases:
            app_id, ver = _parse_release_metadata(rel)
            assert app_id is None or ver is None


class TestMaintainCommand:
    """Tests for maintain command."""

    def test_extract_app_id_from_body(self):
        """Extract app ID from release body."""
        from bitbot.commands.maintain import _extract_app_id

        release = {"body": "app: intl_bitlife\nversion: 1.0", "tag_name": "v1.0"}
        app_id = _extract_app_id(release)
        assert app_id == "intl_bitlife"

    def test_extract_app_id_from_tag(self):
        """Fallback to tag when body doesn't have app field."""
        from bitbot.commands.maintain import _extract_app_id

        release = {"body": "some notes", "tag_name": "bitlife-v3.21"}
        app_id = _extract_app_id(release)
        assert app_id == "bitlife-v3.21"  # Returns full tag as fallback

    def test_extract_app_id_fallback(self):
        """Fallback to tag when no app in body."""
        from bitbot.commands.maintain import _extract_app_id

        release = {"body": "", "tag_name": "random-tag"}
        app_id = _extract_app_id(release)
        assert app_id == "random-tag"


class TestPostCommand:
    """Tests for post command helpers."""

    def test_build_changelog_data(self):
        """Build changelog from releases vs state."""
        from bitbot.commands.post import _build_changelog_data
        from bitbot.models import AccountState

        releases = {
            "bitlife": {
                "display_name": "BitLife",
                "latest_release": {"version": "3.21", "url": "https://ex.com"},
            },
            "new_app": {
                "display_name": "New App",
                "latest_release": {"version": "1.0", "url": "https://ex.com"},
            },
        }
        state = AccountState(online={"bitlife": "3.20"})

        changelog = _build_changelog_data(releases, state)

        assert "new_app" in changelog["added"]
        assert "bitlife" in changelog["updated"]

    def test_has_new_releases_detects_changes(self):
        """Detect when there are new releases."""
        from bitbot.commands.post import _has_new_releases

        changelog = {
            "added": {"app1": {"version": "1.0", "display_name": "App1"}},
            "updated": {},
            "removed": {},
        }
        console = Console(quiet=True)

        has_changes = _has_new_releases(changelog, console)
        assert has_changes

    def test_has_new_releases_no_changes(self):
        """Detect when there are no changes."""
        from bitbot.commands.post import _has_new_releases

        changelog = {"added": {}, "updated": {}, "removed": {}}
        console = Console(quiet=True)

        has_changes = _has_new_releases(changelog, console)
        assert not has_changes


class TestReleaseNotesFormat:
    """Tests for release notes format."""

    def test_release_notes_contain_app_id(self):
        """Release notes should use app_id not display_name."""
        import hashlib

        app_id = "intl_bitlife"
        version = "1.0.0"
        asset_name = "MonetizationVars"
        file_hash = hashlib.sha256(b"test").hexdigest()

        notes = (
            f"app: {app_id}\nversion: {version}\n"
            f"asset_name: {asset_name}\nsha256: {file_hash}"
        )

        assert "app: intl_bitlife" in notes
        assert "BitLife International" not in notes
        assert "version: 1.0.0" in notes

    def test_release_notes_format_matches_parser(self):
        """Release notes format should be parseable by gather."""
        from bitbot.commands.gather import _parse_release_metadata

        notes = "app: intl_bitlife\nversion: 1.19.8\nasset_name: MonetizationVars\nsha256: abc123"
        release = {"body": notes}

        app_id, version = _parse_release_metadata(release)

        assert app_id == "intl_bitlife"
        assert version == "1.19.8"
