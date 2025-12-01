"""Post validation to catch issues before/after posting."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

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
