# 🧪 Lab Praktikum: Analisis Jaringan Polinela.ac.id

**Mata Kuliah**: Teknologi Rekayasa Internet  
**Topik**: Network Diagnostics menggunakan Netdiag  
**Target**: polinela.ac.id (Politeknik Negeri Lampung)  
**Durasi**: 2 x 50 menit  

## 📋 Tujuan Pembelajaran

Setelah menyelesaikan lab ini, mahasiswa diharapkan dapat:
1. Melakukan analisis konektivitas jaringan menggunakan tools Python
2. Memahami konsep DNS resolution dan troubleshooting
3. Menganalisis jalur jaringan menggunakan traceroute
4. Melakukan service discovery dengan port scanning
5. Menginterpretasi hasil analisis untuk troubleshooting

## 🛠️ Persiapan Lab

### Prerequisites
```bash
# Install netdiag
pip install netdiag

# Verify installation
python -c "import netdiag; print(f'Netdiag v{netdiag.__version__} ready!')"
```

### Setup Environment
```python
# Lab setup
import netdiag
from datetime import datetime

# Student information
STUDENT_NAME = "Nama Mahasiswa"
STUDENT_ID = "NPM Mahasiswa"
LAB_SESSION = "Network Diagnostics Lab"
TARGET_DOMAIN = "polinela.ac.id"

print(f"🧪 {LAB_SESSION}")
print(f"👨‍🎓 Student: {STUDENT_NAME} ({STUDENT_ID})")
print(f"🎯 Target: {TARGET_DOMAIN}")
print(f"⏰ Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
```

## 📝 Latihan 1: Basic Connectivity Test

### Task 1.1: Simple Ping Test
```python
print("\n" + "="*50)
print("LATIHAN 1: BASIC CONNECTIVITY TEST")
print("="*50)

# TODO: Lakukan ping test ke polinela.ac.id
result = netdiag.ping("polinela.ac.id")

# Analisis hasil
print(f"📊 Ping Test Results:")
print(f"   Host: {result['host']}")
print(f"   Success: {'✅' if result['success'] else '❌'}")
print(f"   Target IP: {result.get('target_ip', 'N/A')}")

if result['success']:
    print(f"   Average Time: {result['avg_time']} ms")
    print(f"   Packet Loss: {result['packet_loss']}%")
    
    # PERTANYAAN 1: Interpretasi hasil
    if result['avg_time'] < 50:
        latency_status = "Excellent (< 50ms)"
    elif result['avg_time'] < 100:
        latency_status = "Good (50-100ms)"
    elif result['avg_time'] < 200:
        latency_status = "Fair (100-200ms)"
    else:
        latency_status = "Poor (> 200ms)"
    
    print(f"   Latency Assessment: {latency_status}")
else:
    print(f"   Error: {result.get('error', 'Unknown')}")

# ✏️ TUGAS: Jawab pertanyaan berikut
print(f"\n📝 PERTANYAAN LATIHAN 1:")
print(f"   1. Berapa rata-rata response time ke polinela.ac.id?")
print(f"   2. Apakah ada packet loss? Jika ya, berapa persen?")
print(f"   3. Bagaimana kualitas koneksi berdasarkan latency?")
print(f"   4. IP address mana yang digunakan oleh polinela.ac.id?")
```

### Task 1.2: Advanced Ping Analysis
```python
# TODO: Lakukan ping dengan parameter khusus
detailed_ping = netdiag.ping("polinela.ac.id", count=10, timeout=5)

print(f"\n📈 Detailed Ping Analysis (10 packets):")
if detailed_ping['success']:
    print(f"   Packets Sent: {detailed_ping['packets_sent']}")
    print(f"   Packets Received: {detailed_ping['packets_received']}")
    print(f"   Min Time: {detailed_ping['min_time']} ms")
    print(f"   Max Time: {detailed_ping['max_time']} ms")
    print(f"   Average Time: {detailed_ping['avg_time']} ms")
    
    # Hitung jitter
    jitter = detailed_ping['max_time'] - detailed_ping['min_time']
    print(f"   Jitter: {jitter} ms")
    
    # PERTANYAAN 2: Analisis stabilitas
    if jitter < 20:
        stability = "Very Stable"
    elif jitter < 50:
        stability = "Stable"
    elif jitter < 100:
        stability = "Moderate"
    else:
        stability = "Unstable"
    
    print(f"   Connection Stability: {stability}")

# ✏️ TUGAS: Bandingkan dengan ping ke google.com
google_ping = netdiag.ping("google.com", count=10)
print(f"\n🔄 Comparison with Google.com:")
print(f"   Polinela avg: {detailed_ping.get('avg_time', 0)} ms")
print(f"   Google avg: {google_ping.get('avg_time', 0)} ms")
```

