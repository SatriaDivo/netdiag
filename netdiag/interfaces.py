"""
Modul network interfaces untuk mendapatkan informasi interface jaringan
Menggunakan socket dan platform-specific commands untuk menganalisis interface
"""

import socket
import subprocess
import platform
import re
import json


def get_network_interfaces():
    """
    Mendapatkan daftar semua network interfaces yang tersedia
    
    Returns:
        dict: informasi lengkap tentang network interfaces
        
    Example:
        >>> result = get_network_interfaces()
        >>> for interface in result['interfaces']:
        ...     print(f"{interface['name']}: {interface['ip']}")
    """
    
    system = platform.system().lower()
    
    result = {
        'success': False,
        'system': system,
        'interfaces': [],
        'active_interfaces': [],
        'total_interfaces': 0,
        'error': None
    }
    
    try:
        if system == 'windows':
            interfaces = _get_windows_interfaces()
        else:
            interfaces = _get_unix_interfaces()
        
        # Filter dan kategorikan interfaces
        active_interfaces = []
        for interface in interfaces:
            if interface.get('status') == 'up' and interface.get('ip') and interface['ip'] != '127.0.0.1':
                active_interfaces.append(interface)
        
        result.update({
            'success': True,
            'interfaces': interfaces,
            'active_interfaces': active_interfaces,
            'total_interfaces': len(interfaces)
        })
        
    except Exception as e:
        result['error'] = f'Failed to get network interfaces: {str(e)}'
    
    return result


def _get_windows_interfaces():
    """Mendapatkan network interfaces di Windows"""
    interfaces = []
    
    try:
        # Gunakan ipconfig untuk mendapatkan interface info
        result = subprocess.run(['ipconfig', '/all'], capture_output=True, text=True, encoding='cp1252')
        output = result.stdout
        
        # Parse output ipconfig
        current_interface = None
        
        for line in output.split('\n'):
            line = line.strip()
            
            # Deteksi interface baru
            if 'adapter' in line.lower() and ':' in line:
                if current_interface:
                    interfaces.append(current_interface)
                
                # Extract interface name
                adapter_match = re.search(r'adapter (.+?):', line)
                if adapter_match:
                    interface_name = adapter_match.group(1).strip()
                    current_interface = {
                        'name': interface_name,
                        'ip': None,
                        'mac': None,
                        'status': 'unknown',
                        'type': _guess_interface_type(interface_name),
                        'dhcp': False,
                        'dns_servers': []
                    }
            
            elif current_interface:
                # Parse informasi interface
                if 'Physical Address' in line or 'Alamat Fisik' in line:
                    mac_match = re.search(r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})', line)
                    if mac_match:
                        current_interface['mac'] = mac_match.group(0)
                
                elif 'IPv4 Address' in line or 'Alamat IPv4' in line:
                    ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                    if ip_match:
                        current_interface['ip'] = ip_match.group(1)
                        current_interface['status'] = 'up'
                
                elif 'DHCP Enabled' in line or 'DHCP Diaktifkan' in line:
                    if 'Yes' in line or 'Ya' in line:
                        current_interface['dhcp'] = True
                
                elif 'DNS Servers' in line or 'Server DNS' in line:
                    dns_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                    if dns_match:
                        current_interface['dns_servers'].append(dns_match.group(1))
        
        # Tambahkan interface terakhir
        if current_interface:
            interfaces.append(current_interface)
            
    except Exception as e:
        # Fallback: gunakan socket untuk minimal info
        hostname = socket.gethostname()
        try:
            ip = socket.gethostbyname(hostname)
            interfaces.append({
                'name': 'Default',
                'ip': ip,
                'mac': None,
                'status': 'up',
                'type': 'unknown',
                'dhcp': False,
                'dns_servers': []
            })
        except:
            pass
    
    return interfaces


