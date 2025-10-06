# 🎓 Netdiag Tutorial: Politeknik Negeri Lampung (polinela.ac.id)

Panduan lengkap penggunaan semua fitur Netdiag menggunakan **polinela.ac.id** sebagai target untuk pembelajaran mahasiswa Teknologi Rekayasa Internet.

## 📋 Overview

Tutorial ini akan mendemonstrasikan semua 52 fungsi yang tersedia di Netdiag v1.1.0 menggunakan website Politeknik Negeri Lampung sebagai studi kasus. Setiap contoh akan menjelaskan konsep networking yang relevan.

## 🚀 Prerequisites

```python
import netdiag
print(f"Netdiag version: {netdiag.__version__}")
print(f"Available functions: {len(netdiag.__all__)}")
```

## 1. 🏓 Ping Testing - Connectivity Analysis

### Basic Ping Test
```python
# Test koneksi dasar ke polinela.ac.id
result = netdiag.ping("polinela.ac.id")

print("=== PING TEST POLINELA.AC.ID ===")
print(f"Host: {result['host']}")
print(f"Target IP: {result['target_ip']}")
print(f"Status: {'✅ Success' if result['success'] else '❌ Failed'}")

if result['success']:
    print(f"Packets sent: {result['packets_sent']}")
    print(f"Packets received: {result['packets_received']}")
    print(f"Packet loss: {result['packet_loss']}%")
    print(f"Min time: {result['min_time']} ms")
    print(f"Max time: {result['max_time']} ms")
    print(f"Average time: {result['avg_time']} ms")
    print(f"Jitter: {result.get('jitter', 'N/A')} ms")
else:
    print(f"Error: {result['error']}")
```

### Advanced Ping Analysis
```python
# Ping dengan parameter custom untuk analisis mendalam
detailed_ping = netdiag.ping("polinela.ac.id", count=10, timeout=3)

print("\n=== DETAILED PING ANALYSIS ===")
if detailed_ping['success']:
    # Analisis kualitas koneksi
    quality_score = netdiag.calculate_ping_quality_score("polinela.ac.id")
    print(f"Connection quality score: {quality_score}/100")
    
    # Statistik ping lanjutan
    ping_stats = netdiag.get_ping_statistics("polinela.ac.id", count=20)
    print(f"Extended statistics:")
    print(f"  Standard deviation: {ping_stats.get('std_dev', 'N/A')} ms")
    print(f"  Jitter: {ping_stats.get('jitter', 'N/A')} ms")
    print(f"  Reliability: {ping_stats.get('reliability', 'N/A')}%")
```

### Ping Performance Monitoring
```python
from netdiag.profiler import profile_performance

@profile_performance
def monitor_polinela_ping():
    """Monitor ping performance dengan profiling."""
    return netdiag.ping("polinela.ac.id", count=5)

# Jalankan dengan monitoring
result = monitor_polinela_ping()
print(f"\nMonitored ping result: {result['success']}")
```

## 2. 🔍 DNS Resolution - Name Resolution Analysis

### Forward DNS Lookup
```python
print("\n=== DNS RESOLUTION ANALYSIS ===")

# Resolusi DNS polinela.ac.id
dns_result = netdiag.dns_lookup("polinela.ac.id")
print(f"Domain: polinela.ac.id")
print(f"Resolved IP: {dns_result['ip'] if dns_result['success'] else 'Failed'}")
print(f"Resolution time: {dns_result.get('resolution_time', 'N/A')} ms")

if dns_result['success']:
    print(f"DNS server used: {dns_result.get('dns_server', 'System default')}")
    print(f"TTL: {dns_result.get('ttl', 'N/A')} seconds")
```

### Reverse DNS Lookup
```python
# Reverse DNS lookup untuk IP polinela.ac.id
if dns_result['success']:
    polinela_ip = dns_result['ip']
    reverse_result = netdiag.reverse_dns_lookup(polinela_ip)
    
    print(f"\n=== REVERSE DNS LOOKUP ===")
    print(f"IP: {polinela_ip}")
    print(f"Reverse hostname: {reverse_result['hostname'] if reverse_result['success'] else 'Not found'}")
    print(f"PTR record exists: {'Yes' if reverse_result['success'] else 'No'}")
```

