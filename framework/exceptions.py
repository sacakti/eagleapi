"""
Custom exceptions used throughout the API Tester.
"""

class ApiTesterException(Exception):
    """Base exception for the framework."""
    def __init__(self, message: str):
         super().__init__(message)
         self.message = message

class ConfigurationException(ApiTesterException):
    """Raised when configuration is invalid."""

class RequestNotFoundException(ApiTesterException):
    """Raised when a request JSON file cannot be found."""

class EndpointNotFoundException(ApiTesterException):
    """Raised when an endpoint folder does not exist."""

class RequestValidationException(ApiTesterException):
    """Raised when a request JSON is invalid."""

class VariableResolutionException(ApiTesterException):
    """Raised when a variable cannot be resolved."""

class HttpRequestException(ApiTesterException):
    """
    Raised when the HTTP request could not be executed.
    Example:
         - Connection refused
         - DNS failure
         - SSL handshake failure
         - Timeout
    """

class ResponseValidationException(ApiTesterException):
    """Raised when response assertions fail."""

class ReportGenerationException(ApiTesterException):
    """Raised when report generation fails."""

class CertificateException(ApiTesterException):
    """Raised for TLS certificate related failures."""

class AuthenticationException(ApiTesterException):
    """Raised for authentication failures."""

class TimeoutException(ApiTesterException):
    """Raised when request timeout occurs."""