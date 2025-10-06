# 📊 Data Models

Comprehensive documentation for all data models and structures used in the Netdiag toolkit. These models provide type safety, validation, and consistent data representation across all functions.

## 📋 Table of Contents

- [Core Models](#-core-models)
- [Result Models](#-result-models)
- [Configuration Models](#-configuration-models)
- [Advanced Models](#-advanced-models)
- [Utility Models](#-utility-models)
- [Modern Features](#-modern-features)

---

## 🎯 Core Models

### `NetworkResult`
Base result class for all network operations.

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional

@dataclass(frozen=True, slots=True)
class NetworkResult:
    """Base class for all network operation results."""
    target: str
    timestamp: datetime
    success: bool
    data: dict[str, Any]
    error: Optional[str] = None
    duration: Optional[float] = None
    
    def __post_init__(self):
        """Validate result data after initialization."""
        if not self.target:
            raise ValueError("Target cannot be empty")
        if self.duration is not None and self.duration < 0:
            raise ValueError("Duration cannot be negative")
```

**Usage Example:**
```python
from datetime import datetime
from netdiag.models import NetworkResult

result = NetworkResult(
    target="polinela.ac.id",
    timestamp=datetime.now(),
    success=True,
    data={"response_time": 25.5, "status": "ok"},
    duration=0.025
)

print(f"Target: {result.target}")
print(f"Success: {result.success}")
print(f"Duration: {result.duration}s")
```

### `BaseConfiguration`
Base configuration class for network operations.

```python
@dataclass(frozen=True, slots=True)
class BaseConfiguration:
    """Base configuration for network operations."""
    timeout: int = 5
    retries: int = 3
    verbose: bool = False
    ipv6: bool = False
    
    def validate(self) -> None:
        """Validate configuration parameters."""
        if self.timeout <= 0:
            raise ValueError("Timeout must be positive")
        if self.retries < 0:
            raise ValueError("Retries cannot be negative")
```

---

## 📈 Result Models

### `PingResult`
Comprehensive ping test results.

```python
@dataclass(frozen=True, slots=True)
class PingResult:
    """Results from ping operation."""
    target: str
    packets_sent: int
    packets_received: int
    packet_loss: float
    min_time: float
    max_time: float
    avg_time: float
    std_dev: float
    timestamp: datetime = field(default_factory=datetime.now)
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate percentage."""
        if self.packets_sent == 0:
            return 0.0
        return (self.packets_received / self.packets_sent) * 100
    
    def is_successful(self) -> bool:
        """Check if ping was successful."""
        return self.packet_loss < 100.0 and self.packets_received > 0
```

**Usage Example:**
```python
ping_result = netdiag.ping("polinela.ac.id", count=5)
print(f"Success rate: {ping_result.success_rate:.1f}%")
print(f"Average latency: {ping_result.avg_time:.2f}ms")
print(f"Jitter (std dev): {ping_result.std_dev:.2f}ms")
```

### `DNSResult`
DNS lookup and resolution results.

```python
@dataclass(frozen=True, slots=True)
class DNSResult:
    """Results from DNS lookup operation."""
    domain: str
    ip_address: str
    dns_server: str
    query_time: float
    record_type: str
    ttl: int
    authoritative: bool = False
    cached: bool = False
    additional_records: dict[str, list[str]] = field(default_factory=dict)
    
    def is_valid_ip(self) -> bool:
        """Check if returned IP is valid."""
        import ipaddress
        try:
            ipaddress.ip_address(self.ip_address)
            return True
        except ValueError:
            return False
```

**Usage Example:**
```python
dns_result = netdiag.dns_lookup("polinela.ac.id")
print(f"Domain: {dns_result.domain}")
print(f"IP: {dns_result.ip_address}")
print(f"DNS Server: {dns_result.dns_server}")
print(f"Query Time: {dns_result.query_time:.2f}ms")
print(f"TTL: {dns_result.ttl} seconds")
print(f"Authoritative: {dns_result.authoritative}")
```

### `PortScanResult`
Port scanning results with service detection.

```python
@dataclass(frozen=True, slots=True)
class PortScanResult:
    """Results from port scanning operation."""
    target: str
    port: int
    status: str  # 'open', 'closed', 'filtered', 'unknown'
    service: Optional[str] = None
    version: Optional[str] = None
    banner: Optional[str] = None
    scan_time: float = 0.0
    response_time: Optional[float] = None
    
    @property
    def is_open(self) -> bool:
        """Check if port is open."""
        return self.status.lower() == 'open'
    
    @property
    def service_info(self) -> str:
        """Get formatted service information."""
        if self.service:
            info = self.service
            if self.version:
                info += f" {self.version}"
            return info
        return "Unknown service"
```

**Usage Example:**
```python
port_results = netdiag.port_scan("polinela.ac.id", [80, 443, 22])
for result in port_results:
    if result.is_open:
        print(f"Port {result.port}: {result.service_info}")
        if result.banner:
            print(f"  Banner: {result.banner[:50]}...")
```

### `TracerouteResult`
Network route tracing results.

```python
@dataclass(frozen=True, slots=True)
class TracerouteHop:
    """Single hop in traceroute."""
    number: int
    ip: str
    hostname: Optional[str]
    rtt: float
    timeout: bool = False
    
@dataclass(frozen=True, slots=True)
class TracerouteResult:
    """Results from traceroute operation."""
    target: str
    hops: list[TracerouteHop]
    total_hops: int
    success: bool
    duration: float
    destination_reached: bool = False
    
    @property
    def final_hop(self) -> Optional[TracerouteHop]:
        """Get the final hop."""
        return self.hops[-1] if self.hops else None
    
    def get_hop_by_number(self, hop_number: int) -> Optional[TracerouteHop]:
        """Get hop by its number."""
        for hop in self.hops:
            if hop.number == hop_number:
                return hop
        return None
```

**Usage Example:**
```python
trace = netdiag.traceroute("polinela.ac.id")
print(f"Destination reached: {trace.destination_reached}")
print(f"Total hops: {trace.total_hops}")

for hop in trace.hops:
    hostname = hop.hostname or "Unknown"
    print(f"Hop {hop.number}: {hop.ip} ({hostname}) - {hop.rtt:.2f}ms")
```

---

## ⚙️ Configuration Models

### `NetworkConfiguration`
Advanced configuration for network operations.

```python
@dataclass(frozen=True, slots=True)
class NetworkConfiguration:
    """Advanced network operation configuration."""
    timeout: int = 5
    retries: int = 3
    concurrent_limit: int = 50
    user_agent: str = "Netdiag/1.1.0"
    follow_redirects: bool = True
    verify_ssl: bool = True
    interface: Optional[str] = None
    source_ip: Optional[str] = None
    
    @classmethod
    def create_default(cls) -> 'NetworkConfiguration':
        """Create default configuration."""
        return cls()
    
    def with_timeout(self, timeout: int) -> 'NetworkConfiguration':
        """Create new config with different timeout."""
        return dataclasses.replace(self, timeout=timeout)
    
    def with_retries(self, retries: int) -> 'NetworkConfiguration':
        """Create new config with different retry count."""
        return dataclasses.replace(self, retries=retries)
    
    def enable_verbose_logging(self) -> 'NetworkConfiguration':
        """Enable verbose logging."""
        return dataclasses.replace(self, verbose=True)
```

**Usage Example:**
```python
from netdiag.models import NetworkConfiguration

# Method chaining configuration
config = NetworkConfiguration.create_default() \
    .with_timeout(10) \
    .with_retries(5) \
    .enable_verbose_logging()

# Use configuration
result = netdiag.comprehensive_analysis("polinela.ac.id", config=config)
```

### `ScanConfiguration`
Specialized configuration for scanning operations.

```python
@dataclass(frozen=True, slots=True)
class ScanConfiguration:
    """Configuration for scanning operations."""
    ports: list[int] = field(default_factory=lambda: [80, 443, 22, 21, 25])
    threads: int = 50
    timeout_per_port: int = 3
    service_detection: bool = True
    banner_grabbing: bool = False
    stealth_mode: bool = False
    scan_delay: float = 0.0
    
    def validate(self) -> None:
        """Validate scan configuration."""
        if not self.ports:
            raise ValueError("Port list cannot be empty")
        if self.threads <= 0:
            raise ValueError("Thread count must be positive")
        if any(port < 1 or port > 65535 for port in self.ports):
            raise ValueError("Invalid port number")
```

---

## 🔬 Advanced Models

### `PerformanceMetrics`
Performance monitoring data model.

```python
@dataclass(frozen=True, slots=True)
class PerformanceMetrics:
    """Performance metrics collection."""
    latency_ms: float
    jitter_ms: float
    packet_loss_percent: float
    bandwidth_mbps: float
    timestamp: datetime
    
    @property
    def quality_score(self) -> float:
        """Calculate quality score (0-100)."""
        # Lower latency = higher score
        latency_score = max(0, 100 - (self.latency_ms / 10))
        
        # Lower jitter = higher score
        jitter_score = max(0, 100 - (self.jitter_ms * 5))
        
        # Lower packet loss = higher score
        loss_score = max(0, 100 - (self.packet_loss_percent * 10))
        
        return (latency_score + jitter_score + loss_score) / 3

@dataclass(frozen=True, slots=True)
class PerformanceReport:
    """Performance monitoring report."""
    target: str
    duration: int
    metrics: list[PerformanceMetrics]
    start_time: datetime
    end_time: datetime
    
    @property
    def average_latency(self) -> float:
        """Calculate average latency."""
        if not self.metrics:
            return 0.0
        return sum(m.latency_ms for m in self.metrics) / len(self.metrics)
    
    @property
    def average_quality_score(self) -> float:
        """Calculate average quality score."""
        if not self.metrics:
            return 0.0
        return sum(m.quality_score for m in self.metrics) / len(self.metrics)
```

### `SecurityAssessment`
Security analysis results.

```python
@dataclass(frozen=True, slots=True)
class SecurityVulnerability:
    """Individual security vulnerability."""
    name: str
    severity: str  # 'low', 'medium', 'high', 'critical'
    description: str
    recommendation: str
    cve_id: Optional[str] = None
    
@dataclass(frozen=True, slots=True)
class SecurityAssessment:
    """Security assessment results."""
    target: str
    vulnerabilities: list[SecurityVulnerability]
    ssl_grade: Optional[str] = None
    security_headers_score: int = 0
    open_ports: list[int] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    
    @property
    def risk_level(self) -> str:
        """Calculate overall risk level."""
        critical_count = sum(1 for v in self.vulnerabilities if v.severity == 'critical')
        high_count = sum(1 for v in self.vulnerabilities if v.severity == 'high')
        
        if critical_count > 0:
            return 'CRITICAL'
        elif high_count > 2:
            return 'HIGH'
        elif high_count > 0 or len(self.vulnerabilities) > 5:
            return 'MEDIUM'
        else:
            return 'LOW'
```

---

## 🛠️ Utility Models

### `NetworkInterface`
Network interface information.

```python
@dataclass(frozen=True, slots=True)
class NetworkInterface:
    """Network interface information."""
    name: str
    ip_address: str
    netmask: str
    broadcast: str
    mac_address: str
    status: str  # 'up', 'down'
    mtu: int
    interface_type: str  # 'ethernet', 'wireless', 'loopback'
    
    @property
    def network(self) -> str:
        """Calculate network address."""
        import ipaddress
        interface = ipaddress.IPv4Interface(f"{self.ip_address}/{self.netmask}")
        return str(interface.network.network_address)
    
    def is_active(self) -> bool:
        """Check if interface is active."""
        return self.status.lower() == 'up'

@dataclass(frozen=True, slots=True)
class RouteEntry:
    """Routing table entry."""
    destination: str
    gateway: str
    interface: str
    metric: int
    flags: str
    
@dataclass(frozen=True, slots=True)
class ARPEntry:
    """ARP table entry."""
    ip: str
    mac: str
    interface: str
    status: str  # 'static', 'dynamic'
```

### `SubnetInfo`
Subnet calculation results.

```python
@dataclass(frozen=True, slots=True)
class SubnetInfo:
    """Subnet calculation information."""
    network: str
    broadcast: str
    netmask: str
    cidr: int
    num_hosts: int
    first_host: str
    last_host: str
    
    @property
    def network_class(self) -> str:
        """Determine network class."""
        first_octet = int(self.network.split('.')[0])
        if 1 <= first_octet <= 126:
            return 'A'
        elif 128 <= first_octet <= 191:
            return 'B'
        elif 192 <= first_octet <= 223:
            return 'C'
        else:
            return 'Unknown'
    
    def contains_ip(self, ip: str) -> bool:
        """Check if IP is in this subnet."""
        import ipaddress
        network = ipaddress.IPv4Network(f"{self.network}/{self.cidr}")
        try:
            return ipaddress.IPv4Address(ip) in network
        except ValueError:
            return False
```

---

## 🚀 Modern Features

### `EnhancedNetworkResult`
Enhanced result class with modern Python features.

```python
from typing import Protocol, TypedDict, Union
from dataclasses import dataclass, field

class NetworkData(TypedDict):
    """Type-safe network data dictionary."""
    response_time: float
    status_code: int
    headers: dict[str, str]

class ResultProcessor(Protocol):
    """Protocol for result processing."""
    def process(self, result: 'EnhancedNetworkResult') -> dict[str, Any]: ...

@dataclass(frozen=True, slots=True)
class EnhancedNetworkResult:
    """Enhanced network result with modern features."""
    target: str
    data: NetworkData
    metadata: dict[str, Any] = field(default_factory=dict)
    _processors: list[ResultProcessor] = field(default_factory=list, init=False)
    
    def with_processor(self, processor: ResultProcessor) -> 'EnhancedNetworkResult':
        """Add result processor using method chaining."""
        new_processors = self._processors + [processor]
        return dataclasses.replace(self, _processors=new_processors)
    
    def process_all(self) -> dict[str, Any]:
        """Process result with all registered processors."""
        results = {}
        for i, processor in enumerate(self._processors):
            results[f"processor_{i}"] = processor.process(self)
        return results
```

### `ValidationResult`
Comprehensive validation result model.

```python
@dataclass(frozen=True, slots=True)
class ValidationError:
    """Individual validation error."""
    field: str
    value: Any
    message: str
    code: str

@dataclass(frozen=True, slots=True)
class ValidationResult:
    """Validation result with details."""
    is_valid: bool
    errors: list[ValidationError] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    
    def add_error(self, field: str, value: Any, message: str, code: str) -> None:
        """Add validation error."""
        error = ValidationError(field, value, message, code)
        # Note: This would normally require special handling since dataclass is frozen
        object.__setattr__(self, 'errors', self.errors + [error])
        object.__setattr__(self, 'is_valid', False)
    
    @property
    def error_count(self) -> int:
        """Get number of errors."""
        return len(self.errors)
    
    @property
    def summary(self) -> str:
        """Get validation summary."""
        if self.is_valid:
            warning_text = f" ({len(self.warnings)} warnings)" if self.warnings else ""
            return f"✅ Valid{warning_text}"
        else:
            return f"❌ Invalid ({len(self.errors)} errors)"
```

---

## 🎓 Educational Examples

### Student Lab Result Model
```python
@dataclass(frozen=True, slots=True)
class LabExerciseResult:
    """Results from educational lab exercise."""
    student_id: str
    exercise_name: str
    target_domain: str
    completed_tasks: list[str]
    test_results: dict[str, bool]
    score: float
    timestamp: datetime
    notes: str = ""
    
    @property
    def grade_letter(self) -> str:
        """Convert score to letter grade."""
        if self.score >= 90:
            return 'A'
        elif self.score >= 80:
            return 'B'
        elif self.score >= 70:
            return 'C'
        elif self.score >= 60:
            return 'D'
        else:
            return 'F'
    
    def export_to_csv(self) -> str:
        """Export result to CSV format."""
        return f"{self.student_id},{self.exercise_name},{self.score},{self.grade_letter},{self.timestamp}"

# Usage in educational context
lab_result = LabExerciseResult(
    student_id="TRI2023001",
    exercise_name="Polinela Network Analysis",
    target_domain="polinela.ac.id",
    completed_tasks=["ping", "dns_lookup", "port_scan"],
    test_results={"connectivity": True, "dns": True, "ports": True},
    score=95.0,
    timestamp=datetime.now(),
    notes="Excellent work on network analysis"
)

print(f"Student Grade: {lab_result.grade_letter}")
print(f"CSV Export: {lab_result.export_to_csv()}")
```

## 💡 Best Practices

### 1. Using Frozen Dataclasses
```python
# ✅ Good: Using frozen dataclasses for immutability
@dataclass(frozen=True, slots=True)
class Result:
    value: str
    timestamp: datetime

# ❌ Avoid: Mutable dataclasses for results
@dataclass
class Result:
    value: str
    timestamp: datetime
```

### 2. Type Safety with Protocol
```python
# ✅ Good: Using Protocol for type safety
class Analyzer(Protocol):
    def analyze(self, data: NetworkResult) -> dict[str, Any]: ...

def process_result(result: NetworkResult, analyzer: Analyzer) -> dict[str, Any]:
    return analyzer.analyze(result)
```

### 3. Method Chaining Pattern
```python
# ✅ Good: Fluent interface with method chaining
config = NetworkConfiguration.create_default() \
    .with_timeout(10) \
    .with_retries(3) \
    .enable_verbose_logging()
```

### 4. Validation in Models
```python
# ✅ Good: Built-in validation
@dataclass(frozen=True, slots=True)
class PingConfig:
    count: int
    timeout: int
    
    def __post_init__(self):
        if self.count <= 0:
            raise ValueError("Count must be positive")
        if self.timeout <= 0:
            raise ValueError("Timeout must be positive")
```

---

**Total Models: 25+ | Type Safety: 100% | Educational Focus: ✅**

For more information, see:
- [Function Documentation](functions.md)
- [Exception Handling](exceptions.md)
- [API Reference](README.md)