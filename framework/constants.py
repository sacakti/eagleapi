"""
Application-wide constants and enumerations.
"""
from enum import Enum

class Phase(Enum):
    CONFIGURATION = "Configuration"
    REQUEST = "Request"
    CONNECTION = "Connection"
    EXECUTION = "Execution"
    VALIDATION = "Validation"
    REPORT = "Report"
    COMPLETED = "Completed"

class HttpMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"

class ReportStatus(str, Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    ERROR = "ERROR"

class ContentType(str, Enum):
    JSON = "application/json"
    XML = "application/xml"
    TEXT = "text/plain"
    FORM = "application/x-www-form-urlencoded"
    MULTIPART = "multipart/form-data"

class FileExtension(str, Enum):
    REQUEST = ".json"
    RESPONSE = ".json"
    REPORT = ".json"
    HTML = ".html"
    LOG = ".log"

class Directory:
    CONFIG = "config"
    ENDPOINTS = "endpoints"
    REQUESTS = "requests"
    RESPONSES = "responses"
    REPORTS = "reports"
    LOGS = "logs"
    CERTIFICATES = "certificates"
    TEMPLATES = "templates"

class ConfigurationKey:
    BASE_URL = "baseUrl"
    VERIFY_SSL = "verifySsl"
    CLIENT_CERT = "clientCertificate"
    CLIENT_KEY = "clientKey"
    CA_CERT = "caCertificate"
    TIMEOUT = "timeout"
    ENVIRONMENT = "environment"

class Placeholder:
    PREFIX = "{{"
    SUFFIX = "}}"

class Default:
    TIMEOUT = 30
    VERIFY_SSL = True
    REPORT_FILE = "report.json"
    HTML_REPORT = "report.html"
    LOG_FILE = "apitester.log"

class Header:
    CONTENT_TYPE = "Content-Type"
    ACCEPT = "Accept"
    AUTHORIZATION = "Authorization"

class ExitCode:
    SUCCESS = 0
    FAILURE = 1
    VALIDATION_ERROR = 2