## 📝 Latihan 2: DNS Resolution Analysis

### Task 2.1: Forward DNS Lookup
```python
print("\n" + "="*50)
print("LATIHAN 2: DNS RESOLUTION ANALYSIS")
print("="*50)

# TODO: Lakukan DNS lookup untuk polinela.ac.id
dns_result = netdiag.dns_lookup("polinela.ac.id")

print(f"🔍 DNS Lookup Results:")
print(f"   Domain: {TARGET_DOMAIN}")
print(f"   Success: {'✅' if dns_result['success'] else '❌'}")

if dns_result['success']:
    print(f"   Resolved IP: {dns_result['ip']}")
    print(f"   Resolution Time: {dns_result.get('resolution_time', 'N/A')} ms")
    
    # Simpan IP untuk task selanjutnya
    polinela_ip = dns_result['ip']
else:
    print(f"   Error: {dns_result.get('error', 'Unknown')}")
    polinela_ip = None

# ✏️ PERTANYAAN: 
print(f"\n📝 PERTANYAAN LATIHAN 2A:")
print(f"   1. Berapa lama waktu yang dibutuhkan untuk resolve DNS?")
print(f"   2. IP address apa yang dikembalikan?")
print(f"   3. Apakah IP tersebut termasuk public atau private?")
```

### Task 2.2: Reverse DNS Lookup
```python
# TODO: Lakukan reverse DNS lookup jika IP tersedia
if polinela_ip:
    reverse_result = netdiag.reverse_dns_lookup(polinela_ip)
    
    print(f"\n🔄 Reverse DNS Lookup:")
    print(f"   IP: {polinela_ip}")
    print(f"   Success: {'✅' if reverse_result['success'] else '❌'}")
    
    if reverse_result['success']:
        print(f"   Reverse Hostname: {reverse_result['hostname']}")
        print(f"   PTR Record: Available")
    else:
        print(f"   PTR Record: Not available")
        print(f"   Error: {reverse_result.get('error', 'Unknown')}")

# ✏️ PERTANYAAN:
print(f"\n📝 PERTANYAAN LATIHAN 2B:")
print(f"   1. Apakah reverse DNS lookup berhasil?")
print(f"   2. Hostname apa yang dikembalikan?")
print(f"   3. Mengapa penting memiliki PTR record?")
```

### Task 2.3: Bulk DNS Testing
```python
# TODO: Test multiple subdomains
polinela_subdomains = [
    "polinela.ac.id",
    "www.polinela.ac.id",
    "portal.polinela.ac.id",
    "library.polinela.ac.id"
]

print(f"\n📊 Bulk DNS Testing:")
bulk_results = netdiag.dns_bulk_lookup(polinela_subdomains)

for domain, result in bulk_results.items():
    status = "✅" if result['success'] else "❌"
    ip = result['ip'] if result['success'] else "Failed"
    print(f"   {status} {domain:<25} → {ip}")

# Hitung statistik
total_domains = len(polinela_subdomains)
successful_resolutions = sum(1 for r in bulk_results.values() if r['success'])
success_rate = (successful_resolutions / total_domains) * 100

print(f"\n📈 DNS Statistics:")
print(f"   Total domains tested: {total_domains}")
print(f"   Successful resolutions: {successful_resolutions}")
print(f"   Success rate: {success_rate:.1f}%")
```

## 📝 Latihan 3: Network Path Analysis

