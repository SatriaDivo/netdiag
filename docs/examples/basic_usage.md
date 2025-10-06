# 💻 Basic Usage Examples

This document provides comprehensive examples for getting started with Netdiag.

## 🚀 Quick Start

### Import Netdiag
```python
# Basic import
import netdiag

# Or import specific functions
from netdiag import ping, traceroute, scan_ports, dns_lookup
```

### First Network Test
```python
# Simple ping test
result = netdiag.ping("google.com")
print(f"Ping to google.com: {'Success' if result['success'] else 'Failed'}")

if result['success']:
    print(f"Average response time: {result['avg_time']} ms")
    print(f"Packet loss: {result['packet_loss']}%")
```

## 🏓 Ping Examples

### Basic Ping
```python
# Default ping (4 packets, 5 second timeout)
result = netdiag.ping("github.com")
print(result)

# Output:
# {
#     'success': True,
#     'host': 'github.com',
#     'target_ip': '140.82.114.4',
#     'packets_sent': 4,
#     'packets_received': 4,
#     'packet_loss': 0.0,
#     'min_time': 45.2,
#     'max_time': 52.1,
#     'avg_time': 48.7,
#     'timestamp': 1696599600.123
# }
```

### Custom Ping Parameters
```python
# Custom count and timeout
result = netdiag.ping("google.com", count=10, timeout=3)

# Quick ping (1 packet)
quick_result = netdiag.ping("facebook.com", count=1)

# Conservative ping (longer timeout)
slow_result = netdiag.ping("slow-server.com", timeout=10)
```

### Ping Analysis
```python
# Get ping statistics
stats = netdiag.get_ping_statistics("google.com", count=20)
print(f"Jitter: {stats.get('jitter', 'N/A')} ms")

# Calculate ping quality score
quality = netdiag.calculate_ping_quality_score("google.com")
print(f"Connection quality: {quality}/100")
```

## 🔍 IP and DNS Examples

### IP Information
```python
# Get local IP address
local_ip = netdiag.get_local_ip()
print(f"Your local IP: {local_ip['ip']}")

# Get public IP address
public_ip = netdiag.get_public_ip()
print(f"Your public IP: {public_ip['ip']}")

# Get detailed IP information
ip_info = netdiag.get_ip_info("8.8.8.8")
print(f"Google DNS location: {ip_info['city']}, {ip_info['country']}")
```

### DNS Lookups
```python
# Forward DNS lookup
dns_result = netdiag.dns_lookup("google.com")
print(f"Google.com resolves to: {dns_result['ip']}")

# Reverse DNS lookup
reverse_result = netdiag.reverse_dns_lookup("8.8.8.8")
print(f"8.8.8.8 reverse DNS: {reverse_result['hostname']}")

# Bulk DNS lookup
domains = ["google.com", "github.com", "stackoverflow.com"]
bulk_results = netdiag.dns_bulk_lookup(domains)
for domain, result in bulk_results.items():
    print(f"{domain}: {result['ip'] if result['success'] else 'Failed'}")
```

## 🔒 Port Scanning Examples

### Basic Port Scanning
```python
# Scan specific port
result = netdiag.scan_ports("google.com", start_port=80, end_port=80)
print(f"Port 80 status: {'Open' if 80 in result['open_ports'] else 'Closed'}")

# Scan port range
result = netdiag.scan_ports("localhost", start_port=20, end_port=25)
print(f"Open ports in range 20-25: {result['open_ports']}")
```

### Common Ports Scanning
```python
# Scan common ports (faster)
result = netdiag.scan_common_ports("github.com")
print(f"Open services on GitHub:")
for service in result.get('open_services', []):
    print(f"  Port {service['port']}: {service['service']}")
```

### Port Service Detection
```python
# Detailed port scan with service detection
result = netdiag.scan_ports("example.com", start_port=80, end_port=443)

print(f"Scan results for example.com:")
print(f"  Open ports: {result['open_ports']}")
print(f"  Closed ports: {result['closed_ports']}")
print(f"  Total scanned: {result['total_ports']}")
print(f"  Scan duration: {result['duration']:.2f} seconds")
```

## 🛣️ Traceroute Examples

