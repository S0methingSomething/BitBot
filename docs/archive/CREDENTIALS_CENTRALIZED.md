# Credentials Centralization

## Overview

All credential access has been centralized into a single `Credentials` class in `helpers.py`. This provides:
- **Single point of access** for all environment variables
- **Type safety** with proper return types
- **Error handling** with clear error messages
- **Easier testing** and mocking
- **Better maintainability**

## Credentials Class

Located in `src/helpers.py`:

```python
class Credentials:
    """Centralized credential management with type safety and error handling."""

    @staticmethod
    def get_github_token() -> str:
        """Get GitHub token from environment."""
        
    @staticmethod
    def get_github_output() -> str:
        """Get GitHub Actions output file path."""
        
    @staticmethod
    def get_reddit_client_id() -> str:
        """Get Reddit client ID from environment."""
        
    @staticmethod
    def get_reddit_client_secret() -> str:
        """Get Reddit client secret from environment."""
        
    @staticmethod
    def get_reddit_user_agent() -> str:
        """Get Reddit user agent from environment."""
        
    @staticmethod
    def get_reddit_username() -> str:
        """Get Reddit username from environment."""
        
    @staticmethod
    def get_reddit_password() -> str:
        """Get Reddit password from environment."""
```

## Usage

### Before
```python
import os
token = os.environ["GITHUB_TOKEN"]
token = os.getenv("GITHUB_TOKEN", "")
output = os.environ.get("GITHUB_OUTPUT", "")
```

### After
```python
from helpers import Credentials

token = Credentials.get_github_token()
output = Credentials.get_github_output()
```

## Files Updated

1. **helpers.py** - Added `Credentials` class, updated `init_reddit()`
2. **gather_post_data.py** - Uses `Credentials.get_github_token()`
3. **release_manager.py** - Uses `Credentials.get_github_token()` and `Credentials.get_github_output()`
4. **maintain_releases.py** - Uses `Credentials.get_github_token()`
5. **check_comments.py** - Uses `Credentials.get_github_output()`
6. **legacy_release_migrator.py** - Uses `Credentials.get_github_token()`

## Benefits

### Type Safety
- All methods have explicit return types (`str`)
- No more `Optional[str]` confusion
- mypy can verify correct usage

### Error Handling
- `get_github_token()` raises `ValueError` if token is missing
- Clear error messages for debugging
- Consistent behavior across all scripts

### Maintainability
- Single place to update credential logic
- Easy to add validation or logging
- Simplified testing with mocks

### Security
- Centralized access makes auditing easier
- Can add encryption/decryption in one place
- Easier to implement credential rotation

## Environment Variables

Required environment variables:
- `GITHUB_TOKEN` - GitHub API token (required)
- `GITHUB_OUTPUT` - GitHub Actions output file (optional)
- `REDDIT_CLIENT_ID` - Reddit API client ID
- `REDDIT_CLIENT_SECRET` - Reddit API client secret
- `REDDIT_USER_AGENT` - Reddit API user agent
- `REDDIT_USERNAME` - Reddit username
- `REDDIT_PASSWORD` - Reddit password

## Compliance

✅ **Ruff**: All checks passed  
✅ **mypy**: Success: no issues found in 11 source files  
✅ **Type hints**: Complete coverage  
✅ **100% compliance maintained**