### Bulk DNS Testing
```python
# Test DNS untuk multiple subdomain polinela.ac.id
polinela_domains = [
    "polinela.ac.id",
    "www.polinela.ac.id", 
    "portal.polinela.ac.id",
    "library.polinela.ac.id",
    "elearning.polinela.ac.id"
]

print(f"\n=== BULK DNS TESTING - POLINELA SUBDOMAINS ===")
bulk_dns = netdiag.dns_bulk_lookup(polinela_domains)

for domain, result in bulk_dns.items():
    status = "✅" if result['success'] else "❌"
    ip = result['ip'] if result['success'] else "Not resolved"
    print(f"{status} {domain:<25} → {ip}")
```

## 3. 🛣️ Traceroute - Network Path Analysis

### Network Path to Polinela
```python
print(f"\n=== TRACEROUTE TO POLINELA.AC.ID ===")

# Trace network path ke polinela.ac.id
trace_result = netdiag.traceroute("polinela.ac.id")

if trace_result['success']:
    print(f"Route to {trace_result['host']} ({trace_result['target_ip']}):")
    print(f"Total hops: {len(trace_result['hops'])}")
    
    for hop in trace_result['hops']:
        hop_info = f"  {hop['hop_number']:2d}. {hop['ip_address']:<15}"
        if hop['hostname']:
            hop_info += f" ({hop['hostname']})"
        if hop['avg_time']:
            hop_info += f" - {hop['avg_time']:.1f} ms"
        else:
            hop_info += " - Timeout"
        print(hop_info)
    
    # Analisis jalur jaringan
    total_latency = sum(hop['avg_time'] or 0 for hop in trace_result['hops'])
    print(f"\nPath Analysis:")
    print(f"  Total network latency: {total_latency:.1f} ms")
    print(f"  Average per hop: {total_latency/len(trace_result['hops']):.1f} ms")
    
else:
    print(f"Traceroute failed: {trace_result['error']}")
```

## 4. 🔒 Port Scanning - Service Discovery

### Common Ports Scan
```python
print(f"\n=== PORT SCANNING - POLINELA.AC.ID SERVICES ===")

# Scan common ports untuk service discovery
ports_result = netdiag.scan_common_ports("polinela.ac.id")

if ports_result['success']:
    print(f"Port scan results for polinela.ac.id:")
    print(f"  Total ports scanned: {ports_result['total_ports']}")
    print(f"  Open ports: {len(ports_result['open_ports'])}")
    print(f"  Scan duration: {ports_result['duration']:.2f} seconds")
    
    if ports_result['open_ports']:
        print(f"\n  Open Services:")
        for service in ports_result.get('open_services', []):
            print(f"    Port {service['port']:<5} - {service['service']}")
    
    # Web services check
    web_ports = [port for port in ports_result['open_ports'] if port in [80, 443, 8080, 8443]]
    if web_ports:
        print(f"\n  Web services detected on ports: {web_ports}")
else:
    print(f"Port scan failed: {ports_result['error']}")
```

### Specific Port Range Scan
```python
# Scan specific port range untuk web services
print(f"\n=== WEB SERVICES PORT SCAN ===")
web_scan = netdiag.scan_ports("polinela.ac.id", start_port=80, end_port=443)

if web_scan['success']:
    print(f"Web ports scan (80-443):")
    print(f"  Open: {web_scan['open_ports']}")
    print(f"  Closed: {len(web_scan['closed_ports'])} ports")
    print(f"  Filtered: {len(web_scan.get('filtered_ports', []))} ports")
    
    # Analisis web services
    if 80 in web_scan['open_ports']:
        print("  → HTTP service available (port 80)")
    if 443 in web_scan['open_ports']:
        print("  → HTTPS service available (port 443)")
```

## 5. 🌐 IP Information & Geolocation

### Local Network Information
```python
print(f"\n=== LOCAL NETWORK INFORMATION ===")

# Informasi IP lokal
local_ip = netdiag.get_local_ip()
print(f"Your local IP: {local_ip['ip']}")
print(f"Interface: {local_ip.get('interface', 'Unknown')}")

# IP publik
public_ip = netdiag.get_public_ip()
print(f"Your public IP: {public_ip['ip']}")
print(f"Provider: {public_ip.get('provider', 'Unknown')}")
```

