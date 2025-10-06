# NetDiag Troubleshooting Guide

## 🔧 Common Issues and Solutions

### Quick Reference

| Issue Category | Quick Check | Common Cause |
|---------------|-------------|--------------|
| 🔌 **Connection** | `ping 8.8.8.8` | Network connectivity |
| 🐍 **Python** | `python --version` | Python installation |
| 📦 **Dependencies** | `pip list` | Missing packages |
| 🔑 **Permissions** | `whoami` | Insufficient privileges |
| 🌐 **DNS** | `nslookup polinela.ac.id` | DNS resolution |
| 🔥 **Firewall** | Windows Defender settings | Blocked connections |
| 📊 **Performance** | Resource usage | System resources |

### Installation Issues

#### Python Version Compatibility

**Problem:** `ImportError: This package requires Python 3.7 or later`

**Solution:**
```powershell
# Check Python version
python --version

# Install compatible Python version
# Download from https://python.org (3.7 or later)

# Verify installation
python -c "import sys; print(sys.version)"
```

**Campus Network Context:**
```powershell
# Check if Python accessible dari campus network
python -c "import urllib.request; urllib.request.urlopen('https://pypi.org')"
```

#### Package Installation Failures

**Problem:** `pip install netdiag` fails with network errors

**Solution:**
```powershell
# Try dengan different index
pip install --index-url https://pypi.org/simple/ netdiag

# Use trusted hosts for campus firewall
pip install --trusted-host pypi.org --trusted-host pypi.python.org netdiag

# Install dengan user permissions
pip install --user netdiag

# Upgrade pip first
python -m pip install --upgrade pip
```

**Campus Proxy Configuration:**
```powershell
# Configure pip untuk campus proxy (jika diperlukan)
pip config set global.proxy http://proxy.polinela.ac.id:8080
pip config set global.trusted-host "pypi.org pypi.python.org files.pythonhosted.org"
```

#### Virtual Environment Issues

**Problem:** Virtual environment tidak activate properly

**Solution:**
```powershell
# Create virtual environment
python -m venv netdiag_env

# Activate di Windows
netdiag_env\Scripts\activate

# Verify activation
where python
pip list

# Deactivate when done
deactivate
```

**Educational Context:**
Virtual environments prevent dependency conflicts yang common dalam campus computing environments dengan multiple Python projects.

### Network Connectivity Issues

#### Basic Connectivity Testing

**Problem:** NetDiag cannot reach target hosts

**Diagnostic Steps:**
```python
# Test basic connectivity
import netdiag

# 1. Test local connectivity
analyzer = netdiag.NetworkAnalyzer()
local_result = analyzer.ping_host("127.0.0.1")
print(f"Local test: {local_result.avg_latency}ms")

# 2. Test campus gateway
campus_gateway = "192.168.1.1"  # Replace dengan actual gateway
gateway_result = analyzer.ping_host(campus_gateway)
print(f"Gateway test: {gateway_result.avg_latency}ms")

# 3. Test external connectivity
external_result = analyzer.ping_host("8.8.8.8")
print(f"External test: {external_result.avg_latency}ms")

# 4. Test DNS resolution
dns_result = analyzer.ping_host("google.com")
print(f"DNS test: {dns_result.avg_latency}ms")
```

**Campus Network Diagnostics:**
```python
def diagnose_campus_network():
    """Comprehensive campus network diagnostic."""
    
    analyzer = netdiag.NetworkAnalyzer(verbose=True)
    
    # Test internal campus connectivity
    campus_hosts = [
        "polinela.ac.id",
        "portal.polinela.ac.id", 
        "elearning.polinela.ac.id"
    ]
    
    print("🏫 Testing Campus Network Connectivity")
    print("=" * 50)
    
    for host in campus_hosts:
        try:
            result = analyzer.ping_host(host, count=3)
            status = "✅ OK" if result.packet_loss < 5 else "⚠️ Issues"
            print(f"{host:<30} {status:<10} {result.avg_latency:>6.1f}ms")
        except Exception as e:
            print(f"{host:<30} ❌ Failed   {str(e)}")
    
    # Test internet connectivity
    external_hosts = ["8.8.8.8", "1.1.1.1", "google.com"]
    
    print("\n🌐 Testing Internet Connectivity")
    print("=" * 50)
    
    for host in external_hosts:
        try:
            result = analyzer.ping_host(host, count=3)
            status = "✅ OK" if result.packet_loss < 10 else "⚠️ Issues"
            print(f"{host:<30} {status:<10} {result.avg_latency:>6.1f}ms")
        except Exception as e:
            print(f"{host:<30} ❌ Failed   {str(e)}")

# Run diagnostic
diagnose_campus_network()
```