### Task 3.1: Traceroute to Polinela
```python
print("\n" + "="*50)
print("LATIHAN 3: NETWORK PATH ANALYSIS")
print("="*50)

# TODO: Lakukan traceroute ke polinela.ac.id
trace_result = netdiag.traceroute("polinela.ac.id")

print(f"🛣️ Traceroute Results:")
print(f"   Target: {TARGET_DOMAIN}")
print(f"   Success: {'✅' if trace_result['success'] else '❌'}")

if trace_result['success']:
    print(f"   Target IP: {trace_result['target_ip']}")
    print(f"   Total Hops: {len(trace_result['hops'])}")
    
    print(f"\n   Network Path:")
    total_latency = 0
    
    for hop in trace_result['hops']:
        hop_num = hop['hop_number']
        ip = hop['ip_address']
        hostname = hop.get('hostname', 'Unknown')
        time_ms = hop.get('avg_time', 0)
        
        if time_ms:
            total_latency += time_ms
            print(f"   {hop_num:2d}. {ip:<15} ({hostname:<30}) - {time_ms:.1f} ms")
        else:
            print(f"   {hop_num:2d}. {ip:<15} ({hostname:<30}) - Timeout")
    
    print(f"\n📊 Path Analysis:")
    print(f"   Total Network Latency: {total_latency:.1f} ms")
    print(f"   Average per Hop: {total_latency/len(trace_result['hops']):.1f} ms")
    
else:
    print(f"   Error: {trace_result.get('error', 'Unknown')}")

# ✏️ PERTANYAAN:
print(f"\n📝 PERTANYAAN LATIHAN 3:")
print(f"   1. Berapa total hop yang dilalui paket?")
print(f"   2. Hop mana yang memiliki latency tertinggi?")
print(f"   3. Apakah ada hop yang timeout?")
print(f"   4. Dari mana paket keluar dari jaringan lokal?")
```

## 📝 Latihan 4: Service Discovery

### Task 4.1: Common Ports Scanning
```python
print("\n" + "="*50)
print("LATIHAN 4: SERVICE DISCOVERY")
print("="*50)

# TODO: Scan common ports polinela.ac.id
ports_result = netdiag.scan_common_ports("polinela.ac.id")

print(f"🔒 Port Scanning Results:")
print(f"   Target: {TARGET_DOMAIN}")
print(f"   Success: {'✅' if ports_result['success'] else '❌'}")

if ports_result['success']:
    print(f"   Total Ports Scanned: {ports_result['total_ports']}")
    print(f"   Open Ports: {len(ports_result['open_ports'])}")
    print(f"   Scan Duration: {ports_result['duration']:.2f} seconds")
    
    if ports_result['open_ports']:
        print(f"\n   🟢 Open Services:")
        for service in ports_result.get('open_services', []):
            port = service['port']
            service_name = service['service']
            print(f"      Port {port:<5} - {service_name}")
        
        # Analisis web services
        web_ports = [p for p in ports_result['open_ports'] if p in [80, 443, 8080, 8443]]
        if web_ports:
            print(f"\n   🌐 Web Services Detected:")
            for port in web_ports:
                if port == 80:
                    print(f"      HTTP service on port 80")
                elif port == 443:
                    print(f"      HTTPS service on port 443")
                elif port == 8080:
                    print(f"      Alternative HTTP on port 8080")
    else:
        print(f"   No open ports detected")
else:
    print(f"   Error: {ports_result.get('error', 'Unknown')}")

# ✏️ PERTANYAAN:
print(f"\n📝 PERTANYAAN LATIHAN 4:")
print(f"   1. Berapa port yang terbuka pada polinela.ac.id?")
print(f"   2. Service apa saja yang terdeteksi?")
print(f"   3. Apakah website mendukung HTTPS?")
print(f"   4. Port mana yang paling umum terbuka untuk web server?")
```

