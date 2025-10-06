"""
Netdiag - Network Diagnostics Toolkit v1.1.0

Library Python untuk diagnosa jaringan yang dirancang khusus untuk keperluan edukasi 
mahasiswa jurusan Teknologi Rekayasa Internet. Menggunakan clean code architecture
dan best practices untuk memberikan pembelajaran yang berkualitas.

Features:
- Network connectivity testing (ping, traceroute)
- Port scanning dan service discovery  
- DNS resolution dan reverse lookup
- Network interface discovery
- Bandwidth dan latency testing
- Export results dalam berbagai format
- Comprehensive error handling
- Type hints dan documentation

Author: Netdiag Developer Team
License: MIT
Version: 1.1.0
"""

__version__ = "1.1.0"
__author__ = "Netdiag Developer Team"
__description__ = "Network Diagnostics Toolkit for educational purposes"
__license__ = "MIT"

# Import exceptions untuk public API
from .exceptions import (
    NetdiagError,
    NetworkError, 
    HostResolutionError,
    ConnectionTimeoutError,
    PortScanError,
    DNSError,
    ValidationError,
    ExportError,
    SpeedTestError
)

# Import models untuk advanced usage
from .models import (
    NetworkResult,
    PingResult,
    TracerouteResult, 
    PortScanResult,
    DNSResult,
    SpeedTestResult,
    NetworkInterfaceResult,
    ExportResult
)

# Import utilities untuk helper functions
from .utils import (
    validate_hostname,
    validate_port,
    validate_port_range,
    validate_timeout,
    validate_count,
    resolve_hostname,
    format_duration,
    is_private_ip,
    get_common_ports
)

# Import main functions - Core Features
from .ping import ping, get_ping_statistics, calculate_ping_quality_score
from .traceroute import traceroute
from .iputils import get_local_ip, get_public_ip, get_ip_info
from .portscan import scan_ports, scan_common_ports
from .dnslookup import dns_lookup, reverse_dns_lookup, dns_bulk_lookup

# Import enhanced functions - v1.1.0 Features
from .speedtest import bandwidth_test, ping_latency_test, connection_quality_test
from .interfaces import get_network_interfaces, get_default_gateway, analyze_network_config
from .export import export_results, create_logger, batch_export

# Import modern Python 3.7+ features
from .modern_features import (
    NetworkConfiguration,
    EnhancedNetworkResult,
    NetworkTimeoutError,
    create_network_result_factory,
    demonstrate_modern_features
)

# Public API - daftar fungsi yang tersedia untuk import
__all__ = [
    # Core network functions
    'ping',
    'traceroute', 
    'get_local_ip',
    'get_public_ip',
    'scan_ports',
    'dns_lookup',
    
    # Enhanced functions (v1.1.0)
    'get_ip_info',
    'scan_common_ports',
    'reverse_dns_lookup',
    'dns_bulk_lookup',
    'bandwidth_test',
    'ping_latency_test',
    'connection_quality_test',
    'get_network_interfaces',
    'get_default_gateway',
    'analyze_network_config',
    'export_results',
    'create_logger',
    'batch_export',
    
    # Additional utility functions
    'get_ping_statistics',
    'calculate_ping_quality_score',
    
    # Validation utilities
    'validate_hostname',
    'validate_port',
    'validate_port_range', 
    'validate_timeout',
    'validate_count',
    'resolve_hostname',
    'format_duration',
    'is_private_ip',
    'get_common_ports',
    
    # Exception classes
    'NetdiagError',
    'NetworkError',
    'HostResolutionError', 
    'ConnectionTimeoutError',
    'PortScanError',
    'DNSError',
    'ValidationError',
    'ExportError',
    'SpeedTestError',
    
    # Data models
    'NetworkResult',
    'PingResult',
    'TracerouteResult',
    'PortScanResult', 
    'DNSResult',
    'SpeedTestResult',
    'NetworkInterfaceResult',
    'ExportResult',
    
    # Modern Python 3.7+ features
    'NetworkConfiguration',
    'EnhancedNetworkResult',
    'NetworkTimeoutError',
    'create_network_result_factory',
    'demonstrate_modern_features'
]


def get_version() -> str:
    """Get current netdiag version."""
    return __version__


def get_available_functions() -> list:
    """Get list of all available functions."""
    return __all__


def quick_network_test(host: str = "8.8.8.8") -> dict:
    """
    Quick network connectivity test untuk troubleshooting.
    
    Args:
        host: Target host untuk testing (default: Google DNS)
        
    Returns:
        Dictionary dengan hasil quick test
    """
    try:
        # Quick ping test
        ping_result = ping(host, count=3, timeout=5)
        
        # DNS test  
        dns_result = dns_lookup(host)
        
        # Local network info
        local_ip = get_local_ip()
        
        return {
            'success': True,
            'host': host,
            'ping': ping_result,
            'dns': dns_result, 
            'local_ip': local_ip,
            'summary': {
                'connectivity': 'OK' if ping_result['success'] else 'FAILED',
                'dns_resolution': 'OK' if dns_result['success'] else 'FAILED',
                'local_network': 'OK' if local_ip['success'] else 'FAILED'
            }
        }
    except Exception as e:
        return {
            'success': False,
            'error': f"Quick test failed: {str(e)}",
            'host': host
        }


# Package initialization check
def _verify_installation():
    """Verify that package is properly installed."""
    try:
        # Test core imports
        from . import ping, traceroute, iputils, portscan, dnslookup
        from . import speedtest, interfaces, export
        return True
    except ImportError as e:
        print(f"⚠️  Warning: Some netdiag modules may not be properly installed: {e}")
        return False


# Run installation check on import
if not _verify_installation():
    print("🔧 Some features may not be available. Please check your installation.")
    
print(f"🚀 Netdiag v{__version__} loaded successfully!")
print(f"📚 {len(__all__)} functions available. Use help(netdiag) for more info.")