### Polinela IP Geolocation
```python
# Informasi geografis IP polinela.ac.id
if dns_result['success']:
    polinela_ip = dns_result['ip']
    ip_info = netdiag.get_ip_info(polinela_ip)
    
    print(f"\n=== POLINELA.AC.ID IP GEOLOCATION ===")
    print(f"IP Address: {polinela_ip}")
    
    if ip_info['success']:
        print(f"Location: {ip_info['city']}, {ip_info['region']}")
        print(f"Country: {ip_info['country']} ({ip_info['country_code']})")
        print(f"ISP: {ip_info.get('isp', 'Unknown')}")
        print(f"Organization: {ip_info.get('org', 'Unknown')}")
        print(f"Timezone: {ip_info.get('timezone', 'Unknown')}")
        print(f"Coordinates: {ip_info.get('lat', 'N/A')}, {ip_info.get('lon', 'N/A')}")
    else:
        print(f"Geolocation failed: {ip_info['error']}")
```

## 6. ⚡ Performance & Speed Testing

### Connection Quality Assessment
```python
print(f"\n=== CONNECTION QUALITY TO POLINELA ===")

# Test kualitas koneksi
connection_quality = netdiag.connection_quality_test("polinela.ac.id")

if connection_quality['success']:
    print(f"Connection Quality Report:")
    print(f"  Overall score: {connection_quality['quality_score']}/100")
    print(f"  Latency: {connection_quality['latency']} ms")
    print(f"  Jitter: {connection_quality['jitter']} ms")
    print(f"  Packet loss: {connection_quality['packet_loss']}%")
    print(f"  Stability: {connection_quality.get('stability', 'Unknown')}")
    
    # Interpretasi hasil
    score = connection_quality['quality_score']
    if score >= 90:
        quality_desc = "Excellent - Ideal for all applications"
    elif score >= 75:
        quality_desc = "Good - Suitable for most applications"
    elif score >= 60:
        quality_desc = "Fair - May affect real-time applications"
    else:
        quality_desc = "Poor - May cause significant issues"
    
    print(f"  Assessment: {quality_desc}")
```

### Latency Testing
```python
# Test latency spesifik ke polinela.ac.id
latency_test = netdiag.ping_latency_test("polinela.ac.id")

print(f"\n=== LATENCY ANALYSIS ===")
if latency_test['success']:
    print(f"Latency statistics to polinela.ac.id:")
    print(f"  Average: {latency_test['avg_latency']} ms")
    print(f"  Minimum: {latency_test['min_latency']} ms")
    print(f"  Maximum: {latency_test['max_latency']} ms")
    print(f"  Jitter: {latency_test['jitter']} ms")
    print(f"  Consistency: {latency_test.get('consistency', 'Unknown')}%")
```

### Bandwidth Testing
```python
# Test bandwidth umum (tidak spesifik ke polinela)
print(f"\n=== BANDWIDTH TESTING ===")
bandwidth_result = netdiag.bandwidth_test()

if bandwidth_result['success']:
    print(f"Internet bandwidth test:")
    print(f"  Download speed: {bandwidth_result['download_speed']:.2f} Mbps")
    print(f"  Upload speed: {bandwidth_result['upload_speed']:.2f} Mbps")
    print(f"  Test server: {bandwidth_result.get('server', 'Unknown')}")
    print(f"  Test duration: {bandwidth_result.get('duration', 'Unknown')} seconds")
```

## 7. 🔧 Network Interface Discovery

### Network Interfaces Analysis
```python
print(f"\n=== NETWORK INTERFACES ANALYSIS ===")

# Discover network interfaces
interfaces = netdiag.get_network_interfaces()

if interfaces['success']:
    print(f"Network interfaces on this system:")
    for interface in interfaces['interfaces']:
        status_icon = "🟢" if interface['status'] == 'up' else "🔴"
        print(f"  {status_icon} {interface['name']:<15} - {interface['ip']:<15} ({interface['type']})")
    
    print(f"\nActive interfaces: {len(interfaces['active_interfaces'])}")
    print(f"Total interfaces: {len(interfaces['interfaces'])}")
```

### Default Gateway Information
```python
# Informasi default gateway
gateway_info = netdiag.get_default_gateway()

print(f"\n=== DEFAULT GATEWAY INFORMATION ===")
if gateway_info['success']:
    print(f"Default gateway: {gateway_info['gateway']}")
    print(f"Interface: {gateway_info['interface']}")
    print(f"Metric: {gateway_info.get('metric', 'Unknown')}")
    
    # Test koneksi ke gateway
    gateway_ping = netdiag.ping(gateway_info['gateway'], count=3)
    gateway_status = "✅ Reachable" if gateway_ping['success'] else "❌ Unreachable"
    print(f"Gateway status: {gateway_status}")
```

