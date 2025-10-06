# ❓ Frequently Asked Questions (FAQ)

## 🚀 General Questions

### Q: What is Netdiag?
**A:** Netdiag adalah Network Diagnostics Toolkit yang dirancang khusus untuk keperluan edukasi mahasiswa Teknologi Rekayasa Internet. Library ini menggunakan Python standard library untuk memberikan pemahaman mendalam tentang networking fundamentals.

### Q: Who should use Netdiag?
**A:** 
- 🎓 **Students**: Mahasiswa yang belajar networking dan internet technology
- 👨‍🏫 **Educators**: Dosen dan instruktur networking courses
- 💻 **Developers**: Developer yang membutuhkan network diagnostic tools
- 🔍 **Network Engineers**: Professional yang butuh simple diagnostic tools

### Q: What makes Netdiag different from other tools?
**A:**
- ✅ **Educational Focus**: Designed specifically for learning
- ✅ **Clean Code**: Professional architecture with best practices
- ✅ **No Dependencies**: Uses only Python standard library
- ✅ **Cross-Platform**: Works on Windows, macOS, and Linux
- ✅ **Modern Python**: Uses Python 3.7+ features

---

## 🔧 Installation & Setup

### Q: What are the system requirements?
**A:**
- **Python**: 3.7 atau lebih baru
- **OS**: Windows, macOS, atau Linux
- **Internet**: Diperlukan untuk beberapa functions (public IP, IP info)
- **Dependencies**: Tidak ada external dependencies

### Q: How do I install Netdiag?
**A:**
```bash
# From PyPI (recommended)
pip install netdiag

# From source
git clone https://github.com/SatriaDivo/netdiag.git
cd netdiag
pip install -e .
```

### Q: Why do I get "Python 3.7+ required" error?
**A:** Netdiag v1.1.0 requires Python 3.7 or newer for modern features. Upgrade your Python:
```bash
# Check current version
python --version

# Install Python 3.7+ from python.org
# Or update using package manager
```

---

## 💻 Usage Questions

### Q: How do I get started with Netdiag?
**A:**
```python
import netdiag

# Basic ping test
result = netdiag.ping("google.com")
print(f"Ping successful: {result['success']}")

# Get available functions
help(netdiag)
```

### Q: What functions are available?
**A:** Netdiag provides 52 functions in 8 categories:
- **Ping**: ping, get_ping_statistics, calculate_ping_quality_score
- **Traceroute**: traceroute  
- **IP Utils**: get_local_ip, get_public_ip, get_ip_info
- **Port Scan**: scan_ports, scan_common_ports
- **DNS**: dns_lookup, reverse_dns_lookup, dns_bulk_lookup
- **Speed Test**: bandwidth_test, ping_latency_test, connection_quality_test
- **Interfaces**: get_network_interfaces, get_default_gateway, analyze_network_config
- **Export**: export_results, create_logger, batch_export

### Q: How do I handle errors?
**A:**
```python
from netdiag import ping, NetworkError, ValidationError

try:
    result = ping("invalid-host")
except ValidationError as e:
    print(f"Validation error: {e}")
except NetworkError as e:
    print(f"Network error: {e}")
```

---

## 🐛 Troubleshooting

### Q: Ping always returns success=False, what's wrong?
**A:** Common causes:
1. **Invalid hostname**: Check hostname format
2. **Network connectivity**: Test internet connection
3. **Firewall**: May block ping packets
4. **Host unreachable**: Target may be down

```python
# Debug ping issues
result = netdiag.ping("google.com", count=1)
if not result['success']:
    print(f"Error: {result.get('error', 'Unknown')}")
    print(f"Raw output: {result.get('raw_output', 'None')}")
```

### Q: Port scanning is very slow, how to speed up?
**A:**
```python
# Use common ports instead of full range
result = netdiag.scan_common_ports("target-host")

# Or specify smaller range
result = netdiag.scan_ports("target-host", start_port=80, end_port=443)
```

### Q: Why do some functions require admin privileges?
**A:** Functions like `get_network_interfaces` may need elevated privileges on some systems for detailed information. Run as administrator if needed.

---

## 🎓 Educational Questions

### Q: How do I use Netdiag for teaching?
**A:**
1. **Start with basics**: ping, get_local_ip
2. **Progress to advanced**: traceroute, port scanning
3. **Explain results**: Show students what each field means
4. **Hands-on labs**: Create exercises using real networks
5. **Compare tools**: Show difference between netdiag and command-line tools

### Q: What networking concepts can students learn?
**A:**
- **TCP/IP Stack**: Through ping and traceroute
- **DNS Resolution**: Via dns_lookup functions
- **Port Services**: Through port scanning
- **Network Interfaces**: Using interface discovery
- **Latency & Performance**: With speed testing tools
- **Network Topology**: Via traceroute analysis

