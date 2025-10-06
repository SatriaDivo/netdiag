# 📚 API Reference

Welcome to the **Netdiag API Reference** - comprehensive documentation for all functions, classes, and modules in the Netdiag toolkit.

## 📋 Table of Contents

- [Overview](#-overview)
- [Core Modules](#-core-modules)
- [Function Categories](#-function-categories)
- [Data Models](#-data-models)
- [Exception Handling](#-exception-handling)
- [Usage Examples](#-usage-examples)

## 🎯 Overview

Netdiag provides **52 comprehensive network diagnostic functions** organized into logical modules for easy use and maintenance.

### API Design Principles
- **Clean Code**: SOLID principles implementation
- **Type Safety**: Full type hints for Python 3.7+
- **Error Handling**: Comprehensive exception hierarchy
- **Performance**: Optimized for educational and professional use
- **Extensibility**: Modular design for easy expansion

### Version Information
```python
import netdiag
print(f"Version: {netdiag.__version__}")
print(f"Python: {netdiag.__python_version__}")
```

## 🧩 Core Modules

### 1. Core Diagnostics (`netdiag.core`)
Primary network diagnostic functions for connectivity, DNS, and routing.

### 2. Port Scanner (`netdiag.ports`)
Advanced port scanning and service detection capabilities.

### 3. Network Analysis (`netdiag.analysis`)
Network performance analysis and monitoring tools.

### 4. Utils (`netdiag.utils`)
Utility functions for data processing and validation.

### 5. Models (`netdiag.models`)
Data models and structures for network information.

### 6. Exceptions (`netdiag.exceptions`)
Custom exception hierarchy for error handling.

### 7. Profiler (`netdiag.profiler`)
Performance monitoring and profiling tools.

### 8. Modern Features (`netdiag.modern_features`)
Python 3.7+ advanced features and patterns.

## 🔍 Function Categories

### Connectivity Testing
```python
# Basic connectivity
netdiag.ping(target, count=4, timeout=3)
netdiag.check_connectivity(target)
netdiag.is_host_alive(target)

# Advanced connectivity
netdiag.ping_sweep(network_range)
netdiag.multi_ping(targets)
netdiag.continuous_ping(target, duration=60)
```

### DNS Operations
```python
# DNS lookup and resolution
netdiag.dns_lookup(domain)
netdiag.reverse_dns(ip_address)
netdiag.dns_record_lookup(domain, record_type)

# Advanced DNS
netdiag.dns_performance_test(domain)
netdiag.dns_server_test(dns_server)
netdiag.dns_cache_analysis()
```

### Port Scanning
```python
# Port operations
netdiag.check_port(target, port)
netdiag.port_scan(target, ports)
netdiag.port_range_scan(target, start_port, end_port)

# Service detection
netdiag.service_detection(target, port)
netdiag.banner_grabbing(target, port)
netdiag.os_fingerprinting(target)
```

### Network Routing
```python
# Route analysis
netdiag.traceroute(target)
netdiag.trace_path(target)
netdiag.route_analysis(target)

# Advanced routing
netdiag.mtr_analysis(target)
netdiag.network_path_discovery(target)
netdiag.hop_analysis(target)
```

### Performance Monitoring
```python
# Performance testing
netdiag.bandwidth_test(target)
netdiag.latency_test(target)
netdiag.jitter_analysis(target)

# Monitoring
netdiag.network_monitor(target, duration)
netdiag.performance_baseline(target)
netdiag.quality_assessment(target)
```

### Network Information
```python
# Interface information
netdiag.get_network_interfaces()
netdiag.get_default_gateway()
netdiag.get_local_ip()

# System information
netdiag.get_network_config()
netdiag.get_routing_table()
netdiag.get_arp_table()
```

### Security Analysis
```python
# Security scanning
netdiag.vulnerability_scan(target)
netdiag.ssl_certificate_check(target)
netdiag.security_headers_check(target)

# Protocol analysis
netdiag.protocol_analysis(target)
netdiag.encryption_check(target)
netdiag.firewall_detection(target)
```

### Utilities and Helpers
```python
# Data processing
netdiag.ip_range_generator(network)
netdiag.subnet_calculator(network)
netdiag.mac_address_lookup(mac)

# Validation
netdiag.validate_ip(ip_address)
netdiag.validate_domain(domain)
netdiag.validate_port(port)

# Conversion
netdiag.cidr_to_netmask(cidr)
netdiag.netmask_to_cidr(netmask)
netdiag.ip_to_binary(ip_address)
```

## 📊 Data Models

### NetworkResult
```python
from netdiag.models import NetworkResult

@dataclass(frozen=True, slots=True)
class NetworkResult:
    target: str
    timestamp: datetime
    success: bool
    data: dict[str, Any]
    error: Optional[str] = None
    duration: Optional[float] = None
```

### PingResult
```python
from netdiag.models import PingResult

@dataclass(frozen=True, slots=True)
class PingResult:
    target: str
    packets_sent: int
    packets_received: int
    packet_loss: float
    min_time: float
    max_time: float
    avg_time: float
    std_dev: float
```

### DNSResult
```python
from netdiag.models import DNSResult

@dataclass(frozen=True, slots=True)
class DNSResult:
    domain: str
    ip_address: str
    dns_server: str
    query_time: float
    record_type: str
    ttl: int
```

### PortScanResult
```python
from netdiag.models import PortScanResult

@dataclass(frozen=True, slots=True)
class PortScanResult:
    target: str
    port: int
    status: str  # 'open', 'closed', 'filtered'
    service: Optional[str]
    banner: Optional[str]
    scan_time: float
```

### TracerouteResult
```python
from netdiag.models import TracerouteResult

@dataclass(frozen=True, slots=True)
class TracerouteResult:
    target: str
    hops: list[TracerouteHop]
    total_hops: int
    success: bool
    duration: float
```

## ⚠️ Exception Handling

### Exception Hierarchy
```python
from netdiag.exceptions import (
    NetdiagError,          # Base exception
    NetworkError,          # Network-related errors
    DNSError,             # DNS-specific errors
    PortError,            # Port-related errors
    TimeoutError,         # Timeout errors
    ValidationError,      # Input validation errors
    ConfigurationError,   # Configuration errors
    PermissionError       # Permission-related errors
)
```

### Error Handling Examples
```python
from netdiag.exceptions import NetworkError, DNSError

try:
    result = netdiag.ping("invalid-domain.xyz")
except DNSError as e:
    print(f"DNS Error: {e}")
except NetworkError as e:
    print(f"Network Error: {e}")
except Exception as e:
    print(f"Unexpected Error: {e}")
```

## 🎓 Usage Examples

### Basic Usage
```python
import netdiag

# Simple connectivity test
if netdiag.ping("polinela.ac.id"):
    print("✅ Connected to Polinela")
else:
    print("❌ Connection failed")
```

### Advanced Usage with Error Handling
```python
import netdiag
from netdiag.exceptions import NetworkError

try:
    # Comprehensive network analysis
    target = "polinela.ac.id"
    
    # Connectivity
    ping_result = netdiag.ping(target, count=5)
    print(f"Ping: {ping_result.avg_time:.2f}ms")
    
    # DNS
    dns_result = netdiag.dns_lookup(target)
    print(f"IP: {dns_result.ip_address}")
    
    # Ports
    ports = netdiag.port_scan(target, [80, 443, 22])
    open_ports = [p.port for p in ports if p.status == 'open']
    print(f"Open ports: {open_ports}")
    
except NetworkError as e:
    print(f"Network error: {e}")
```

### Professional Usage with Modern Features
```python
from netdiag.modern_features import NetworkConfiguration, EnhancedNetworkResult
from typing import Protocol

class NetworkAnalyzer(Protocol):
    def analyze(self, target: str) -> EnhancedNetworkResult: ...

# Configuration
config = NetworkConfiguration.create_default() \
    .with_timeout(10) \
    .with_retries(3) \
    .enable_verbose_logging()

# Analysis
result = netdiag.comprehensive_analysis("polinela.ac.id", config=config)
```

## 📖 Detailed Documentation

For comprehensive information about each function and class:

- **[Function Documentation](functions.md)** - Detailed reference for all 52 functions
- **[Data Models](models.md)** - Complete model specifications
- **[Exception Handling](exceptions.md)** - Error handling best practices

## 🔗 Quick Reference Links

### Core Functions
- [`ping()`](functions.md#ping) - ICMP connectivity test
- [`dns_lookup()`](functions.md#dns_lookup) - DNS resolution
- [`port_scan()`](functions.md#port_scan) - Port scanning
- [`traceroute()`](functions.md#traceroute) - Route tracing

### Advanced Functions
- [`comprehensive_analysis()`](functions.md#comprehensive_analysis) - Full network analysis
- [`performance_monitor()`](functions.md#performance_monitor) - Performance monitoring
- [`security_scan()`](functions.md#security_scan) - Security assessment
- [`network_discovery()`](functions.md#network_discovery) - Network discovery

### Utility Functions
- [`validate_target()`](functions.md#validate_target) - Input validation
- [`format_results()`](functions.md#format_results) - Result formatting
- [`export_report()`](functions.md#export_report) - Report generation
- [`configure_logging()`](functions.md#configure_logging) - Logging setup

## 💡 Best Practices

1. **Always handle exceptions** for robust applications
2. **Use type hints** for better code quality
3. **Configure timeouts** appropriately for your environment
4. **Validate inputs** before processing
5. **Log operations** for debugging and auditing
6. **Use modern features** for better performance and maintainability

## 🤝 Contributing to API

We welcome contributions to improve the API:

1. **Found a bug?** [Report it](https://github.com/SatriaDivo/netdiag/issues)
2. **Want to add features?** [Submit a PR](https://github.com/SatriaDivo/netdiag/pulls)
3. **Need clarification?** [Start a discussion](https://github.com/SatriaDivo/netdiag/discussions)

---

**Explore the full API power! 🚀**