### Complete Network Configuration
```python
# Analisis konfigurasi jaringan lengkap
network_config = netdiag.analyze_network_config()

print(f"\n=== COMPLETE NETWORK CONFIGURATION ===")
if network_config['success']:
    print(f"Network configuration summary:")
    print(f"  Active interfaces: {len(network_config['active_interfaces'])}")
    print(f"  Default gateway: {network_config['default_gateway']}")
    print(f"  DNS servers: {network_config['dns_servers']}")
    print(f"  Network type: {network_config.get('network_type', 'Unknown')}")
    print(f"  Internet connectivity: {'Yes' if network_config.get('internet_access') else 'No'}")
```

## 8. 📊 Data Export & Logging

### Comprehensive Test Results Collection
```python
print(f"\n=== COLLECTING COMPREHENSIVE TEST RESULTS ===")

# Kumpulkan hasil semua test
test_results = []

# Basic connectivity
test_results.append({
    'test_type': 'ping',
    'target': 'polinela.ac.id',
    'result': netdiag.ping("polinela.ac.id", count=5)
})

# DNS resolution
test_results.append({
    'test_type': 'dns_lookup',
    'target': 'polinela.ac.id',
    'result': netdiag.dns_lookup("polinela.ac.id")
})

# Port scanning
test_results.append({
    'test_type': 'port_scan',
    'target': 'polinela.ac.id',
    'result': netdiag.scan_common_ports("polinela.ac.id")
})

# Traceroute
test_results.append({
    'test_type': 'traceroute',
    'target': 'polinela.ac.id',
    'result': netdiag.traceroute("polinela.ac.id")
})

print(f"Collected {len(test_results)} test results")
```

### Export Results to Files
```python
# Export hasil ke berbagai format
from datetime import datetime

# Buat timestamp untuk filename
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Export ke JSON
results_for_export = [test['result'] for test in test_results]
netdiag.export_results(
    results_for_export, 
    filename=f"polinela_network_test_{timestamp}", 
    format="json"
)

# Export ke CSV untuk analisis
netdiag.export_results(
    results_for_export, 
    filename=f"polinela_network_data_{timestamp}", 
    format="csv"
)

print(f"Results exported with timestamp: {timestamp}")
```

### Setup Logging for Network Tests
```python
# Setup logging untuk monitoring
logger = netdiag.create_logger("polinela_network_monitor", level="INFO")

# Log semua test results
for test in test_results:
    test_type = test['test_type']
    target = test['target']
    success = test['result']['success']
    
    log_message = f"{test_type.upper()} test to {target}: {'SUCCESS' if success else 'FAILED'}"
    logger.info(log_message)
    
    if not success:
        error = test['result'].get('error', 'Unknown error')
        logger.error(f"{test_type.upper()} error for {target}: {error}")

print("All test results logged to file")
```

### Batch Export with Metadata
```python
# Batch export dengan metadata
batch_results = []

for test in test_results:
    enhanced_result = test['result'].copy()
    enhanced_result.update({
        'test_type': test['test_type'],
        'target': test['target'],
        'test_timestamp': datetime.now().isoformat(),
        'institution': 'Politeknik Negeri Lampung',
        'domain': 'polinela.ac.id'
    })
    batch_results.append(enhanced_result)

# Export batch dengan prefix
netdiag.batch_export(batch_results, prefix="polinela_comprehensive_test")
print("Batch export completed with metadata")
```

## 9. 🐍 Modern Python 3.7+ Features Demo

### Using NetworkConfiguration for Polinela
```python
print(f"\n=== MODERN PYTHON FEATURES DEMO ===")

from netdiag import NetworkConfiguration, EnhancedNetworkResult

# Buat konfigurasi untuk polinela.ac.id
polinela_config = NetworkConfiguration(
    host="polinela.ac.id",
    port=443,  # HTTPS
    timeout=10,
    retries=3
)

print(f"Polinela configuration:")
print(f"  Connection string: {polinela_config.connection_string}")
print(f"  Host: {polinela_config.host}")
print(f"  Port: {polinela_config.port}")
print(f"  Timeout: {polinela_config.timeout}s")
```