def _get_unix_interfaces():
    """Mendapatkan network interfaces di Linux/Mac"""
    interfaces = []
    
    try:
        # Coba gunakan ip command (Linux modern)
        result = subprocess.run(['ip', 'addr', 'show'], capture_output=True, text=True)
        
        if result.returncode == 0:
            interfaces = _parse_ip_command_output(result.stdout)
        else:
            # Fallback ke ifconfig
            result = subprocess.run(['ifconfig', '-a'], capture_output=True, text=True)
            if result.returncode == 0:
                interfaces = _parse_ifconfig_output(result.stdout)
                
    except FileNotFoundError:
        # Jika ip/ifconfig tidak tersedia, gunakan socket fallback
        try:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            interfaces.append({
                'name': 'Default',
                'ip': ip,
                'mac': None,
                'status': 'up',
                'type': 'unknown',
                'dhcp': False,
                'dns_servers': []
            })
        except:
            pass
    
    return interfaces


def _parse_ip_command_output(output):
    """Parse output dari 'ip addr show' command"""
    interfaces = []
    current_interface = None
    
    for line in output.split('\n'):
        line = line.strip()
        
        # Interface line: "2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500"
        interface_match = re.match(r'\d+:\s+([^:]+):\s+<([^>]+)>', line)
        if interface_match:
            if current_interface:
                interfaces.append(current_interface)
            
            interface_name = interface_match.group(1)
            flags = interface_match.group(2)
            
            current_interface = {
                'name': interface_name,
                'ip': None,
                'mac': None,
                'status': 'up' if 'UP' in flags else 'down',
                'type': _guess_interface_type(interface_name),
                'dhcp': False,
                'dns_servers': []
            }
        
        elif current_interface:
            # MAC address line: "link/ether 08:00:27:3c:2f:4e brd ff:ff:ff:ff:ff:ff"
            mac_match = re.search(r'link/ether\s+([0-9a-f:]{17})', line)
            if mac_match:
                current_interface['mac'] = mac_match.group(1)
            
            # IP address line: "inet 192.168.1.100/24 brd 192.168.1.255 scope global eth0"
            ip_match = re.search(r'inet\s+(\d+\.\d+\.\d+\.\d+)', line)
            if ip_match and not current_interface['ip']:  # Ambil IP pertama saja
                current_interface['ip'] = ip_match.group(1)
    
    if current_interface:
        interfaces.append(current_interface)
    
    return interfaces


def _parse_ifconfig_output(output):
    """Parse output dari 'ifconfig -a' command"""
    interfaces = []
    current_interface = None
    
    for line in output.split('\n'):
        # Interface line biasanya dimulai dengan nama interface
        if not line.startswith(' ') and not line.startswith('\t') and ':' not in line and line.strip():
            if current_interface:
                interfaces.append(current_interface)
            
            interface_name = line.split()[0]
            current_interface = {
                'name': interface_name,
                'ip': None,
                'mac': None,
                'status': 'up' if 'UP' in line else 'down',
                'type': _guess_interface_type(interface_name),
                'dhcp': False,
                'dns_servers': []
            }
        
        elif current_interface and line.strip():
            # MAC address (ether)
            mac_match = re.search(r'ether\s+([0-9a-f:]{17})', line)
            if mac_match:
                current_interface['mac'] = mac_match.group(1)
            
            # IP address
            ip_match = re.search(r'inet\s+(\d+\.\d+\.\d+\.\d+)', line)
            if ip_match and not current_interface['ip']:
                current_interface['ip'] = ip_match.group(1)
    
    if current_interface:
        interfaces.append(current_interface)
    
    return interfaces


def _guess_interface_type(interface_name):
    """Guess tipe interface berdasarkan nama"""
    name_lower = interface_name.lower()
    
    if 'eth' in name_lower or 'lan' in name_lower:
        return 'ethernet'
    elif 'wlan' in name_lower or 'wifi' in name_lower or 'wi-fi' in name_lower:
        return 'wireless'
    elif 'lo' in name_lower or 'loopback' in name_lower:
        return 'loopback'
    elif 'tun' in name_lower or 'tap' in name_lower:
        return 'tunnel'
    elif 'ppp' in name_lower:
        return 'ppp'
    elif 'vmware' in name_lower or 'vbox' in name_lower or 'virtual' in name_lower:
        return 'virtual'
    else:
        return 'unknown'


