"""
Custom exceptions untuk netdiag package.
Menyediakan exception classes yang spesifik untuk berbagai error scenarios.
"""

from typing import Any, Optional


class NetdiagError(Exception):
    """Base exception untuk semua netdiag errors."""
    
    def __init__(self, message: str, details: Optional[Any] = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details


class NetworkError(NetdiagError):
    """Exception untuk network-related errors."""
    
    def __init__(self, message: str, host: Optional[str] = None, 
                 timeout: Optional[float] = None) -> None:
        super().__init__(message)
        self.host = host
        self.timeout = timeout


class HostResolutionError(NetworkError):
    """Exception ketika hostname tidak bisa di-resolve."""
    pass


class ConnectionTimeoutError(NetworkError):
    """Exception ketika koneksi timeout."""
    pass


class PortScanError(NetdiagError):
    """Exception untuk port scanning errors."""
    
    def __init__(self, message: str, port: Optional[int] = None,
                 host: Optional[str] = None) -> None:
        super().__init__(message)
        self.port = port
        self.host = host


class DNSError(NetdiagError):
    """Exception untuk DNS lookup errors."""
    
    def __init__(self, message: str, hostname: Optional[str] = None,
                 query_type: Optional[str] = None) -> None:
        super().__init__(message)
        self.hostname = hostname
        self.query_type = query_type


class ValidationError(NetdiagError):
    """Exception untuk input validation errors."""
    
    def __init__(self, message: str, field: Optional[str] = None,
                 value: Optional[Any] = None) -> None:
        super().__init__(message)
        self.field = field
        self.value = value


class ExportError(NetdiagError):
    """Exception untuk export/file operation errors."""
    
    def __init__(self, message: str, filename: Optional[str] = None,
                 format_type: Optional[str] = None) -> None:
        super().__init__(message)
        self.filename = filename
        self.format_type = format_type


class SpeedTestError(NetdiagError):
    """Exception untuk speed test errors."""
    
    def __init__(self, message: str, test_type: Optional[str] = None,
                 host: Optional[str] = None) -> None:
        super().__init__(message)
        self.test_type = test_type
        self.host = host