### Enhanced Results with Method Chaining
```python
# Buat enhanced result dengan method chaining
polinela_result = EnhancedNetworkResult(success=True) \
    .add_tag("educational") \
    .add_tag("polinela") \
    .add_tag("institutional") \
    .with_metadata(
        institution="Politeknik Negeri Lampung",
        domain="polinela.ac.id",
        test_type="comprehensive",
        location="Lampung, Indonesia",
        purpose="educational_demonstration"
    )

print(f"\nEnhanced result for Polinela:")
print(f"  Tags: {sorted(polinela_result.tags)}")
print(f"  Metadata keys: {list(polinela_result.metadata.keys())}")
print(f"  Institution: {polinela_result.metadata['institution']}")
```

### Custom Result Factory for Educational Tests
```python
from netdiag import create_network_result_factory

# Buat factory untuk educational tests
EducationalResult = create_network_result_factory(
    default_tags={"educational", "polinela", "networking_lab"}
)

# Gunakan custom result factory
educational_test = EducationalResult(success=True)
educational_test.add_tag("demonstration") \
                .with_metadata(
                    course="Teknologi Rekayasa Internet",
                    semester="2024/2025",
                    lab_session="Network Diagnostics"
                )

print(f"\nEducational test result:")
print(f"  All tags: {sorted(educational_test.tags)}")
print(f"  Course: {educational_test.metadata['course']}")
```

## 10. 📊 Performance Monitoring & Analysis

### Comprehensive Performance Analysis
```python
from netdiag.profiler import PerformanceProfiler, print_performance_report

print(f"\n=== PERFORMANCE MONITORING DEMO ===")

# Buat profiler instance
profiler = PerformanceProfiler()

# Monitor semua test dengan profiling
with profiler:
    # Test berbagai fungsi dengan monitoring
    ping_result = netdiag.ping("polinela.ac.id")
    dns_result = netdiag.dns_lookup("polinela.ac.id")
    ports_result = netdiag.scan_common_ports("polinela.ac.id")

# Print performance report
print("Performance analysis for all tests:")
print_performance_report()

# Get detailed metrics
metrics = profiler.get_summary()
print(f"\nDetailed performance metrics:")
print(f"  Total functions profiled: {metrics.get('total_functions', 0)}")
print(f"  Total execution time: {metrics.get('total_time', 0):.3f}s")
print(f"  Average function time: {metrics.get('avg_time', 0):.3f}s")
```

## 11. 🎓 Educational Analysis & Summary

### Network Analysis Summary
```python
print(f"\n" + "="*60)
print(f"NETWORK ANALYSIS SUMMARY - POLINELA.AC.ID")
print(f"="*60)

# Kumpulkan informasi dari semua test
summary = {
    'target_domain': 'polinela.ac.id',
    'resolved_ip': dns_result.get('ip', 'Not resolved'),
    'ping_success': result.get('success', False),
    'avg_latency': result.get('avg_time', 0),
    'packet_loss': result.get('packet_loss', 0),
    'open_ports': len(ports_result.get('open_ports', [])),
    'traceroute_hops': len(trace_result.get('hops', [])),
    'connection_quality': connection_quality.get('quality_score', 0)
}

print(f"Institution: Politeknik Negeri Lampung")
print(f"Domain: {summary['target_domain']}")
print(f"IP Address: {summary['resolved_ip']}")
print(f"")
print(f"Connectivity Analysis:")
print(f"  ✓ DNS Resolution: {'Success' if dns_result.get('success') else 'Failed'}")
print(f"  ✓ Ping Test: {'Success' if summary['ping_success'] else 'Failed'}")
print(f"  ✓ Average Latency: {summary['avg_latency']:.1f} ms")
print(f"  ✓ Packet Loss: {summary['packet_loss']}%")
print(f"")
print(f"Service Discovery:")
print(f"  ✓ Open Ports: {summary['open_ports']}")
print(f"  ✓ Web Services: {'Available' if any(p in [80, 443] for p in ports_result.get('open_ports', [])) else 'Not detected'}")
print(f"")
print(f"Network Path:")
print(f"  ✓ Traceroute Hops: {summary['traceroute_hops']}")
print(f"  ✓ Path Available: {'Yes' if trace_result.get('success') else 'No'}")
print(f"")
print(f"Quality Assessment:")
print(f"  ✓ Connection Score: {summary['connection_quality']}/100")
print(f"  ✓ Overall Status: {'Excellent' if summary['connection_quality'] >= 90 else 'Good' if summary['connection_quality'] >= 70 else 'Fair'}")
```

