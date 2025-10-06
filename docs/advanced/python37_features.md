# Fitur Python 3.7+ dalam NetDiag

## 🐍 Memanfaatkan Fitur Modern Python

### Pengenalan Fitur Python 3.7+

NetDiag dirancang untuk memanfaatkan fitur-fitur modern Python 3.7+ untuk memberikan pengalaman development yang optimal dengan type safety, performance, dan readability yang tinggi.

### Dataclasses (Python 3.7+)

#### Basic Dataclass Usage
```python
from dataclasses import dataclass, field
from typing import List, Optional, Dict
import time

@dataclass
class PingResult:
    """Hasil ping dengan dataclass"""
    host: str
    ip_address: Optional[str] = None
    packets_sent: int = 0
    packets_received: int = 0
    packet_loss: float = 0.0
    min_latency: float = 0.0
    max_latency: float = 0.0
    avg_latency: float = 0.0
    timestamp: float = field(default_factory=time.time)
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate as percentage"""
        if self.packets_sent == 0:
            return 0.0
        return (self.packets_received / self.packets_sent) * 100
    
    def is_healthy(self, threshold: float = 95.0) -> bool:
        """Check if ping result indicates healthy connection"""
        return self.success_rate >= threshold and self.avg_latency < 100

@dataclass
class NetworkInterface:
    """Network interface information"""
    name: str
    ip_address: str
    netmask: str
    is_up: bool = True
    speed: Optional[int] = None  # Mbps
    mtu: int = 1500
    mac_address: Optional[str] = None
    rx_bytes: int = 0
    tx_bytes: int = 0
    
    def __post_init__(self):
        """Validation setelah object creation"""
        if not self.name:
            raise ValueError("Interface name cannot be empty")
        if not self.ip_address:
            raise ValueError("IP address must be specified")

# Usage examples
ping_result = PingResult(
    host="polinela.ac.id",
    ip_address="192.168.1.100",
    packets_sent=4,
    packets_received=4,
    avg_latency=25.5
)

print(f"Success rate: {ping_result.success_rate:.1f}%")
print(f"Connection healthy: {ping_result.is_healthy()}")

interface = NetworkInterface(
    name="eth0",
    ip_address="192.168.1.50",
    netmask="255.255.255.0",
    speed=1000,
    mac_address="aa:bb:cc:dd:ee:ff"
)
```

#### Advanced Dataclass Features
```python
from dataclasses import dataclass, field, InitVar
from typing import List, Dict, Any
import json

@dataclass
class NetworkScanResult:
    """Advanced dataclass dengan complex fields"""
    target_network: str
    scan_type: str
    start_time: float
    duration: float
    hosts_discovered: List[Dict[str, Any]] = field(default_factory=list)
    open_ports: Dict[str, List[int]] = field(default_factory=dict)
    services_detected: Dict[str, str] = field(default_factory=dict)
    
    # Field yang tidak disimpan dalam __init__
    _scan_summary: Dict[str, Any] = field(default_factory=dict, init=False, repr=False)
    
    def __post_init__(self):
        """Generate scan summary"""
        self._scan_summary = {
            'total_hosts': len(self.hosts_discovered),
            'total_open_ports': sum(len(ports) for ports in self.open_ports.values()),
            'scan_rate': len(self.hosts_discovered) / self.duration if self.duration > 0 else 0
        }
    
    @property
    def summary(self) -> Dict[str, Any]:
        """Get scan summary"""
        return self._scan_summary
    
    def to_json(self) -> str:
        """Export to JSON (excluding internal fields)"""
        export_data = {
            'target_network': self.target_network,
            'scan_type': self.scan_type,
            'start_time': self.start_time,
            'duration': self.duration,
            'hosts_discovered': self.hosts_discovered,
            'open_ports': self.open_ports,
            'services_detected': self.services_detected,
            'summary': self._scan_summary
        }
        return json.dumps(export_data, indent=2)

@dataclass
class MonitoringConfig:
    """Configuration dengan validation dan conversion"""
    target: str
    interval: InitVar[int]  # Tidak disimpan sebagai field
    timeout: int = 5
    retries: int = 3
    
    # Field yang dihitung dari InitVar
    interval_seconds: int = field(init=False)
    
    def __post_init__(self, interval: int):
        """Process InitVar and validate"""
        if interval < 10:
            raise ValueError("Interval must be at least 10 seconds")
        
        self.interval_seconds = interval
        
        # Additional validation
        if self.timeout >= self.interval_seconds:
            raise ValueError("Timeout must be less than interval")

# Usage
scan_result = NetworkScanResult(
    target_network="192.168.1.0/24",
    scan_type="tcp_connect",
    start_time=time.time(),
    duration=45.2
)

scan_result.hosts_discovered.append({
    'ip': '192.168.1.1',
    'hostname': 'gateway.polinela.ac.id',
    'status': 'up'
})

print(f"Scan summary: {scan_result.summary}")
print(scan_result.to_json())
```

