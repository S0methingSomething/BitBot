#!/usr/bin/env python3
"""Code quality depth analyzer - checks for placeholders, stubs, and incomplete implementations."""

import ast
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class QualityIssue:
    """A code quality issue."""

    file: str
    line: int
    function: str
    issue_type: str
    description: str


class QualityAnalyzer(ast.NodeVisitor):
    """AST visitor for analyzing code quality depth."""

    def __init__(self, content: str, filepath: Path):
        self.content = content
        self.filepath = filepath
        self.issues: list[QualityIssue] = []
        self.lines = content.split("\n")

    def visit_FunctionDef(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        """Visit function definition."""
        if node.name.startswith("_") and node.name != "__init__":
            return

        func_name = node.name

        # Check docstring quality
        docstring = ast.get_docstring(node)
        if docstring:
            self._check_docstring_quality(node, func_name, docstring)

        # Check for stub implementations
        self._check_stub_implementation(node, func_name)

        # Check for placeholder comments
        self._check_placeholder_comments(node, func_name)

        # Check for debug code
        self._check_debug_code(node, func_name)

        # Check error handling
        self._check_error_handling(node, func_name)

        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """Visit async function definition."""
        self.visit_FunctionDef(node)

    def _check_docstring_quality(
        self, node: ast.FunctionDef | ast.AsyncFunctionDef, func_name: str, docstring: str
    ) -> None:
        """Check if docstring is meaningful."""
        # Placeholder patterns
        placeholders = ["todo", "tbd", "fixme", "...", "placeholder"]
        if any(p in docstring.lower() for p in placeholders):
            self.issues.append(
                QualityIssue(
                    file=str(self.filepath.relative_to("src")),
                    line=node.lineno,
                    function=func_name,
                    issue_type="placeholder_docstring",
                    description=f"Docstring contains placeholder: {docstring[:50]}",
                )
            )

        # Too short (single word or < 10 chars)
        if len(docstring.strip()) < 10:
            self.issues.append(
                QualityIssue(
                    file=str(self.filepath.relative_to("src")),
                    line=node.lineno,
                    function=func_name,
                    issue_type="short_docstring",
                    description=f"Docstring too short: '{docstring.strip()}'",
                )
            )

    def _check_stub_implementation(
        self, node: ast.FunctionDef | ast.AsyncFunctionDef, func_name: str
    ) -> None:
        """Check if function is just a stub."""
        # Get function body (skip docstring)
        body = node.body
        if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant):
            body = body[1:]  # Skip docstring

        if not body:
            self.issues.append(
                QualityIssue(
                    file=str(self.filepath.relative_to("src")),
                    line=node.lineno,
                    function=func_name,
                    issue_type="empty_function",
                    description="Function has no implementation (only docstring)",
                )
            )
            return

        # Check for pass statement
        if len(body) == 1 and isinstance(body[0], ast.Pass):
            self.issues.append(
                QualityIssue(
                    file=str(self.filepath.relative_to("src")),
                    line=node.lineno,
                    function=func_name,
                    issue_type="stub_function",
                    description="Function only contains 'pass'",
                )
            )

        # Check for NotImplementedError
        for stmt in ast.walk(node):
            if isinstance(stmt, ast.Raise):
                if isinstance(stmt.exc, ast.Name) and stmt.exc.id == "NotImplementedError":
                    self.issues.append(
                        QualityIssue(
                            file=str(self.filepath.relative_to("src")),
                            line=stmt.lineno,
                            function=func_name,
                            issue_type="not_implemented",
                            description="Function raises NotImplementedError",
                        )
                    )

    def _check_placeholder_comments(
        self, node: ast.FunctionDef | ast.AsyncFunctionDef, func_name: str
    ) -> None:
        """Check for TODO/FIXME comments."""
        func_start = node.lineno
        func_end = node.end_lineno or func_start

        for line_num in range(func_start - 1, min(func_end, len(self.lines))):
            line = self.lines[line_num]
            if any(marker in line for marker in ["# TODO", "# FIXME", "# HACK", "# XXX"]):
                self.issues.append(
                    QualityIssue(
                        file=str(self.filepath.relative_to("src")),
                        line=line_num + 1,
                        function=func_name,
                        issue_type="placeholder_comment",
                        description=f"Placeholder comment: {line.strip()}",
                    )
                )

    def _check_debug_code(
        self, node: ast.FunctionDef | ast.AsyncFunctionDef, func_name: str
    ) -> None:
        """Check for debug print statements."""
        for stmt in ast.walk(node):
            if isinstance(stmt, ast.Call):
                if isinstance(stmt.func, ast.Name) and stmt.func.id == "print":
                    self.issues.append(
                        QualityIssue(
                            file=str(self.filepath.relative_to("src")),
                            line=stmt.lineno,
                            function=func_name,
                            issue_type="debug_print",
                            description="Uses print() instead of logger",
                        )
                    )

    def _check_error_handling(
        self, node: ast.FunctionDef | ast.AsyncFunctionDef, func_name: str
    ) -> None:
        """Check for poor error handling."""
        for stmt in ast.walk(node):
            if isinstance(stmt, ast.ExceptHandler):
                # Bare except
                if stmt.type is None:
                    self.issues.append(
                        QualityIssue(
                            file=str(self.filepath.relative_to("src")),
                            line=stmt.lineno,
                            function=func_name,
                            issue_type="bare_except",
                            description="Bare except: clause (catches all exceptions)",
                        )
                    )

                # except Exception: pass
                if stmt.type and isinstance(stmt.type, ast.Name) and stmt.type.id == "Exception":
                    if len(stmt.body) == 1 and isinstance(stmt.body[0], ast.Pass):
                        self.issues.append(
                            QualityIssue(
                                file=str(self.filepath.relative_to("src")),
                                line=stmt.lineno,
                                function=func_name,
                                issue_type="silent_exception",
                                description="Silent exception handling (except Exception: pass)",
                            )
                        )


