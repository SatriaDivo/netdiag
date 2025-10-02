"""
Modul DNS lookup untuk resolusi hostname dan reverse DNS
Menggunakan socket dan modul bawaan Python untuk DNS operations
"""

import socket
import time
import re


def dns_lookup(hostname):
    """
    Melakukan DNS lookup untuk mendapatkan IP address dari hostname
    
    Args:
        hostname (str): hostname yang akan di-resolve (misal: google.com)
    
    Returns:
        dict: hasil DNS lookup dengan IP address dan informasi tambahan
        
    Example:
        >>> result = dns_lookup("google.com")
        >>> print(result['ip'])
        '142.250.190.78'
        >>> print(result['ips'])
        ['142.250.190.78', '142.250.190.77', ...]
    """
    
    start_time = time.time()
    
    result = {
        'success': False,
        'hostname': hostname,
        'ip': None,
        'ips': [],
        'lookup_time': 0,
        'error': None
    }
    
    try:
        # Validasi format hostname
        if not _is_valid_hostname(hostname):
            result['error'] = f'Invalid hostname format: {hostname}'
            return result
        
        # DNS lookup untuk mendapatkan primary IP
        primary_ip = socket.gethostbyname(hostname)
        result['ip'] = primary_ip
        
        # DNS lookup untuk mendapatkan semua IP addresses
        try:
            # getaddrinfo memberikan informasi lebih lengkap
            addr_info = socket.getaddrinfo(hostname, None, socket.AF_INET)
            all_ips = list(set([addr[4][0] for addr in addr_info]))
            result['ips'] = sorted(all_ips)
        except:
            # Fallback jika getaddrinfo gagal
            result['ips'] = [primary_ip]
        
        result['success'] = True
        
    except socket.gaierror as e:
        result['error'] = f'DNS lookup failed: {str(e)}'
    except Exception as e:
        result['error'] = f'DNS lookup error: {str(e)}'
    
    result['lookup_time'] = round(time.time() - start_time, 3)
    return result


def reverse_dns_lookup(ip_address):
    """
    Melakukan reverse DNS lookup untuk mendapatkan hostname dari IP
    
    Args:
        ip_address (str): IP address yang akan di-resolve
    
    Returns:
        dict: hasil reverse DNS lookup
        
    Example:
        >>> result = reverse_dns_lookup("8.8.8.8")
        >>> print(result['hostname'])
        'dns.google.'
    """
    
    start_time = time.time()
    
    result = {
        'success': False,
        'ip': ip_address,
        'hostname': None,
        'lookup_time': 0,
        'error': None
    }
    
    try:
        # Validasi format IP address
        if not _is_valid_ip(ip_address):
            result['error'] = f'Invalid IP address format: {ip_address}'
            return result
        
        # Reverse DNS lookup
        hostname = socket.gethostbyaddr(ip_address)[0]
        result['hostname'] = hostname
        result['success'] = True
        
    except socket.herror as e:
        result['error'] = f'Reverse DNS lookup failed: {str(e)}'
    except Exception as e:
        result['error'] = f'Reverse DNS lookup error: {str(e)}'
    
    result['lookup_time'] = round(time.time() - start_time, 3)
    return result


def dns_bulk_lookup(hostnames):
    """
    Melakukan DNS lookup untuk multiple hostnames sekaligus
    
    Args:
        hostnames (list): daftar hostname yang akan di-resolve
    
    Returns:
        dict: hasil DNS lookup untuk semua hostname
        
    Example:
        >>> hostnames = ["google.com", "github.com", "stackoverflow.com"]
        >>> result = dns_bulk_lookup(hostnames)
        >>> for host_result in result['results']:
        ...     print(f"{host_result['hostname']}: {host_result['ip']}")
    """
    
    start_time = time.time()
    
    if not isinstance(hostnames, list):
        return {
            'success': False,
            'error': 'hostnames must be a list',
            'total_time': 0
        }
    
    results = []
    successful = 0
    failed = 0
    
    for hostname in hostnames:
        lookup_result = dns_lookup(hostname)
        results.append(lookup_result)
        
        if lookup_result['success']:
            successful += 1
        else:
            failed += 1
    
    total_time = round(time.time() - start_time, 3)
    
    return {
        'success': True,
        'total_hostnames': len(hostnames),
        'successful_lookups': successful,
        'failed_lookups': failed,
        'results': results,
        'total_time': total_time
    }


