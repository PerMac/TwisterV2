class TwisterException(Exception):
    """General twister exception."""


class YamlException(TwisterException):
    """Custom exception for error reporting."""


class TwisterFatalError(TwisterException):
    """Twister fatal error exception."""


class ProjectExecutionFailed(TwisterException):
    """Project execution failed exception."""
