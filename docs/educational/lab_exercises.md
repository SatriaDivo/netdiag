# 🧪 Laboratory Exercises

Hands-on laboratory exercises designed for **Teknologi Rekayasa Internet** students at Politeknik Negeri Lampung. These exercises provide practical experience with network diagnostics and analysis.

## 📚 Lab Exercise Overview

### Course Integration
- **Networking Fundamentals** - Labs 1-3
- **Network Security** - Labs 4-5  
- **Performance Analysis** - Labs 6-7
- **Advanced Topics** - Labs 8-10

### Prerequisites
- Basic understanding of IP networking
- Python programming basics
- Netdiag toolkit installed
- Access to campus network

---

## 🧪 Lab 1: Basic Network Connectivity

**Duration**: 2 hours  
**Difficulty**: Beginner  
**Learning Objectives**:
- Understand ICMP ping protocol
- Analyze network connectivity issues
- Interpret ping statistics

### Exercise 1.1: Campus Connectivity Test
```python
import netdiag
from datetime import datetime

def lab1_campus_connectivity():
    """Lab 1: Test connectivity to various campus services."""
    
    print("🏫 Lab 1: Politeknik Negeri Lampung Connectivity Test")
    print("Student: [Your Name Here]")
    print("Date:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 60)
    
    # Campus targets to test
    campus_targets = {
        "Main Website": "polinela.ac.id",
        "E-Learning": "elearning.polinela.ac.id", 
        "Library": "library.polinela.ac.id",
        "Student Portal": "portal.polinela.ac.id",
        "Local Gateway": "192.168.1.1",  # Typical campus gateway
        "Google DNS": "8.8.8.8",
        "Localhost": "127.0.0.1"
    }
    
    results = {}
    
    for name, target in campus_targets.items():
        print(f"\n📍 Testing {name} ({target}):")
        
        try:
            # Perform ping test
            ping_result = netdiag.ping(target, count=5, timeout=3)
            
            # Store results
            results[name] = {
                'target': target,
                'success': True,
                'avg_time': ping_result.avg_time,
                'packet_loss': ping_result.packet_loss,
                'min_time': ping_result.min_time,
                'max_time': ping_result.max_time
            }
            
            # Display results
            print(f"  ✅ Success!")
            print(f"  📊 Statistics:")
            print(f"     Average latency: {ping_result.avg_time:.2f} ms")
            print(f"     Packet loss: {ping_result.packet_loss:.1f}%")
            print(f"     Range: {ping_result.min_time:.2f} - {ping_result.max_time:.2f} ms")
            
            # Analysis
            if ping_result.avg_time < 10:
                print(f"     📈 Analysis: Excellent connectivity (local network)")
            elif ping_result.avg_time < 50:
                print(f"     📈 Analysis: Good connectivity (campus/local ISP)")
            elif ping_result.avg_time < 150:
                print(f"     📈 Analysis: Acceptable connectivity (internet)")
            else:
                print(f"     📈 Analysis: Slow connectivity (investigate)")
                
        except Exception as e:
            results[name] = {
                'target': target,
                'success': False,
                'error': str(e)
            }
            print(f"  ❌ Failed: {e}")
    
    # Generate summary report
    print(f"\n📋 Lab 1 Summary Report")
    print("=" * 40)
    
    successful_tests = [r for r in results.values() if r['success']]
    failed_tests = [r for r in results.values() if not r['success']]
    
    print(f"Total tests: {len(results)}")
    print(f"Successful: {len(successful_tests)}")
    print(f"Failed: {len(failed_tests)}")
    
    if successful_tests:
        avg_latency = sum(r['avg_time'] for r in successful_tests) / len(successful_tests)
        print(f"Average campus latency: {avg_latency:.2f} ms")
    
    return results

# Run Lab 1
lab1_results = lab1_campus_connectivity()
```

### Lab 1 Questions
1. **Analysis Questions**:
   - Which target had the lowest latency? Why?
   - What does packet loss indicate about network quality?
   - How does latency vary between local and external targets?

2. **Troubleshooting Scenarios**:
   - If `polinela.ac.id` fails but `8.8.8.8` succeeds, what might be the issue?
   - What could cause high latency to local targets?

---

## 🧪 Lab 2: DNS Resolution Analysis

