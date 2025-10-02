"""
Modul port scanning untuk melakukan scanning TCP ports
Menggunakan socket untuk koneksi TCP ke port target
"""

import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


def scan_ports(host, start_port=1, end_port=1024, timeout=1, max_threads=100):
    """
    Melakukan TCP port scanning pada range port tertentu
    
    Args:
        host (str): hostname atau IP address target
        start_port (int): port awal untuk scanning (default: 1)
        end_port (int): port akhir untuk scanning (default: 1024)
        timeout (float): timeout koneksi dalam detik (default: 1)
        max_threads (int): maksimum jumlah thread untuk scanning (default: 100)
    
    Returns:
        dict: hasil port scanning dengan daftar port terbuka/tertutup
        
    Example:
        >>> result = scan_ports("google.com", 20, 100)
        >>> print(f"Open ports: {result['open_ports']}")
        [80, 443]
    """
    
    start_time = time.time()
    
    # Validasi input
    if start_port < 1 or start_port > 65535:
        return {
            'success': False,
            'error': 'Start port must be between 1 and 65535'
        }
    
    if end_port < 1 or end_port > 65535:
        return {
            'success': False,
            'error': 'End port must be between 1 and 65535'
        }
    
    if start_port > end_port:
        return {
            'success': False,
            'error': 'Start port cannot be greater than end port'
        }
    
    # Resolve hostname to IP
    try:
        target_ip = socket.gethostbyname(host)
    except socket.gaierror as e:
        return {
            'success': False,
            'error': f'Failed to resolve hostname {host}: {str(e)}',
            'host': host
        }
    
    result = {
        'success': False,
        'host': host,
        'target_ip': target_ip,
        'start_port': start_port,
        'end_port': end_port,
        'open_ports': [],
        'closed_ports': [],
        'filtered_ports': [],
        'total_ports_scanned': 0,
        'scan_time': 0,
        'timeout': timeout,
        'error': None
    }
    
    # Daftar port untuk di-scan
    ports_to_scan = list(range(start_port, end_port + 1))
    result['total_ports_scanned'] = len(ports_to_scan)
    
    # Batasi jumlah threads agar tidak terlalu banyak
    actual_threads = min(max_threads, len(ports_to_scan))
    
    try:
        # Gunakan ThreadPoolExecutor untuk scanning paralel
        with ThreadPoolExecutor(max_workers=actual_threads) as executor:
            # Submit tasks untuk setiap port
            future_to_port = {
                executor.submit(_scan_single_port, target_ip, port, timeout): port 
                for port in ports_to_scan
            }
            
            # Collect results
            for future in as_completed(future_to_port):
                port = future_to_port[future]
                try:
                    port_status = future.result()
                    
                    if port_status == 'open':
                        result['open_ports'].append(port)
                    elif port_status == 'closed':
                        result['closed_ports'].append(port)
                    else:  # filtered/timeout
                        result['filtered_ports'].append(port)
                        
                except Exception as e:
                    # Jika ada error pada scanning port tertentu
                    result['filtered_ports'].append(port)
        
        # Sort hasil untuk output yang rapi
        result['open_ports'].sort()
        result['closed_ports'].sort()
        result['filtered_ports'].sort()
        
        result['success'] = True
        
    except Exception as e:
        result['error'] = f'Port scanning failed: {str(e)}'
    
    result['scan_time'] = round(time.time() - start_time, 2)
    return result


def _scan_single_port(ip, port, timeout):
    """
    Scan single port dengan socket connection
    
    Args:
        ip (str): IP address target
        port (int): port number yang akan di-scan
        timeout (float): timeout untuk koneksi
    
    Returns:
        str: status port ('open', 'closed', 'filtered')
    """
    try:
        # Buat socket connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        # Coba connect ke port
        result = sock.connect_ex((ip, port))
        sock.close()
        
        if result == 0:
            return 'open'
        else:
            return 'closed'
            
    except socket.timeout:
        return 'filtered'
    except Exception:
        return 'filtered'


def scan_common_ports(host, timeout=1):
    """
    Scan port-port umum yang sering digunakan
    
    Args:
        host (str): hostname atau IP address target
        timeout (float): timeout koneksi dalam detik (default: 1)
    
    Returns:
        dict: hasil scanning port-port umum
    """
    
    # Daftar port umum dan servicenya
    common_ports = {
        21: 'FTP',
        22: 'SSH',
        23: 'Telnet',
        25: 'SMTP',
        53: 'DNS',
        80: 'HTTP',
        110: 'POP3',
        143: 'IMAP',
        443: 'HTTPS',
        993: 'IMAPS',
        995: 'POP3S',
        1433: 'MSSQL',
        3306: 'MySQL',
        3389: 'RDP',
        5432: 'PostgreSQL',
        5900: 'VNC',
        6379: 'Redis',
        8080: 'HTTP-Alt',
        8443: 'HTTPS-Alt',
        27017: 'MongoDB'
    }
    
    ports_list = list(common_ports.keys())
    
    # Gunakan fungsi scan_ports dengan port list khusus
    result = _scan_port_list(host, ports_list, timeout)
    
    if result['success']:
        # Tambahkan informasi service untuk port yang terbuka
        open_services = []
        for port in result['open_ports']:
            service = common_ports.get(port, 'Unknown')
            open_services.append({
                'port': port,
                'service': service,
                'status': 'open'
            })
        
        result['open_services'] = open_services
        result['common_ports'] = common_ports
    
    return result


