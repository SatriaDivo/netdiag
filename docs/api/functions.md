# 📋 Function Documentation

Comprehensive documentation for all **52 functions** in the Netdiag toolkit, organized by category and complexity.

## 📚 Table of Contents

- [Connectivity Functions](#-connectivity-functions)
- [DNS Functions](#-dns-functions)
- [Port Scanning Functions](#-port-scanning-functions)
- [Routing Functions](#-routing-functions)
- [Performance Functions](#-performance-functions)
- [Network Information Functions](#-network-information-functions)
- [Security Functions](#-security-functions)
- [Utility Functions](#-utility-functions)
- [Advanced Functions](#-advanced-functions)

---

## 🔌 Connectivity Functions

### `ping(target, count=4, timeout=3, packet_size=32)`
Performs ICMP ping test to check basic connectivity.

**Parameters:**
- `target` (str): Target IP address or domain name
- `count` (int, optional): Number of ping packets to send. Default: 4
- `timeout` (int, optional): Timeout in seconds. Default: 3
- `packet_size` (int, optional): Size of ping packet in bytes. Default: 32

**Returns:**
- `PingResult`: Object containing ping statistics

**Example:**
```python
import netdiag

# Basic ping
result = netdiag.ping("polinela.ac.id")
print(f"Average time: {result.avg_time}ms")
print(f"Packet loss: {result.packet_loss}%")

# Advanced ping with custom parameters
result = netdiag.ping("8.8.8.8", count=10, timeout=5)
```

**Raises:**
- `NetworkError`: When network is unreachable
- `DNSError`: When hostname cannot be resolved
- `TimeoutError`: When ping timeout is exceeded

---

### `check_connectivity(target, timeout=5)`
Quick connectivity check with boolean result.

**Parameters:**
- `target` (str): Target to check
- `timeout` (int, optional): Timeout in seconds. Default: 5

**Returns:**
- `bool`: True if target is reachable, False otherwise

**Example:**
```python
if netdiag.check_connectivity("polinela.ac.id"):
    print("✅ Connected")
else:
    print("❌ No connection")
```

---

### `is_host_alive(target, methods=['ping', 'tcp'])`
Comprehensive host availability check using multiple methods.

**Parameters:**
- `target` (str): Target host
- `methods` (list, optional): Methods to use. Default: ['ping', 'tcp']

**Returns:**
- `HostStatusResult`: Detailed host status information

**Example:**
```python
status = netdiag.is_host_alive("polinela.ac.id")
print(f"Host alive: {status.is_alive}")
print(f"Methods used: {status.methods_tested}")
```

---

### `ping_sweep(network_range, threads=10)`
Perform ping sweep across a network range.

**Parameters:**
- `network_range` (str): Network in CIDR notation (e.g., "192.168.1.0/24")
- `threads` (int, optional): Number of threads to use. Default: 10

**Returns:**
- `list[PingSweepResult]`: List of ping results for each host

**Example:**
```python
# Scan local network
results = netdiag.ping_sweep("192.168.1.0/24")
alive_hosts = [r.target for r in results if r.is_alive]
print(f"Found {len(alive_hosts)} alive hosts")
```

---

### `multi_ping(targets, concurrent=True)`
Ping multiple targets simultaneously.

**Parameters:**
- `targets` (list[str]): List of targets to ping
- `concurrent` (bool, optional): Use concurrent execution. Default: True

**Returns:**
- `dict[str, PingResult]`: Results keyed by target

**Example:**
```python
targets = ["google.com", "polinela.ac.id", "github.com"]
results = netdiag.multi_ping(targets)

for target, result in results.items():
    print(f"{target}: {result.avg_time}ms")
```

---

### `continuous_ping(target, duration=60, interval=1)`
Continuous ping monitoring for specified duration.

**Parameters:**
- `target` (str): Target to monitor
- `duration` (int, optional): Duration in seconds. Default: 60
- `interval` (int, optional): Interval between pings. Default: 1

**Returns:**
- `ContinuousPingResult`: Statistics over the monitoring period

**Example:**
```python
# Monitor for 5 minutes
result = netdiag.continuous_ping("polinela.ac.id", duration=300)
print(f"Average response time: {result.avg_response_time}ms")
print(f"Uptime: {result.uptime_percentage}%")
```

---

## 🌐 DNS Functions

### `dns_lookup(domain, record_type='A', dns_server=None)`
Perform DNS lookup for specified domain and record type.

**Parameters:**
- `domain` (str): Domain name to lookup
- `record_type` (str, optional): DNS record type. Default: 'A'
- `dns_server` (str, optional): Custom DNS server. Default: None (system default)

**Returns:**
- `DNSResult`: DNS lookup result with IP and metadata

**Example:**
```python
# Basic DNS lookup
result = netdiag.dns_lookup("polinela.ac.id")
print(f"IP Address: {result.ip_address}")

# Lookup MX records
mx_result = netdiag.dns_lookup("polinela.ac.id", record_type='MX')
print(f"Mail servers: {mx_result.records}")

# Use custom DNS server
result = netdiag.dns_lookup("polinela.ac.id", dns_server="8.8.8.8")
```

**Supported Record Types:**
- `A`: IPv4 address
- `AAAA`: IPv6 address
- `MX`: Mail exchange
- `CNAME`: Canonical name
- `TXT`: Text records
- `NS`: Name servers
- `SOA`: Start of authority

---

### `reverse_dns(ip_address, timeout=5)`
Perform reverse DNS lookup (PTR record).

**Parameters:**
- `ip_address` (str): IP address to lookup
- `timeout` (int, optional): Timeout in seconds. Default: 5

**Returns:**
- `ReverseDNSResult`: Reverse DNS result

**Example:**
```python
result = netdiag.reverse_dns("8.8.8.8")
print(f"Hostname: {result.hostname}")
```

---

### `dns_record_lookup(domain, record_types=['A', 'MX', 'NS'])`
Lookup multiple DNS record types for a domain.

**Parameters:**
- `domain` (str): Domain to lookup
- `record_types` (list, optional): List of record types. Default: ['A', 'MX', 'NS']

**Returns:**
- `dict[str, list]`: Records grouped by type

**Example:**
```python
records = netdiag.dns_record_lookup("polinela.ac.id")
print(f"A records: {records['A']}")
print(f"MX records: {records['MX']}")
print(f"NS records: {records['NS']}")
```

---

### `dns_performance_test(domain, dns_servers=None, iterations=10)`
Test DNS performance across multiple servers.

**Parameters:**
- `domain` (str): Domain to test
- `dns_servers` (list, optional): List of DNS servers. Default: None (common servers)
- `iterations` (int, optional): Number of test iterations. Default: 10

**Returns:**
- `DNSPerformanceResult`: Performance comparison results

**Example:**
```python
result = netdiag.dns_performance_test("polinela.ac.id")
fastest_server = result.fastest_server
print(f"Fastest DNS: {fastest_server.server} ({fastest_server.avg_time}ms)")
```

---

### `dns_server_test(dns_server, test_domains=None)`
Test DNS server functionality and performance.

**Parameters:**
- `dns_server` (str): DNS server to test
- `test_domains` (list, optional): Domains to test with. Default: None (standard test domains)

**Returns:**
- `DNSServerTestResult`: Server test results

**Example:**
```python
result = netdiag.dns_server_test("8.8.8.8")
print(f"Server status: {result.status}")
print(f"Response time: {result.avg_response_time}ms")
```

---

### `dns_cache_analysis()`
Analyze local DNS cache.

**Returns:**
- `DNSCacheResult`: DNS cache analysis

**Example:**
```python
cache = netdiag.dns_cache_analysis()
print(f"Cache entries: {len(cache.entries)}")
print(f"Hit ratio: {cache.hit_ratio}%")
```

---

## 🔍 Port Scanning Functions

### `check_port(target, port, timeout=3, protocol='tcp')`
Check if a specific port is open on target.

**Parameters:**
- `target` (str): Target IP or domain
- `port` (int): Port number to check
- `timeout` (int, optional): Connection timeout. Default: 3
- `protocol` (str, optional): Protocol to use ('tcp' or 'udp'). Default: 'tcp'

**Returns:**
- `PortResult`: Port status and metadata

**Example:**
```python
# Check HTTP port
result = netdiag.check_port("polinela.ac.id", 80)
print(f"Port 80: {'Open' if result.is_open else 'Closed'}")

# Check with UDP
result = netdiag.check_port("8.8.8.8", 53, protocol='udp')
```

---

### `port_scan(target, ports, threads=50, timeout=3)`
Scan multiple ports on target.

**Parameters:**
- `target` (str): Target to scan
- `ports` (list[int]): List of ports to scan
- `threads` (int, optional): Number of threads. Default: 50
- `timeout` (int, optional): Per-port timeout. Default: 3

**Returns:**
- `list[PortScanResult]`: List of port scan results

**Example:**
```python
# Scan common ports
common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995]
results = netdiag.port_scan("polinela.ac.id", common_ports)

# Show open ports
open_ports = [r for r in results if r.status == 'open']
for port_result in open_ports:
    print(f"Port {port_result.port}: {port_result.service}")
```

---

### `port_range_scan(target, start_port, end_port, threads=50)`
Scan a range of ports.

**Parameters:**
- `target` (str): Target to scan
- `start_port` (int): Starting port number
- `end_port` (int): Ending port number
- `threads` (int, optional): Number of threads. Default: 50

**Returns:**
- `PortRangeScanResult`: Scan results for the port range

**Example:**
```python
# Scan well-known ports (1-1024)
result = netdiag.port_range_scan("polinela.ac.id", 1, 1024)
print(f"Open ports: {result.open_ports}")
print(f"Scan duration: {result.duration}s")
```

---

### `service_detection(target, port, timeout=5)`
Detect service running on specific port.

**Parameters:**
- `target` (str): Target host
- `port` (int): Port to analyze
- `timeout` (int, optional): Detection timeout. Default: 5

**Returns:**
- `ServiceDetectionResult`: Service information

**Example:**
```python
service = netdiag.service_detection("polinela.ac.id", 80)
print(f"Service: {service.name}")
print(f"Version: {service.version}")
print(f"Banner: {service.banner}")
```

---

### `banner_grabbing(target, port, timeout=5)`
Grab service banner from port.

**Parameters:**
- `target` (str): Target host
- `port` (int): Target port
- `timeout` (int, optional): Timeout for banner grab. Default: 5

**Returns:**
- `BannerResult`: Service banner information

**Example:**
```python
banner = netdiag.banner_grabbing("polinela.ac.id", 80)
print(f"Server: {banner.server}")
print(f"Banner: {banner.banner}")
```

---

### `os_fingerprinting(target, method='tcp')`
Attempt to determine target operating system.

**Parameters:**
- `target` (str): Target to fingerprint
- `method` (str, optional): Fingerprinting method. Default: 'tcp'

**Returns:**
- `OSFingerprintResult`: OS detection results

**Example:**
```python
os_info = netdiag.os_fingerprinting("polinela.ac.id")
print(f"Detected OS: {os_info.os_family}")
print(f"Confidence: {os_info.confidence}%")
```

---

## 🛣️ Routing Functions

### `traceroute(target, max_hops=30, timeout=5)`
Trace network route to target.

**Parameters:**
- `target` (str): Destination target
- `max_hops` (int, optional): Maximum number of hops. Default: 30
- `timeout` (int, optional): Per-hop timeout. Default: 5

**Returns:**
- `TracerouteResult`: Route tracing results

**Example:**
```python
route = netdiag.traceroute("polinela.ac.id")
print(f"Total hops: {route.total_hops}")

for i, hop in enumerate(route.hops, 1):
    print(f"Hop {i}: {hop.ip} ({hop.hostname}) - {hop.rtt}ms")
```

---

### `trace_path(target, protocol='icmp')`
Advanced path tracing with multiple protocols.

**Parameters:**
- `target` (str): Target to trace
- `protocol` (str, optional): Protocol to use. Default: 'icmp'

**Returns:**
- `PathTraceResult`: Detailed path information

**Example:**
```python
path = netdiag.trace_path("polinela.ac.id", protocol='udp')
print(f"Path discovered: {path.complete}")
print(f"AS numbers: {path.as_numbers}")
```

---

### `route_analysis(target)`
Comprehensive route analysis.

**Parameters:**
- `target` (str): Target for analysis

**Returns:**
- `RouteAnalysisResult`: Detailed route analysis

**Example:**
```python
analysis = netdiag.route_analysis("polinela.ac.id")
print(f"Route efficiency: {analysis.efficiency_score}")
print(f"Potential issues: {analysis.issues}")
```

---

### `mtr_analysis(target, count=10, interval=1)`
MTR-style continuous route monitoring.

**Parameters:**
- `target` (str): Target to monitor
- `count` (int, optional): Number of tests. Default: 10
- `interval` (int, optional): Interval between tests. Default: 1

**Returns:**
- `MTRResult`: MTR analysis results

**Example:**
```python
mtr = netdiag.mtr_analysis("polinela.ac.id", count=20)
for hop in mtr.hops:
    print(f"Hop {hop.number}: {hop.ip} - Loss: {hop.loss}% Avg: {hop.avg}ms")
```

---

### `network_path_discovery(target)`
Discover network paths and topology.

**Parameters:**
- `target` (str): Target for discovery

**Returns:**
- `PathDiscoveryResult`: Network path information

**Example:**
```python
discovery = netdiag.network_path_discovery("polinela.ac.id")
print(f"Paths found: {len(discovery.paths)}")
print(f"Load balancing detected: {discovery.load_balancing}")
```

---

### `hop_analysis(target, hop_number)`
Analyze specific hop in route.

**Parameters:**
- `target` (str): Target destination
- `hop_number` (int): Hop number to analyze

**Returns:**
- `HopAnalysisResult`: Detailed hop information

**Example:**
```python
hop_info = netdiag.hop_analysis("polinela.ac.id", 5)
print(f"Hop 5 details: {hop_info.details}")
print(f"Geographic location: {hop_info.location}")
```

---

## ⚡ Performance Functions

### `bandwidth_test(target, duration=10, packet_size=1024)`
Test network bandwidth to target.

**Parameters:**
- `target` (str): Target for bandwidth test
- `duration` (int, optional): Test duration in seconds. Default: 10
- `packet_size` (int, optional): Packet size in bytes. Default: 1024

**Returns:**
- `BandwidthResult`: Bandwidth test results

**Example:**
```python
bw = netdiag.bandwidth_test("polinela.ac.id")
print(f"Download speed: {bw.download_mbps} Mbps")
print(f"Upload speed: {bw.upload_mbps} Mbps")
print(f"Latency: {bw.latency} ms")
```

---

### `latency_test(target, samples=100, interval=0.1)`
Comprehensive latency testing.

**Parameters:**
- `target` (str): Target to test
- `samples` (int, optional): Number of samples. Default: 100
- `interval` (float, optional): Interval between samples. Default: 0.1

**Returns:**
- `LatencyResult`: Latency statistics

**Example:**
```python
latency = netdiag.latency_test("polinela.ac.id")
print(f"Average latency: {latency.avg} ms")
print(f"Jitter: {latency.jitter} ms")
print(f"95th percentile: {latency.p95} ms")
```

---

### `jitter_analysis(target, duration=60)`
Analyze network jitter over time.

**Parameters:**
- `target` (str): Target for jitter analysis
- `duration` (int, optional): Analysis duration. Default: 60

**Returns:**
- `JitterResult`: Jitter analysis results

**Example:**
```python
jitter = netdiag.jitter_analysis("polinela.ac.id")
print(f"Average jitter: {jitter.avg_jitter} ms")
print(f"Max jitter: {jitter.max_jitter} ms")
```

---

### `network_monitor(target, duration=300, metrics=['latency', 'loss'])`
Continuous network monitoring.

**Parameters:**
- `target` (str): Target to monitor
- `duration` (int, optional): Monitoring duration. Default: 300
- `metrics` (list, optional): Metrics to collect. Default: ['latency', 'loss']

**Returns:**
- `MonitoringResult`: Monitoring data

**Example:**
```python
monitor = netdiag.network_monitor("polinela.ac.id", duration=600)
print(f"Average uptime: {monitor.uptime_percentage}%")
print(f"SLA compliance: {monitor.sla_compliance}")
```

---

### `performance_baseline(target, duration=3600)`
Establish performance baseline.

**Parameters:**
- `target` (str): Target for baseline
- `duration` (int, optional): Baseline duration. Default: 3600

**Returns:**
- `BaselineResult`: Performance baseline data

**Example:**
```python
baseline = netdiag.performance_baseline("polinela.ac.id")
print(f"Baseline latency: {baseline.baseline_latency} ms")
print(f"Acceptable range: {baseline.acceptable_range}")
```

---

### `quality_assessment(target)`
Network quality assessment.

**Parameters:**
- `target` (str): Target for assessment

**Returns:**
- `QualityResult`: Network quality metrics

**Example:**
```python
quality = netdiag.quality_assessment("polinela.ac.id")
print(f"Overall score: {quality.score}/100")
print(f"Quality rating: {quality.rating}")
```

---

## ℹ️ Network Information Functions

### `get_network_interfaces()`
Get local network interface information.

**Returns:**
- `list[NetworkInterface]`: List of network interfaces

**Example:**
```python
interfaces = netdiag.get_network_interfaces()
for iface in interfaces:
    print(f"Interface: {iface.name}")
    print(f"IP: {iface.ip_address}")
    print(f"Status: {iface.status}")
```

---

### `get_default_gateway()`
Get default gateway information.

**Returns:**
- `GatewayInfo`: Default gateway details

**Example:**
```python
gateway = netdiag.get_default_gateway()
print(f"Gateway IP: {gateway.ip}")
print(f"Interface: {gateway.interface}")
```

---

### `get_local_ip(interface=None)`
Get local IP address.

**Parameters:**
- `interface` (str, optional): Specific interface. Default: None (primary interface)

**Returns:**
- `str`: Local IP address

**Example:**
```python
local_ip = netdiag.get_local_ip()
print(f"Local IP: {local_ip}")

# Get IP for specific interface
wifi_ip = netdiag.get_local_ip("wlan0")
```

---

### `get_network_config()`
Get comprehensive network configuration.

**Returns:**
- `NetworkConfig`: Network configuration details

**Example:**
```python
config = netdiag.get_network_config()
print(f"Hostname: {config.hostname}")
print(f"Domain: {config.domain}")
print(f"DNS servers: {config.dns_servers}")
```

---

### `get_routing_table()`
Get system routing table.

**Returns:**
- `list[RouteEntry]`: Routing table entries

**Example:**
```python
routes = netdiag.get_routing_table()
for route in routes:
    print(f"Destination: {route.destination}")
    print(f"Gateway: {route.gateway}")
    print(f"Interface: {route.interface}")
```

---

### `get_arp_table()`
Get ARP table entries.

**Returns:**
- `list[ARPEntry]`: ARP table entries

**Example:**
```python
arp_table = netdiag.get_arp_table()
for entry in arp_table:
    print(f"IP: {entry.ip} -> MAC: {entry.mac}")
```

---

## 🔒 Security Functions

### `vulnerability_scan(target, scan_type='basic')`
Scan for network vulnerabilities.

**Parameters:**
- `target` (str): Target to scan
- `scan_type` (str, optional): Type of scan. Default: 'basic'

**Returns:**
- `VulnerabilityScanResult`: Vulnerability scan results

**Example:**
```python
vuln_scan = netdiag.vulnerability_scan("polinela.ac.id")
print(f"Vulnerabilities found: {len(vuln_scan.vulnerabilities)}")
for vuln in vuln_scan.vulnerabilities:
    print(f"- {vuln.name} (Severity: {vuln.severity})")
```

---

### `ssl_certificate_check(target, port=443)`
Check SSL certificate details.

**Parameters:**
- `target` (str): Target to check
- `port` (int, optional): HTTPS port. Default: 443

**Returns:**
- `SSLCertificateResult`: Certificate information

**Example:**
```python
ssl_info = netdiag.ssl_certificate_check("polinela.ac.id")
print(f"Valid: {ssl_info.is_valid}")
print(f"Expires: {ssl_info.expiry_date}")
print(f"Issuer: {ssl_info.issuer}")
```

---

### `security_headers_check(target)`
Check security headers in HTTP response.

**Parameters:**
- `target` (str): Target website

**Returns:**
- `SecurityHeadersResult`: Security headers analysis

**Example:**
```python
headers = netdiag.security_headers_check("polinela.ac.id")
print(f"Security score: {headers.score}/100")
print(f"Missing headers: {headers.missing_headers}")
```

---

### `protocol_analysis(target, protocols=['http', 'https', 'ssh'])`
Analyze supported protocols.

**Parameters:**
- `target` (str): Target to analyze
- `protocols` (list, optional): Protocols to check. Default: ['http', 'https', 'ssh']

**Returns:**
- `ProtocolAnalysisResult`: Protocol support information

**Example:**
```python
protocols = netdiag.protocol_analysis("polinela.ac.id")
print(f"Supported protocols: {protocols.supported}")
print(f"Security issues: {protocols.security_issues}")
```

---

### `encryption_check(target, port=443)`
Check encryption capabilities.

**Parameters:**
- `target` (str): Target to check
- `port` (int, optional): Port to check. Default: 443

**Returns:**
- `EncryptionResult`: Encryption analysis

**Example:**
```python
encryption = netdiag.encryption_check("polinela.ac.id")
print(f"TLS version: {encryption.tls_version}")
print(f"Cipher suite: {encryption.cipher_suite}")
```

---

### `firewall_detection(target)`
Detect firewall presence and type.

**Parameters:**
- `target` (str): Target to analyze

**Returns:**
- `FirewallDetectionResult`: Firewall detection results

**Example:**
```python
firewall = netdiag.firewall_detection("polinela.ac.id")
print(f"Firewall detected: {firewall.detected}")
print(f"Type: {firewall.type}")
print(f"Filtered ports: {firewall.filtered_ports}")
```

---

## 🛠️ Utility Functions

### `ip_range_generator(network)`
Generate IP addresses in network range.

**Parameters:**
- `network` (str): Network in CIDR notation

**Returns:**
- `Generator[str]`: IP address generator

**Example:**
```python
for ip in netdiag.ip_range_generator("192.168.1.0/24"):
    print(ip)
    # Prints: 192.168.1.1, 192.168.1.2, ..., 192.168.1.254
```

---

### `subnet_calculator(network)`
Calculate subnet information.

**Parameters:**
- `network` (str): Network in CIDR notation

**Returns:**
- `SubnetInfo`: Subnet calculation results

**Example:**
```python
subnet = netdiag.subnet_calculator("192.168.1.0/24")
print(f"Network: {subnet.network}")
print(f"Broadcast: {subnet.broadcast}")
print(f"Hosts: {subnet.num_hosts}")
print(f"Netmask: {subnet.netmask}")
```

---

### `mac_address_lookup(mac)`
Lookup MAC address vendor information.

**Parameters:**
- `mac` (str): MAC address

**Returns:**
- `MACLookupResult`: MAC address information

**Example:**
```python
mac_info = netdiag.mac_address_lookup("00:1B:44:11:3A:B7")
print(f"Vendor: {mac_info.vendor}")
print(f"Organization: {mac_info.organization}")
```

---

### `validate_ip(ip_address)`
Validate IP address format.

**Parameters:**
- `ip_address` (str): IP address to validate

**Returns:**
- `IPValidationResult`: Validation result

**Example:**
```python
validation = netdiag.validate_ip("192.168.1.1")
print(f"Valid: {validation.is_valid}")
print(f"Version: {validation.version}")  # 4 or 6
print(f"Type: {validation.type}")  # public, private, loopback, etc.
```

---

### `validate_domain(domain)`
Validate domain name format.

**Parameters:**
- `domain` (str): Domain to validate

**Returns:**
- `DomainValidationResult`: Validation result

**Example:**
```python
validation = netdiag.validate_domain("polinela.ac.id")
print(f"Valid: {validation.is_valid}")
print(f"TLD: {validation.tld}")
print(f"Registrable: {validation.is_registrable}")
```

---

### `validate_port(port)`
Validate port number.

**Parameters:**
- `port` (int): Port number to validate

**Returns:**
- `PortValidationResult`: Validation result

**Example:**
```python
validation = netdiag.validate_port(80)
print(f"Valid: {validation.is_valid}")
print(f"Type: {validation.type}")  # well-known, registered, dynamic
print(f"Service: {validation.common_service}")
```

---

### `cidr_to_netmask(cidr)`
Convert CIDR notation to netmask.

**Parameters:**
- `cidr` (int): CIDR prefix length

**Returns:**
- `str`: Netmask in dotted decimal notation

**Example:**
```python
netmask = netdiag.cidr_to_netmask(24)
print(f"CIDR /24 = {netmask}")  # Output: 255.255.255.0
```

---

### `netmask_to_cidr(netmask)`
Convert netmask to CIDR notation.

**Parameters:**
- `netmask` (str): Netmask in dotted decimal notation

**Returns:**
- `int`: CIDR prefix length

**Example:**
```python
cidr = netdiag.netmask_to_cidr("255.255.255.0")
print(f"Netmask 255.255.255.0 = /{cidr}")  # Output: /24
```

---

### `ip_to_binary(ip_address)`
Convert IP address to binary representation.

**Parameters:**
- `ip_address` (str): IP address

**Returns:**
- `str`: Binary representation

**Example:**
```python
binary = netdiag.ip_to_binary("192.168.1.1")
print(f"Binary: {binary}")
# Output: 11000000.10101000.00000001.00000001
```

---

## 🚀 Advanced Functions

### `comprehensive_analysis(target, config=None)`
Perform comprehensive network analysis.

**Parameters:**
- `target` (str): Target for analysis
- `config` (NetworkConfiguration, optional): Analysis configuration

**Returns:**
- `ComprehensiveAnalysisResult`: Complete analysis results

**Example:**
```python
from netdiag.modern_features import NetworkConfiguration

config = NetworkConfiguration.create_default().with_timeout(10)
analysis = netdiag.comprehensive_analysis("polinela.ac.id", config)

print(f"Overall score: {analysis.score}/100")
print(f"Issues found: {len(analysis.issues)}")
print(f"Recommendations: {analysis.recommendations}")
```

---

### `network_discovery(network_range, methods=['ping', 'arp'])`
Discover devices on network.

**Parameters:**
- `network_range` (str): Network to scan
- `methods` (list, optional): Discovery methods. Default: ['ping', 'arp']

**Returns:**
- `NetworkDiscoveryResult`: Discovered devices

**Example:**
```python
discovery = netdiag.network_discovery("192.168.1.0/24")
print(f"Devices found: {len(discovery.devices)}")

for device in discovery.devices:
    print(f"IP: {device.ip}")
    print(f"MAC: {device.mac}")
    print(f"Vendor: {device.vendor}")
    print(f"Hostname: {device.hostname}")
```

---

## 🎓 Educational Examples

### Polinela Campus Network Analysis
```python
# Complete campus network analysis
campus_analysis = netdiag.comprehensive_analysis("polinela.ac.id")

# DNS infrastructure check
dns_servers = ["ns1.polinela.ac.id", "ns2.polinela.ac.id"]
for dns in dns_servers:
    result = netdiag.dns_server_test(dns)
    print(f"DNS {dns}: {result.status}")

# Web services check
web_services = [
    ("Main Website", "polinela.ac.id", 80),
    ("Secure Site", "polinela.ac.id", 443),
    ("E-learning", "elearning.polinela.ac.id", 443),
    ("Library", "library.polinela.ac.id", 443)
]

for name, host, port in web_services:
    status = netdiag.check_port(host, port)
    print(f"{name}: {'✅' if status.is_open else '❌'}")
```

---

**Total Functions: 52 | Categories: 8 | Educational Focus: 100%**

For more information about data models and exceptions, see:
- [Data Models Documentation](models.md)
- [Exception Handling Guide](exceptions.md)