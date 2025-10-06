# 🚀 Quick Start Tutorial

Welcome to the **Netdiag Quick Start Tutorial**! This guide will get you up and running with network diagnostics in just a few minutes.

## 🎯 Learning Objectives

By the end of this tutorial, you will:
- ✅ Understand basic netdiag concepts
- ✅ Perform your first network diagnostics
- ✅ Analyze network connectivity issues
- ✅ Generate comprehensive network reports
- ✅ Use educational examples with real domains

## 📋 Prerequisites

- Python 3.7+ installed
- Netdiag package installed ([Installation Guide](../installation.md))
- Basic understanding of networking concepts
- Internet connection for testing

## 🏁 Your First Network Diagnostic

### Step 1: Import Netdiag
```python
import netdiag
print(f"Netdiag version: {netdiag.__version__}")
```

### Step 2: Basic Connectivity Test
```python
# Test connectivity to a reliable server
target = "8.8.8.8"  # Google DNS
result = netdiag.ping(target)

if result:
    print(f"✅ Successfully connected to {target}")
    print(f"Response time: {result.get('avg_time', 'N/A')} ms")
else:
    print(f"❌ Failed to connect to {target}")
```

### Step 3: Domain Name Resolution
```python
# Test DNS resolution
domain = "google.com"
dns_result = netdiag.dns_lookup(domain)

if dns_result:
    print(f"✅ DNS resolution successful for {domain}")
    print(f"IP Address: {dns_result.get('ip', 'N/A')}")
else:
    print(f"❌ DNS resolution failed for {domain}")
```

## 🎓 Educational Example: Polinela.ac.id

Let's use **Politeknik Negeri Lampung** as our learning example:

### Complete Diagnostic Workflow
```python
import netdiag
from datetime import datetime

# Educational target
target = "polinela.ac.id"
print(f"🎓 Network Diagnostics for {target}")
print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 50)

# 1. Basic Connectivity
print("\n1️⃣ CONNECTIVITY TEST")
ping_result = netdiag.ping(target)
if ping_result:
    print(f"✅ Ping successful")
    print(f"   Response time: {ping_result.get('avg_time', 'N/A')} ms")
    print(f"   Packet loss: {ping_result.get('packet_loss', 'N/A')}%")
else:
    print("❌ Ping failed")

# 2. DNS Analysis
print("\n2️⃣ DNS ANALYSIS")
dns_result = netdiag.dns_lookup(target)
if dns_result:
    print(f"✅ DNS resolution successful")
    print(f"   IP Address: {dns_result.get('ip', 'N/A')}")
    print(f"   DNS Server: {dns_result.get('dns_server', 'N/A')}")
else:
    print("❌ DNS resolution failed")

# 3. Port Analysis
print("\n3️⃣ PORT ANALYSIS")
common_ports = [80, 443, 22, 21, 25]
for port in common_ports:
    port_result = netdiag.check_port(target, port)
    status = "🟢 OPEN" if port_result else "🔴 CLOSED"
    service = {80: "HTTP", 443: "HTTPS", 22: "SSH", 21: "FTP", 25: "SMTP"}.get(port, "Unknown")
    print(f"   Port {port} ({service}): {status}")

# 4. Network Route
print("\n4️⃣ NETWORK ROUTE")
traceroute_result = netdiag.traceroute(target)
if traceroute_result:
    print(f"✅ Traceroute completed")
    hops = traceroute_result.get('hops', [])
    print(f"   Total hops: {len(hops)}")
    for i, hop in enumerate(hops[:5], 1):  # Show first 5 hops
        print(f"   Hop {i}: {hop.get('ip', 'N/A')} ({hop.get('time', 'N/A')} ms)")
    if len(hops) > 5:
        print(f"   ... and {len(hops) - 5} more hops")
else:
    print("❌ Traceroute failed")

print("\n" + "=" * 50)
print("🎉 Diagnostic completed!")
```

## 🔍 Advanced Quick Examples

### Example 1: Multiple Target Analysis
```python
# Test multiple educational domains
targets = [
    "polinela.ac.id",
    "unila.ac.id", 
    "kemendikbud.go.id",
    "google.com"
]

print("🎯 MULTI-TARGET ANALYSIS")
print("=" * 40)

for target in targets:
    print(f"\n📍 Testing {target}")
    
    # Quick connectivity check
    ping_ok = bool(netdiag.ping(target))
    dns_ok = bool(netdiag.dns_lookup(target))
    http_ok = bool(netdiag.check_port(target, 80))
    https_ok = bool(netdiag.check_port(target, 443))
    
    # Results summary
    print(f"   Ping: {'✅' if ping_ok else '❌'}")
    print(f"   DNS:  {'✅' if dns_ok else '❌'}")
    print(f"   HTTP: {'✅' if http_ok else '❌'}")
    print(f"   HTTPS:{'✅' if https_ok else '❌'}")
    
    # Overall status
    overall = all([ping_ok, dns_ok])
    print(f"   Status: {'🟢 HEALTHY' if overall else '🔴 ISSUES'}")
```