#### DNS Resolution Problems

**Problem:** Cannot resolve hostnames

**Solution:**
```python
import socket
import netdiag

def test_dns_resolution():
    """Test DNS resolution capabilities."""
    
    test_hosts = [
        "polinela.ac.id",
        "google.com",
        "github.com"
    ]
    
    print("🔍 DNS Resolution Test")
    print("=" * 40)
    
    for host in test_hosts:
        try:
            # Test standard resolution
            ip = socket.gethostbyname(host)
            print(f"✅ {host:<20} → {ip}")
            
            # Test reverse resolution
            try:
                reverse = socket.gethostbyaddr(ip)
                print(f"   Reverse: {reverse[0]}")
            except:
                print(f"   Reverse: Not available")
                
        except socket.gaierror as e:
            print(f"❌ {host:<20} → DNS Error: {e}")
        except Exception as e:
            print(f"❌ {host:<20} → Error: {e}")

test_dns_resolution()
```

**Manual DNS Configuration:**
```python
# Override DNS servers untuk testing
import socket
import netdiag

# Use custom DNS server
custom_analyzer = netdiag.NetworkAnalyzer()

# Alternative: Use different DNS servers
dns_servers = ["8.8.8.8", "1.1.1.1", "208.67.222.222"]

for dns in dns_servers:
    print(f"Testing dengan DNS server: {dns}")
    try:
        result = custom_analyzer.ping_host(dns)
        print(f"  Response time: {result.avg_latency:.1f}ms")
    except Exception as e:
        print(f"  Error: {e}")
```

### Permission Issues

#### Administrator Privileges

**Problem:** `PermissionError` when using certain network functions

**Solution:**
```powershell
# Run PowerShell as Administrator
# Right-click PowerShell → "Run as Administrator"

# Check current permissions
whoami /groups | findstr "S-1-5-32-544"

# Alternative: Use elevated Python
python -c "import ctypes; print('Admin:', ctypes.windll.shell32.IsUserAnAdmin())"
```

**Educational Context:**
Some network operations require elevated privileges dalam Windows environment. This teaches students about security models dalam operating systems.

#### Windows Firewall Issues

**Problem:** Windows Firewall blocks network operations

**Solution:**
```powershell
# Check firewall status
netsh advfirewall show allprofiles

# Allow Python through firewall (as Administrator)
netsh advfirewall firewall add rule name="Python" dir=in action=allow program="C:\Python39\python.exe"

# Alternative: Temporary disable (untuk testing only)
netsh advfirewall set allprofiles state off
# Remember to re-enable: netsh advfirewall set allprofiles state on
```

**Campus Firewall Considerations:**
```python
def test_firewall_connectivity():
    """Test connectivity through campus firewall."""
    
    # Common ports yang might be blocked
    test_ports = [
        (80, "HTTP"),
        (443, "HTTPS"), 
        (53, "DNS"),
        (22, "SSH"),
        (23, "Telnet"),
        (80, "HTTP Alt")
    ]
    
    import socket
    
    print("🔥 Firewall Connectivity Test")
    print("=" * 40)
    
    for port, description in test_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex(("google.com", port))
            sock.close()
            
            if result == 0:
                print(f"✅ Port {port:>3} ({description:<10}) - Open")
            else:
                print(f"❌ Port {port:>3} ({description:<10}) - Blocked")
                
        except Exception as e:
            print(f"❌ Port {port:>3} ({description:<10}) - Error: {e}")

test_firewall_connectivity()
```