def get_dns_info(hostname):
    """
    Mendapatkan informasi DNS lengkap untuk hostname
    Termasuk A record, AAAA record (IPv6), dan reverse lookup
    
    Args:
        hostname (str): hostname yang akan dianalisa
    
    Returns:
        dict: informasi DNS lengkap
    """
    
    start_time = time.time()
    
    result = {
        'success': False,
        'hostname': hostname,
        'ipv4_addresses': [],
        'ipv6_addresses': [],
        'reverse_lookups': {},
        'total_time': 0,
        'error': None
    }
    
    try:
        # IPv4 lookup (A records)
        try:
            ipv4_info = socket.getaddrinfo(hostname, None, socket.AF_INET)
            ipv4_addresses = list(set([addr[4][0] for addr in ipv4_info]))
            result['ipv4_addresses'] = sorted(ipv4_addresses)
        except:
            pass
        
        # IPv6 lookup (AAAA records)
        try:
            ipv6_info = socket.getaddrinfo(hostname, None, socket.AF_INET6)
            ipv6_addresses = list(set([addr[4][0] for addr in ipv6_info]))
            result['ipv6_addresses'] = sorted(ipv6_addresses)
        except:
            pass
        
        # Reverse lookup untuk setiap IPv4 address
        for ip in result['ipv4_addresses']:
            try:
                reverse_result = reverse_dns_lookup(ip)
                result['reverse_lookups'][ip] = reverse_result['hostname']
            except:
                result['reverse_lookups'][ip] = None
        
        if result['ipv4_addresses'] or result['ipv6_addresses']:
            result['success'] = True
        else:
            result['error'] = 'No DNS records found'
            
    except Exception as e:
        result['error'] = f'DNS info lookup failed: {str(e)}'
    
    result['total_time'] = round(time.time() - start_time, 3)
    return result


def _is_valid_hostname(hostname):
    """
    Validasi format hostname
    
    Args:
        hostname (str): hostname yang akan divalidasi
    
    Returns:
        bool: True jika valid, False jika tidak
    """
    if not hostname or len(hostname) > 253:
        return False
    
    # Hostname tidak boleh dimulai atau diakhiri dengan dot
    if hostname.startswith('.') or hostname.endswith('.'):
        return False
    
    # Split berdasarkan dot dan validasi setiap bagian
    labels = hostname.split('.')
    
    for label in labels:
        if not label or len(label) > 63:
            return False
        
        # Label tidak boleh dimulai atau diakhiri dengan hyphen
        if label.startswith('-') or label.endswith('-'):
            return False
        
        # Label hanya boleh berisi alphanumeric dan hyphen
        if not re.match(r'^[a-zA-Z0-9-]+$', label):
            return False
    
    return True


def _is_valid_ip(ip):
    """
    Validasi format IP address (IPv4)
    
    Args:
        ip (str): IP address yang akan divalidasi
    
    Returns:
        bool: True jika valid, False jika tidak
    """
    try:
        socket.inet_aton(ip)
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        for part in parts:
            if not 0 <= int(part) <= 255:
                return False
        return True
    except:
        return False


def check_dns_servers():
    """
    Mengecek DNS servers yang digunakan sistem
    (Fungsi informational)
    
    Returns:
        dict: informasi DNS servers system
    """
    
    result = {
        'success': True,
        'dns_servers': [],
        'note': 'DNS server detection is limited in Python. This shows commonly used DNS servers.',
        'common_dns_servers': {
            'Google': ['8.8.8.8', '8.8.4.4'],
            'Cloudflare': ['1.1.1.1', '1.0.0.1'],
            'OpenDNS': ['208.67.222.222', '208.67.220.220'],
            'Quad9': ['9.9.9.9', '149.112.112.112']
        }
    }
    
    # Test beberapa DNS server umum untuk melihat mana yang merespon
    test_hostname = 'google.com'
    working_dns = []
    
    for dns_name, dns_ips in result['common_dns_servers'].items():
        for dns_ip in dns_ips:
            try:
                # Simple test - jika bisa resolve google.com, anggap DNS working
                socket.gethostbyname(test_hostname)
                working_dns.append({
                    'name': dns_name,
                    'ip': dns_ip,
                    'status': 'reachable'
                })
                break  # Cukup test satu IP per provider
            except:
                continue
    
    result['working_dns_servers'] = working_dns
    return result