### Example 2: Performance Monitoring
```python
import time

def monitor_connectivity(target, duration_minutes=5):
    """Monitor connectivity over time"""
    print(f"📊 PERFORMANCE MONITORING: {target}")
    print(f"⏱️  Duration: {duration_minutes} minutes")
    print("=" * 40)
    
    start_time = time.time()
    test_count = 0
    success_count = 0
    response_times = []
    
    while time.time() - start_time < duration_minutes * 60:
        test_count += 1
        
        # Perform ping test
        result = netdiag.ping(target)
        
        if result:
            success_count += 1
            avg_time = result.get('avg_time', 0)
            response_times.append(avg_time)
            status = "✅"
        else:
            status = "❌"
        
        print(f"Test {test_count}: {status} {target} - {result.get('avg_time', 'N/A')} ms")
        
        # Wait 30 seconds between tests
        time.sleep(30)
    
    # Generate summary
    success_rate = (success_count / test_count) * 100
    avg_response = sum(response_times) / len(response_times) if response_times else 0
    
    print("\n📈 MONITORING SUMMARY")
    print(f"Total tests: {test_count}")
    print(f"Success rate: {success_rate:.1f}%")
    print(f"Average response time: {avg_response:.1f} ms")

# Run monitoring (uncomment to use)
# monitor_connectivity("polinela.ac.id", duration_minutes=2)
```

### Example 3: Network Report Generation
```python
import json
from datetime import datetime

def generate_network_report(target):
    """Generate comprehensive network report"""
    
    report = {
        "target": target,
        "timestamp": datetime.now().isoformat(),
        "tests": {}
    }
    
    print(f"📋 GENERATING REPORT FOR: {target}")
    print("=" * 40)
    
    # Connectivity Test
    print("🔍 Testing connectivity...")
    ping_result = netdiag.ping(target)
    report["tests"]["ping"] = {
        "success": bool(ping_result),
        "data": ping_result or {}
    }
    
    # DNS Test
    print("🔍 Testing DNS resolution...")
    dns_result = netdiag.dns_lookup(target)
    report["tests"]["dns"] = {
        "success": bool(dns_result),
        "data": dns_result or {}
    }
    
    # Port Scan
    print("🔍 Scanning common ports...")
    ports_to_scan = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995]
    port_results = {}
    
    for port in ports_to_scan:
        port_result = netdiag.check_port(target, port)
        port_results[str(port)] = bool(port_result)
    
    report["tests"]["ports"] = {
        "success": True,
        "data": port_results
    }
    
    # Generate summary
    total_tests = 3
    passed_tests = sum([
        report["tests"]["ping"]["success"],
        report["tests"]["dns"]["success"],
        len([p for p in port_results.values() if p]) > 0
    ])
    
    report["summary"] = {
        "total_tests": total_tests,
        "passed_tests": passed_tests,
        "success_rate": (passed_tests / total_tests) * 100,
        "overall_status": "PASS" if passed_tests >= 2 else "FAIL"
    }
    
    # Display results
    print(f"\n📊 REPORT SUMMARY")
    print(f"Target: {target}")
    print(f"Tests passed: {passed_tests}/{total_tests}")
    print(f"Success rate: {report['summary']['success_rate']:.1f}%")
    print(f"Overall status: {report['summary']['overall_status']}")
    
    # Save report
    filename = f"netdiag_report_{target.replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"📄 Report saved: {filename}")
    return report

# Generate report for educational domain
# report = generate_network_report("polinela.ac.id")
```

## 🎓 Educational Exercises

### Exercise 1: Campus Network Analysis
```python
# Analyze your campus network
campus_domains = [
    "polinela.ac.id",      # Main campus website
    "elearning.polinela.ac.id",  # E-learning platform
    "library.polinela.ac.id",    # Digital library
]

print("🏫 CAMPUS NETWORK ANALYSIS")
for domain in campus_domains:
    print(f"\n📍 Analyzing {domain}")
    # Your code here: implement ping, DNS, and port checks
    pass
```

### Exercise 2: Internet Provider Comparison
```python
# Compare different DNS servers
dns_servers = [
    ("Google", "8.8.8.8"),
    ("Cloudflare", "1.1.1.1"),
    ("OpenDNS", "208.67.222.222")
]

target = "polinela.ac.id"
print("🌐 DNS PERFORMANCE COMPARISON")

for name, dns_ip in dns_servers:
    print(f"\n🔍 Testing {name} DNS ({dns_ip})")
    # Your code here: implement DNS lookup with specific server
    pass
```

## 🎯 Key Takeaways

After completing this tutorial, you should understand:

1. **Basic Network Diagnostics**
   - How to test connectivity with ping
   - DNS resolution and lookup
   - Port scanning and service detection

2. **Real-world Applications**
   - Educational network analysis
   - Performance monitoring
   - Report generation

3. **Best Practices**
   - Systematic testing approach
   - Proper error handling
   - Documentation and reporting

## 📚 Next Steps

1. **Explore Advanced Features**: [Advanced Usage](../advanced/)
2. **Learn Networking Concepts**: [Educational Resources](../educational/)
3. **Try Laboratory Exercises**: [Lab Exercises](../examples/polinela_lab_praktikum.md)
4. **Read API Documentation**: [API Reference](../api/)

## 💡 Tips for Success

- **Start Simple**: Begin with basic ping and DNS tests
- **Use Real Examples**: Practice with domains you know
- **Document Everything**: Keep track of your results
- **Ask Questions**: Use GitHub Issues for help
- **Practice Regularly**: Network conditions change over time

## 🤝 Getting Help

- 📧 **Email**: [satriadivop354@gmail.com](mailto:satriadivop354@gmail.com)
- 🐛 **Issues**: [GitHub Issues](https://github.com/SatriaDivo/netdiag/issues)
- 📖 **Documentation**: [docs/README.md](../README.md)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/SatriaDivo/netdiag/discussions)

---

**Ready to dive deeper? Explore our comprehensive tutorials! 🚀**