### Task 4.2: Specific Port Range Scan
```python
# TODO: Scan port range untuk web services
web_scan = netdiag.scan_ports("polinela.ac.id", start_port=80, end_port=443)

print(f"\n🔍 Web Services Port Scan (80-443):")
if web_scan['success']:
    print(f"   Port Range: 80-443")
    print(f"   Open Ports: {web_scan['open_ports']}")
    print(f"   Closed Ports: {len(web_scan['closed_ports'])}")
    
    # Security analysis
    if 80 in web_scan['open_ports'] and 443 in web_scan['open_ports']:
        security_note = "Both HTTP and HTTPS available"
    elif 443 in web_scan['open_ports']:
        security_note = "Only HTTPS available (Good security)"
    elif 80 in web_scan['open_ports']:
        security_note = "Only HTTP available (Security concern)"
    else:
        security_note = "No web services detected"
    
    print(f"   Security Assessment: {security_note}")
```

## 📝 Latihan 5: Performance Analysis

### Task 5.1: Connection Quality Test
```python
print("\n" + "="*50)
print("LATIHAN 5: PERFORMANCE ANALYSIS")
print("="*50)

# TODO: Test kualitas koneksi ke polinela.ac.id
quality_result = netdiag.connection_quality_test("polinela.ac.id")

print(f"⚡ Connection Quality Test:")
print(f"   Target: {TARGET_DOMAIN}")
print(f"   Success: {'✅' if quality_result['success'] else '❌'}")

if quality_result['success']:
    score = quality_result['quality_score']
    latency = quality_result['latency']
    jitter = quality_result['jitter']
    packet_loss = quality_result['packet_loss']
    
    print(f"   Overall Score: {score}/100")
    print(f"   Latency: {latency} ms")
    print(f"   Jitter: {jitter} ms")
    print(f"   Packet Loss: {packet_loss}%")
    
    # Interpretasi hasil
    if score >= 90:
        quality_desc = "Excellent - Ideal for all applications"
        emoji = "🟢"
    elif score >= 75:
        quality_desc = "Good - Suitable for most applications"
        emoji = "🟡"
    elif score >= 60:
        quality_desc = "Fair - May affect real-time applications"
        emoji = "🟠"
    else:
        quality_desc = "Poor - May cause significant issues"
        emoji = "🔴"
    
    print(f"   {emoji} Assessment: {quality_desc}")
    
else:
    print(f"   Error: {quality_result.get('error', 'Unknown')}")

# ✏️ PERTANYAAN:
print(f"\n📝 PERTANYAAN LATIHAN 5:")
print(f"   1. Berapa skor kualitas koneksi ke polinela.ac.id?")
print(f"   2. Aplikasi apa yang cocok dengan kualitas ini?")
print(f"   3. Faktor apa yang mempengaruhi kualitas koneksi?")
```

## 📝 Latihan 6: IP Geolocation & Network Info

### Task 6.1: IP Information Analysis
```python
print("\n" + "="*50)
print("LATIHAN 6: IP GEOLOCATION & NETWORK INFO")
print("="*50)

# TODO: Analisis informasi IP polinela.ac.id
if polinela_ip:
    ip_info = netdiag.get_ip_info(polinela_ip)
    
    print(f"🌐 IP Geolocation Analysis:")
    print(f"   IP Address: {polinela_ip}")
    print(f"   Success: {'✅' if ip_info['success'] else '❌'}")
    
    if ip_info['success']:
        print(f"   Location: {ip_info['city']}, {ip_info['region']}")
        print(f"   Country: {ip_info['country']} ({ip_info['country_code']})")
        print(f"   ISP: {ip_info.get('isp', 'Unknown')}")
        print(f"   Organization: {ip_info.get('org', 'Unknown')}")
        print(f"   Timezone: {ip_info.get('timezone', 'Unknown')}")
        
        # Analisis lokasi
        if 'lampung' in ip_info['region'].lower() or 'lampung' in ip_info['city'].lower():
            location_match = "✅ Location matches institution"
        else:
            location_match = "⚠️ Location may not match institution"
        
        print(f"   {location_match}")
    else:
        print(f"   Error: {ip_info.get('error', 'Unknown')}")

# TODO: Bandingkan dengan IP lokal dan publik
local_ip = netdiag.get_local_ip()
public_ip = netdiag.get_public_ip()

print(f"\n🏠 Your Network Information:")
print(f"   Local IP: {local_ip['ip']}")
print(f"   Public IP: {public_ip['ip']}")

# Analisis IP range
if local_ip['ip'].startswith('192.168.'):
    ip_type = "Private Class C (Home/Office network)"
elif local_ip['ip'].startswith('10.'):
    ip_type = "Private Class A (Large organization)"
elif local_ip['ip'].startswith('172.'):
    ip_type = "Private Class B (Medium organization)"
else:
    ip_type = "Public IP (Direct connection)"

print(f"   Network Type: {ip_type}")
```