def _scan_port_list(host, ports_list, timeout=1):
    """
    Scan daftar port tertentu (helper function untuk scan_common_ports)
    """
    
    start_time = time.time()
    
    # Resolve hostname to IP
    try:
        target_ip = socket.gethostbyname(host)
    except socket.gaierror as e:
        return {
            'success': False,
            'error': f'Failed to resolve hostname {host}: {str(e)}',
            'host': host
        }
    
    result = {
        'success': False,
        'host': host,
        'target_ip': target_ip,
        'open_ports': [],
        'closed_ports': [],
        'filtered_ports': [],
        'total_ports_scanned': len(ports_list),
        'scan_time': 0,
        'timeout': timeout,
        'error': None
    }
    
    try:
        # Scan setiap port dalam list
        for port in ports_list:
            port_status = _scan_single_port(target_ip, port, timeout)
            
            if port_status == 'open':
                result['open_ports'].append(port)
            elif port_status == 'closed':
                result['closed_ports'].append(port)
            else:  # filtered
                result['filtered_ports'].append(port)
        
        # Sort hasil
        result['open_ports'].sort()
        result['closed_ports'].sort()
        result['filtered_ports'].sort()
        
        result['success'] = True
        
    except Exception as e:
        result['error'] = f'Port scanning failed: {str(e)}'
    
    result['scan_time'] = round(time.time() - start_time, 2)
    return result


def get_service_name(port):
    """
    Mendapatkan nama service berdasarkan port number
    
    Args:
        port (int): port number
    
    Returns:
        str: nama service atau 'Unknown'
    """
    
    try:
        # Gunakan socket.getservbyport untuk mendapatkan service name
        service = socket.getservbyport(port, 'tcp')
        return service
    except:
        # Fallback ke daftar service umum
        common_services = {
            21: 'FTP',
            22: 'SSH',
            23: 'Telnet',
            25: 'SMTP',
            53: 'DNS',
            80: 'HTTP',
            110: 'POP3',
            143: 'IMAP',
            443: 'HTTPS',
            993: 'IMAPS',
            995: 'POP3S',
            1433: 'MSSQL',
            3306: 'MySQL',
            3389: 'RDP',
            5432: 'PostgreSQL',
            5900: 'VNC',
            6379: 'Redis',
            8080: 'HTTP-Alt',
            8443: 'HTTPS-Alt',
            27017: 'MongoDB'
        }
        
        return common_services.get(port, 'Unknown')


if __name__ == "__main__":
    # Test function jika dijalankan langsung
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python portscan.py <host> [start_port] [end_port]")
        print("  python portscan.py <host> common")
        print("\nExamples:")
        print("  python portscan.py google.com 1 100")
        print("  python portscan.py 192.168.1.1 common")
        sys.exit(1)
    
    host = sys.argv[1]
    
    if len(sys.argv) > 2 and sys.argv[2].lower() == 'common':
        # Scan common ports
        print(f"Scanning common ports on {host}...")
        result = scan_common_ports(host)
        
        if result['success']:
            print(f"✅ Port scan completed!")
            print(f"   Host: {result['host']} ({result['target_ip']})")
            print(f"   Scan time: {result['scan_time']} seconds")
            print(f"   Total ports scanned: {result['total_ports_scanned']}")
            
            if result['open_ports']:
                print(f"\n   Open ports ({len(result['open_ports'])}):")
                for service_info in result['open_services']:
                    print(f"   - {service_info['port']}/tcp ({service_info['service']})")
            else:
                print("   No open ports found")
                
            if result['filtered_ports']:
                print(f"\n   Filtered/timeout ports: {len(result['filtered_ports'])}")
        else:
            print(f"❌ Port scan failed: {result['error']}")
    
    else:
        # Range port scan
        start_port = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        end_port = int(sys.argv[3]) if len(sys.argv) > 3 else 100
        
        print(f"Scanning ports {start_port}-{end_port} on {host}...")
        result = scan_ports(host, start_port, end_port)
        
        if result['success']:
            print(f"✅ Port scan completed!")
            print(f"   Host: {result['host']} ({result['target_ip']})")
            print(f"   Port range: {result['start_port']}-{result['end_port']}")
            print(f"   Scan time: {result['scan_time']} seconds")
            print(f"   Total ports scanned: {result['total_ports_scanned']}")
            
            if result['open_ports']:
                print(f"\n   Open ports ({len(result['open_ports'])}):")
                for port in result['open_ports']:
                    service = get_service_name(port)
                    print(f"   - {port}/tcp ({service})")
            else:
                print("   No open ports found")
                
            print(f"\n   Closed ports: {len(result['closed_ports'])}")
            if result['filtered_ports']:
                print(f"   Filtered/timeout ports: {len(result['filtered_ports'])}")
        else:
            print(f"❌ Port scan failed: {result['error']}")