### Type Hints yang Advanced

#### Union Types dan Optional
```python
from typing import Union, Optional, List, Dict, Callable, TypeVar, Generic
from ipaddress import IPv4Address, IPv6Address

# Type aliases untuk readability
IPAddress = Union[IPv4Address, IPv6Address]
HostIdentifier = Union[str, IPAddress]
PortNumber = int
ServiceMap = Dict[PortNumber, str]

def resolve_host(host: HostIdentifier) -> Optional[IPAddress]:
    """Resolve hostname to IP address"""
    if isinstance(host, (IPv4Address, IPv6Address)):
        return host
    
    try:
        # DNS resolution logic
        return IPv4Address("192.168.1.100")  # Simplified
    except Exception:
        return None

def scan_ports(
    target: HostIdentifier,
    ports: List[PortNumber],
    timeout: float = 5.0,
    callback: Optional[Callable[[PortNumber, bool], None]] = None
) -> ServiceMap:
    """Scan ports dengan type hints yang comprehensive"""
    
    resolved_ip = resolve_host(target)
    if not resolved_ip:
        raise ValueError(f"Cannot resolve host: {target}")
    
    service_map: ServiceMap = {}
    
    for port in ports:
        # Port scanning logic
        is_open = True  # Simplified
        
        if callback:
            callback(port, is_open)
        
        if is_open:
            service_map[port] = f"service_on_{port}"
    
    return service_map

# Usage dengan type checking
target_host: HostIdentifier = "polinela.ac.id"
common_ports: List[PortNumber] = [22, 80, 443, 8080]

def port_callback(port: PortNumber, is_open: bool) -> None:
    status = "OPEN" if is_open else "CLOSED"
    print(f"Port {port}: {status}")

services = scan_ports(target_host, common_ports, callback=port_callback)
```

#### Generic Types dan TypeVar
```python
from typing import TypeVar, Generic, List, Optional, Iterator
from abc import ABC, abstractmethod

T = TypeVar('T')
ResultType = TypeVar('ResultType')

class DataCollector(Generic[T]):
    """Generic data collector"""
    
    def __init__(self):
        self._data: List[T] = []
    
    def add(self, item: T) -> None:
        """Add item to collection"""
        self._data.append(item)
    
    def get_all(self) -> List[T]:
        """Get all collected data"""
        return self._data.copy()
    
    def filter(self, predicate: Callable[[T], bool]) -> List[T]:
        """Filter data based on predicate"""
        return [item for item in self._data if predicate(item)]
    
    def __iter__(self) -> Iterator[T]:
        """Make collector iterable"""
        return iter(self._data)

class Processor(ABC, Generic[T, ResultType]):
    """Abstract processor dengan generic types"""
    
    @abstractmethod
    def process(self, data: T) -> ResultType:
        """Process single data item"""
        pass
    
    def process_batch(self, data: List[T]) -> List[ResultType]:
        """Process batch of data"""
        return [self.process(item) for item in data]

class PingProcessor(Processor[str, PingResult]):
    """Concrete processor untuk ping operations"""
    
    def process(self, host: str) -> PingResult:
        """Process ping untuk single host"""
        # Ping logic here
        return PingResult(
            host=host,
            ip_address="192.168.1.100",
            packets_sent=4,
            packets_received=4,
            avg_latency=25.0
        )

# Usage
ping_collector: DataCollector[str] = DataCollector()
ping_collector.add("polinela.ac.id")
ping_collector.add("mail.polinela.ac.id")

processor = PingProcessor()
results = processor.process_batch(ping_collector.get_all())

for result in results:
    print(f"{result.host}: {result.avg_latency}ms")
```

### Protocol Types (Python 3.8+)