## 📊 Report Generation & Analysis

### Final Lab Report
```python
print("\n" + "="*60)
print("LAB REPORT GENERATION")
print("="*60)

# TODO: Kumpulkan semua hasil test
lab_results = {
    'student_info': {
        'name': STUDENT_NAME,
        'id': STUDENT_ID,
        'session': LAB_SESSION,
        'date': datetime.now().isoformat()
    },
    'target_analysis': {
        'domain': TARGET_DOMAIN,
        'ip_address': polinela_ip,
        'location': ip_info.get('city', 'Unknown') if 'ip_info' in locals() and ip_info['success'] else 'Unknown'
    },
    'connectivity_tests': {
        'ping_success': result['success'],
        'avg_latency': result.get('avg_time', 0),
        'packet_loss': result.get('packet_loss', 0),
        'dns_resolution': dns_result['success'],
        'quality_score': quality_result.get('quality_score', 0) if 'quality_result' in locals() else 0
    },
    'service_discovery': {
        'total_ports_scanned': ports_result.get('total_ports', 0) if 'ports_result' in locals() else 0,
        'open_ports': len(ports_result.get('open_ports', [])) if 'ports_result' in locals() else 0,
        'web_services': any(p in [80, 443] for p in ports_result.get('open_ports', [])) if 'ports_result' in locals() else False
    },
    'network_path': {
        'traceroute_success': trace_result['success'] if 'trace_result' in locals() else False,
        'total_hops': len(trace_result.get('hops', [])) if 'trace_result' in locals() and trace_result['success'] else 0
    }
}

# Generate summary
print(f"📊 LAB SUMMARY REPORT")
print(f"Student: {lab_results['student_info']['name']} ({lab_results['student_info']['id']})")
print(f"Target: {lab_results['target_analysis']['domain']}")
print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"")
print(f"🔍 Test Results Overview:")
print(f"   ✓ Ping Test: {'PASS' if lab_results['connectivity_tests']['ping_success'] else 'FAIL'}")
print(f"   ✓ DNS Resolution: {'PASS' if lab_results['connectivity_tests']['dns_resolution'] else 'FAIL'}")
print(f"   ✓ Service Discovery: {lab_results['service_discovery']['open_ports']} services found")
print(f"   ✓ Network Path: {lab_results['network_path']['total_hops']} hops")
print(f"   ✓ Quality Score: {lab_results['connectivity_tests']['quality_score']}/100")

# Performance assessment
total_tests = 5  # ping, dns, ports, traceroute, quality
passed_tests = sum([
    lab_results['connectivity_tests']['ping_success'],
    lab_results['connectivity_tests']['dns_resolution'],
    lab_results['service_discovery']['open_ports'] > 0,
    lab_results['network_path']['total_hops'] > 0,
    lab_results['connectivity_tests']['quality_score'] > 0
])

lab_score = (passed_tests / total_tests) * 100
print(f"")
print(f"🎯 Lab Performance: {lab_score:.1f}% ({passed_tests}/{total_tests} tests passed)")

if lab_score >= 80:
    grade = "A - Excellent"
    emoji = "🏆"
elif lab_score >= 70:
    grade = "B - Good"
    emoji = "🥈"
elif lab_score >= 60:
    grade = "C - Satisfactory"
    emoji = "🥉"
else:
    grade = "D - Needs Improvement"
    emoji = "📚"

print(f"{emoji} Assessment: {grade}")
```

## 🎓 Learning Outcomes Assessment

