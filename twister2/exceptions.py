class TwisterException(Exception):
    """General twister exception."""


class YamlException(TwisterException):
    """Custom exception for error reporting."""


class TwisterFatalError(TwisterException):
    """Twister fatal error exception."""


class ProjectExecutionFailed(TwisterException):
    """Project execution failed exception."""


class TwisterBuilderException(TwisterException):
    """Any exception during building."""


class TwisterRunException(TwisterException):
    """Any exception during executing."""
