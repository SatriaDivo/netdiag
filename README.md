# 🔧 Netdiag - Network Diagnostics Toolkit

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Educational](https://img.shields.io/badge/purpose-educational-orange.svg)](https://github.com/yourusername/netdiag)

**Netdiag** adalah library Python untuk diagnosa jaringan yang dirancang khusus untuk keperluan edukasi mahasiswa jurusan Teknologi Rekayasa Internet. Library ini menggunakan modul bawaan Python sebanyak mungkin untuk memberikan pemahaman mendalam tentang networking fundamentals.

## 📋 Daftar Isi

- [Fitur Utama](#-fitur-utama)
- [Instalasi](#-instalasi)
- [Penggunaan Dasar](#-penggunaan-dasar)
- [Fungsi yang Tersedia](#-fungsi-yang-tersedia)
- [Command Line Interface](#-command-line-interface)
- [Contoh Penggunaan](#-contoh-penggunaan)
- [Struktur Proyek](#-struktur-proyek)
- [Pengembangan](#-pengembangan)
- [Lisensi](#-lisensi)

## 🚀 Fitur Utama

### 🏓 Ping
- Ping ke host dengan deteksi OS otomatis (Windows/Linux/Mac)
- Parsing output untuk statistik packet loss dan response time
- Support untuk custom count dan timeout

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

### 🔎 DNS Lookup
- Forward DNS lookup (hostname → IP)
- Reverse DNS lookup (IP → hostname)
- Bulk DNS lookup untuk multiple hostnames
- Full DNS info dengan IPv4/IPv6 support

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
from netdiag import ping, traceroute, get_local_ip, get_public_ip, scan_ports, dns_lookup
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

## 🖥️ Command Line Interface

Netdiag juga dapat digunakan melalui command line:

### Ping
```bash
python -m netdiag ping google.com
python -m netdiag ping google.com 5 10  # 5 packets, 10s timeout
```

### Traceroute
```bash
python -m netdiag traceroute google.com
python -m netdiag traceroute google.com 20 3  # max 20 hops, 3s timeout
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

### Help
```bash
python -m netdiag help
```

## 💡 Contoh Penggunaan

### Analisis Host Lengkap

```python
from netdiag import *

def analyze_host(hostname):
    print(f"🔬 Analyzing {hostname}...")
    
    # 1. DNS Resolution
    dns_result = dns_lookup(hostname)
    if dns_result['success']:
        ip = dns_result['ip']
        print(f"✅ Resolved to: {ip}")
    else:
        print(f"❌ DNS failed: {dns_result['error']}")
        return
    
    # 2. Ping Test
    ping_result = ping(ip, count=3)
    if ping_result['success']:
        print(f"✅ Host reachable (avg: {ping_result['avg_time']} ms)")
    else:
        print(f"❌ Host unreachable")
    
    # 3. Port Scan
    from netdiag.portscan import scan_common_ports
    port_result = scan_common_ports(hostname)
    if port_result['success'] and port_result['open_ports']:
        print(f"✅ Open services: {port_result['open_ports']}")
    else:
        print("🔒 No common services found")

# Jalankan analisis
analyze_host("github.com")
```

### Monitoring Multiple Hosts

```python
from netdiag.dnslookup import dns_bulk_lookup
from netdiag import ping

def monitor_hosts(hostnames):
    # Bulk DNS lookup
    dns_results = dns_bulk_lookup(hostnames)
    
    for result in dns_results['results']:
        if result['success']:
            # Ping each resolved host
            ping_result = ping(result['ip'], count=1, timeout=3)
            status = "🟢 UP" if ping_result['success'] else "🔴 DOWN"
            print(f"{status} {result['hostname']} ({result['ip']})")

# Monitor beberapa host
hosts = ["google.com", "github.com", "stackoverflow.com"]
monitor_hosts(hosts)
```

### Network Information Gathering

```python
from netdiag import get_local_ip, get_public_ip
from netdiag.iputils import get_ip_info

def network_info():
    # Local network info
    local = get_local_ip()
    if local['success']:
        print(f"🏠 Local IP: {local['ip']}")
    
    # Public network info
    public = get_public_ip()
    if public['success']:
        print(f"🌐 Public IP: {public['ip']}")
        
        # Get geolocation info
        info = get_ip_info(public['ip'])
        if info['success']:
            print(f"📍 Location: {info['city']}, {info['country']}")
            print(f"🏢 ISP: {info['isp']}")

network_info()
```

## 📁 Struktur Proyek

```
netdiag/
├── netdiag/
│   ├── __init__.py          # Main package exports
│   ├── __main__.py          # CLI interface
│   ├── ping.py              # Ping functionality
│   ├── traceroute.py        # Traceroute functionality
│   ├── iputils.py           # IP utilities (local/public IP, IP info)
│   ├── portscan.py          # Port scanning
│   └── dnslookup.py         # DNS lookup operations
├── setup.py                 # Package setup
├── README.md               # Documentation (this file)
└── example.py              # Usage examples
```

## 🧪 Testing dan Development

### Menjalankan Contoh

```bash
# Jalankan semua demo
python example.py

# Jalankan demo spesifik
python example.py ping
python example.py dns
python example.py port
```

### Testing Manual

```bash
# Test individual modules
python -m netdiag.ping google.com
python -m netdiag.traceroute google.com
python -m netdiag.portscan google.com common
```

## 🎓 Educational Notes

### Konsep yang Dipelajari

1. **Networking Fundamentals**
   - TCP/IP stack
   - DNS resolution
   - Port dan services
   - Routing dan path analysis

2. **Python Programming**
   - Subprocess handling
   - Socket programming
   - Threading untuk performance
   - Error handling dan exception management
   - Regular expressions untuk parsing

3. **System Administration**
   - Cross-platform compatibility
   - Command-line tools integration
   - Network diagnostics workflow

### Best Practices Demonstrated

- Menggunakan standard library sebanyak mungkin
- Error handling yang robust
- Documentation yang lengkap
- Code yang modular dan reusable
- Cross-platform compatibility

## 🔧 Advanced Usage

### Custom Port Scanning

```python
from netdiag.portscan import scan_ports, get_service_name

# Custom port range dengan threading
result = scan_ports("target.com", 1, 1000, timeout=0.5, max_threads=50)

# Print detailed results
for port in result['open_ports']:
    service = get_service_name(port)
    print(f"Port {port}: {service}")
```

### Comprehensive DNS Analysis

```python
from netdiag.dnslookup import get_dns_info, reverse_dns_lookup

# Full DNS information
dns_info = get_dns_info("example.com")

if dns_info['success']:
    print(f"IPv4 addresses: {dns_info['ipv4_addresses']}")
    print(f"IPv6 addresses: {dns_info['ipv6_addresses']}")
    
    # Reverse lookup for each IP
    for ip in dns_info['ipv4_addresses']:
        reverse = reverse_dns_lookup(ip)
        if reverse['success']:
            print(f"{ip} → {reverse['hostname']}")
```

## ⚠️ Limitations dan Considerations

1. **Performance**: Port scanning bisa lambat untuk range yang besar
2. **Network Dependencies**: Beberapa fungsi membutuhkan koneksi internet
3. **Permissions**: Beberapa fitur mungkin membutuhkan elevated privileges
4. **Platform Differences**: Output parsing bisa berbeda antar OS
5. **Rate Limiting**: API eksternal mungkin memiliki rate limiting

## 🤝 Contributing

Kontribusi sangat diharapkan! Silakan:

1. Fork repository ini
2. Buat feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📜 License

Distributed under the MIT License. See `LICENSE` file for more information.

## 📞 Support

Jika ada pertanyaan atau issues:

- 📧 Email: developer@netdiag.edu
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/netdiag/issues)
- 📖 Docs: [Documentation](https://github.com/yourusername/netdiag/blob/main/README.md)

## 🙏 Acknowledgments

- Terima kasih kepada komunitas Python untuk standard library yang powerful
- Inspirasi dari tools networking klasik seperti ping, traceroute, nmap
- Educational focus untuk mahasiswa Teknologi Rekayasa Internet

---

**Happy Networking! 🚀**

> *"Understanding networks through code"* - Netdiag Team