### Performance Issues

#### Slow Network Operations

**Problem:** NetDiag operations are very slow

**Diagnostic:**
```python
import time
import netdiag

def performance_diagnostic():
    """Diagnose performance issues."""
    
    analyzer = netdiag.NetworkAnalyzer(verbose=True)
    
    # Test different timeout values
    timeouts = [1, 3, 5, 10]
    host = "google.com"
    
    print("⏱️ Performance Diagnostic")
    print("=" * 40)
    
    for timeout in timeouts:
        analyzer.timeout = timeout
        
        start_time = time.time()
        try:
            result = analyzer.ping_host(host, count=1)
            end_time = time.time()
            
            print(f"Timeout {timeout}s: {end_time - start_time:.2f}s actual")
            print(f"  Latency: {result.avg_latency:.1f}ms")
            print(f"  Success: {result.packets_received > 0}")
            
        except Exception as e:
            end_time = time.time()
            print(f"Timeout {timeout}s: {end_time - start_time:.2f}s (failed)")
            print(f"  Error: {e}")
        
        print()

performance_diagnostic()
```

**Memory Usage Monitoring:**
```python
import psutil
import netdiag

def monitor_memory_usage():
    """Monitor memory usage during operations."""
    
    process = psutil.Process()
    analyzer = netdiag.NetworkAnalyzer()
    
    print("📊 Memory Usage Monitoring")
    print("=" * 40)
    
    # Baseline memory
    baseline = process.memory_info().rss / 1024 / 1024
    print(f"Baseline memory: {baseline:.1f} MB")
    
    # Test multiple operations
    hosts = ["google.com", "github.com", "stackoverflow.com"] * 10
    
    for i, host in enumerate(hosts, 1):
        try:
            result = analyzer.ping_host(host)
            current_memory = process.memory_info().rss / 1024 / 1024
            memory_delta = current_memory - baseline
            
            if i % 5 == 0:  # Report every 5th operation
                print(f"Operation {i:2d}: {memory_delta:+6.1f} MB delta")
                
        except Exception as e:
            print(f"Operation {i:2d}: Error - {e}")

monitor_memory_usage()
```

### Educational Usage Issues

#### Lab Exercise Problems

**Problem:** Students cannot complete lab exercises

**Common Solutions:**

1. **Network Access in Labs:**
```python
# Check lab network configuration
def check_lab_environment():
    """Check if lab environment is properly configured."""
    
    import netdiag
    import sys
    import platform
    
    print("🧪 Lab Environment Check")
    print("=" * 40)
    
    # System information
    print(f"Python version: {sys.version}")
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"NetDiag version: {netdiag.__version__ if hasattr(netdiag, '__version__') else 'Unknown'}")
    
    # Network capabilities
    analyzer = netdiag.NetworkAnalyzer()
    
    try:
        # Test basic functionality
        result = analyzer.ping_host("127.0.0.1", count=1)
        print(f"✅ Basic ping works: {result.avg_latency:.1f}ms")
        
        # Test campus connectivity
        campus_result = analyzer.ping_host("polinela.ac.id", count=1)
        print(f"✅ Campus connectivity: {campus_result.avg_latency:.1f}ms")
        
        # Test internet access
        internet_result = analyzer.ping_host("8.8.8.8", count=1)
        print(f"✅ Internet access: {internet_result.avg_latency:.1f}ms")
        
        print("\n🎯 Lab environment ready for exercises!")
        
    except Exception as e:
        print(f"❌ Environment issue: {e}")
        print("\n🔧 Contact lab administrator untuk assistance")

check_lab_environment()
```

