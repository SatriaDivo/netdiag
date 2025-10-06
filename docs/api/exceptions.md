# ⚠️ Exception Handling

Comprehensive guide to exception handling in the Netdiag toolkit. Learn about the exception hierarchy, best practices, and how to handle errors gracefully in network diagnostics applications.

## 📋 Table of Contents

- [Exception Hierarchy](#-exception-hierarchy)
- [Core Exceptions](#-core-exceptions)
- [Specialized Exceptions](#-specialized-exceptions)
- [Error Handling Patterns](#-error-handling-patterns)
- [Best Practices](#-best-practices)
- [Educational Examples](#-educational-examples)

---

## 🏗️ Exception Hierarchy

The Netdiag exception hierarchy provides specific error types for different failure scenarios:

```
NetdiagError (Base)
├── NetworkError
│   ├── ConnectivityError
│   ├── TimeoutError
│   └── ProtocolError
├── DNSError
│   ├── DNSResolutionError
│   ├── DNSTimeoutError
│   └── DNSConfigurationError
├── PortError
│   ├── PortTimeoutError
│   ├── PortClosedError
│   └── ServiceDetectionError
├── ValidationError
│   ├── IPValidationError
│   ├── DomainValidationError
│   └── PortValidationError
├── ConfigurationError
│   ├── InvalidConfigurationError
│   └── MissingConfigurationError
└── PermissionError
    ├── InsufficientPrivilegesError
    └── FirewallBlockedError
```

## 🔧 Core Exceptions

### `NetdiagError`
Base exception class for all Netdiag-related errors.

```python
class NetdiagError(Exception):
    """Base exception for all Netdiag errors."""
    
    def __init__(self, message: str, target: Optional[str] = None, 
                 error_code: Optional[str] = None, details: Optional[dict] = None):
        super().__init__(message)
        self.message = message
        self.target = target
        self.error_code = error_code
        self.details = details or {}
        self.timestamp = datetime.now()
    
    def __str__(self) -> str:
        """Return formatted error message."""
        base_msg = self.message
        if self.target:
            base_msg = f"[{self.target}] {base_msg}"
        if self.error_code:
            base_msg = f"{base_msg} (Code: {self.error_code})"
        return base_msg
    
    def to_dict(self) -> dict[str, Any]:
        """Convert exception to dictionary."""
        return {
            'error_type': self.__class__.__name__,
            'message': self.message,
            'target': self.target,
            'error_code': self.error_code,
            'details': self.details,
            'timestamp': self.timestamp.isoformat()
        }
```

**Usage Example:**
```python
try:
    result = netdiag.ping("invalid-target")
except NetdiagError as e:
    print(f"Error: {e}")
    print(f"Target: {e.target}")
    print(f"Timestamp: {e.timestamp}")
    print(f"Details: {e.details}")
```

### `NetworkError`
Base class for all network-related errors.

```python
class NetworkError(NetdiagError):
    """Network-related errors."""
    
    def __init__(self, message: str, target: Optional[str] = None, 
                 network_code: Optional[int] = None, **kwargs):
        super().__init__(message, target, **kwargs)
        self.network_code = network_code
    
    @property
    def is_temporary(self) -> bool:
        """Check if error might be temporary."""
        temporary_codes = [110, 111, 113]  # Connection timeout, refused, no route
        return self.network_code in temporary_codes
```

---

## 🌐 Specialized Exceptions

### DNS Exceptions

#### `DNSError`
Base class for DNS-related errors.

```python
class DNSError(NetdiagError):
    """DNS operation errors."""
    
    def __init__(self, message: str, domain: Optional[str] = None, 
                 dns_server: Optional[str] = None, **kwargs):
        super().__init__(message, target=domain, **kwargs)
        self.domain = domain
        self.dns_server = dns_server

class DNSResolutionError(DNSError):
    """DNS resolution failed."""
    
    def __init__(self, domain: str, dns_server: Optional[str] = None):
        message = f"Failed to resolve domain: {domain}"
        if dns_server:
            message += f" using DNS server {dns_server}"
        super().__init__(message, domain=domain, dns_server=dns_server, 
                        error_code="DNS_RESOLUTION_FAILED")

class DNSTimeoutError(DNSError):
    """DNS query timeout."""
    
    def __init__(self, domain: str, timeout: int, dns_server: Optional[str] = None):
        message = f"DNS query timeout for {domain} after {timeout}s"
        super().__init__(message, domain=domain, dns_server=dns_server,
                        error_code="DNS_TIMEOUT")
        self.timeout = timeout

class DNSConfigurationError(DNSError):
    """DNS configuration error."""
    
    def __init__(self, message: str, config_issue: str):
        super().__init__(message, error_code="DNS_CONFIG_ERROR")
        self.config_issue = config_issue
```

**Usage Example:**
```python
try:
    result = netdiag.dns_lookup("invalid-domain.xyz")
except DNSResolutionError as e:
    print(f"DNS Resolution failed: {e.domain}")
    print(f"DNS Server: {e.dns_server}")
except DNSTimeoutError as e:
    print(f"DNS Timeout: {e.timeout}s")
except DNSError as e:
    print(f"General DNS Error: {e}")
```

### Port Exceptions

#### `PortError`
Base class for port-related errors.

```python
class PortError(NetdiagError):
    """Port operation errors."""
    
    def __init__(self, message: str, target: Optional[str] = None, 
                 port: Optional[int] = None, **kwargs):
        super().__init__(message, target=target, **kwargs)
        self.port = port

class PortTimeoutError(PortError):
    """Port connection timeout."""
    
    def __init__(self, target: str, port: int, timeout: int):
        message = f"Connection timeout to {target}:{port} after {timeout}s"
        super().__init__(message, target=target, port=port, 
                        error_code="PORT_TIMEOUT")
        self.timeout = timeout

class PortClosedError(PortError):
    """Port is closed or filtered."""
    
    def __init__(self, target: str, port: int):
        message = f"Port {port} is closed on {target}"
        super().__init__(message, target=target, port=port,
                        error_code="PORT_CLOSED")

class ServiceDetectionError(PortError):
    """Service detection failed."""
    
    def __init__(self, target: str, port: int, reason: str):
        message = f"Service detection failed for {target}:{port} - {reason}"
        super().__init__(message, target=target, port=port,
                        error_code="SERVICE_DETECTION_FAILED")
        self.reason = reason
```

### Validation Exceptions

#### `ValidationError`
Base class for input validation errors.

```python
class ValidationError(NetdiagError):
    """Input validation errors."""
    
    def __init__(self, message: str, field: str, value: Any, **kwargs):
        super().__init__(message, **kwargs)
        self.field = field
        self.value = value

class IPValidationError(ValidationError):
    """Invalid IP address format."""
    
    def __init__(self, ip_address: str):
        message = f"Invalid IP address format: {ip_address}"
        super().__init__(message, field="ip_address", value=ip_address,
                        error_code="INVALID_IP")

class DomainValidationError(ValidationError):
    """Invalid domain name format."""
    
    def __init__(self, domain: str, reason: str):
        message = f"Invalid domain name '{domain}': {reason}"
        super().__init__(message, field="domain", value=domain,
                        error_code="INVALID_DOMAIN")
        self.reason = reason

class PortValidationError(ValidationError):
    """Invalid port number."""
    
    def __init__(self, port: Any):
        message = f"Invalid port number: {port} (must be 1-65535)"
        super().__init__(message, field="port", value=port,
                        error_code="INVALID_PORT")
```

### Configuration Exceptions

#### `ConfigurationError`
Configuration-related errors.

```python
class ConfigurationError(NetdiagError):
    """Configuration errors."""
    
    def __init__(self, message: str, config_key: Optional[str] = None, **kwargs):
        super().__init__(message, **kwargs)
        self.config_key = config_key

class InvalidConfigurationError(ConfigurationError):
    """Invalid configuration value."""
    
    def __init__(self, config_key: str, value: Any, expected: str):
        message = f"Invalid configuration for '{config_key}': {value} (expected: {expected})"
        super().__init__(message, config_key=config_key,
                        error_code="INVALID_CONFIG_VALUE")
        self.value = value
        self.expected = expected

class MissingConfigurationError(ConfigurationError):
    """Required configuration missing."""
    
    def __init__(self, config_key: str):
        message = f"Required configuration missing: {config_key}"
        super().__init__(message, config_key=config_key,
                        error_code="MISSING_CONFIG")
```

### Permission Exceptions

#### `PermissionError`
Permission and privilege-related errors.

```python
class NetdiagPermissionError(NetdiagError):  # Avoid conflict with built-in PermissionError
    """Permission and privilege errors."""
    
    def __init__(self, message: str, required_privilege: Optional[str] = None, **kwargs):
        super().__init__(message, **kwargs)
        self.required_privilege = required_privilege

class InsufficientPrivilegesError(NetdiagPermissionError):
    """Insufficient privileges for operation."""
    
    def __init__(self, operation: str, required_privilege: str):
        message = f"Insufficient privileges for {operation}. Required: {required_privilege}"
        super().__init__(message, required_privilege=required_privilege,
                        error_code="INSUFFICIENT_PRIVILEGES")
        self.operation = operation

class FirewallBlockedError(NetdiagPermissionError):
    """Operation blocked by firewall."""
    
    def __init__(self, target: str, port: Optional[int] = None):
        if port:
            message = f"Connection to {target}:{port} blocked by firewall"
        else:
            message = f"Connection to {target} blocked by firewall"
        super().__init__(message, target=target, error_code="FIREWALL_BLOCKED")
        self.port = port
```

---

## 🔄 Error Handling Patterns

### Pattern 1: Specific Exception Handling
```python
import netdiag
from netdiag.exceptions import (
    DNSResolutionError, PortTimeoutError, ValidationError
)

def diagnose_target(target: str) -> dict[str, Any]:
    """Diagnose target with comprehensive error handling."""
    results = {
        'target': target,
        'ping': None,
        'dns': None,
        'ports': None,
        'errors': []
    }
    
    # Ping test with specific error handling
    try:
        ping_result = netdiag.ping(target)
        results['ping'] = {
            'success': True,
            'avg_time': ping_result.avg_time,
            'packet_loss': ping_result.packet_loss
        }
    except DNSResolutionError as e:
        results['errors'].append({
            'type': 'DNS_RESOLUTION',
            'message': str(e),
            'domain': e.domain
        })
    except ValidationError as e:
        results['errors'].append({
            'type': 'VALIDATION',
            'message': str(e),
            'field': e.field,
            'value': e.value
        })
    except Exception as e:
        results['errors'].append({
            'type': 'UNEXPECTED',
            'message': str(e)
        })
    
    # DNS lookup with error handling
    try:
        dns_result = netdiag.dns_lookup(target)
        results['dns'] = {
            'success': True,
            'ip_address': dns_result.ip_address,
            'query_time': dns_result.query_time
        }
    except DNSResolutionError as e:
        results['errors'].append({
            'type': 'DNS_RESOLUTION',
            'message': str(e)
        })
    
    # Port scan with error handling
    try:
        port_results = netdiag.port_scan(target, [80, 443, 22])
        open_ports = [r.port for r in port_results if r.is_open]
        results['ports'] = {
            'success': True,
            'open_ports': open_ports,
            'total_scanned': len(port_results)
        }
    except PortTimeoutError as e:
        results['errors'].append({
            'type': 'PORT_TIMEOUT',
            'message': str(e),
            'port': e.port
        })
    
    return results
```

### Pattern 2: Error Recovery and Retry
```python
import time
from functools import wraps
from typing import Callable, TypeVar, Any

T = TypeVar('T')

def retry_on_error(max_retries: int = 3, delay: float = 1.0, 
                  backoff_factor: float = 2.0) -> Callable:
    """Decorator for retrying operations on specific errors."""
    
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                
                except (DNSTimeoutError, PortTimeoutError, NetworkError) as e:
                    last_exception = e
                    
                    if attempt < max_retries:
                        wait_time = delay * (backoff_factor ** attempt)
                        print(f"Attempt {attempt + 1} failed: {e}")
                        print(f"Retrying in {wait_time:.1f} seconds...")
                        time.sleep(wait_time)
                    else:
                        print(f"All {max_retries + 1} attempts failed")
                        break
                
                except ValidationError:
                    # Don't retry validation errors
                    raise
            
            # Re-raise the last exception if all retries failed
            if last_exception:
                raise last_exception
        
        return wrapper
    return decorator

# Usage example
@retry_on_error(max_retries=3, delay=2.0)
def reliable_ping(target: str) -> Any:
    """Ping with automatic retry on timeout."""
    return netdiag.ping(target)

# Use the function
try:
    result = reliable_ping("polinela.ac.id")
    print(f"Ping successful: {result.avg_time}ms")
except Exception as e:
    print(f"Ping failed after retries: {e}")
```

### Pattern 3: Context Manager for Error Handling
```python
from contextlib import contextmanager
from typing import Generator, Optional

@contextmanager
def network_operation(target: str, operation: str) -> Generator[None, None, None]:
    """Context manager for network operations with standardized error handling."""
    
    print(f"Starting {operation} for {target}...")
    start_time = time.time()
    
    try:
        yield
        
    except DNSError as e:
        duration = time.time() - start_time
        print(f"❌ DNS Error in {operation} after {duration:.2f}s: {e}")
        raise
        
    except PortError as e:
        duration = time.time() - start_time
        print(f"❌ Port Error in {operation} after {duration:.2f}s: {e}")
        raise
        
    except ValidationError as e:
        print(f"❌ Validation Error in {operation}: {e}")
        raise
        
    except NetworkError as e:
        duration = time.time() - start_time
        print(f"❌ Network Error in {operation} after {duration:.2f}s: {e}")
        raise
        
    except Exception as e:
        duration = time.time() - start_time
        print(f"❌ Unexpected Error in {operation} after {duration:.2f}s: {e}")
        raise
        
    else:
        duration = time.time() - start_time
        print(f"✅ {operation} completed successfully in {duration:.2f}s")

# Usage example
try:
    with network_operation("polinela.ac.id", "comprehensive analysis"):
        ping_result = netdiag.ping("polinela.ac.id")
        dns_result = netdiag.dns_lookup("polinela.ac.id")
        port_results = netdiag.port_scan("polinela.ac.id", [80, 443])
        
except NetdiagError as e:
    print(f"Network diagnostic failed: {e}")
```

---

## 💡 Best Practices

### 1. Catch Specific Exceptions First
```python
# ✅ Good: Specific to general exception handling
try:
    result = netdiag.dns_lookup("example.com")
except DNSResolutionError as e:
    # Handle DNS resolution issues
    print(f"Cannot resolve domain: {e.domain}")
except DNSTimeoutError as e:
    # Handle DNS timeout
    print(f"DNS query timed out after {e.timeout}s")
except DNSError as e:
    # Handle other DNS errors
    print(f"DNS error: {e}")
except NetdiagError as e:
    # Handle any other netdiag errors
    print(f"Network diagnostic error: {e}")
except Exception as e:
    # Handle unexpected errors
    print(f"Unexpected error: {e}")

# ❌ Avoid: Catching general exceptions first
try:
    result = netdiag.dns_lookup("example.com")
except Exception as e:  # This catches everything!
    print(f"Error: {e}")
```

### 2. Use Exception Details
```python
# ✅ Good: Use exception details for better error handling
try:
    result = netdiag.port_scan("target.com", [80, 443])
except PortTimeoutError as e:
    if e.timeout > 30:
        print("Long timeout suggests network issues")
    else:
        print("Quick timeout suggests port filtering")
    
    # Log structured error information
    logger.error("Port scan failed", extra={
        'target': e.target,
        'port': e.port,
        'timeout': e.timeout,
        'error_code': e.error_code
    })
```

### 3. Validate Input Early
```python
# ✅ Good: Validate inputs before processing
def analyze_network(target: str, ports: list[int]) -> dict:
    """Analyze network with input validation."""
    
    # Validate target
    if not target:
        raise ValidationError("Target cannot be empty", "target", target)
    
    # Validate IP or domain
    if not (netdiag.validate_ip(target).is_valid or 
            netdiag.validate_domain(target).is_valid):
        raise ValidationError(f"Invalid target: {target}", "target", target)
    
    # Validate ports
    for port in ports:
        if not (1 <= port <= 65535):
            raise PortValidationError(port)
    
    # Proceed with analysis
    try:
        return {
            'ping': netdiag.ping(target),
            'ports': netdiag.port_scan(target, ports)
        }
    except NetdiagError:
        raise  # Re-raise netdiag errors
```

### 4. Provide Helpful Error Messages
```python
# ✅ Good: Descriptive error messages
class EducationalNetworkAnalyzer:
    """Educational network analyzer with helpful error messages."""
    
    def analyze_campus_network(self, domain: str) -> dict:
        """Analyze campus network for educational purposes."""
        
        try:
            return self._perform_analysis(domain)
            
        except DNSResolutionError as e:
            # Provide educational context
            raise DNSResolutionError(
                f"Cannot resolve campus domain '{domain}'. "
                f"This might be because:\n"
                f"1. The domain name is misspelled\n"
                f"2. The campus DNS server is down\n"
                f"3. Your internet connection has issues\n"
                f"4. The domain doesn't exist\n\n"
                f"Try checking your spelling or testing with a known domain like 'google.com'."
            )
            
        except PortTimeoutError as e:
            raise PortTimeoutError(
                target=e.target,
                port=e.port,
                timeout=e.timeout
            ) from e.__cause__
```

---

## 🎓 Educational Examples

### Student Lab Error Handling
```python
class StudentLabSession:
    """Handles errors in student lab exercises."""
    
    def __init__(self, student_id: str, lab_name: str):
        self.student_id = student_id
        self.lab_name = lab_name
        self.errors = []
        self.attempts = {}
    
    def safe_ping(self, target: str) -> dict:
        """Ping with educational error handling."""
        attempt_key = f"ping_{target}"
        self.attempts[attempt_key] = self.attempts.get(attempt_key, 0) + 1
        
        try:
            result = netdiag.ping(target)
            return {
                'success': True,
                'result': result,
                'message': f"✅ Ping to {target} successful!"
            }
            
        except DNSResolutionError as e:
            error_msg = (
                f"❌ Cannot resolve '{target}'. "
                f"Check if the domain name is correct. "
                f"Common campus domains end with '.ac.id' in Indonesia."
            )
            self.errors.append({
                'type': 'DNS Resolution',
                'target': target,
                'message': error_msg,
                'attempt': self.attempts[attempt_key],
                'suggestion': "Try 'polinela.ac.id' or 'google.com'"
            })
            return {'success': False, 'message': error_msg}
            
        except NetworkError as e:
            if e.is_temporary:
                error_msg = (
                    f"❌ Network timeout to {target}. "
                    f"This might be temporary. Try again in a moment."
                )
                suggestion = "Wait 30 seconds and try again"
            else:
                error_msg = (
                    f"❌ Network error connecting to {target}. "
                    f"Check your internet connection."
                )
                suggestion = "Check network connection or try a different target"
            
            self.errors.append({
                'type': 'Network Error',
                'target': target,
                'message': error_msg,
                'attempt': self.attempts[attempt_key],
                'suggestion': suggestion
            })
            return {'success': False, 'message': error_msg}
    
    def generate_error_report(self) -> str:
        """Generate educational error report."""
        if not self.errors:
            return "🎉 No errors encountered! Great job!"
        
        report = f"📋 Error Report for {self.student_id} - {self.lab_name}\n"
        report += "=" * 50 + "\n\n"
        
        for i, error in enumerate(self.errors, 1):
            report += f"{i}. {error['type']} (Attempt {error['attempt']})\n"
            report += f"   Target: {error['target']}\n"
            report += f"   Issue: {error['message']}\n"
            report += f"   💡 Suggestion: {error['suggestion']}\n\n"
        
        report += "\n🎯 Learning Points:\n"
        if any(e['type'] == 'DNS Resolution' for e in self.errors):
            report += "• DNS resolution is the first step in network communication\n"
            report += "• Always verify domain names are spelled correctly\n"
        
        if any(e['type'] == 'Network Error' for e in self.errors):
            report += "• Network timeouts can indicate connectivity issues\n"
            report += "• Some errors are temporary and retrying may help\n"
        
        return report

# Usage in educational context
lab_session = StudentLabSession("TRI2023001", "Network Diagnostics Lab")

# Student tries different targets
targets_to_test = ["polinela.ac.id", "invalid-domain.xyz", "google.com"]

for target in targets_to_test:
    result = lab_session.safe_ping(target)
    print(result['message'])

# Generate final report
print("\n" + lab_session.generate_error_report())
```

### Instructor Dashboard Error Monitoring
```python
class InstructorDashboard:
    """Monitor and analyze student errors for educational insights."""
    
    def __init__(self):
        self.student_errors = {}
        self.common_issues = {}
    
    def log_student_error(self, student_id: str, error: NetdiagError):
        """Log student error for analysis."""
        if student_id not in self.student_errors:
            self.student_errors[student_id] = []
        
        error_data = {
            'timestamp': datetime.now(),
            'error_type': error.__class__.__name__,
            'message': str(error),
            'target': getattr(error, 'target', None),
            'error_code': getattr(error, 'error_code', None)
        }
        
        self.student_errors[student_id].append(error_data)
        
        # Track common issues
        error_type = error.__class__.__name__
        self.common_issues[error_type] = self.common_issues.get(error_type, 0) + 1
    
    def get_teaching_insights(self) -> dict:
        """Generate insights for teaching improvement."""
        total_errors = sum(self.common_issues.values())
        
        if total_errors == 0:
            return {'message': 'No errors to analyze yet.'}
        
        insights = {
            'total_students': len(self.student_errors),
            'total_errors': total_errors,
            'common_issues': [],
            'teaching_recommendations': []
        }
        
        # Analyze common issues
        for error_type, count in sorted(self.common_issues.items(), 
                                      key=lambda x: x[1], reverse=True):
            percentage = (count / total_errors) * 100
            insights['common_issues'].append({
                'error_type': error_type,
                'count': count,
                'percentage': percentage
            })
        
        # Generate teaching recommendations
        if 'DNSResolutionError' in self.common_issues:
            insights['teaching_recommendations'].append(
                "Many students struggle with DNS concepts. "
                "Consider additional explanation of domain name resolution."
            )
        
        if 'ValidationError' in self.common_issues:
            insights['teaching_recommendations'].append(
                "Input validation errors are common. "
                "Emphasize the importance of proper IP/domain format."
            )
        
        if 'PortTimeoutError' in self.common_issues:
            insights['teaching_recommendations'].append(
                "Port timeout errors suggest network latency issues. "
                "Discuss network performance factors and timeout settings."
            )
        
        return insights

# Usage example
dashboard = InstructorDashboard()

# Simulate student errors during lab
try:
    netdiag.ping("invalid-domain")
except DNSResolutionError as e:
    dashboard.log_student_error("student_001", e)

try:
    netdiag.port_scan("slow-server.com", [80])
except PortTimeoutError as e:
    dashboard.log_student_error("student_002", e)

# Get insights for teaching
insights = dashboard.get_teaching_insights()
print("Teaching Insights:", insights)
```

---

## 🔍 Debugging Tips

### 1. Enable Verbose Error Information
```python
import logging
from netdiag.exceptions import NetdiagError

# Configure detailed logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('netdiag')

try:
    result = netdiag.comprehensive_analysis("problematic-target.com")
except NetdiagError as e:
    # Log detailed error information
    logger.error("Network analysis failed", extra={
        'error_dict': e.to_dict(),
        'target': e.target,
        'error_code': e.error_code,
        'details': e.details
    })
```

### 2. Create Custom Exception Classes
```python
class CampusNetworkError(NetdiagError):
    """Campus-specific network errors."""
    
    def __init__(self, message: str, campus_building: str, 
                 network_segment: str, **kwargs):
        super().__init__(message, **kwargs)
        self.campus_building = building
        self.network_segment = network_segment
    
    def get_help_desk_info(self) -> str:
        """Get campus help desk information."""
        return f"Contact IT Support for {self.campus_building} network issues."

# Usage in campus-specific applications
def analyze_campus_connectivity(building: str, segment: str):
    try:
        # Perform campus network analysis
        pass
    except NetdiagError as e:
        # Wrap in campus-specific error
        raise CampusNetworkError(
            f"Campus network issue in {building}",
            campus_building=building,
            network_segment=segment
        ) from e
```

---

**Exception Safety: 100% | Error Recovery: ✅ | Educational Focus: 🎓**

For more information, see:
- [Function Documentation](functions.md)
- [Data Models](models.md)
- [API Reference](README.md)