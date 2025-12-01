"""Tests for post validation."""

from bitbot.reddit.posting.validator import ValidationResult, validate_post, validate_url


class TestValidateUrl:
    """Tests for URL validation."""

    def test_valid_https_url(self):
        """Valid HTTPS URL passes."""
        issues = validate_url("https://github.com/user/repo")
        assert issues == []

    def test_valid_http_url(self):
        """Valid HTTP URL passes."""
        issues = validate_url("http://example.com/path")
        assert issues == []

    def test_empty_url(self):
        """Empty URL fails."""
        issues = validate_url("")
        assert "URL is empty" in issues

    def test_double_protocol(self):
        """Double protocol detected."""
        issues = validate_url("https://https://example.com")
        assert any("multiple protocols" in i for i in issues)

    def test_typo_htttps(self):
        """Typo htttps detected."""
        issues = validate_url("htttps://example.com")
        assert any("typo" in i.lower() for i in issues)

    def test_missing_scheme(self):
        """Missing scheme detected."""
        issues = validate_url("example.com/path")
        assert any("scheme" in i.lower() for i in issues)

    def test_missing_domain(self):
        """Missing domain detected."""
        issues = validate_url("https://")
        assert any("domain" in i.lower() for i in issues)


class TestValidatePost:
    """Tests for pre-post validation."""

    def test_valid_post(self, config):
        """Test a valid post passes validation."""
        title = "[BitBot] BitLife v3.21.0 Released"
        body = """## Changelog

### Added
- BitLife v3.21.0

## Available Apps
| App | Version |
|-----|---------|
| BitLife | v3.21.0 |

Download: https://example.com/download
"""
        result = validate_post(title, body, config)
        assert result.is_valid
        assert not result.has_errors

    def test_title_too_long(self, config):
        """Test title exceeding 300 chars."""
        title = "x" * 301
        body = "Valid body with version v1.0.0 and https://example.com"
        result = validate_post(title, body, config)
        assert result.has_errors
        assert any("300" in i.message for i in result.issues)

    def test_empty_body(self, config):
        """Test empty body fails."""
        result = validate_post("Valid Title", "", config)
        assert result.has_errors

    def test_unresolved_placeholders_in_title(self, config):
        """Test unresolved placeholders in title."""
        title = "[BitBot] {{app_name}} Released"
        body = "Valid body v1.0.0 https://example.com"
        result = validate_post(title, body, config)
        assert result.has_errors
        assert any("placeholder" in i.message.lower() for i in result.issues)

    def test_unresolved_placeholders_in_body(self, config):
        """Test unresolved placeholders in body."""
        title = "Valid Title"
        body = "Download {{download_url}} for version v1.0.0"
        result = validate_post(title, body, config)
        assert result.has_errors
        assert any("placeholder" in i.message.lower() for i in result.issues)

    def test_broken_markdown_links(self, config):
        """Test broken markdown links detected."""
        title = "Valid Title"
        body = "Click [here]() to download v1.0.0 https://example.com"
        result = validate_post(title, body, config)
        assert result.has_errors
        assert any("broken" in i.message.lower() for i in result.issues)

    def test_no_version_warning(self, config):
        """Test warning when no version numbers."""
        title = "Valid Title"
        body = "Some content without versions https://example.com ## Section"
        result = validate_post(title, body, config)
        assert result.has_warnings
        assert any("version" in i.message.lower() for i in result.issues)

    def test_no_urls_warning(self, config):
        """Test warning when no URLs."""
        title = "Valid Title"
        body = "Some content with version v1.0.0 but no links ## Section"
        result = validate_post(title, body, config)
        assert result.has_warnings
        assert any("url" in i.message.lower() for i in result.issues)

    def test_body_too_long(self, config):
        """Test body exceeding Reddit limit."""
        title = "Valid Title"
        body = "x" * 40001
        result = validate_post(title, body, config)
        assert result.has_errors
        assert any("40000" in i.message for i in result.issues)

    def test_malformed_url_double_protocol(self, config):
        """Test double protocol URL detected."""
        title = "Valid Title"
        body = "Download from https://https://example.com v1.0.0 ## Section"
        result = validate_post(title, body, config)
        assert result.has_errors
        assert any("double protocol" in i.message.lower() for i in result.issues)

    def test_malformed_url_typo_htttps(self, config):
        """Test htttps typo detected."""
        title = "Valid Title"
        body = "Download from htttps://example.com v1.0.0 ## Section"
        result = validate_post(title, body, config)
        assert result.has_errors
        assert any("typo" in i.message.lower() for i in result.issues)

    def test_multiple_issues(self, config):
        """Test multiple issues detected."""
        title = "x" * 301  # Too long
        body = "Short"  # Too short, no version, no URL
        result = validate_post(title, body, config)
        assert len(result.issues) >= 2


class TestValidationResult:
    """Tests for ValidationResult."""

    def test_is_valid_no_issues(self):
        """Test is_valid with no issues."""
        result = ValidationResult(issues=[])
        assert result.is_valid
        assert not result.has_errors
        assert not result.has_warnings

    def test_is_valid_with_warnings_only(self):
        """Test is_valid with only warnings."""
        from bitbot.reddit.posting.validator import ValidationIssue

        result = ValidationResult(issues=[ValidationIssue("warning", "test")])
        assert result.is_valid  # Warnings don't block
        assert result.has_warnings
        assert not result.has_errors

    def test_is_valid_with_errors(self):
        """Test is_valid with errors."""
        from bitbot.reddit.posting.validator import ValidationIssue

        result = ValidationResult(issues=[ValidationIssue("error", "test")])
        assert not result.is_valid
        assert result.has_errors