2. **Assignment Debugging:**
```python
def debug_assignment_code(student_code_function):
    """Help debug common assignment issues."""
    
    print("🎓 Assignment Debugging Helper")
    print("=" * 40)
    
    try:
        # Test student's function
        result = student_code_function()
        
        # Validate result format
        if hasattr(result, 'avg_latency'):
            print("✅ Function returns proper result object")
            print(f"   Average latency: {result.avg_latency:.1f}ms")
            print(f"   Packet loss: {result.packet_loss:.1f}%")
        else:
            print("❌ Function doesn't return proper result object")
            print(f"   Returned: {type(result)} - {result}")
        
        # Check for common issues
        if hasattr(result, 'packets_sent') and result.packets_sent == 0:
            print("⚠️ Warning: No packets were sent")
            
        if hasattr(result, 'avg_latency') and result.avg_latency == 0:
            print("⚠️ Warning: Latency is zero (possible error)")
            
    except Exception as e:
        print(f"❌ Function execution failed: {e}")
        print("   Common fixes:")
        print("   - Check function parameters")
        print("   - Verify network connectivity") 
        print("   - Check for typos dalam host names")

# Example usage for students
def example_student_function():
    analyzer = netdiag.NetworkAnalyzer()
    return analyzer.ping_host("google.com")

debug_assignment_code(example_student_function)
```

### Advanced Troubleshooting

#### Network Protocol Analysis

**Problem:** Need detailed protocol-level debugging

**Solution:**
```python
import netdiag
import logging

# Enable detailed logging
logging.basicConfig(level=logging.DEBUG)

def detailed_network_analysis(host):
    """Perform detailed network analysis untuk troubleshooting."""
    
    analyzer = netdiag.NetworkAnalyzer(verbose=True)
    
    print(f"🔬 Detailed Analysis for {host}")
    print("=" * 50)
    
    # Multiple analysis techniques
    analyses = [
        ("Basic Ping", lambda: analyzer.ping_host(host)),
        ("Extended Ping", lambda: analyzer.ping_host(host, count=10)),
        ("Large Packet", lambda: analyzer.ping_host(host, packet_size=1024)),
    ]
    
    results = {}
    
    for name, analysis_func in analyses:
        print(f"\n📊 {name}")
        print("-" * 30)
        
        try:
            result = analysis_func()
            results[name] = result
            
            print(f"✅ Success: {result.avg_latency:.1f}ms")
            print(f"   Packets: {result.packets_received}/{result.packets_sent}")
            print(f"   Loss: {result.packet_loss:.1f}%")
            
            if hasattr(result, 'additional_metrics'):
                for key, value in result.additional_metrics.items():
                    print(f"   {key}: {value}")
                    
        except Exception as e:
            print(f"❌ Failed: {e}")
            results[name] = None
    
    # Analysis summary
    print(f"\n📋 Analysis Summary")
    print("=" * 30)
    
    successful_tests = sum(1 for r in results.values() if r is not None)
    total_tests = len(results)
    
    print(f"Success rate: {successful_tests}/{total_tests}")
    
    if successful_tests > 0:
        avg_latencies = [r.avg_latency for r in results.values() if r is not None]
        print(f"Average latency: {sum(avg_latencies)/len(avg_latencies):.1f}ms")
    
    return results

# Example usage
detailed_network_analysis("polinela.ac.id")
```

#### System Resource Monitoring

**Problem:** Need to understand system resource usage