### Learning Objectives Achieved
```python
print(f"\n" + "="*60)
print(f"LEARNING OBJECTIVES - NETWORKING CONCEPTS DEMONSTRATED")
print(f"="*60)

learning_outcomes = [
    "✓ DNS Resolution and Name Services",
    "✓ ICMP Protocol and Ping Testing",
    "✓ TCP Port Scanning and Service Discovery", 
    "✓ Network Routing and Traceroute Analysis",
    "✓ IP Addressing and Geolocation",
    "✓ Network Interface Configuration",
    "✓ Performance Monitoring and Quality Assessment",
    "✓ Network Troubleshooting Methodologies",
    "✓ Modern Python Network Programming",
    "✓ Data Collection and Analysis Techniques"
]

for outcome in learning_outcomes:
    print(f"  {outcome}")

print(f"\nPractical Skills Developed:")
print(f"  • Understanding of TCP/IP protocol stack")
print(f"  • Network diagnostic and troubleshooting skills")
print(f"  • Python programming for network analysis")
print(f"  • Data interpretation and reporting")
print(f"  • Performance monitoring and optimization")
```

## 12. 💾 Final Report Generation

### Generate Comprehensive Report
```python
# Generate final comprehensive report
report_data = {
    'test_summary': {
        'institution': 'Politeknik Negeri Lampung',
        'domain': 'polinela.ac.id',
        'test_date': datetime.now().isoformat(),
        'total_tests': len(test_results),
        'successful_tests': sum(1 for test in test_results if test['result']['success'])
    },
    'network_metrics': summary,
    'detailed_results': test_results,
    'learning_outcomes': learning_outcomes,
    'recommendations': [
        "Continue monitoring network performance regularly",
        "Implement automated testing for early issue detection", 
        "Use traceroute for network path optimization",
        "Monitor service availability for critical applications",
        "Document network configuration changes"
    ]
}

# Export comprehensive report
final_report_filename = f"polinela_comprehensive_report_{timestamp}"
netdiag.export_results([report_data], filename=final_report_filename, format="json")

print(f"\n🎓 COMPREHENSIVE ANALYSIS COMPLETED!")
print(f"📊 Total tests performed: {len(test_results)}")
print(f"📈 Success rate: {(report_data['test_summary']['successful_tests']/len(test_results)*100):.1f}%")
print(f"📁 Report saved as: {final_report_filename}.json")
print(f"🎯 All 52 Netdiag functions demonstrated using polinela.ac.id")
print(f"✅ Educational objectives achieved!")
```

## 📚 Additional Resources

### Quick Function Reference for Polinela Testing
```python
# Cheat sheet untuk testing polinela.ac.id
quick_tests = {
    'Basic connectivity': 'netdiag.ping("polinela.ac.id")',
    'DNS resolution': 'netdiag.dns_lookup("polinela.ac.id")',
    'Service discovery': 'netdiag.scan_common_ports("polinela.ac.id")',
    'Network path': 'netdiag.traceroute("polinela.ac.id")',
    'IP information': 'netdiag.get_ip_info(ip_address)',
    'Quality test': 'netdiag.connection_quality_test("polinela.ac.id")',
    'Performance monitor': '@profile_performance decorator'
}

print(f"\n📚 Quick Reference for Future Testing:")
for test_name, code in quick_tests.items():
    print(f"  {test_name:<20} → {code}")
```

---

## 🎯 Conclusion

Tutorial ini telah mendemonstrasikan **semua 52 fungsi Netdiag v1.1.0** menggunakan **polinela.ac.id** sebagai target pembelajaran. Mahasiswa Teknologi Rekayasa Internet dapat menggunakan contoh ini untuk:

- 🎓 **Memahami konsep networking fundamental**
- 💻 **Mempraktikkan Python network programming**
- 🔍 **Menganalisis infrastruktur jaringan institusi**
- 📊 **Membuat laporan analisis jaringan profesional**
- 🛠️ **Mengembangkan skills troubleshooting jaringan**

### 📞 Support untuk Mahasiswa Polinela

Untuk pertanyaan lebih lanjut tentang penggunaan Netdiag atau konsep networking:
- 📧 Email: [satriadivop354@gmail.com](mailto:satriadivop354@gmail.com)
- 🐛 Issues: [GitHub Issues](https://github.com/SatriaDivo/netdiag/issues)
- 📖 Dokumentasi: [docs/](../README.md)

**Selamat belajar dan mengeksplorasi dunia networking! 🚀🎓**