### Q: Are there lab exercises available?
**A:** Yes! Check `/docs/educational/lab_exercises.md` for:
- Basic connectivity testing
- Network discovery exercises  
- Performance analysis labs
- Troubleshooting scenarios
- Advanced network analysis

---

## 🔍 Performance Questions

### Q: How fast is Netdiag compared to command-line tools?
**A:** Netdiag performance:
- **Ping**: Comparable to system ping command
- **Port Scan**: Threading-optimized for good performance
- **DNS Lookup**: Uses system resolvers for optimal speed
- **Traceroute**: Similar to system traceroute

Performance tips:
```python
# Use profiling to monitor performance
from netdiag import profile_performance

@profile_performance
def my_network_test():
    return netdiag.ping("google.com")

# Get performance metrics
from netdiag import get_performance_summary
print(get_performance_summary())
```

### Q: Can I monitor Netdiag performance?
**A:** Yes! Netdiag includes built-in performance monitoring:
```python
# Enable profiling
from netdiag.profiler import print_performance_report

# Run your tests
netdiag.ping("google.com")
netdiag.scan_common_ports("localhost")

# View performance report
print_performance_report()
```

---

## 🔧 Advanced Usage

### Q: Can I customize result formats?
**A:**
```python
# Use modern NetworkConfiguration
from netdiag import NetworkConfiguration, EnhancedNetworkResult

config = NetworkConfiguration("example.com", port=8080)
result = EnhancedNetworkResult(True).add_tag("custom").with_metadata(source="test")
```

### Q: How do I integrate Netdiag with my application?
**A:**
```python
# Export results to different formats
from netdiag import export_results, create_logger

# Setup logging
logger = create_logger("network_tests", level="INFO")

# Run tests and export
results = [
    netdiag.ping("google.com"),
    netdiag.dns_lookup("github.com")
]

export_results(results, filename="network_report", format="json")
```

### Q: Can I extend Netdiag functionality?
**A:** Yes! Netdiag is designed to be extensible:
```python
# Create custom network test using Netdiag components
from netdiag.utils import validate_hostname
from netdiag.models import NetworkResult
from netdiag.profiler import profile_performance

@profile_performance
def custom_network_test(host):
    validated_host = validate_hostname(host)
    # Your custom logic here
    return NetworkResult(success=True, host=validated_host)
```

---

## 📞 Support Questions

### Q: Where can I get help?
**A:**
- 📧 **Email**: [satriadivop354@gmail.com](mailto:satriadivop354@gmail.com)
- 🐛 **GitHub Issues**: [Report bugs or request features](https://github.com/SatriaDivo/netdiag/issues)
- 📖 **Documentation**: Browse [docs folder](README.md)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/SatriaDivo/netdiag/discussions)

### Q: How do I report a bug?
**A:**
1. Check [existing issues](https://github.com/SatriaDivo/netdiag/issues)
2. Use [bug report template](https://github.com/SatriaDivo/netdiag/issues/new?template=bug_report.md)
3. Include system info, code sample, and error output
4. Add relevant labels and detailed description

### Q: Can I contribute to Netdiag?
**A:** Absolutely! We welcome contributions:
1. **Code**: Fix bugs, add features, improve performance
2. **Documentation**: Improve guides, add examples, fix errors
3. **Testing**: Add test cases, report issues
4. **Educational**: Create tutorials, lab exercises, examples

See [Contributing Guide](development/contributing.md) for details.

### Q: Is Netdiag suitable for production use?
**A:** Netdiag is primarily designed for **educational purposes**. For production:
- ✅ **Simple diagnostics**: Yes, it's reliable
- ⚠️ **Mission-critical**: Consider specialized tools
- ✅ **Monitoring scripts**: Good for basic monitoring
- ⚠️ **Enterprise environments**: May need additional features

---

## 🆕 Version-Specific Questions

### Q: What's new in v1.1.0?
**A:** Major improvements:
- **Python 3.7+ requirement** with modern features
- **Clean code architecture** following SOLID principles
- **Enhanced error handling** with custom exceptions
- **Performance monitoring** with built-in profiling
- **Modern type hints** using built-in collections
- **52 total functions** (increased from 47)

### Q: Is v1.1.0 backward compatible?
**A:**
- ✅ **API compatibility**: All existing code works
- ⚠️ **Python version**: Now requires 3.7+ (was 3.6+)
- ✅ **Return formats**: Same output structures
- ✅ **Function names**: No breaking changes

### Q: Should I upgrade from v1.0.0?
**A:** **Yes!** Benefits of upgrading:
- Better performance and memory efficiency
- Enhanced error messages and debugging
- Modern Python features and type safety
- Comprehensive documentation and examples
- Professional-grade architecture

---

**Still have questions? Contact us at [satriadivop354@gmail.com](mailto:satriadivop354@gmail.com)!** 📧