**Solution:**
```python
import psutil
import time
import threading
import netdiag

class ResourceMonitor:
    """Monitor system resources during network operations."""
    
    def __init__(self):
        self.monitoring = False
        self.stats = []
    
    def start_monitoring(self):
        """Start resource monitoring."""
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop resource monitoring."""
        self.monitoring = False
        if hasattr(self, 'monitor_thread'):
            self.monitor_thread.join(timeout=1)
    
    def _monitor_loop(self):
        """Monitor system resources."""
        while self.monitoring:
            try:
                # CPU usage
                cpu_percent = psutil.cpu_percent(interval=0.1)
                
                # Memory usage
                memory = psutil.virtual_memory()
                
                # Network I/O
                network = psutil.net_io_counters()
                
                # Store stats
                self.stats.append({
                    'timestamp': time.time(),
                    'cpu_percent': cpu_percent,
                    'memory_percent': memory.percent,
                    'memory_used_mb': memory.used / 1024 / 1024,
                    'bytes_sent': network.bytes_sent,
                    'bytes_recv': network.bytes_recv
                })
                
                time.sleep(0.5)  # Monitor every 500ms
                
            except Exception as e:
                print(f"Monitoring error: {e}")
                break
    
    def get_report(self):
        """Generate resource usage report."""
        if not self.stats:
            return "No monitoring data available"
        
        # Calculate averages
        avg_cpu = sum(s['cpu_percent'] for s in self.stats) / len(self.stats)
        avg_memory = sum(s['memory_percent'] for s in self.stats) / len(self.stats)
        max_memory_mb = max(s['memory_used_mb'] for s in self.stats)
        
        # Calculate network transfer
        if len(self.stats) > 1:
            bytes_sent_delta = self.stats[-1]['bytes_sent'] - self.stats[0]['bytes_sent']
            bytes_recv_delta = self.stats[-1]['bytes_recv'] - self.stats[0]['bytes_recv']
        else:
            bytes_sent_delta = bytes_recv_delta = 0
        
        return f"""
📊 Resource Usage Report
========================
Duration: {len(self.stats) * 0.5:.1f} seconds
Average CPU: {avg_cpu:.1f}%
Average Memory: {avg_memory:.1f}%
Peak Memory: {max_memory_mb:.1f} MB
Network Sent: {bytes_sent_delta:,} bytes
Network Received: {bytes_recv_delta:,} bytes
"""

def test_with_monitoring(host="google.com"):
    """Test network operations dengan resource monitoring."""
    
    monitor = ResourceMonitor()
    analyzer = netdiag.NetworkAnalyzer()
    
    print(f"🔍 Testing {host} dengan resource monitoring...")
    
    # Start monitoring
    monitor.start_monitoring()
    
    try:
        # Perform network operations
        result = analyzer.ping_host(host, count=5)
        
        # Wait a bit untuk complete monitoring
        time.sleep(1)
        
        # Stop monitoring
        monitor.stop_monitoring()
        
        # Print results
        print(f"✅ Network test completed:")
        print(f"   Latency: {result.avg_latency:.1f}ms")
        print(f"   Packet loss: {result.packet_loss:.1f}%")
        
        print(monitor.get_report())
        
    except Exception as e:
        monitor.stop_monitoring()
        print(f"❌ Test failed: {e}")

# Run monitoring test
test_with_monitoring("polinela.ac.id")
```

### Getting Help

#### Support Resources

1. **Documentation:** Read comprehensive docs dalam `docs/` directory
2. **Examples:** Check `examples/` directory untuk practical use cases
3. **Tests:** Review `tests/` directory untuk usage patterns
4. **Campus Support:** Contact IT support untuk network-related issues

#### Reporting Issues

When reporting issues, include:

```python
def generate_debug_report():
    """Generate comprehensive debug report untuk issue reporting."""
    
    import sys
    import platform
    import netdiag
    
    report = f"""
NetDiag Debug Report
==================
Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}

System Information:
- Python: {sys.version}
- Platform: {platform.system()} {platform.release()}
- Architecture: {platform.architecture()[0]}
- NetDiag Version: {getattr(netdiag, '__version__', 'Unknown')}

Network Test:
"""
    
    try:
        analyzer = netdiag.NetworkAnalyzer()
        result = analyzer.ping_host("8.8.8.8", count=3)
        
        report += f"""
- Basic connectivity: ✅ Working
- Average latency: {result.avg_latency:.1f}ms
- Packet loss: {result.packet_loss:.1f}%
"""
    except Exception as e:
        report += f"""
- Basic connectivity: ❌ Failed
- Error: {e}
"""
    
    # System resources
    try:
        import psutil
        memory = psutil.virtual_memory()
        cpu_percent = psutil.cpu_percent()
        
        report += f"""
System Resources:
- Memory usage: {memory.percent:.1f}%
- CPU usage: {cpu_percent:.1f}%
- Available memory: {memory.available / 1024 / 1024:.0f} MB
"""
    except:
        report += "\nSystem Resources: Unable to collect"
    
    print(report)
    return report

# Generate report untuk troubleshooting
generate_debug_report()
```

