# Common Issues Reference

## 📋 Quick Issue Reference Guide

This document provides a rapid reference untuk most frequently encountered issues dalam NetDiag usage, especially dalam campus environment di Politeknik Negeri Lampung.

### 🚀 Quick Fix Index

| Problem | Quick Command | Section |
|---------|---------------|---------|
| 🐍 Python not found | `python --version` | [Python Issues](#python-issues) |
| 📦 Package not found | `pip install netdiag` | [Installation Issues](#installation-issues) |
| 🔌 Connection timeout | `ping 8.8.8.8` | [Network Issues](#network-issues) |
| 🔑 Permission denied | Run as Administrator | [Permission Issues](#permission-issues) |
| 🌐 DNS not working | `nslookup google.com` | [DNS Issues](#dns-issues) |
| 🔥 Firewall blocked | Check Windows Defender | [Firewall Issues](#firewall-issues) |
| 📊 Slow performance | Check system resources | [Performance Issues](#performance-issues) |
| 🎓 Lab exercise failed | Check lab network | [Educational Issues](#educational-issues) |

---

## Python Issues

### Issue: `'python' is not recognized`

**Symptoms:**
```
'python' is not recognized as an internal or external command
```

**Quick Fix:**
```powershell
# Add Python to PATH atau use full path
C:\Python39\python.exe --version

# Alternative: Use py launcher
py --version
py -3 --version
```

**Campus Environment Fix:**
```powershell
# Check available Python installations
py -0
py -3.9 -c "print('Python 3.9 available')"
```

### Issue: `ImportError: No module named 'netdiag'`

**Symptoms:**
```python
>>> import netdiag
ImportError: No module named 'netdiag'
```

**Quick Fix:**
```powershell
# Install in current environment
pip install netdiag

# Check if installed
pip list | findstr netdiag

# Alternative: Use --user flag
pip install --user netdiag
```

### Issue: Python version too old

**Symptoms:**
```
This package requires Python 3.7 or later
```

**Quick Fix:**
```powershell
# Check version
python --version

# Install newer Python
# Download from https://python.org

# Use specific version launcher
py -3.9 script.py
```

---

## Installation Issues

### Issue: `pip` command not found

**Symptoms:**
```
'pip' is not recognized as an internal or external command
```

**Quick Fix:**
```powershell
# Use module form
python -m pip install netdiag

# Check pip installation
python -m pip --version

# Upgrade pip
python -m pip install --upgrade pip
```

### Issue: SSL Certificate errors

**Symptoms:**
```
SSL: CERTIFICATE_VERIFY_FAILED
```

**Quick Fix:**
```powershell
# Use trusted hosts
pip install --trusted-host pypi.org --trusted-host pypi.python.org netdiag

# Campus network fix
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --index-url https://pypi.org/simple/ netdiag
```

### Issue: Permission errors during installation

**Symptoms:**
```
PermissionError: [Errno 13] Permission denied
```

**Quick Fix:**
```powershell
# Install untuk user only
pip install --user netdiag

# Alternative: Use virtual environment
python -m venv netdiag_env
netdiag_env\Scripts\activate
pip install netdiag
```

### Issue: Virtual environment activation fails

**Symptoms:**
```
The system cannot find the path specified
```

**Quick Fix:**
```powershell
# Check if virtual environment exists
dir netdiag_env\Scripts\

# Create if missing
python -m venv netdiag_env

# Activate dengan full path
.\netdiag_env\Scripts\activate

# Alternative activation
netdiag_env\Scripts\activate.bat
```

---

## Network Issues

### Issue: Connection timeout

**Symptoms:**
```python
TimeoutError: Network operation timeout
```

**Quick Fix:**
```python
# Increase timeout
import netdiag
analyzer = netdiag.NetworkAnalyzer(timeout=10)
result = analyzer.ping_host("target.com")
```

**Campus Network Fix:**
```python
# Use campus-friendly settings
analyzer = netdiag.NetworkAnalyzer(
    timeout=15,      # Longer timeout untuk campus network
    retries=5        # More retries untuk stability
)
```

### Issue: Cannot reach external hosts

**Symptoms:**
```
Network is unreachable
```

**Quick Fix:**
```powershell
# Test basic connectivity
ping 8.8.8.8
ping google.com

# Check network configuration
ipconfig /all
netsh interface show interface
```

**Diagnostic Script:**
```python
import netdiag

def quick_network_test():
    analyzer = netdiag.NetworkAnalyzer()
    
    # Test local
    try:
        local = analyzer.ping_host("127.0.0.1")
        print(f"✅ Local: {local.avg_latency:.1f}ms")
    except:
        print("❌ Local network failed")
    
    # Test gateway (adjust IP as needed)
    try:
        gateway = analyzer.ping_host("192.168.1.1")
        print(f"✅ Gateway: {gateway.avg_latency:.1f}ms")
    except:
        print("❌ Gateway unreachable")
    
    # Test external
    try:
        external = analyzer.ping_host("8.8.8.8")
        print(f"✅ External: {external.avg_latency:.1f}ms")
    except:
        print("❌ External network failed")

quick_network_test()
```

### Issue: High packet loss

**Symptoms:**
```
Packet loss: 50.0%
```

**Quick Fix:**
```python
# Test dengan different settings
analyzer = netdiag.NetworkAnalyzer()

# Try smaller packets
result1 = analyzer.ping_host("target.com", packet_size=32)

# Try more frequent pings
result2 = analyzer.ping_host("target.com", count=10)

print(f"Small packets: {result1.packet_loss:.1f}% loss")
print(f"More pings: {result2.packet_loss:.1f}% loss")
```

---

## Permission Issues

### Issue: Administrator privileges required

**Symptoms:**
```
PermissionError: Operation requires elevation
```

**Quick Fix:**
```powershell
# Run PowerShell as Administrator
# Right-click PowerShell → "Run as administrator"

# Check admin status
whoami /groups | findstr "S-1-5-32-544"
```

**Alternative for Students:**
```python
# Use limited functionality mode
import netdiag

# Some operations may work without admin rights
analyzer = netdiag.NetworkAnalyzer()
try:
    result = analyzer.ping_host("google.com")
    print("✅ Basic ping works without admin")
except PermissionError:
    print("❌ This operation requires administrator privileges")
```

### Issue: Windows Defender blocking

**Symptoms:**
```
Windows Defender has blocked this operation
```

**Quick Fix:**
```powershell
# Add exception untuk Python (as Administrator)
# Windows Defender → Virus & threat protection → Exclusions → Add exclusion

# Temporary: Allow through firewall
netsh advfirewall firewall add rule name="Python NetDiag" dir=out action=allow program="C:\Python39\python.exe"
```

---

## DNS Issues

### Issue: Cannot resolve hostnames

**Symptoms:**
```
socket.gaierror: [Errno 11001] getaddrinfo failed
```

**Quick Fix:**
```powershell
# Test DNS resolution
nslookup google.com
nslookup polinela.ac.id

# Flush DNS cache
ipconfig /flushdns

# Check DNS servers
ipconfig /all | findstr "DNS"
```

**Alternative DNS Test:**
```python
import socket

def test_dns():
    hosts = ["google.com", "polinela.ac.id", "github.com"]
    
    for host in hosts:
        try:
            ip = socket.gethostbyname(host)
            print(f"✅ {host} → {ip}")
        except socket.gaierror:
            print(f"❌ {host} → DNS failed")

test_dns()
```

### Issue: Slow DNS resolution

**Symptoms:**
Very slow hostname resolution

**Quick Fix:**
```python
# Use IP addresses instead of hostnames
import netdiag

analyzer = netdiag.NetworkAnalyzer()

# Instead of: analyzer.ping_host("google.com")
# Use: analyzer.ping_host("8.8.8.8")

# Test DNS performance
import time
start = time.time()
ip = socket.gethostbyname("google.com")
dns_time = time.time() - start
print(f"DNS resolution took: {dns_time:.3f} seconds")
```

---

## Firewall Issues

### Issue: Windows Firewall blocking connections

**Symptoms:**
```
Connection blocked by firewall
```

**Quick Fix:**
```powershell
# Check firewall status
netsh advfirewall show allprofiles state

# Allow specific application (as Administrator)
netsh advfirewall firewall add rule name="NetDiag" dir=out action=allow program="python.exe"

# Alternative: Check firewall logs
netsh advfirewall show currentprofile logging
```

### Issue: Campus firewall restrictions

**Symptoms:**
Cannot access external network resources

**Campus Network Solution:**
```python
# Test which services are available
import socket

def test_campus_ports():
    """Test common ports dalam campus environment."""
    
    test_ports = [
        (80, "HTTP"),
        (443, "HTTPS"),
        (53, "DNS"), 
        (22, "SSH"),
        (21, "FTP")
    ]
    
    host = "google.com"
    
    for port, service in test_ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        
        try:
            result = sock.connect_ex((host, port))
            if result == 0:
                print(f"✅ {service} (port {port}) - Available")
            else:
                print(f"❌ {service} (port {port}) - Blocked")
        except Exception as e:
            print(f"❌ {service} (port {port}) - Error: {e}")
        finally:
            sock.close()

test_campus_ports()
```

---

## Performance Issues

### Issue: Very slow operations

**Symptoms:**
NetDiag operations take very long time

**Quick Fix:**
```python
# Reduce timeout dan retries
import netdiag

analyzer = netdiag.NetworkAnalyzer(
    timeout=3,       # Faster timeout
    retries=1        # Fewer retries
)

# Test dengan minimal settings
result = analyzer.ping_host("google.com", count=1)
```

### Issue: High memory usage

**Symptoms:**
Python process uses too much memory

**Quick Fix:**
```python
# Monitor memory usage
import psutil
import netdiag

process = psutil.Process()
print(f"Initial memory: {process.memory_info().rss / 1024 / 1024:.1f} MB")

# Use analyzer efficiently
analyzer = netdiag.NetworkAnalyzer()
result = analyzer.ping_host("google.com")

print(f"After ping: {process.memory_info().rss / 1024 / 1024:.1f} MB")

# Clean up
del analyzer
import gc
gc.collect()
```

### Issue: CPU usage too high

**Symptoms:**
Python process uses 100% CPU

**Quick Fix:**
```python
# Add delays between operations
import time
import netdiag

analyzer = netdiag.NetworkAnalyzer()

hosts = ["google.com", "github.com", "stackoverflow.com"]

for host in hosts:
    result = analyzer.ping_host(host)
    print(f"{host}: {result.avg_latency:.1f}ms")
    
    # Add small delay untuk reduce CPU usage
    time.sleep(0.1)
```

---

## Educational Issues

### Issue: Lab exercise not working

**Symptoms:**
Cannot complete assigned lab exercise

**Quick Check:**
```python
# Verify lab environment
import netdiag
import sys

def lab_environment_check():
    print("🧪 Lab Environment Check")
    print("=" * 30)
    
    # Check Python version
    print(f"Python version: {sys.version}")
    
    # Check NetDiag installation
    try:
        analyzer = netdiag.NetworkAnalyzer()
        print("✅ NetDiag imported successfully")
    except ImportError:
        print("❌ NetDiag not available")
        return False
    
    # Test basic functionality
    try:
        result = analyzer.ping_host("127.0.0.1", count=1)
        print(f"✅ Basic ping: {result.avg_latency:.1f}ms")
    except Exception as e:
        print(f"❌ Basic ping failed: {e}")
        return False
    
    # Test campus connectivity
    try:
        result = analyzer.ping_host("polinela.ac.id", count=1)
        print(f"✅ Campus access: {result.avg_latency:.1f}ms")
    except Exception as e:
        print(f"⚠️ Campus access issue: {e}")
    
    print("✅ Lab environment ready")
    return True

lab_environment_check()
```

### Issue: Assignment code not working

**Symptoms:**
Student's assignment code produces errors

**Common Student Errors:**
```python
# ❌ Common mistake 1: No error handling
def bad_ping_function(host):
    analyzer = netdiag.NetworkAnalyzer()
    return analyzer.ping_host(host)  # Can raise exception

# ✅ Better version dengan error handling
def good_ping_function(host):
    try:
        analyzer = netdiag.NetworkAnalyzer()
        return analyzer.ping_host(host)
    except Exception as e:
        print(f"Error pinging {host}: {e}")
        return None

# ❌ Common mistake 2: Wrong parameter types
def bad_multiple_ping(hosts):
    analyzer = netdiag.NetworkAnalyzer()
    for host in hosts:
        result = analyzer.ping_host(host, count="5")  # String instead of int

# ✅ Better version dengan validation
def good_multiple_ping(hosts):
    if not isinstance(hosts, list):
        print("Hosts must be a list")
        return
    
    analyzer = netdiag.NetworkAnalyzer()
    results = []
    
    for host in hosts:
        try:
            result = analyzer.ping_host(host, count=5)  # Proper int
            results.append(result)
        except Exception as e:
            print(f"Failed to ping {host}: {e}")
    
    return results
```

### Issue: Cannot understand error messages

**Symptoms:**
Error messages are confusing

**Common Error Explanations:**

1. **`TimeoutError`**: Network operation took too long
   - **Fix**: Increase timeout atau check network connection

2. **`PermissionError`**: Need administrator privileges
   - **Fix**: Run as administrator atau use limited functions

3. **`socket.gaierror`**: Cannot resolve hostname
   - **Fix**: Check DNS settings atau use IP address

4. **`ImportError`**: Module not found
   - **Fix**: Install missing package dengan pip

5. **`ValueError`**: Invalid parameter
   - **Fix**: Check parameter types dan values

---

## Emergency Quick Fixes

### Complete Network Reset (Windows)

```powershell
# Run as Administrator
netsh winsock reset
netsh int ip reset
ipconfig /release
ipconfig /renew
ipconfig /flushdns

# Restart computer if needed
```

### Fresh Python Environment

```powershell
# Deactivate current environment
deactivate

# Remove old environment
rmdir /s netdiag_env

# Create fresh environment
python -m venv netdiag_env
netdiag_env\Scripts\activate
pip install --upgrade pip
pip install netdiag
```

### Emergency Network Test

```python
import subprocess
import sys

def emergency_test():
    """Emergency connectivity test using system commands."""
    
    # Test 1: Basic ping
    try:
        result = subprocess.run(['ping', '-n', '1', '8.8.8.8'], 
                              capture_output=True, text=True)
        if "TTL=" in result.stdout:
            print("✅ Internet connectivity working")
        else:
            print("❌ Internet connectivity failed")
    except:
        print("❌ Cannot run ping command")
    
    # Test 2: Campus connectivity
    try:
        result = subprocess.run(['ping', '-n', '1', 'polinela.ac.id'], 
                              capture_output=True, text=True)
        if "TTL=" in result.stdout:
            print("✅ Campus connectivity working")
        else:
            print("❌ Campus connectivity failed")
    except:
        print("❌ Cannot test campus connectivity")

emergency_test()
```

---

## Getting Help

### When All Else Fails

1. **Check system logs**: Windows Event Viewer → Windows Logs → System
2. **Contact IT support**: Campus network issues
3. **Ask instructor**: Assignment-specific problems
4. **Use study groups**: Collaborative problem solving
5. **Online resources**: Python documentation, Stack Overflow

### Creating Bug Reports

Include this information:

```python
def create_bug_report():
    """Generate information untuk bug reports."""
    
    import sys
    import platform
    import netdiag
    
    print("Bug Report Information:")
    print(f"Python: {sys.version}")
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"NetDiag: {getattr(netdiag, '__version__', 'Unknown')}")
    
    # Test basic functionality
    try:
        analyzer = netdiag.NetworkAnalyzer()
        result = analyzer.ping_host("8.8.8.8", count=1)
        print(f"Basic test: SUCCESS ({result.avg_latency:.1f}ms)")
    except Exception as e:
        print(f"Basic test: FAILED - {e}")

create_bug_report()
```

This reference guide provides immediate solutions untuk most common issues encountered dalam campus environment. Keep this handy untuk quick troubleshooting during lab sessions atau assignments!