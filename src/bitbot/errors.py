"""Custom exceptions for BitBot."""


class InvalidCredentialsError(Exception):
    """Raised when API credentials are invalid."""

    def __init__(self, service: str, details: str):
        """
        Initializes the InvalidCredentialsError.

        Args:
            service: The name of the service that failed (e.g., "GitHub", "Reddit").
            details: The details of the error from the API.
        """
        self.service = service
        self.details = details
        super().__init__(self.message())

    def message(self) -> str:
        """Generates a user-friendly error message."""
        return (
            f"{self.service} credentials are invalid. Please check your .env file.\n"
            f"  Details: {self.details}"
        )

