# Netdiag - Network Diagnostics Toolkit
# Library untuk diagnosa jaringan menggunakan modul bawaan Python

__version__ = "1.1.0"
__author__ = "Netdiag Developer"
__description__ = "Network Diagnostics Toolkit for educational purposes"

# Import semua fungsi utama agar bisa diakses langsung dari package
from .ping import ping
from .traceroute import traceroute
from .iputils import get_local_ip, get_public_ip, get_ip_info
from .portscan import scan_ports, scan_common_ports
from .dnslookup import dns_lookup, reverse_dns_lookup, dns_bulk_lookup
from .speedtest import bandwidth_test, ping_latency_test, connection_quality_test
from .interfaces import get_network_interfaces, get_default_gateway, analyze_network_config
from .export import export_results, create_logger, batch_export

# Daftar fungsi yang akan di-export
__all__ = [
    # Core functions
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
    'batch_export'
]