#### Structural Typing dengan Protocol
```python
from typing import Protocol, runtime_checkable
from abc import abstractmethod

@runtime_checkable
class Pingable(Protocol):
    """Protocol untuk objects yang bisa di-ping"""
    
    def ping(self, timeout: float = 5.0) -> PingResult:
        """Ping the target"""
        ...
    
    @property
    def address(self) -> str:
        """Get target address"""
        ...

@runtime_checkable
class Monitorable(Protocol):
    """Protocol untuk objects yang bisa di-monitor"""
    
    def start_monitoring(self, interval: int) -> None:
        """Start monitoring"""
        ...
    
    def stop_monitoring(self) -> None:
        """Stop monitoring"""
        ...
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status"""
        ...

class NetworkHost:
    """Concrete implementation of protocols"""
    
    def __init__(self, hostname: str):
        self.hostname = hostname
        self._monitoring = False
    
    def ping(self, timeout: float = 5.0) -> PingResult:
        """Implement Pingable protocol"""
        return PingResult(host=self.hostname, avg_latency=25.0)
    
    @property
    def address(self) -> str:
        """Implement Pingable protocol"""
        return self.hostname
    
    def start_monitoring(self, interval: int) -> None:
        """Implement Monitorable protocol"""
        self._monitoring = True
        print(f"Started monitoring {self.hostname} every {interval}s")
    
    def stop_monitoring(self) -> None:
        """Implement Monitorable protocol"""
        self._monitoring = False
        print(f"Stopped monitoring {self.hostname}")
    
    def get_status(self) -> Dict[str, Any]:
        """Implement Monitorable protocol"""
        return {
            'hostname': self.hostname,
            'monitoring': self._monitoring,
            'last_check': time.time()
        }

def monitor_target(target: Monitorable) -> None:
    """Function yang menggunakan Protocol"""
    target.start_monitoring(30)
    status = target.get_status()
    print(f"Monitoring status: {status}")

def ping_target(target: Pingable) -> PingResult:
    """Function yang menggunakan Protocol"""
    return target.ping()

# Usage - duck typing dengan runtime checking
host = NetworkHost("polinela.ac.id")

# Runtime checking
if isinstance(host, Pingable):
    result = ping_target(host)
    print(f"Ping result: {result.avg_latency}ms")

if isinstance(host, Monitorable):
    monitor_target(host)
```

### F-strings yang Advanced (Python 3.8+)

#### Debugging dan Formatting
```python
import time
from datetime import datetime

def advanced_formatting_examples():
    """Contoh advanced f-string formatting"""
    
    # Basic variables
    host = "polinela.ac.id"
    latency = 25.567
    packet_loss = 0.02
    timestamp = time.time()
    
    # Debugging dengan = (Python 3.8+)
    print(f"{host=}")  # host='polinela.ac.id'
    print(f"{latency=:.2f}")  # latency=25.57
    
    # Formatting angka
    print(f"Latency: {latency:.2f}ms")
    print(f"Packet loss: {packet_loss:.1%}")  # 2.0%
    print(f"Bandwidth: {1024**3:,} bytes")    # 1,073,741,824 bytes
    
    # Datetime formatting
    dt = datetime.fromtimestamp(timestamp)
    print(f"Time: {dt:%Y-%m-%d %H:%M:%S}")
    
    # Conditional formatting
    status = "HEALTHY" if latency < 50 else "SLOW"
    print(f"Status: {status}")
    
    # Multi-line f-strings
    report = f"""
Network Analysis Report
======================
Host: {host}
Latency: {latency:.2f}ms
Packet Loss: {packet_loss:.1%}
Status: {status}
Timestamp: {dt:%Y-%m-%d %H:%M:%S}
    """
    print(report)
    
    # Expression evaluation dalam f-strings
    speeds = [100, 250, 500, 1000]
    print(f"Max speed: {max(speeds)}Mbps")
    print(f"Average: {sum(speeds)/len(speeds):.1f}Mbps")

# Network monitoring dengan f-strings
def format_monitoring_output(results: List[PingResult]) -> str:
    """Format monitoring results dengan advanced f-strings"""
    
    if not results:
        return "No monitoring data available"
    
    # Calculate statistics
    avg_latency = sum(r.avg_latency for r in results) / len(results)
    max_latency = max(r.avg_latency for r in results)
    min_latency = min(r.avg_latency for r in results)
    
    # Generate report
    return f"""
Monitoring Summary ({len(results)} samples)
{'='*50}
Average Latency: {avg_latency:>8.2f}ms
Maximum Latency: {max_latency:>8.2f}ms  
Minimum Latency: {min_latency:>8.2f}ms
Latency Range:   {max_latency - min_latency:>8.2f}ms

Recent Results:
{chr(10).join(f"  {r.host:<20} {r.avg_latency:>6.1f}ms" for r in results[-5:])}
    """

# Usage
results = [
    PingResult("polinela.ac.id", avg_latency=25.5),
    PingResult("mail.polinela.ac.id", avg_latency=30.2),
    PingResult("library.polinela.ac.id", avg_latency=22.8)
]

print(format_monitoring_output(results))
```

