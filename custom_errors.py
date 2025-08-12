class FavQsError(Exception):
    """Base class for all FavQsClient errors."""
    def __str__(self):
        return self.__doc__


class FavQsConfigError(FavQsError):
    """FAVQS_API_KEY env variable is not set or API token was not provided."""


class FavQsAuthError(FavQsError):
    """FAVQS_API_KEY env variable is not set."""
