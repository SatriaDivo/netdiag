"""
Utility functions untuk netdiag package.
Berisi helper functions, validators, dan common utilities.
"""

import ipaddress
import re
import socket
from typing import Any, Optional, Union

from .exceptions import ValidationError


def validate_hostname(hostname: str) -> str:
    """
    Validate hostname format.
    
    Args:
        hostname: Hostname or IP address to validate
        
    Returns:
        Cleaned hostname string
        
    Raises:
        ValidationError: If hostname is invalid
    """
    if not hostname or not isinstance(hostname, str):
        raise ValidationError("Hostname must be a non-empty string", "hostname", hostname)
    
    hostname = hostname.strip()
    
    if not hostname:
        raise ValidationError("Hostname cannot be empty", "hostname", hostname)
    
    # Check if it's a valid IP address
    try:
        ipaddress.ip_address(hostname)
        return hostname
    except ValueError:
        pass
    
    # Validate hostname format
    if len(hostname) > 253:
        raise ValidationError("Hostname too long (max 253 characters)", "hostname", hostname)
    
    # Basic hostname pattern validation
    hostname_pattern = re.compile(
        r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?'
        r'(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
    )
    
    if not hostname_pattern.match(hostname):
        raise ValidationError("Invalid hostname format", "hostname", hostname)
    
    return hostname


def validate_port(port: Union[int, str]) -> int:
    """
    Validate port number.
    
    Args:
        port: Port number to validate
        
    Returns:
        Valid port number as integer
        
    Raises:
        ValidationError: If port is invalid
    """
    try:
        port_int = int(port)
    except (ValueError, TypeError):
        raise ValidationError("Port must be a valid integer", "port", port)
    
    if not (1 <= port_int <= 65535):
        raise ValidationError("Port must be between 1 and 65535", "port", port_int)
    
    return port_int


def validate_port_range(start_port: Union[int, str], end_port: Union[int, str]) -> tuple:
    """
    Validate port range.
    
    Args:
        start_port: Starting port number
        end_port: Ending port number
        
    Returns:
        Tuple of validated (start_port, end_port)
        
    Raises:
        ValidationError: If port range is invalid
    """
    start = validate_port(start_port)
    end = validate_port(end_port)
    
    if start > end:
        raise ValidationError("Start port cannot be greater than end port", 
                            "port_range", (start, end))
    
    if end - start > 10000:
        raise ValidationError("Port range too large (max 10000 ports)", 
                            "port_range", (start, end))
    
    return start, end


def validate_timeout(timeout: Union[int, float, str]) -> float:
    """
    Validate timeout value.
    
    Args:
        timeout: Timeout value in seconds
        
    Returns:
        Valid timeout as float
        
    Raises:
        ValidationError: If timeout is invalid
    """
    try:
        timeout_float = float(timeout)
    except (ValueError, TypeError):
        raise ValidationError("Timeout must be a valid number", "timeout", timeout)
    
    if timeout_float <= 0:
        raise ValidationError("Timeout must be positive", "timeout", timeout_float)
    
    if timeout_float > 300:  # 5 minutes max
        raise ValidationError("Timeout too large (max 300 seconds)", "timeout", timeout_float)
    
    return timeout_float


def validate_count(count: Union[int, str]) -> int:
    """
    Validate count parameter.
    
    Args:
        count: Count value
        
    Returns:
        Valid count as integer
        
    Raises:
        ValidationError: If count is invalid
    """
    try:
        count_int = int(count)
    except (ValueError, TypeError):
        raise ValidationError("Count must be a valid integer", "count", count)
    
    if count_int <= 0:
        raise ValidationError("Count must be positive", "count", count_int)
    
    if count_int > 100:
        raise ValidationError("Count too large (max 100)", "count", count_int)
    
    return count_int


def resolve_hostname(hostname: str) -> str:
    """
    Resolve hostname to IP address.
    
    Args:
        hostname: Hostname to resolve
        
    Returns:
        IP address string
        
    Raises:
        ValidationError: If hostname cannot be resolved
    """
    validated_hostname = validate_hostname(hostname)
    
    try:
        # Check if it's already an IP address
        ipaddress.ip_address(validated_hostname)
        return validated_hostname
    except ValueError:
        pass
    
    try:
        ip_address = socket.gethostbyname(validated_hostname)
        return ip_address
    except socket.gaierror as e:
        raise ValidationError(f"Cannot resolve hostname: {e}", "hostname", hostname)


def format_duration(seconds: float) -> str:
    """
    Format duration in human-readable format.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string
    """
    if seconds < 1:
        return f"{seconds*1000:.1f}ms"
    elif seconds < 60:
        return f"{seconds:.2f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.1f}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"


def safe_get_dict_value(data: dict[str, Any], key: str, default: Any = None) -> Any:
    """
    Safely get value from dictionary with error handling.
    
    Args:
        data: Dictionary to get value from
        key: Key to retrieve
        default: Default value if key not found
        
    Returns:
        Value from dictionary or default
    """
    try:
        return data.get(key, default)
    except (AttributeError, TypeError):
        return default


def create_result_dict(success: bool = True, **kwargs) -> dict[str, Any]:
    """
    Create standardized result dictionary.
    
    Args:
        success: Whether operation was successful
        **kwargs: Additional fields to include
        
    Returns:
        Standardized result dictionary
    """
    result = {"success": success}
    result.update(kwargs)
    return result


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe file operations.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove or replace invalid characters
    invalid_chars = '<>:"|?*\\/'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip(' .')
    
    # Ensure filename is not empty
    if not filename:
        filename = "netdiag_output"
    
    return filename


def is_private_ip(ip: str) -> bool:
    """
    Check if IP address is private.
    
    Args:
        ip: IP address string
        
    Returns:
        True if IP is private, False otherwise
    """
    try:
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.is_private
    except ValueError:
        return False


def get_common_ports() -> dict[int, str]:
    """
    Get dictionary of common ports and their services.
    
    Returns:
        Dictionary mapping port numbers to service names
    """
    return {
        21: 'FTP',
        22: 'SSH',
        23: 'Telnet',
        25: 'SMTP',
        53: 'DNS',
        67: 'DHCP',
        68: 'DHCP',
        69: 'TFTP',
        80: 'HTTP',
        110: 'POP3',
        143: 'IMAP',
        443: 'HTTPS',
        993: 'IMAPS',
        995: 'POP3S',
        587: 'SMTP-TLS',
        465: 'SMTP-SSL',
        135: 'RPC',
        139: 'NetBIOS',
        445: 'SMB',
        1433: 'MSSQL',
        3306: 'MySQL',
        3389: 'RDP',
        5432: 'PostgreSQL',
        5900: 'VNC',
        6379: 'Redis',
        8080: 'HTTP-Alt',
        8443: 'HTTPS-Alt',
        27017: 'MongoDB'
    }