### Basic Traceroute
```python
# Trace route to destination
result = netdiag.traceroute("google.com")

if result['success']:
    print(f"Route to {result['host']}:")
    for hop in result['hops']:
        print(f"  {hop['hop_number']}. {hop['ip_address']} ({hop['hostname']}) - {hop['avg_time']} ms")
else:
    print(f"Traceroute failed: {result['error']}")
```

### Traceroute Analysis
```python
# Analyze network path
result = netdiag.traceroute("github.com")

if result['success']:
    total_hops = len(result['hops'])
    total_time = sum(hop['avg_time'] or 0 for hop in result['hops'])
    
    print(f"Network path analysis:")
    print(f"  Total hops: {total_hops}")
    print(f"  Total latency: {total_time:.1f} ms")
    print(f"  Average per hop: {total_time/total_hops:.1f} ms")
```

## ⚡ Speed Testing Examples

### Bandwidth Testing
```python
# Test download speed
result = netdiag.bandwidth_test()
print(f"Download speed: {result['download_speed']} Mbps")
print(f"Upload speed: {result['upload_speed']} Mbps")

# Test with custom parameters
result = netdiag.bandwidth_test(test_duration=30, test_size="large")
```

### Latency Testing
```python
# Test latency to multiple servers
servers = ["google.com", "cloudflare.com", "github.com"]
for server in servers:
    result = netdiag.ping_latency_test(server)
    print(f"{server}: {result['avg_latency']} ms")
```

### Connection Quality Assessment
```python
# Comprehensive connection quality test
result = netdiag.connection_quality_test()

print(f"Connection Quality Report:")
print(f"  Overall score: {result['quality_score']}/100")
print(f"  Latency: {result['latency']} ms")
print(f"  Jitter: {result['jitter']} ms")
print(f"  Packet loss: {result['packet_loss']}%")
print(f"  Bandwidth: {result['bandwidth']} Mbps")
```

## 🌐 Network Interface Examples

### Interface Discovery
```python
# Get all network interfaces
interfaces = netdiag.get_network_interfaces()

print("Network Interfaces:")
for interface in interfaces['interfaces']:
    print(f"  {interface['name']}: {interface['ip']} ({interface['status']})")
```

### Gateway Information
```python
# Get default gateway
gateway = netdiag.get_default_gateway()
print(f"Default gateway: {gateway['gateway']} via {gateway['interface']}")

# Network configuration analysis
config = netdiag.analyze_network_config()
print(f"Network configuration summary:")
print(f"  Active interfaces: {len(config['active_interfaces'])}")
print(f"  Default gateway: {config['default_gateway']}")
print(f"  DNS servers: {config['dns_servers']}")
```

## 📊 Data Export Examples

### Export Results
```python
# Collect multiple test results
results = []
results.append(netdiag.ping("google.com"))
results.append(netdiag.dns_lookup("github.com"))
results.append(netdiag.scan_common_ports("localhost"))

# Export to JSON
netdiag.export_results(results, filename="network_report", format="json")

# Export to CSV
netdiag.export_results(results, filename="network_data", format="csv")
```

### Logging Setup
```python
# Create logger for network tests
logger = netdiag.create_logger("network_diagnostics", level="INFO")

# Run tests with logging
result = netdiag.ping("google.com")
logger.info(f"Ping test completed: {result['success']}")

# Batch export with logging
test_results = [
    netdiag.ping("google.com"),
    netdiag.ping("github.com"),
    netdiag.ping("stackoverflow.com")
]

netdiag.batch_export(test_results, prefix="daily_tests")
```

## 🐍 Modern Python 3.7+ Features

### Using NetworkConfiguration
```python
from netdiag import NetworkConfiguration

# Create network configuration
config = NetworkConfiguration(
    host="api.example.com",
    port=443,
    timeout=10,
    retries=3
)

print(f"Connection string: {config.connection_string}")
# Output: api.example.com:443?timeout=10&retries=3
```

### Enhanced Results with Method Chaining
```python
from netdiag import EnhancedNetworkResult

# Create result with method chaining
result = EnhancedNetworkResult(success=True) \
    .add_tag("production") \
    .add_tag("monitoring") \
    .with_metadata(
        test_type="connectivity",
        environment="staging",
        priority="high"
    )

print(f"Tags: {result.tags}")
print(f"Metadata: {result.metadata}")
```