### Knowledge Check Questions
```python
print(f"\n" + "="*60)
print("KNOWLEDGE CHECK - JAWAB PERTANYAAN BERIKUT")
print("="*60)

questions = [
    {
        'no': 1,
        'question': 'Apa perbedaan antara DNS lookup dan reverse DNS lookup?',
        'points': 10
    },
    {
        'no': 2, 
        'question': 'Mengapa traceroute penting dalam troubleshooting jaringan?',
        'points': 10
    },
    {
        'no': 3,
        'question': 'Apa yang ditunjukkan oleh packet loss dalam ping test?',
        'points': 10
    },
    {
        'no': 4,
        'question': 'Port 80 dan 443 digunakan untuk service apa?',
        'points': 10
    },
    {
        'no': 5,
        'question': 'Bagaimana cara menginterpretasi hasil quality score?',
        'points': 10
    },
    {
        'no': 6,
        'question': 'Apa fungsi dari geolocation IP address?',
        'points': 10
    },
    {
        'no': 7,
        'question': 'Mengapa penting memahami network path dalam troubleshooting?',
        'points': 15
    },
    {
        'no': 8,
        'question': 'Bagaimana cara optimasi performa jaringan berdasarkan hasil analisis?',
        'points': 15
    },
    {
        'no': 9,
        'question': 'Apa saja faktor yang mempengaruhi kualitas koneksi jaringan?',
        'points': 10
    }
]

total_points = sum(q['points'] for q in questions)

print(f"💯 TOTAL POINTS AVAILABLE: {total_points}")
print(f"")

for q in questions:
    print(f"❓ Question {q['no']} ({q['points']} points):")
    print(f"   {q['question']}")
    print(f"   Answer: _________________________________")
    print(f"")

print(f"📝 PRACTICAL TASKS TO COMPLETE:")
print(f"   □ Export all test results to JSON file")
print(f"   □ Create network diagram based on traceroute")
print(f"   □ Write recommendations for network optimization")
print(f"   □ Compare results with other educational institutions")
print(f"   □ Document troubleshooting methodology used")
```

## 💾 Export Lab Results

### Save Lab Data
```python
print(f"\n" + "="*60)
print("EXPORT LAB RESULTS")
print("="*60)

# TODO: Export hasil lab ke file
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
lab_filename = f"polinela_lab_{STUDENT_ID}_{timestamp}"

# Prepare data for export
export_data = {
    'lab_info': lab_results,
    'raw_results': {
        'ping': result if 'result' in locals() else {},
        'dns': dns_result if 'dns_result' in locals() else {},
        'ports': ports_result if 'ports_result' in locals() else {},
        'traceroute': trace_result if 'trace_result' in locals() else {},
        'quality': quality_result if 'quality_result' in locals() else {},
        'ip_info': ip_info if 'ip_info' in locals() else {}
    },
    'questions': questions,
    'export_timestamp': datetime.now().isoformat()
}

# Export to JSON
try:
    netdiag.export_results([export_data], filename=lab_filename, format="json")
    print(f"✅ Lab results exported successfully!")
    print(f"📁 Filename: {lab_filename}.json")
    print(f"📊 Data includes: All test results, lab summary, and questions")
except Exception as e:
    print(f"❌ Export failed: {e}")

print(f"\n🎓 LAB COMPLETED!")
print(f"📧 Submit results to: instructor@polinela.ac.id")
print(f"📚 Review: docs/examples/ for additional tutorials")
print(f"⏰ End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
```

---

## 📚 Additional Resources

### Further Reading
- 📖 [Netdiag Documentation](../README.md)
- 🔍 [Advanced Examples](basic_usage.md)
- 🧪 [More Lab Exercises](../educational/lab_exercises.md)
- 💻 [Python Networking Guide](../tutorials/)

### Contact & Support
- 📧 **Instructor**: instructor@polinela.ac.id
- 💬 **Lab Assistant**: assistant@polinela.ac.id  
- 🐛 **Technical Issues**: [GitHub Issues](https://github.com/SatriaDivo/netdiag/issues)
- 📞 **Developer**: [satriadivop354@gmail.com](mailto:satriadivop354@gmail.com)

**Selamat mengeksplorasi dunia networking! 🚀🎓**