def get_default_gateway():
    """
    Mendapatkan default gateway dari sistem
    
    Returns:
        dict: informasi default gateway
    """
    
    system = platform.system().lower()
    result = {
        'success': False,
        'gateway_ip': None,
        'interface': None,
        'error': None
    }
    
    try:
        if system == 'windows':
            # Windows: route print
            cmd_result = subprocess.run(['route', 'print', '0.0.0.0'], capture_output=True, text=True)
            output = cmd_result.stdout
            
            # Cari default route (0.0.0.0)
            for line in output.split('\n'):
                if '0.0.0.0' in line and '0.0.0.0' in line:
                    parts = line.split()
                    if len(parts) >= 3:
                        result['gateway_ip'] = parts[2]
                        result['success'] = True
                        break
        else:
            # Linux/Mac: ip route atau route
            try:
                cmd_result = subprocess.run(['ip', 'route', 'show', 'default'], capture_output=True, text=True)
                output = cmd_result.stdout
                
                # Parse: "default via 192.168.1.1 dev eth0"
                gateway_match = re.search(r'default via (\d+\.\d+\.\d+\.\d+)', output)
                if gateway_match:
                    result['gateway_ip'] = gateway_match.group(1)
                    result['success'] = True
                    
                    interface_match = re.search(r'dev (\w+)', output)
                    if interface_match:
                        result['interface'] = interface_match.group(1)
                        
            except FileNotFoundError:
                # Fallback ke route command
                cmd_result = subprocess.run(['route', '-n', 'get', 'default'], capture_output=True, text=True)
                output = cmd_result.stdout
                
                gateway_match = re.search(r'gateway:\s*(\d+\.\d+\.\d+\.\d+)', output)
                if gateway_match:
                    result['gateway_ip'] = gateway_match.group(1)
                    result['success'] = True
                    
    except Exception as e:
        result['error'] = f'Failed to get default gateway: {str(e)}'
    
    return result


def analyze_network_config():
    """
    Analisis konfigurasi jaringan lengkap
    
    Returns:
        dict: analisis lengkap konfigurasi jaringan
    """
    
    result = {
        'success': False,
        'interfaces': {},
        'gateway': {},
        'dns_info': {},
        'connectivity': {},
        'summary': {},
        'error': None
    }
    
    try:
        print("🔍 Analyzing network configuration...")
        
        # 1. Get interfaces
        print("  Getting network interfaces...")
        interfaces_result = get_network_interfaces()
        result['interfaces'] = interfaces_result
        
        # 2. Get gateway
        print("  Getting default gateway...")
        gateway_result = get_default_gateway()
        result['gateway'] = gateway_result
        
        # 3. Test DNS
        print("  Testing DNS resolution...")
        from .dnslookup import dns_lookup
        dns_test = dns_lookup('google.com')
        result['dns_info'] = dns_test
        
        # 4. Test connectivity
        print("  Testing internet connectivity...")
        from .ping import ping
        connectivity_test = ping('8.8.8.8', count=3, timeout=5)
        result['connectivity'] = connectivity_test
        
        # 5. Generate summary
        summary = _generate_network_summary(interfaces_result, gateway_result, dns_test, connectivity_test)
        result['summary'] = summary
        
        result['success'] = True
        
    except Exception as e:
        result['error'] = f'Network analysis failed: {str(e)}'
    
    return result