#### Educational Support

For students di Politeknik Negeri Lampung:

1. **Lab Hours:** Consult with lab assistants during scheduled hours
2. **Course Forums:** Use course discussion forums untuk technical questions
3. **Study Groups:** Form study groups untuk collaborative troubleshooting
4. **Office Hours:** Visit instructor office hours untuk complex issues

### Prevention Tips

#### Best Practices

1. **Regular Updates:**
```powershell
# Keep NetDiag updated
pip install --upgrade netdiag

# Update dependencies
pip install --upgrade -r requirements.txt
```

2. **Environment Management:**
```powershell
# Use virtual environments
python -m venv netdiag_env
netdiag_env\Scripts\activate
pip install netdiag
```

3. **Configuration Backup:**
```python
# Save working configuration
import netdiag
import json

config = {
    'timeout': 5,
    'retries': 3,
    'campus_settings': {
        'proxy': None,
        'dns_servers': ['8.8.8.8', '1.1.1.1']
    }
}

with open('netdiag_config.json', 'w') as f:
    json.dump(config, f, indent=2)
```

4. **Regular Testing:**
```python
# Daily connectivity test
def daily_connectivity_check():
    """Run daily connectivity check untuk early issue detection."""
    
    analyzer = netdiag.NetworkAnalyzer()
    
    critical_hosts = [
        "127.0.0.1",        # Local
        "192.168.1.1",      # Gateway (adjust as needed)
        "8.8.8.8",          # External DNS
        "polinela.ac.id"    # Campus
    ]
    
    all_good = True
    
    for host in critical_hosts:
        try:
            result = analyzer.ping_host(host, count=1)
            if result.packet_loss > 50:
                print(f"⚠️ High packet loss to {host}")
                all_good = False
        except:
            print(f"❌ Cannot reach {host}")
            all_good = False
    
    if all_good:
        print("✅ All connectivity checks passed")
    else:
        print("⚠️ Some connectivity issues detected")
    
    return all_good

# Run check
daily_connectivity_check()
```

### Emergency Procedures

#### Critical Issues

If NetDiag completely stops working:

1. **Restart Python Environment:**
```powershell
# Deactivate current environment
deactivate

# Recreate environment
python -m venv fresh_env
fresh_env\Scripts\activate
pip install netdiag
```

2. **Network Reset (Windows):**
```powershell
# Reset network configuration (as Administrator)
netsh winsock reset
netsh int ip reset
ipconfig /release
ipconfig /renew
ipconfig /flushdns
```

3. **Campus Network Issues:**
   - Contact campus IT support
   - Check campus network status page
   - Try alternative network connection
   - Use mobile hotspot untuk testing

#### Recovery Steps

```python
def emergency_network_test():
    """Emergency network connectivity test."""
    
    print("🚨 Emergency Network Test")
    print("=" * 30)
    
    # Most basic test
    import subprocess
    
    # Test 1: Basic ping
    try:
        result = subprocess.run(['ping', '-n', '1', '8.8.8.8'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Basic ping works")
        else:
            print("❌ Basic ping failed")
    except:
        print("❌ Cannot execute ping command")
    
    # Test 2: DNS resolution
    try:
        import socket
        socket.gethostbyname('google.com')
        print("✅ DNS resolution works")
    except:
        print("❌ DNS resolution failed")
    
    # Test 3: HTTP connectivity
    try:
        import urllib.request
        urllib.request.urlopen('http://google.com', timeout=10)
        print("✅ HTTP connectivity works")
    except:
        print("❌ HTTP connectivity failed")
    
    print("\nIf all tests fail, contact network administrator")

# Run emergency test
emergency_network_test()
```

This troubleshooting guide provides comprehensive solutions untuk common issues yang students dan users might encounter when using NetDiag dalam campus environment di Politeknik Negeri Lampung.