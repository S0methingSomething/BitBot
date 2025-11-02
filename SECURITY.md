# Security Policy

## Known Vulnerabilities

### PYSEC-2022-42969 (py 1.11.0)
- **Severity**: Low
- **Package**: `py` (transitive dependency via `pdbpp`)
- **Type**: ReDoS (Regular Expression Denial of Service)
- **Description**: The py library through 1.11.0 allows remote attackers to conduct a ReDoS attack via a Subversion repository with crafted info data.
- **Impact**: Development-only dependency (debugging tool)
- **Mitigation**: Not exploitable in production; only used in local development
- **Status**: Accepted risk - `pdbpp` is a dev-only debugging tool, not used in production

## Security Scanning

This project uses multiple security scanning tools:

1. **pip-audit**: Scans all dependencies for known vulnerabilities
2. **safety**: Additional vulnerability scanning (requires authentication)
3. **Pre-commit hooks**: Runs security checks before each commit

## Reporting Security Issues

If you discover a security vulnerability, please email the maintainer directly rather than opening a public issue.

## Security Best Practices

- All dependencies are pinned with minimum versions
- Python 3.13+ required for latest security patches
- Strict type checking with mypy prevents many runtime errors
- Runtime validation with beartype and deal contracts
- Pydantic models validate all configuration and state data