### Custom Result Factory
```python
from netdiag import create_network_result_factory

# Create custom result type
MonitoringResult = create_network_result_factory(
    default_tags={"monitoring", "automated"}
)

# Use custom result
result = MonitoringResult(success=True)
result.add_tag("scheduled")
print(f"All tags: {result.tags}")
# Output: {'monitoring', 'automated', 'scheduled'}
```

## 🎓 Educational Examples

### Basic Network Connectivity Check
```python
def check_internet_connectivity():
    """Simple function to check internet connectivity."""
    test_sites = ["google.com", "cloudflare.com", "github.com"]
    
    print("Testing internet connectivity...")
    for site in test_sites:
        result = netdiag.ping(site, count=1)
        status = "✅ Connected" if result['success'] else "❌ Failed"
        print(f"  {site}: {status}")

check_internet_connectivity()
```

### Network Discovery Lab
```python
def network_discovery_lab():
    """Comprehensive network discovery exercise."""
    print("=== Network Discovery Lab ===\n")
    
    # Step 1: Local network info
    print("1. Local Network Information:")
    local_ip = netdiag.get_local_ip()
    print(f"   Local IP: {local_ip['ip']}")
    
    # Step 2: Public IP and location
    print("\n2. Public IP Information:")
    public_ip = netdiag.get_public_ip()
    ip_info = netdiag.get_ip_info(public_ip['ip'])
    print(f"   Public IP: {public_ip['ip']}")
    print(f"   Location: {ip_info['city']}, {ip_info['country']}")
    
    # Step 3: DNS resolution
    print("\n3. DNS Resolution Test:")
    dns_result = netdiag.dns_lookup("google.com")
    print(f"   google.com → {dns_result['ip']}")
    
    # Step 4: Connectivity test
    print("\n4. Connectivity Test:")
    ping_result = netdiag.ping("google.com", count=3)
    print(f"   Ping success: {ping_result['success']}")
    print(f"   Average time: {ping_result['avg_time']} ms")
    
    # Step 5: Service discovery
    print("\n5. Service Discovery:")
    ports_result = netdiag.scan_common_ports("google.com")
    print(f"   Open services: {len(ports_result['open_ports'])}")

network_discovery_lab()
```

### Performance Monitoring Example
```python
from netdiag.profiler import profile_performance, print_performance_report

@profile_performance
def network_performance_test():
    """Monitor network test performance."""
    # Run various tests
    netdiag.ping("google.com")
    netdiag.dns_lookup("github.com")
    netdiag.scan_common_ports("localhost")

# Run test with performance monitoring
network_performance_test()

# Print performance report
print_performance_report()
```

## 🔧 Error Handling Examples

### Comprehensive Error Handling
```python
from netdiag import (
    ping, NetworkError, ValidationError, 
    HostResolutionError, ConnectionTimeoutError
)

def safe_network_test(host):
    """Network test with comprehensive error handling."""
    try:
        result = ping(host)
        return result
        
    except ValidationError as e:
        print(f"Invalid input: {e}")
        return {'success': False, 'error': f'Validation failed: {e}'}
        
    except HostResolutionError as e:
        print(f"Cannot resolve host: {e}")
        return {'success': False, 'error': f'Host resolution failed: {e}'}
        
    except ConnectionTimeoutError as e:
        print(f"Connection timeout: {e}")
        return {'success': False, 'error': f'Connection timeout: {e}'}
        
    except NetworkError as e:
        print(f"Network error: {e}")
        return {'success': False, 'error': f'Network error: {e}'}
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {'success': False, 'error': f'Unexpected error: {e}'}

# Test with error handling
result = safe_network_test("invalid-host-name-123")
print(result)
```

## 📝 Quick Reference

### Most Common Functions
```python
# Essential functions for daily use
netdiag.ping("host")                    # Test connectivity
netdiag.get_local_ip()                 # Get local IP
netdiag.get_public_ip()                # Get public IP
netdiag.dns_lookup("domain")           # Resolve domain
netdiag.scan_common_ports("host")      # Check services
netdiag.traceroute("host")             # Trace network path
```

### Result Structure
```python
# All functions return dictionaries with consistent structure:
{
    'success': True/False,          # Operation status
    'timestamp': float,             # Unix timestamp
    'error': str or None,          # Error message if failed
    # ... function-specific data
}
```

---

**Ready to explore more? Check out [Advanced Examples](../advanced/) or [API Reference](../api/)!** 🚀