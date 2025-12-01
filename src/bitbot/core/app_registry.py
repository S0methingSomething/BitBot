"""App registry for centralized app lookup."""

from beartype import beartype

from bitbot.models import App


class AppNotFoundError(ValueError):
    """Raised when an app identifier doesn't match any configured app."""

    @beartype
    def __init__(self, identifier: str, available: list[str]) -> None:
        """Initialize with identifier and available apps."""
        self.identifier = identifier
        self.available = available
        super().__init__(f"App '{identifier}' not found. Available: {', '.join(available)}")


class AppRegistry:
    """Registry for looking up apps by any identifier.

    Supports lookup by:
    - Exact app ID
    - Display name
    - Case-insensitive matching
    """

    @beartype
    def __init__(self, apps: list[App]) -> None:
        """Initialize registry with list of apps."""
        self._apps = apps
        self._by_id: dict[str, App] = {app.id: app for app in apps}
        # Build case-insensitive lookup index
        self._by_identifier: dict[str, App] = {}
        for app in apps:
            for identifier in app.identifiers:
                self._by_identifier[identifier.lower()] = app

    @beartype
    def get(self, identifier: str) -> App | None:
        """Get app by any identifier (case-insensitive).

        Args:
            identifier: App ID, display name, or any known identifier

        Returns:
            App if found, None otherwise
        """
        # Try exact match first
        if identifier in self._by_id:
            return self._by_id[identifier]
        # Try case-insensitive lookup
        return self._by_identifier.get(identifier.lower())

    @beartype
    def get_or_raise(self, identifier: str) -> App:
        """Get app by identifier or raise AppNotFoundError.

        Args:
            identifier: App ID, display name, or any known identifier

        Returns:
            App if found

        Raises:
            AppNotFoundError: If no app matches the identifier
        """
        app = self.get(identifier)
        if app is None:
            raise AppNotFoundError(identifier, [a.id for a in self._apps])
        return app

    @beartype
    def exists(self, identifier: str) -> bool:
        """Check if identifier matches any configured app."""
        return self.get(identifier) is not None

    @property
    def all(self) -> list[App]:
        """All configured apps."""
        return list(self._apps)

    @property
    def ids(self) -> frozenset[str]:
        """All app IDs."""
        return frozenset(self._by_id.keys())

    @beartype
    def __len__(self) -> int:
        """Number of configured apps."""
        return len(self._apps)

    @beartype
    def __contains__(self, identifier: str) -> bool:
        """Check if identifier matches any app."""
        return self.exists(identifier)