def _generate_network_summary(interfaces_result, gateway_result, dns_test, connectivity_test):
    """Generate ringkasan analisis jaringan"""
    
    summary = {
        'total_interfaces': 0,
        'active_interfaces': 0,
        'primary_interface': None,
        'has_gateway': False,
        'dns_working': False,
        'internet_connectivity': False,
        'issues': [],
        'recommendations': []
    }
    
    if interfaces_result['success']:
        summary['total_interfaces'] = interfaces_result['total_interfaces']
        summary['active_interfaces'] = len(interfaces_result['active_interfaces'])
        
        # Find primary interface (biasanya yang bukan loopback dan punya IP)
        for interface in interfaces_result['active_interfaces']:
            if interface['type'] != 'loopback':
                summary['primary_interface'] = interface['name']
                break
    
    if gateway_result['success']:
        summary['has_gateway'] = True
    else:
        summary['issues'].append('No default gateway found')
        summary['recommendations'].append('Check network configuration and router connection')
    
    if dns_test['success']:
        summary['dns_working'] = True
    else:
        summary['issues'].append('DNS resolution not working')
        summary['recommendations'].append('Check DNS server configuration')
    
    if connectivity_test['success']:
        summary['internet_connectivity'] = True
    else:
        summary['issues'].append('No internet connectivity')
        summary['recommendations'].append('Check internet connection and firewall settings')
    
    # Additional recommendations
    if summary['active_interfaces'] == 0:
        summary['issues'].append('No active network interfaces')
        summary['recommendations'].append('Check network adapter drivers and connections')
    elif summary['active_interfaces'] > 3:
        summary['recommendations'].append('Consider disabling unused network interfaces')
    
    return summary


if __name__ == "__main__":
    # Test functions jika dijalankan langsung
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python interfaces.py list         # List all network interfaces")
        print("  python interfaces.py gateway      # Show default gateway")
        print("  python interfaces.py analyze      # Full network analysis")
        print("\nExamples:")
        print("  python interfaces.py list")
        print("  python interfaces.py analyze")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "list":
        print("Getting network interfaces...")
        result = get_network_interfaces()
        
        if result['success']:
            print(f"✅ Found {result['total_interfaces']} network interfaces")
            print(f"   Active interfaces: {len(result['active_interfaces'])}")
            print(f"   System: {result['system']}")
            
            print(f"\n   All interfaces:")
            for interface in result['interfaces']:
                status_icon = "🟢" if interface['status'] == 'up' else "🔴"
                print(f"   {status_icon} {interface['name']} ({interface['type']})")
                if interface['ip']:
                    print(f"      IP: {interface['ip']}")
                if interface['mac']:
                    print(f"      MAC: {interface['mac']}")
                print()
        else:
            print(f"❌ Failed to get interfaces: {result['error']}")
    
    elif command == "gateway":
        print("Getting default gateway...")
        result = get_default_gateway()
        
        if result['success']:
            print(f"✅ Default gateway found!")
            print(f"   Gateway IP: {result['gateway_ip']}")
            if result['interface']:
                print(f"   Interface: {result['interface']}")
        else:
            print(f"❌ Failed to get gateway: {result['error']}")
    
    elif command == "analyze":
        print("Starting network analysis...")
        result = analyze_network_config()
        
        if result['success']:
            print(f"\n✅ Network analysis completed!")
            
            summary = result['summary']
            print(f"\n📊 Summary:")
            print(f"   Total interfaces: {summary['total_interfaces']}")
            print(f"   Active interfaces: {summary['active_interfaces']}")
            if summary['primary_interface']:
                print(f"   Primary interface: {summary['primary_interface']}")
            print(f"   Has gateway: {'✅' if summary['has_gateway'] else '❌'}")
            print(f"   DNS working: {'✅' if summary['dns_working'] else '❌'}")
            print(f"   Internet connectivity: {'✅' if summary['internet_connectivity'] else '❌'}")
            
            if summary['issues']:
                print(f"\n⚠️  Issues found:")
                for issue in summary['issues']:
                    print(f"   - {issue}")
            
            if summary['recommendations']:
                print(f"\n💡 Recommendations:")
                for rec in summary['recommendations']:
                    print(f"   - {rec}")
        else:
            print(f"❌ Network analysis failed: {result['error']}")
    
    else:
        print("❌ Unknown command")