### Walrus Operator (Python 3.8+)

#### Assignment Expressions
```python
import re
import time

def network_analysis_with_walrus():
    """Contoh penggunaan walrus operator dalam network analysis"""
    
    # Reading dan processing dalam satu expression
    log_entries = [
        "192.168.1.1 - ping successful - 25ms",
        "192.168.1.2 - ping failed - timeout",
        "192.168.1.3 - ping successful - 45ms"
    ]
    
    # Extract latency values menggunakan walrus operator
    latencies = []
    for entry in log_entries:
        if (match := re.search(r'(\d+)ms', entry)):
            latencies.append(int(match.group(1)))
    
    print(f"Extracted latencies: {latencies}")
    
    # Conditional assignment
    hosts_to_check = ["polinela.ac.id", "google.com", "cloudflare.com"]
    fast_hosts = []
    
    for host in hosts_to_check:
        # Simulate ping
        if (ping_time := simulate_ping(host)) < 50:
            fast_hosts.append((host, ping_time))
    
    print(f"Fast hosts: {fast_hosts}")
    
    # Loop dengan condition check
    monitoring_data = []
    start_time = time.time()
    
    while (elapsed := time.time() - start_time) < 10:  # Monitor for 10 seconds
        # Simulate data collection
        if (current_latency := simulate_ping("polinela.ac.id")) is not None:
            monitoring_data.append({
                'timestamp': time.time(),
                'latency': current_latency,
                'elapsed': elapsed
            })
        
        time.sleep(1)
    
    return monitoring_data

def simulate_ping(host: str) -> Optional[float]:
    """Simulate ping operation"""
    import random
    return random.uniform(10, 100)

def process_network_logs(log_file: str):
    """Process network logs dengan walrus operator"""
    
    with open(log_file, 'r') as file:
        # Process lines dan filter dalam satu loop
        error_count = 0
        warning_count = 0
        
        while (line := file.readline()):
            line = line.strip()
            
            if 'ERROR' in line:
                error_count += 1
                if (match := re.search(r'(\d+\.\d+\.\d+\.\d+)', line)):
                    print(f"Error from IP: {match.group(1)}")
            
            elif 'WARNING' in line and (severity := extract_severity(line)):
                warning_count += 1
                print(f"Warning level {severity}")
        
        return {'errors': error_count, 'warnings': warning_count}

def extract_severity(log_line: str) -> Optional[int]:
    """Extract severity level from log line"""
    if match := re.search(r'level (\d+)', log_line):
        return int(match.group(1))
    return None
```

### Positional-Only Parameters (Python 3.8+)

#### API Design dengan Parameter Control
```python
def ping_host(host, /, *, timeout=5, retries=3, verbose=False):
    """
    Ping host dengan controlled parameter passing
    
    Parameters:
    - host: positional-only parameter
    - timeout, retries, verbose: keyword-only parameters
    """
    if verbose:
        print(f"Pinging {host} with timeout={timeout}, retries={retries}")
    
    # Ping implementation
    return PingResult(host=host, avg_latency=25.0)

def analyze_network(network_range, /, scan_type="ping", *, 
                   concurrent_threads=4, timeout=5, save_results=True):
    """
    Network analysis dengan parameter restrictions
    
    Args:
        network_range: Must be positional (/) 
        scan_type: Can be positional or keyword
        concurrent_threads, timeout, save_results: Must be keyword-only (*)
    """
    print(f"Analyzing {network_range} using {scan_type}")
    print(f"Threads: {concurrent_threads}, Timeout: {timeout}")
    print(f"Save results: {save_results}")

# Usage examples - benar
ping_host("polinela.ac.id")  # ✓
ping_host("polinela.ac.id", timeout=10)  # ✓
analyze_network("192.168.1.0/24", concurrent_threads=8)  # ✓

# Usage examples - akan error
# ping_host(host="polinela.ac.id")  # ✗ host harus positional
# analyze_network("192.168.1.0/24", 10)  # ✗ timeout harus keyword

def create_connection(host, port, /, username=None, password=None, *, 
                     ssl=False, verify_cert=True, timeout=30):
    """
    Create network connection dengan mixed parameter types
    
    Positional-only: host, port
    Normal: username, password  
    Keyword-only: ssl, verify_cert, timeout
    """
    connection_info = {
        'host': host,
        'port': port,
        'username': username,
        'ssl': ssl,
        'verify_cert': verify_cert,
        'timeout': timeout
    }
    
    print(f"Creating connection: {connection_info}")
    return connection_info

# Flexible usage
conn1 = create_connection("polinela.ac.id", 443, ssl=True)
conn2 = create_connection("mail.polinela.ac.id", 993, "admin", "secret", ssl=True)
```