**Duration**: 2 hours  
**Difficulty**: Beginner-Intermediate  
**Learning Objectives**:
- Understand DNS resolution process
- Compare DNS server performance
- Analyze different DNS record types

### Exercise 2.1: DNS Deep Dive
```python
def lab2_dns_analysis():
    """Lab 2: Comprehensive DNS analysis of campus infrastructure."""
    
    print("🌐 Lab 2: DNS Resolution Analysis")
    print("Student: [Your Name Here]")
    print("=" * 50)
    
    # Domains to analyze
    domains_to_test = [
        "polinela.ac.id",
        "google.com", 
        "github.com",
        "stackoverflow.com"
    ]
    
    # DNS servers to compare
    dns_servers = {
        "Campus DNS": None,  # Use system default
        "Google DNS": "8.8.8.8",
        "Cloudflare DNS": "1.1.1.1", 
        "OpenDNS": "208.67.222.222"
    }
    
    print("\n1. DNS Record Type Analysis:")
    print("-" * 40)
    
    for domain in domains_to_test[:2]:  # Test first 2 domains
        print(f"\n🔍 Analyzing {domain}:")
        
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT']
        for record_type in record_types:
            try:
                result = netdiag.dns_lookup(domain, record_type=record_type)
                print(f"  {record_type:4s}: {result.data}")
            except Exception as e:
                print(f"  {record_type:4s}: Not found or error")
    
    print("\n\n2. DNS Server Performance Comparison:")
    print("-" * 50)
    
    test_domain = "polinela.ac.id"
    performance_results = {}
    
    for dns_name, dns_server in dns_servers.items():
        try:
            # Perform multiple lookups for average
            times = []
            for _ in range(3):
                result = netdiag.dns_lookup(test_domain, dns_server=dns_server)
                times.append(result.query_time)
            
            avg_time = sum(times) / len(times)
            performance_results[dns_name] = avg_time
            
            print(f"  {dns_name:15s}: {avg_time:6.2f} ms (avg of 3 queries)")
            
        except Exception as e:
            print(f"  {dns_name:15s}: Failed - {e}")
    
    # Find fastest DNS
    if performance_results:
        fastest = min(performance_results.items(), key=lambda x: x[1])
        print(f"\n🏆 Fastest DNS: {fastest[0]} ({fastest[1]:.2f} ms)")
    
    print("\n\n3. Reverse DNS Lookup:")
    print("-" * 30)
    
    famous_ips = ["8.8.8.8", "1.1.1.1", "208.67.222.222"]
    for ip in famous_ips:
        try:
            reverse_result = netdiag.reverse_dns(ip)
            print(f"  {ip:15s} -> {reverse_result.hostname}")
        except Exception:
            print(f"  {ip:15s} -> No reverse DNS")

# Run Lab 2
lab2_dns_analysis()
```

### Lab 2 Assignment
**Submit a report analyzing**:
1. DNS record differences between domains
2. Performance comparison between DNS servers
3. Explanation of why certain DNS servers might be faster

---

## 🧪 Lab 3: Port Scanning and Service Detection

**Duration**: 3 hours  
**Difficulty**: Intermediate  
**Learning Objectives**:
- Understand network ports and services
- Learn ethical scanning practices
- Analyze service fingerprints

