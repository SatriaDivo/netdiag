# 🔧 Netdiag - Network Diagnostics Toolkit v1.1.0

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Educational](https://img.shields.io/badge/purpose-educational-orange.svg)](https://github.com/SatriaDivo/netdiag)
[![Version](https://img.shields.io/badge/version-1.1.0-green.svg)](https://github.com/SatriaDivo/netdiag)

**Netdiag** adalah library Python untuk diagnosa jaringan yang dirancang khusus untuk keperluan edukasi mahasiswa jurusan Teknologi Rekayasa Internet. Library ini menggunakan modul bawaan Python sebanyak mungkin untuk memberikan pemahaman mendalam tentang networking fundamentals.

## 📋 Daftar Isi

- [Fitur Utama](#-fitur-utama)
- [Fitur Baru v1.1.0](#-fitur-baru-v110)
- [Instalasi](#-instalasi)
- [Penggunaan Dasar](#-penggunaan-dasar)
- [Fungsi yang Tersedia](#-fungsi-yang-tersedia)
- [Command Line Interface](#-command-line-interface)
- [Contoh Penggunaan](#-contoh-penggunaan)
- [Struktur Proyek](#-struktur-proyek)
- [Pengembangan](#-pengembangan)
- [Changelog](#-changelog)
- [Lisensi](#-lisensi)

## 🚀 Fitur Utama

### 🏓 Ping
- Ping ke host dengan deteksi OS otomatis (Windows/Linux/Mac)
- Parsing output untuk statistik packet loss dan response time
- Support untuk custom count dan timeout
- **NEW v1.1.0**: Advanced latency analysis dengan jitter calculation

### 🔍 Traceroute
- Traceroute dengan dukungan multi-platform
- Parsing hop-by-hop analysis
- Deteksi jika destination tercapai

### 🌐 IP Utilities
- **Local IP**: Mendapatkan IP address lokal dari interface aktif
- **Public IP**: Mendapatkan IP publik menggunakan multiple API services
- **IP Info**: Informasi geografis dan ISP dari IP address

### 🔒 Port Scanning
- TCP port scanning dengan threading untuk performa optimal
- Scanning port range custom atau common ports
- Service detection untuk port yang terbuka
- **NEW v1.1.0**: Optimized common ports scanning

### 🔎 DNS Lookup
- Forward DNS lookup (hostname → IP)
- Reverse DNS lookup (IP → hostname)
- Bulk DNS lookup untuk multiple hostnames
- Full DNS info dengan IPv4/IPv6 support
- **NEW v1.1.0**: Enhanced DNS operations dan batch processing

## 🆕 Fitur Baru v1.1.0

### 🚀 Speed Testing & Performance Analysis
- **`bandwidth_test()`** - Measure download speed dengan test files
- **`ping_latency_test()`** - Advanced latency analysis dengan statistik lengkap
- **`connection_quality_test()`** - Comprehensive connection quality assessment

### 🌐 Network Interface Management
- **`get_network_interfaces()`** - Discover semua network interfaces system
- **`get_default_gateway()`** - Informasi default gateway
- **`analyze_network_config()`** - Complete network configuration analysis

### 📤 Export & Logging System
- **`export_results()`** - Export test results ke JSON, CSV, atau TXT
- **`create_logger()`** - Advanced logging dengan multiple levels
- **`batch_export()`** - Export multiple results dalam berbagai format

### 🔧 Enhanced CLI Commands
- **`speedtest`** - Speed testing dari command line
- **`interfaces`** - Network interface analysis
- **`analyze`** - Complete network analysis
- **`export`** - Result export functionality

## 💻 Instalasi

### Instalasi Lokal (Development)

```bash
# Clone atau download project
git clone https://github.com/yourusername/netdiag.git
cd netdiag

# Install dalam mode development
pip install -e .
```

### Instalasi dari PyPI (jika sudah dipublish)

```bash
pip install netdiag
```

### Requirements

- Python 3.6 atau lebih baru
- Tidak ada external dependencies (hanya menggunakan standard library)
- Akses internet untuk fungsi IP publik dan IP info

## 📖 Penggunaan Dasar

### Import Library

```python
# Core functions (v1.0.0)
from netdiag import ping, traceroute, get_local_ip, get_public_ip, scan_ports, dns_lookup

# Enhanced functions (v1.1.0)
from netdiag import (
    # Speed testing
    bandwidth_test, ping_latency_test, connection_quality_test,
    # Network interfaces  
    get_network_interfaces, get_default_gateway, analyze_network_config,
    # Export & logging
    export_results, create_logger, batch_export,
    # Enhanced DNS & ports
    reverse_dns_lookup, dns_bulk_lookup, scan_common_ports, get_ip_info
)
```

### Contoh Sederhana

```python
# Ping test
result = ping("google.com")
print(f"Ping success: {result['success']}")
print(f"Average time: {result['avg_time']} ms")

# DNS lookup
result = dns_lookup("github.com")
print(f"IP address: {result['ip']}")

# Get public IP
result = get_public_ip()
print(f"Your public IP: {result['ip']}")

# NEW v1.1.0: Speed test
speed_result = bandwidth_test('5MB')
print(f"Download speed: {speed_result['download_speed_mbps']} Mbps")

# NEW v1.1.0: Network interfaces
interfaces = get_network_interfaces()
for interface in interfaces['active_interfaces']:
    print(f"{interface['name']}: {interface['ip']}")
```

## 🛠️ Fungsi yang Tersedia

### 🏓 `ping(host, count=4, timeout=5)`

Melakukan ping ke host target.

**Parameters:**
- `host` (str): Hostname atau IP address
- `count` (int): Jumlah ping packets (default: 4)
- `timeout` (int): Timeout dalam detik (default: 5)

**Returns:**
```python
{
    'success': True,
    'host': 'google.com',
    'packets_sent': 4,
    'packets_received': 4,
    'packet_loss': 0.0,
    'avg_time': 25.3,
    'min_time': 23.1,
    'max_time': 28.7
}
```

**Contoh:**
```python
result = ping("google.com", count=3, timeout=10)
if result['success']:
    print(f"Ping berhasil! Packet loss: {result['packet_loss']}%")
```

### 🔍 `traceroute(host, max_hops=30, timeout=5)`

Melakukan traceroute ke host target.

**Parameters:**
- `host` (str): Hostname atau IP address
- `max_hops` (int): Maximum hops (default: 30)
- `timeout` (int): Timeout per hop (default: 5)

**Returns:**
```python
{
    'success': True,
    'host': 'google.com',
    'total_hops': 12,
    'destination_reached': True,
    'hops': [
        {
            'number': 1,
            'ip': '192.168.1.1',
            'hostname': 'router.local',
            'avg_time': 1.2,
            'status': 'success'
        },
        # ... more hops
    ]
}
```

### 🏠 `get_local_ip()`

Mendapatkan IP address lokal.

**Returns:**
```python
{
    'success': True,
    'ip': '192.168.1.100',
    'method': 'socket_connect'
}
```

### 🌐 `get_public_ip()`

Mendapatkan IP address publik.

**Returns:**
```python
{
    'success': True,
    'ip': '203.194.112.34',
    'service': 'ipify'
}
```

### 🔒 `scan_ports(host, start_port=1, end_port=1024, timeout=1)`

Melakukan TCP port scanning.

**Parameters:**
- `host` (str): Target hostname atau IP
- `start_port` (int): Port awal (default: 1)
- `end_port` (int): Port akhir (default: 1024)
- `timeout` (float): Connection timeout (default: 1)

**Returns:**
```python
{
    'success': True,
    'host': 'google.com',
    'target_ip': '142.250.190.78',
    'open_ports': [80, 443],
    'closed_ports': [21, 22, 23, ...],
    'total_ports_scanned': 1024,
    'scan_time': 15.3
}
```

### 🔎 `dns_lookup(hostname)`

Melakukan DNS lookup.

**Parameters:**
- `hostname` (str): Hostname yang akan di-resolve

**Returns:**
```python
{
    'success': True,
    'hostname': 'google.com',
    'ip': '142.250.190.78',
    'ips': ['142.250.190.78', '142.250.190.77'],
    'lookup_time': 0.045
}
```

## 🆕 Fungsi Baru v1.1.0

### 🚀 `bandwidth_test(test_size='5MB', timeout=30)`

Melakukan bandwidth test dengan download file test.

**Parameters:**
- `test_size` (str): Ukuran test file ('1MB', '5MB', '10MB')
- `timeout` (int): Timeout dalam detik (default: 30)

**Returns:**
```python
{
    'success': True,
    'test_size': '5MB',
    'download_speed_mbps': 25.34,
    'download_time': 1.58,
    'bytes_downloaded': 5242880,
    'test_url': 'https://speed.hetzner.de/5MB.bin'
}
```

### 📊 `ping_latency_test(host, count=10)`

Advanced latency analysis dengan statistik lengkap.

**Parameters:**
- `host` (str): Hostname atau IP address
- `count` (int): Jumlah ping (default: 10)

**Returns:**
```python
{
    'success': True,
    'host': 'google.com',
    'total_pings': 10,
    'successful_pings': 10,
    'avg_latency': 28.5,
    'min_latency': 22.1,
    'max_latency': 35.7,
    'jitter': 4.2,
    'packet_loss_percent': 0.0
}
```

### 🌐 `get_network_interfaces()`

Mendapatkan informasi semua network interfaces.

**Returns:**
```python
{
    'success': True,
    'system': 'windows',
    'total_interfaces': 5,
    'active_interfaces': [
        {
            'name': 'Wi-Fi',
            'ip': '192.168.1.100',
            'mac': '00:11:22:33:44:55',
            'status': 'up',
            'type': 'wireless'
        }
    ]
}
```

### 📤 `export_results(results, filename, format='json')`

Export test results ke file.

**Parameters:**
- `results` (dict): Hasil dari fungsi netdiag
- `filename` (str): Nama file output
- `format` (str): Format export ('json', 'csv', 'txt')

**Returns:**
```python
{
    'success': True,
    'filename': 'ping_test_20251002.json',
    'format': 'json',
    'file_size': 1024,
    'records_exported': 1
}
```

### 🔍 `connection_quality_test(host)`

Comprehensive connection quality assessment.

**Returns:**
```python
{
    'success': True,
    'quality_score': 85,
    'quality_rating': 'Very Good',
    'bandwidth_test': {...},
    'latency_test': {...},
    'recommendations': [
        'Connection quality looks good!',
        'Suitable for HD streaming and gaming'
    ]
}
```
```

## 🖥️ Command Line Interface

Netdiag menyediakan interface command line yang lengkap:

### Network Diagnostics
```bash
# Ping testing
python -m netdiag ping google.com
python -m netdiag ping google.com 5 10  # 5 packets, 10s timeout

# Traceroute
python -m netdiag traceroute google.com
python -m netdiag traceroute google.com 20 3  # max 20 hops, 3s timeout

# Port scanning
python -m netdiag scan google.com 80 443 22
python -m netdiag scan-range google.com 80 90  # scan range 80-90
```

### 🚀 Performance Testing (NEW v1.1.0)
```bash
# Speed test - bandwidth testing
python -m netdiag speedtest
python -m netdiag speedtest --host httpbin.org --duration 10

# Latency analysis
python -m netdiag latency google.com
python -m netdiag latency google.com --count 20

# Connection quality assessment
python -m netdiag quality google.com
```

### 🔧 System Analysis (NEW v1.1.0)
```bash
# Network interfaces discovery
python -m netdiag interfaces

# Network configuration analysis
python -m netdiag analyze
```

### 📊 Export & Logging (NEW v1.1.0)
```bash
# Export results to various formats
python -m netdiag export results.json --format json
python -m netdiag export results.csv --format csv
```

### IP Utilities
```bash
python -m netdiag localip
python -m netdiag publicip
python -m netdiag ipinfo 8.8.8.8
```

### Port Scanning
```bash
python -m netdiag portscan google.com common
python -m netdiag portscan google.com 1 100
```

### DNS Lookup
```bash
python -m netdiag dns google.com
python -m netdiag dns reverse 8.8.8.8
python -m netdiag dns info github.com
python -m netdiag dns bulk google.com,github.com,stackoverflow.com
```

### 🆕 NEW v1.1.0 Commands

### Speed Testing
```bash
python -m netdiag speedtest 5MB
python -m netdiag speedtest latency google.com
python -m netdiag speedtest quality google.com
```

### Network Interfaces
```bash
python -m netdiag interfaces
python -m netdiag interfaces gateway
```

### Network Analysis
```bash
python -m netdiag analyze
```

### Export Results
```bash
python -m netdiag export json results
python -m netdiag export csv results
```

### Help
```bash
python -m netdiag help
```

## 💡 Contoh Penggunaan

### 🔬 Analisis Host Lengkap dengan Fitur Baru

```python
from netdiag import *

def comprehensive_host_analysis(hostname):
    print(f"🔬 Comprehensive Analysis of {hostname}...")
    
    # 1. DNS Resolution
    dns_result = dns_lookup(hostname)
    if dns_result['success']:
        ip = dns_result['ip']
        print(f"✅ Resolved to: {ip}")
    else:
        print(f"❌ DNS failed: {dns_result['error']}")
        return
    
    # 2. Connectivity Test
    ping_result = ping(ip, count=5)
    if ping_result['success']:
        print(f"✅ Host reachable (avg: {ping_result['avg_time']} ms)")
    else:
        print(f"❌ Host unreachable")
        return
    
    # 3. Connection Quality Assessment (NEW v1.1.0)
    quality_result = connection_quality_test(hostname)
    if quality_result['success']:
        print(f"🎯 Connection Quality: {quality_result['quality_rating']} (Score: {quality_result['quality_score']}/100)")
    
    # 4. Bandwidth Test (NEW v1.1.0)
    bandwidth_result = bandwidth_test(host=hostname, duration=5)
    if bandwidth_result['success']:
        print(f"🚀 Bandwidth: {bandwidth_result['download_speed']:.2f} MB/s down, {bandwidth_result['upload_speed']:.2f} MB/s up")
    
    # 5. Port Scan
    from netdiag.portscan import scan_common_ports
    port_result = scan_common_ports(hostname)
    if port_result['success'] and port_result['open_ports']:
        print(f"🔓 Open services: {port_result['open_ports']}")
    
    # 6. Export Results (NEW v1.1.0)
    results = {
        'hostname': hostname,
        'dns': dns_result,
        'ping': ping_result,
        'quality': quality_result,
        'bandwidth': bandwidth_result,
        'ports': port_result
    }
    
    export_result = export_results(results, f'{hostname}_analysis', 'json')
    if export_result['success']:
        print(f"📄 Results exported to: {export_result['filename']}")

# Jalankan analisis lengkap
comprehensive_host_analysis("github.com")
```

### 🌐 Network System Analysis (NEW v1.1.0)

```python
from netdiag import get_network_interfaces, get_default_gateway, analyze_network_config

def analyze_network_system():
    print("🔧 Analyzing Network System Configuration...")
    
    # 1. Network Interfaces
    interfaces = get_network_interfaces()
    if interfaces['success']:
        print(f"🔌 Found {len(interfaces['interfaces'])} network interfaces:")
        for iface in interfaces['interfaces']:
            print(f"  - {iface['name']}: {iface['ip']} ({iface['status']})")
    
    # 2. Default Gateway
    gateway = get_default_gateway()
    if gateway['success']:
        print(f"🌉 Default Gateway: {gateway['gateway']}")
    
    # 3. Network Configuration Analysis
    config = analyze_network_config()
    if config['success']:
        print(f"� Network Analysis:")
        print(f"  - Active Interfaces: {len(config['active_interfaces'])}")
        print(f"  - Default Route: {config['default_route']}")
        print(f"  - DNS Servers: {', '.join(config.get('dns_servers', []))}")

analyze_network_system()
```

### 📊 Performance Monitoring with Export

```python
from netdiag import ping_latency_test, bandwidth_test, export_results
from netdiag.export import NetdiagLogger
import time

def monitor_performance(host, duration_minutes=5):
    logger = NetdiagLogger('performance_monitor')
    results = []
    
    print(f"📈 Monitoring {host} for {duration_minutes} minutes...")
    
    end_time = time.time() + (duration_minutes * 60)
    
    while time.time() < end_time:
        # Latency test
        latency = ping_latency_test(host, count=3)
        
        # Bandwidth test (shorter duration for monitoring)
        bandwidth = bandwidth_test(host=host, duration=3)
        
        result = {
            'timestamp': time.time(),
            'host': host,
            'latency': latency,
            'bandwidth': bandwidth
        }
        
        results.append(result)
        logger.log_test_result('performance_monitor', result)
        
        if latency['success']:
            print(f"⏱️  Latency: {latency['avg_ms']:.1f}ms", end="")
        
        if bandwidth['success']:
            print(f" | 🚀 Speed: {bandwidth['download_speed']:.1f} MB/s")
        
        time.sleep(30)  # Test every 30 seconds
    
    # Export all results
    export_results(results, f'{host}_performance_monitor', 'csv')
    print(f"✅ Monitoring complete. Results saved.")

# Monitor performance
monitor_performance("google.com", duration_minutes=2)
```

### 🔍 Multi-Host Network Assessment

```python
from netdiag import dns_bulk_lookup, ping, connection_quality_test

def assess_multiple_hosts(hostnames):
    print("🎯 Assessing Multiple Hosts...")
    
    # Bulk DNS lookup
    dns_results = dns_bulk_lookup(hostnames)
    assessment_results = []
    
    for result in dns_results['results']:
        if result['success']:
            host_assessment = {
                'hostname': result['hostname'],
                'ip': result['ip']
            }
            
            # Quick ping test
            ping_result = ping(result['ip'], count=3, timeout=5)
            host_assessment['ping'] = ping_result
            
            # Quality assessment for reachable hosts
            if ping_result['success']:
                quality = connection_quality_test(result['hostname'])
                host_assessment['quality'] = quality
                
                status = "� EXCELLENT" if quality.get('quality_score', 0) > 80 else \
                        "🟡 GOOD" if quality.get('quality_score', 0) > 60 else \
                        "🔴 POOR"
                
                print(f"{status} {result['hostname']}: {quality.get('quality_rating', 'Unknown')}")
            else:
                print(f"🔴 DOWN {result['hostname']}: Unreachable")
            
            assessment_results.append(host_assessment)
    
    # Export comprehensive results
    export_results(assessment_results, 'multi_host_assessment', 'json')
    return assessment_results

# Assess multiple hosts
hosts = ["google.com", "github.com", "stackoverflow.com", "reddit.com"]
assess_multiple_hosts(hosts)
```

## 📁 Struktur Proyek v1.1.0

```
netdiag/
├── netdiag/
│   ├── __init__.py          # Main package exports (19 functions)
│   ├── __main__.py          # Enhanced CLI interface (11 commands)
│   ├── ping.py              # Ping functionality
│   ├── traceroute.py        # Traceroute functionality  
│   ├── iputils.py           # IP utilities (local/public IP, IP info)
│   ├── portscan.py          # Port scanning capabilities
│   ├── dnslookup.py         # DNS lookup operations
│   ├── speedtest.py         # 🆕 Bandwidth testing & latency analysis
│   ├── interfaces.py        # 🆕 Network interfaces & system discovery
│   └── export.py            # 🆕 Results export & advanced logging
├── setup.py                 # Package setup (v1.1.0)
├── README.md               # Enhanced documentation  
├── CHANGELOG.md            # 🆕 Version history & features
└── example.py              # Updated usage examples with new features
```

### 🆕 New Modules in v1.1.0

- **speedtest.py**: Bandwidth testing, latency analysis, connection quality assessment
- **interfaces.py**: Network interface discovery, gateway detection, configuration analysis  
- **export.py**: Multi-format export (JSON/CSV/TXT), advanced logging, batch operations

## 🧪 Testing dan Development

### Menjalankan Contoh dengan Fitur Baru

```bash
# Jalankan semua demo (including new v1.1.0 features)
python example.py

# Jalankan demo spesifik
python example.py ping
python example.py dns  
python example.py port
python example.py speedtest    # 🆕 NEW v1.1.0
python example.py interfaces   # 🆕 NEW v1.1.0
```

### Testing Fitur Baru v1.1.0

```bash
# Test bandwidth capabilities
python -c "from netdiag import bandwidth_test; print(bandwidth_test())"

# Test network interfaces
python -c "from netdiag import get_network_interfaces; print(get_network_interfaces())"

# Test connection quality  
python -c "from netdiag import connection_quality_test; print(connection_quality_test('google.com'))"

# Test export functionality
python -c "from netdiag import export_results; print(export_results({'test': 'data'}, 'test', 'json'))"
```

### Manual Testing dari Command Line

```bash
# Test original functionality
python -m netdiag ping google.com
python -m netdiag traceroute google.com  
python -m netdiag portscan google.com common

# Test new v1.1.0 CLI commands
python -m netdiag speedtest
python -m netdiag interfaces
python -m netdiag analyze
python -m netdiag export test_results.json --format json
```

## 🎓 Educational Notes

### Konsep yang Dipelajari dalam v1.1.0

1. **Advanced Networking**
   - Bandwidth measurement techniques
   - Network interface enumeration
   - Quality of Service (QoS) assessment
   - Performance monitoring methodologies

2. **Enhanced Python Programming**
   - Concurrent testing with threading
   - File I/O operations (JSON, CSV, TXT)
   - Cross-platform system calls
   - Advanced data structure manipulation
   - Logging and monitoring systems

3. **Professional Development Practices**
   - Version management and changelog maintenance
   - Backward compatibility preservation
   - Comprehensive documentation
   - Modular architecture design

### Best Practices Demonstrated

- ✅ Standard library preference for compatibility
- ✅ Robust error handling with detailed feedback
- ✅ Comprehensive documentation with examples
- ✅ Modular, reusable code architecture
- ✅ Cross-platform compatibility maintained
- ✅ **NEW**: Performance testing methodologies
- ✅ **NEW**: Data export and persistence patterns
- ✅ **NEW**: System configuration analysis

## 🔧 Advanced Usage Examples

### Custom Performance Monitoring

```python
from netdiag import ping_latency_test, bandwidth_test
from netdiag.export import NetdiagLogger
import time

# Setup monitoring
logger = NetdiagLogger('network_monitor')
hosts = ['google.com', 'github.com', 'stackoverflow.com']

for host in hosts:
    # Comprehensive testing
    latency = ping_latency_test(host, count=10)
    bandwidth = bandwidth_test(host=host, duration=5)
    
    # Log results
    logger.log_test_result('monitoring', {
        'host': host,
        'latency': latency,
        'bandwidth': bandwidth,
        'timestamp': time.time()
    })
```

### Network Interface Analysis

```python
from netdiag import get_network_interfaces, get_default_gateway, analyze_network_config

# Get detailed interface information
interfaces = get_network_interfaces()
gateway = get_default_gateway()
config = analyze_network_config()

# Analyze configuration
if all([interfaces['success'], gateway['success'], config['success']]):
    print("🔧 Network Configuration Summary:")
    print(f"   Active Interfaces: {len(config['active_interfaces'])}")
    print(f"   Default Gateway: {gateway['gateway']}")
    print(f"   Primary Interface: {config.get('primary_interface', 'Unknown')}")
```

## 🆕 What's New in v1.1.0

### Major Enhancements
- 🚀 **Bandwidth Testing**: Real-world speed testing capabilities
- 🔧 **System Analysis**: Network interface and configuration discovery  
- 📊 **Export Functions**: Multi-format result export with logging
- ⚡ **Performance Tools**: Latency analysis and connection quality assessment
- 🎯 **Enhanced CLI**: 4 new command-line tools for advanced diagnostics

### Compatibility
- ✅ **Backward Compatible**: All existing code continues to work
- ✅ **Python 3.6+**: Maintained compatibility with older Python versions
- ✅ **Cross-Platform**: Windows, macOS, and Linux support preserved
- ✅ **Dependencies**: Still uses only Python standard library

## ⚠️ Limitations dan Considerations

### Performance Considerations
- **Bandwidth Testing**: May consume network data during testing
- **Port Scanning**: Large ranges may take significant time
- **Concurrent Operations**: Threading used but limited by network latency

### Platform-Specific Notes
- **Windows**: Some network interface data requires elevated privileges
- **macOS/Linux**: Better support for detailed interface information
- **Network Dependencies**: Internet connection required for external tests

### Rate Limiting
- **External APIs**: IP geolocation services may have rate limits
- **Bandwidth Tests**: Avoid excessive testing to prevent ISP throttling
- **DNS Queries**: Bulk operations should be used responsibly

## 🤝 Contributing

Contributions welcome! For v1.1.0 and beyond:

1. Fork repository ini
2. Buat feature branch (`git checkout -b feature/AmazingFeature`)
3. Test fitur baru dengan `python example.py`
4. Update documentation jika diperlukan
5. Commit changes (`git commit -m 'Add some AmazingFeature'`)
6. Push ke branch (`git push origin feature/AmazingFeature`)
7. Buat Pull Request

### Development Areas for Future Versions
- IPv6 support enhancement
- Additional export formats (XML, YAML)
- Real-time monitoring dashboard
- Network security scanning features
- Integration with network monitoring tools

## 📜 License

Distributed under the MIT License. See `LICENSE` file for more information.

## 📞 Support & Resources

- 📚 **Documentation**: This README and inline code comments
- 🐛 **Bug Reports**: Please open GitHub issues
- 💡 **Feature Requests**: Suggestions welcome via GitHub discussions
- 📖 **Learning**: Check `example.py` for practical usage patterns
- 📋 **Changelog**: See `CHANGELOG.md` for version history

---

**netdiag v1.1.0** - From simple educational tool to professional networking toolkit! 🚀

Jika ada pertanyaan atau issues:

- 📧 Email: satriadivop354@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/netdiag/issues)
- 📖 Docs: [Documentation](https://github.com/yourusername/netdiag/blob/main/README.md)

## 🙏 Acknowledgments

- Terima kasih kepada komunitas Python untuk standard library yang powerful
- Inspirasi dari tools networking klasik seperti ping, traceroute, nmap
- Educational focus untuk mahasiswa Teknologi Rekayasa Internet

---

**Happy Networking! 🚀**

> *"Understanding networks through code"* - Netdiag Team