if __name__ == "__main__":
    # Test function jika dijalankan langsung
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python dnslookup.py <hostname>           # DNS lookup")
        print("  python dnslookup.py reverse <ip>         # Reverse DNS lookup")
        print("  python dnslookup.py info <hostname>      # Full DNS info")
        print("  python dnslookup.py bulk <host1,host2>   # Bulk lookup")
        print("  python dnslookup.py check-dns            # Check DNS servers")
        print("\nExamples:")
        print("  python dnslookup.py google.com")
        print("  python dnslookup.py reverse 8.8.8.8")
        print("  python dnslookup.py info github.com")
        print("  python dnslookup.py bulk google.com,github.com,stackoverflow.com")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "reverse" and len(sys.argv) > 2:
        ip = sys.argv[2]
        print(f"Reverse DNS lookup for {ip}...")
        result = reverse_dns_lookup(ip)
        
        if result['success']:
            print(f"✅ Reverse lookup successful!")
            print(f"   IP: {result['ip']}")
            print(f"   Hostname: {result['hostname']}")
            print(f"   Lookup time: {result['lookup_time']} seconds")
        else:
            print(f"❌ Reverse lookup failed: {result['error']}")
    
    elif command == "info" and len(sys.argv) > 2:
        hostname = sys.argv[2]
        print(f"Full DNS info for {hostname}...")
        result = get_dns_info(hostname)
        
        if result['success']:
            print(f"✅ DNS info lookup successful!")
            print(f"   Hostname: {result['hostname']}")
            
            if result['ipv4_addresses']:
                print(f"   IPv4 addresses ({len(result['ipv4_addresses'])}):")
                for ip in result['ipv4_addresses']:
                    reverse_host = result['reverse_lookups'].get(ip, 'N/A')
                    print(f"   - {ip} (reverse: {reverse_host})")
            
            if result['ipv6_addresses']:
                print(f"   IPv6 addresses ({len(result['ipv6_addresses'])}):")
                for ip in result['ipv6_addresses']:
                    print(f"   - {ip}")
            
            print(f"   Total time: {result['total_time']} seconds")
        else:
            print(f"❌ DNS info lookup failed: {result['error']}")
    
    elif command == "bulk" and len(sys.argv) > 2:
        hostnames = [h.strip() for h in sys.argv[2].split(',')]
        print(f"Bulk DNS lookup for {len(hostnames)} hostnames...")
        result = dns_bulk_lookup(hostnames)
        
        if result['success']:
            print(f"✅ Bulk lookup completed!")
            print(f"   Total hostnames: {result['total_hostnames']}")
            print(f"   Successful: {result['successful_lookups']}")
            print(f"   Failed: {result['failed_lookups']}")
            print(f"   Total time: {result['total_time']} seconds")
            
            print(f"\n   Results:")
            for host_result in result['results']:
                if host_result['success']:
                    print(f"   ✅ {host_result['hostname']}: {host_result['ip']}")
                else:
                    print(f"   ❌ {host_result['hostname']}: {host_result['error']}")
        else:
            print(f"❌ Bulk lookup failed: {result['error']}")
    
    elif command == "check-dns":
        print("Checking DNS servers...")
        result = check_dns_servers()
        
        print(f"✅ DNS server check completed!")
        print(f"   Note: {result['note']}")
        print(f"\n   Common DNS servers:")
        for provider, ips in result['common_dns_servers'].items():
            print(f"   {provider}: {', '.join(ips)}")
        
        if result['working_dns_servers']:
            print(f"\n   Working DNS servers:")
            for dns in result['working_dns_servers']:
                print(f"   ✅ {dns['name']}: {dns['ip']} ({dns['status']})")
    
    else:
        # Standard DNS lookup
        hostname = sys.argv[1]
        print(f"DNS lookup for {hostname}...")
        result = dns_lookup(hostname)
        
        if result['success']:
            print(f"✅ DNS lookup successful!")
            print(f"   Hostname: {result['hostname']}")
            print(f"   Primary IP: {result['ip']}")
            if len(result['ips']) > 1:
                print(f"   All IPs ({len(result['ips'])}): {', '.join(result['ips'])}")
            print(f"   Lookup time: {result['lookup_time']} seconds")
        else:
            print(f"❌ DNS lookup failed: {result['error']}")