### Exercise 3.1: Campus Service Discovery
```python
def lab3_service_discovery():
    """Lab 3: Ethical service discovery on campus infrastructure."""
    
    print("🔍 Lab 3: Campus Service Discovery")
    print("🛡️  IMPORTANT: Only scan authorized targets!")
    print("=" * 50)
    
    # Authorized campus targets for educational scanning
    authorized_targets = [
        "polinela.ac.id",
        "elearning.polinela.ac.id"
    ]
    
    # Educational port ranges
    educational_ports = {
        "Web Services": [80, 443, 8080, 8443],
        "Email Services": [25, 110, 143, 993, 995],
        "Remote Access": [22, 23, 3389],
        "Database": [3306, 5432, 1433],
        "DNS": [53],
        "FTP": [21, 22]
    }
    
    for target in authorized_targets:
        print(f"\n🎯 Scanning {target}:")
        print("=" * 40)
        
        all_ports = []
        for category, ports in educational_ports.items():
            all_ports.extend(ports)
        
        # Remove duplicates and sort
        unique_ports = sorted(list(set(all_ports)))
        
        # Perform scan
        try:
            scan_results = netdiag.port_scan(target, unique_ports, threads=10)
            
            # Organize results by category
            for category, category_ports in educational_ports.items():
                print(f"\n📂 {category}:")
                
                category_results = [r for r in scan_results if r.port in category_ports]
                open_ports = [r for r in category_results if r.is_open]
                
                if open_ports:
                    for port_result in open_ports:
                        print(f"  ✅ Port {port_result.port}: {port_result.service or 'Unknown'}")
                        
                        # Service detection for open ports
                        try:
                            service_info = netdiag.service_detection(target, port_result.port)
                            if service_info.version:
                                print(f"      Version: {service_info.version}")
                            if service_info.banner:
                                print(f"      Banner: {service_info.banner[:60]}...")
                        except Exception:
                            pass
                else:
                    print(f"  ❌ No open ports in this category")
        
        except Exception as e:
            print(f"❌ Scan failed: {e}")

# Run Lab 3
lab3_service_discovery()
```

### Lab 3 Ethical Guidelines
Before starting this lab, students must acknowledge:
1. ✅ Only scan systems you own or have permission to test
2. ✅ Use reasonable scan rates to avoid disruption
3. ✅ Document all scanning activities
4. ❌ Never attempt to exploit discovered services
5. ❌ Never scan external systems without permission

---

## 🧪 Lab 4: Network Security Assessment

**Duration**: 3 hours  
**Difficulty**: Intermediate-Advanced  
**Learning Objectives**:
- Understand security scanning principles
- Analyze SSL/TLS configurations
- Identify common vulnerabilities

### Exercise 4.1: Campus Security Analysis
```python
def lab4_security_assessment():
    """Lab 4: Campus infrastructure security assessment."""
    
    print("🛡️  Lab 4: Campus Security Assessment")
    print("📚 Educational Purpose Only - Authorized Targets Only")
    print("=" * 60)
    
    # Authorized educational targets
    campus_sites = [
        "polinela.ac.id",
        "elearning.polinela.ac.id"
    ]
    
    for site in campus_sites:
        print(f"\n🔒 Security Assessment: {site}")
        print("-" * 40)
        
        # 1. SSL/TLS Certificate Analysis
        print("\n1. SSL/TLS Certificate Check:")
        try:
            ssl_result = netdiag.ssl_certificate_check(site)
            print(f"   Certificate Valid: {'✅ Yes' if ssl_result.is_valid else '❌ No'}")
            print(f"   Issued by: {ssl_result.issuer}")
            print(f"   Expires: {ssl_result.expiry_date}")
            print(f"   Days until expiry: {ssl_result.days_until_expiry}")
            
            if ssl_result.days_until_expiry < 30:
                print("   ⚠️  Certificate expires soon!")
                
        except Exception as e:
            print(f"   ❌ SSL check failed: {e}")
        
        # 2. Security Headers Analysis
        print("\n2. Security Headers Check:")
        try:
            headers_result = netdiag.security_headers_check(site)
            print(f"   Security Score: {headers_result.score}/100")
            
            if headers_result.present_headers:
                print("   ✅ Present Headers:")
                for header in headers_result.present_headers:
                    print(f"      - {header}")
            
            if headers_result.missing_headers:
                print("   ❌ Missing Headers:")
                for header in headers_result.missing_headers:
                    print(f"      - {header}")
                    
        except Exception as e:
            print(f"   ❌ Headers check failed: {e}")
        
        # 3. Common Vulnerability Scan
        print("\n3. Basic Vulnerability Assessment:")
        try:
            vuln_result = netdiag.vulnerability_scan(site, scan_type='basic')
            
            if vuln_result.vulnerabilities:
                print(f"   ⚠️  {len(vuln_result.vulnerabilities)} potential issues found:")
                for vuln in vuln_result.vulnerabilities[:5]:  # Show first 5
                    print(f"      - {vuln.name} (Severity: {vuln.severity})")
            else:
                print("   ✅ No obvious vulnerabilities detected")
                
        except Exception as e:
            print(f"   ❌ Vulnerability scan failed: {e}")

# Run Lab 4
lab4_security_assessment()
```

