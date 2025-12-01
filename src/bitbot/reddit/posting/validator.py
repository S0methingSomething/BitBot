"""Post validation to catch issues before/after posting."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING
from urllib.parse import urlparse

from beartype import beartype

from bitbot.config_models import Config  # noqa: TC001 - needed for beartype

if TYPE_CHECKING:
    import praw


@dataclass
class ValidationIssue:
    """A validation issue found in a post."""

    severity: str  # "error", "warning"
    message: str


@dataclass
class ValidationResult:
    """Result of post validation."""

    issues: list[ValidationIssue]

    @property
    def has_errors(self) -> bool:
        """Check if any errors found."""
        return any(i.severity == "error" for i in self.issues)

    @property
    def has_warnings(self) -> bool:
        """Check if any warnings found."""
        return any(i.severity == "warning" for i in self.issues)

    @property
    def is_valid(self) -> bool:
        """Check if post is valid (no errors)."""
        return not self.has_errors


# Patterns for malformed URLs
_MALFORMED_URL_PATTERNS = [
    (r"https?://https?://", "Double protocol (https://https://)"),
    (r"htttps://", "Typo in protocol (htttps)"),
    (r"httttp://", "Typo in protocol (httttp)"),
    (r"httpss://", "Typo in protocol (httpss)"),
    (r"htp://", "Typo in protocol (htp)"),
    (r"\(https?://\s*\)", "Empty URL in markdown link"),
    (r"https?://\s+", "URL with trailing whitespace"),
    (r"https?://[^)\s]*\s+[^)\s]+\)", "URL with space in middle"),
    (r"https?://$", "URL with no domain"),
    (r"https?://\)", "URL immediately followed by )"),
]

# Pattern to extract all URLs
_URL_PATTERN = re.compile(r'https?://[^\s\)\]"\'<>]+')


@beartype
def _validate_urls(body: str, issues: list[ValidationIssue]) -> None:
    """Validate all URLs in the body."""
    # Check for known malformed patterns
    for pattern, description in _MALFORMED_URL_PATTERNS:
        if re.search(pattern, body, re.IGNORECASE):
            issues.append(ValidationIssue("error", f"Malformed URL detected: {description}"))

    # Extract and validate each URL
    urls = _URL_PATTERN.findall(body)
    for url in urls:
        # Clean trailing punctuation that might have been captured
        url = url.rstrip(".,;:!?")
        
        try:
            parsed = urlparse(url)
            
            # Check for valid scheme
            if parsed.scheme not in ("http", "https"):
                issues.append(ValidationIssue("error", f"Invalid URL scheme: {url[:50]}"))
                continue
            
            # Check for valid netloc (domain)
            if not parsed.netloc:
                issues.append(ValidationIssue("error", f"URL missing domain: {url[:50]}"))
                continue
            
            # Check for suspicious patterns in domain
            if "https" in parsed.netloc.lower() or "http" in parsed.netloc.lower():
                issues.append(ValidationIssue("error", f"URL has protocol in domain: {url[:50]}"))
                continue
            
            # Check for double slashes in path (excluding the protocol)
            if "//" in parsed.path:
                issues.append(ValidationIssue("warning", f"URL has double slashes in path: {url[:50]}"))
            
            # Check for common typos in known domains
            domain = parsed.netloc.lower()
            if "githbu" in domain or "guthub" in domain:
                issues.append(ValidationIssue("error", f"Typo in GitHub domain: {url[:50]}"))
            if "redidt" in domain or "redit" in domain:
                issues.append(ValidationIssue("error", f"Typo in Reddit domain: {url[:50]}"))
                
        except Exception:
            issues.append(ValidationIssue("error", f"Invalid URL format: {url[:50]}"))


@beartype
def _validate_markdown_links(body: str, issues: list[ValidationIssue]) -> None:
    """Validate markdown link syntax."""
    # Find all markdown links: [text](url)
    link_pattern = re.compile(r'\[([^\]]*)\]\(([^)]*)\)')
    
    for match in link_pattern.finditer(body):
        text, url = match.groups()
        
        # Check for empty text
        if not text.strip():
            issues.append(ValidationIssue("warning", f"Link with empty text: [{text}]({url[:30]}...)"))
        
        # Check for empty URL
        if not url.strip():
            issues.append(ValidationIssue("error", f"Link with empty URL: [{text[:20]}]()"))
            continue
        
        # Check URL starts with valid protocol or is relative
        url_stripped = url.strip()
        if url_stripped and not url_stripped.startswith(("http://", "https://", "/", "#")):
            # Could be a relative URL or malformed
            if "." in url_stripped and not url_stripped.startswith("."):
                issues.append(ValidationIssue("warning", f"Link may be missing protocol: {url_stripped[:50]}"))


@beartype
def validate_post(title: str, body: str, config: Config) -> ValidationResult:
    """Validate a post for common issues."""
    issues: list[ValidationIssue] = []

    # Get limits from config
    safety = config.safety
    title_max = safety.get("title_max_length", 300)
    title_min = safety.get("title_min_length", 10)
    body_min = safety.get("body_min_length", 50)
    body_max = safety.get("body_max_length", 40000)

    # Title checks
    _validate_title(title, issues, title_max, title_min)

    # Body checks
    _validate_body(body, issues, body_min, body_max)
    
    # URL validation (critical!)
    _validate_urls(body, issues)
    
    # Markdown link validation
    _validate_markdown_links(body, issues)

    return ValidationResult(issues=issues)


def _validate_title(title: str, issues: list[ValidationIssue], max_len: int, min_len: int) -> None:
    """Validate title."""
    if len(title) > max_len:
        issues.append(ValidationIssue("error", f"Title too long: {len(title)}/{max_len} chars"))
    if len(title) < min_len:
        issues.append(ValidationIssue("warning", "Title seems too short"))
    if "{{" in title or "}}" in title:
        issues.append(ValidationIssue("error", "Unresolved placeholder in title"))


def _validate_body(body: str, issues: list[ValidationIssue], min_len: int, max_len: int) -> None:
    """Validate body."""
    if not body or len(body.strip()) < min_len:
        issues.append(ValidationIssue("error", "Post body too short or empty"))

    if len(body) > max_len:
        issues.append(ValidationIssue("error", f"Body too long: {len(body)}/{max_len} chars"))

    # Check for unresolved placeholders
    placeholders = re.findall(r"\{\{[^}]+\}\}", body)
    if placeholders:
        issues.append(
            ValidationIssue("error", f"Unresolved placeholders: {', '.join(placeholders[:3])}")
        )

    # Check for broken markdown links
    broken_links = re.findall(r"\[([^\]]*)\]\(\s*\)", body)
    if broken_links:
        issues.append(ValidationIssue("error", f"Broken links (empty URL): {broken_links[:3]}"))

    # Check for empty link text
    if re.search(r"\[\s*\]\([^)]+\)", body):
        issues.append(ValidationIssue("warning", "Links with empty text found"))

    # Check version numbers
    if not re.search(r"v?\d+\.\d+(\.\d+)?", body):
        issues.append(ValidationIssue("warning", "No version numbers found in post"))

    # Check for URLs
    if "http" not in body.lower():
        issues.append(ValidationIssue("warning", "No URLs found in post"))

    # Check section headers
    if "###" not in body and "##" not in body:
        issues.append(ValidationIssue("warning", "No section headers found"))
    
    # Check for common template issues
    if "None" in body and ("version" in body.lower() or "url" in body.lower()):
        issues.append(ValidationIssue("warning", "Possible None value in template output"))
    
    if "undefined" in body.lower():
        issues.append(ValidationIssue("warning", "Possible undefined value in template output"))


@beartype
def validate_posted(submission: praw.models.Submission) -> ValidationResult:
    """Validate a post after it's been submitted."""
    issues: list[ValidationIssue] = []

    if submission.removed_by_category:
        issues.append(ValidationIssue("error", f"Post removed: {submission.removed_by_category}"))

    if hasattr(submission, "spam") and submission.spam:
        issues.append(ValidationIssue("error", "Post marked as spam"))

    if submission.score < 0:
        issues.append(ValidationIssue("warning", f"Post has negative score: {submission.score}"))

    return ValidationResult(issues=issues)


@beartype
def validate_url(url: str) -> list[str]:
    """Validate a single URL and return list of issues."""
    issues: list[str] = []
    
    if not url:
        issues.append("URL is empty")
        return issues
    
    # Check for double protocol
    if url.count("://") > 1:
        issues.append("URL has multiple protocols")
    
    # Check for typos
    if "htttps" in url.lower() or "htttp" in url.lower():
        issues.append("URL has typo in protocol")
    
    try:
        parsed = urlparse(url)
        if not parsed.scheme:
            issues.append("URL missing scheme (http/https)")
        if not parsed.netloc:
            issues.append("URL missing domain")
        if parsed.scheme and parsed.scheme not in ("http", "https"):
            issues.append(f"Invalid scheme: {parsed.scheme}")
    except Exception as e:
        issues.append(f"URL parse error: {e}")
    
    return issues