def analyze_file(filepath: Path) -> list[QualityIssue]:
    """Analyze a single file for quality issues."""
    try:
        with open(filepath, encoding="utf-8") as f:
            content = f.read()

        tree = ast.parse(content, filename=str(filepath))
        analyzer = QualityAnalyzer(content, filepath)
        analyzer.visit(tree)

        return analyzer.issues

    except SyntaxError:
        return []
    except Exception:
        return []


def main() -> None:
    """Run code quality depth analysis."""
    src_dir = Path("src")
    all_issues: list[QualityIssue] = []

    # Analyze all files
    for filepath in sorted(src_dir.rglob("*.py")):
        if filepath.name == "__init__.py":
            continue

        issues = analyze_file(filepath)
        all_issues.extend(issues)

    # Group by issue type
    issues_by_type: dict[str, list[QualityIssue]] = {}
    for issue in all_issues:
        if issue.issue_type not in issues_by_type:
            issues_by_type[issue.issue_type] = []
        issues_by_type[issue.issue_type].append(issue)

    # Print report
    print("=== CODE QUALITY DEPTH ANALYSIS ===\n")

    if not all_issues:
        print("✅ No quality issues found! Code is production-ready.\n")
        return

    print(f"⚠️  Found {len(all_issues)} quality issues\n")

    # Issue type descriptions
    issue_descriptions = {
        "placeholder_docstring": "Docstrings with TODO/TBD/FIXME",
        "short_docstring": "Docstrings too short (<10 chars)",
        "empty_function": "Functions with no implementation",
        "stub_function": "Functions with only 'pass'",
        "not_implemented": "Functions raising NotImplementedError",
        "placeholder_comment": "TODO/FIXME/HACK comments",
        "debug_print": "Debug print() statements",
        "bare_except": "Bare except: clauses",
        "silent_exception": "Silent exception handling",
    }

    for issue_type, issues in sorted(issues_by_type.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"❌ {issue_type.upper().replace('_', ' ')} ({len(issues)} occurrences)")
        print(f"   {issue_descriptions.get(issue_type, 'Quality issue')}")

        for issue in issues[:5]:  # Show first 5
            print(f"   • {issue.file}:{issue.line} - {issue.function}()")
            print(f"     {issue.description}")

        if len(issues) > 5:
            print(f"   ... and {len(issues) - 5} more")
        print()

    # Calculate quality score
    total_functions = len(set((i.file, i.function) for i in all_issues))
    quality_score = max(0, 100 - (len(all_issues) * 2))  # -2 points per issue

    print(f"🎯 CODE QUALITY SCORE: {quality_score}/100")

    if quality_score >= 90:
        print("✅ Excellent - production ready")
    elif quality_score >= 70:
        print("⚠️  Good - minor issues to address")
    elif quality_score >= 50:
        print("⚠️  Fair - several issues need attention")
    else:
        print("❌ Poor - significant quality issues")

    # Exit with error if critical issues
    critical_issues = ["stub_function", "not_implemented", "empty_function"]
    if any(issue_type in issues_by_type for issue_type in critical_issues):
        sys.exit(1)


if __name__ == "__main__":
    main()