### Match-Case Statements (Python 3.10+)

#### Structural Pattern Matching
```python
from enum import Enum
from typing import Union

class NetworkEventType(Enum):
    PING_SUCCESS = "ping_success"
    PING_FAILURE = "ping_failure"
    CONNECTION_LOST = "connection_lost"
    BANDWIDTH_LOW = "bandwidth_low"
    DNS_FAILURE = "dns_failure"

@dataclass
class NetworkEvent:
    event_type: NetworkEventType
    host: str
    timestamp: float
    data: Dict[str, Any] = field(default_factory=dict)

def handle_network_event(event: NetworkEvent) -> str:
    """Handle network events using match-case"""
    
    match event.event_type:
        case NetworkEventType.PING_SUCCESS:
            latency = event.data.get('latency', 0)
            return f"✓ {event.host} responded in {latency}ms"
        
        case NetworkEventType.PING_FAILURE:
            reason = event.data.get('reason', 'unknown')
            return f"✗ {event.host} ping failed: {reason}"
        
        case NetworkEventType.CONNECTION_LOST:
            duration = event.data.get('duration', 0)
            return f"⚠ Connection to {event.host} lost for {duration}s"
        
        case NetworkEventType.BANDWIDTH_LOW:
            current = event.data.get('current_speed', 0)
            threshold = event.data.get('threshold', 0)
            return f"📶 Low bandwidth on {event.host}: {current}Mbps < {threshold}Mbps"
        
        case NetworkEventType.DNS_FAILURE:
            return f"🔍 DNS resolution failed for {event.host}"
        
        case _:
            return f"Unknown event for {event.host}"

def analyze_ping_result(result: Union[PingResult, dict, None]) -> str:
    """Analyze ping result dengan pattern matching"""
    
    match result:
        # Match PingResult object
        case PingResult(avg_latency=latency) if latency < 20:
            return f"Excellent connection: {latency}ms"
        
        case PingResult(avg_latency=latency) if 20 <= latency < 50:
            return f"Good connection: {latency}ms"
        
        case PingResult(avg_latency=latency) if latency >= 50:
            return f"Slow connection: {latency}ms"
        
        case PingResult(packet_loss=loss) if loss > 0:
            return f"Packet loss detected: {loss}%"
        
        # Match dictionary format
        case {"status": "success", "latency": float(latency)}:
            return f"Success: {latency}ms"
        
        case {"status": "failure", "error": str(error)}:
            return f"Failed: {error}"
        
        # Match None
        case None:
            return "No ping result available"
        
        # Default case
        case _:
            return "Unknown ping result format"

def process_network_config(config: dict) -> str:
    """Process network configuration dengan match-case"""
    
    match config:
        # Match specific patterns
        case {
            "type": "ethernet",
            "speed": int(speed),
            "duplex": "full"
        } if speed >= 1000:
            return f"High-speed Ethernet: {speed}Mbps full-duplex"
        
        case {
            "type": "wifi", 
            "ssid": str(ssid),
            "security": "WPA2" | "WPA3"
        }:
            return f"Secure WiFi: {ssid}"
        
        case {
            "type": "vpn",
            "protocol": "wireguard" | "openvpn",
            "server": str(server)
        }:
            return f"VPN connection to {server}"
        
        case {"type": str(net_type)} if net_type in ["ethernet", "wifi", "vpn"]:
            return f"Basic {net_type} configuration"
        
        case _:
            return "Unknown network configuration"

# Usage examples
events = [
    NetworkEvent(
        NetworkEventType.PING_SUCCESS,
        "polinela.ac.id",
        time.time(),
        {"latency": 25.5}
    ),
    NetworkEvent(
        NetworkEventType.BANDWIDTH_LOW,
        "student.polinela.ac.id", 
        time.time(),
        {"current_speed": 50, "threshold": 100}
    )
]

for event in events:
    print(handle_network_event(event))

# Test ping analysis
ping_results = [
    PingResult("fast.com", avg_latency=15.2),
    PingResult("slow.com", avg_latency=75.8, packet_loss=2.0),
    {"status": "success", "latency": 30.5},
    None
]

for result in ping_results:
    print(analyze_ping_result(result))
```