---

## 🧪 Lab 5: Network Performance Analysis

**Duration**: 2 hours  
**Difficulty**: Intermediate  
**Learning Objectives**:
- Measure network performance metrics
- Understand latency, jitter, and throughput
- Create performance baselines

### Exercise 5.1: Campus Network Performance
```python
def lab5_performance_analysis():
    """Lab 5: Campus network performance analysis."""
    
    print("📊 Lab 5: Network Performance Analysis")
    print("=" * 40)
    
    targets = [
        ("Campus Main", "polinela.ac.id"),
        ("Local Gateway", "192.168.1.1"),
        ("Google DNS", "8.8.8.8"),
        ("Local Server", "127.0.0.1")
    ]
    
    for name, target in targets:
        print(f"\n📈 Performance Analysis: {name} ({target})")
        print("-" * 50)
        
        # 1. Latency Analysis
        print("1. Latency Analysis (50 samples):")
        try:
            latency_result = netdiag.latency_test(target, samples=50)
            print(f"   Average: {latency_result.avg:.2f} ms")
            print(f"   Minimum: {latency_result.min:.2f} ms")
            print(f"   Maximum: {latency_result.max:.2f} ms")
            print(f"   Jitter (std dev): {latency_result.jitter:.2f} ms")
            print(f"   95th percentile: {latency_result.p95:.2f} ms")
            
        except Exception as e:
            print(f"   ❌ Latency test failed: {e}")
        
        # 2. Connection Quality Assessment
        print("\n2. Connection Quality:")
        try:
            quality_result = netdiag.quality_assessment(target)
            print(f"   Overall Score: {quality_result.score}/100")
            print(f"   Quality Rating: {quality_result.rating}")
            print(f"   Recommended for: {quality_result.suitable_applications}")
            
        except Exception as e:
            print(f"   ❌ Quality assessment failed: {e}")

# Run Lab 5
lab5_performance_analysis()
```

---

## 🧪 Advanced Labs (6-10)

### Lab 6: Network Topology Discovery
- Use traceroute to map network paths
- Identify network hops and their roles
- Create network topology diagrams

### Lab 7: Automated Monitoring
- Set up continuous network monitoring
- Create alerting for performance degradation
- Generate automated reports

### Lab 8: Protocol Analysis
- Deep dive into specific protocols
- Analyze protocol behavior
- Compare protocol efficiency

### Lab 9: Security Hardening
- Implement security best practices
- Test security configurations
- Document security improvements

### Lab 10: Capstone Project
- Comprehensive network analysis project
- Combine all learned techniques
- Present findings and recommendations

---

## 📝 Lab Assessment Rubric

### Grading Criteria (100 points total)

#### Technical Execution (40 points)
- Correct use of netdiag functions (20 points)
- Proper data collection and analysis (20 points)

#### Understanding and Analysis (30 points)
- Interpretation of results (15 points)
- Problem-solving approach (15 points)

#### Documentation and Reporting (20 points)
- Clear and complete lab reports (10 points)
- Professional presentation of findings (10 points)

#### Safety and Ethics (10 points)
- Following ethical guidelines (5 points)
- Proper authorization awareness (5 points)

### Grade Scale
- A: 90-100 points (Excellent understanding and execution)
- B: 80-89 points (Good understanding with minor issues)
- C: 70-79 points (Satisfactory work with some gaps)
- D: 60-69 points (Below expectations, needs improvement)
- F: Below 60 points (Inadequate work)

---

## 🎓 Lab Completion Certificate

Upon successful completion of all laboratory exercises, students receive:

```
🏆 CERTIFICATE OF COMPLETION
   Network Diagnostics Laboratory Series
   
   This certifies that [Student Name]
   has successfully completed the Network Diagnostics
   Laboratory Series at Politeknik Negeri Lampung
   
   Skills Demonstrated:
   ✅ Network Connectivity Analysis
   ✅ DNS Resolution Troubleshooting  
   ✅ Port Scanning and Service Detection
   ✅ Security Assessment Principles
   ✅ Performance Analysis Techniques
   
   Date: [Completion Date]
   Instructor: [Instructor Name]
```

---

**Laboratory Excellence: 🧪 | Practical Skills: 🛠️ | Industry Readiness: 🚀**