### Async/Await Improvements

#### Modern Async Patterns
```python
import asyncio
import aiohttp
import time
from typing import AsyncIterator, AsyncGenerator

async def async_ping_host(host: str, timeout: float = 5.0) -> PingResult:
    """Async ping implementation"""
    start_time = time.time()
    
    try:
        # Simulate async ping operation
        await asyncio.sleep(0.1)  # Simulate network delay
        
        latency = (time.time() - start_time) * 1000
        return PingResult(
            host=host,
            ip_address="192.168.1.100",
            packets_sent=1,
            packets_received=1,
            avg_latency=latency
        )
    
    except asyncio.TimeoutError:
        return PingResult(
            host=host,
            packets_sent=1,
            packets_received=0,
            packet_loss=100.0
        )

async def ping_multiple_hosts(hosts: List[str]) -> List[PingResult]:
    """Ping multiple hosts concurrently"""
    
    # Create tasks for all hosts
    tasks = [async_ping_host(host) for host in hosts]
    
    # Wait for all tasks to complete
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Filter out exceptions
    return [result for result in results if isinstance(result, PingResult)]

async def monitor_host_continuously(
    host: str, 
    interval: int = 30
) -> AsyncIterator[PingResult]:
    """Continuously monitor host dengan async generator"""
    
    while True:
        result = await async_ping_host(host)
        yield result
        await asyncio.sleep(interval)

async def collect_monitoring_data(
    host: str, 
    duration: int = 300,  # 5 minutes
    interval: int = 30
) -> List[PingResult]:
    """Collect monitoring data for specified duration"""
    
    results = []
    end_time = time.time() + duration
    
    async for result in monitor_host_continuously(host, interval):
        results.append(result)
        
        if time.time() >= end_time:
            break
    
    return results

# Context manager untuk async operations
class AsyncNetworkMonitor:
    def __init__(self, hosts: List[str]):
        self.hosts = hosts
        self.monitoring = False
        self.tasks = []
    
    async def __aenter__(self):
        """Start monitoring when entering context"""
        self.monitoring = True
        
        # Start monitoring tasks for each host
        for host in self.hosts:
            task = asyncio.create_task(self._monitor_host(host))
            self.tasks.append(task)
        
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Stop monitoring when exiting context"""
        self.monitoring = False
        
        # Cancel all monitoring tasks
        for task in self.tasks:
            task.cancel()
        
        # Wait for tasks to complete
        await asyncio.gather(*self.tasks, return_exceptions=True)
    
    async def _monitor_host(self, host: str):
        """Monitor single host"""
        while self.monitoring:
            try:
                result = await async_ping_host(host)
                print(f"{host}: {result.avg_latency:.1f}ms")
                await asyncio.sleep(30)
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error monitoring {host}: {e}")
                await asyncio.sleep(60)

# Usage examples
async def main():
    """Main async function"""
    
    # Single host ping
    result = await async_ping_host("polinela.ac.id")
    print(f"Single ping: {result.avg_latency:.1f}ms")
    
    # Multiple hosts ping
    hosts = [
        "polinela.ac.id",
        "mail.polinela.ac.id", 
        "library.polinela.ac.id"
    ]
    
    results = await ping_multiple_hosts(hosts)
    for result in results:
        print(f"{result.host}: {result.avg_latency:.1f}ms")
    
    # Continuous monitoring dengan context manager
    async with AsyncNetworkMonitor(hosts[:2]) as monitor:
        print("Monitoring started...")
        await asyncio.sleep(120)  # Monitor for 2 minutes
        print("Monitoring stopped.")

# Run async main
if __name__ == "__main__":
    asyncio.run(main())
```

### Kesimpulan

Fitur Python 3.7+ yang digunakan dalam NetDiag:

1. **Dataclasses** - Struktur data yang clean dan type-safe
2. **Type Hints** - Better code documentation dan IDE support
3. **Protocol Types** - Structural typing untuk flexibility
4. **F-strings** - Advanced string formatting dan debugging
5. **Walrus Operator** - Concise assignment expressions
6. **Positional-Only Parameters** - Better API design
7. **Match-Case** - Powerful pattern matching
8. **Async/Await** - Modern asynchronous programming

Implementasi fitur-fitur ini meningkatkan code quality, maintainability, dan performance aplikasi NetDiag.