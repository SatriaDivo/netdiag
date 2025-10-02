"""
Modul IP utilities untuk mendapatkan informasi IP lokal dan publik
Menggunakan socket dan urllib untuk koneksi ke API eksternal
"""

import socket
import urllib.request
import urllib.error
import json
import re


def get_local_ip():
    """
    Mendapatkan IP address lokal dari interface yang aktif
    
    Returns:
        dict: informasi IP lokal
        
    Example:
        >>> result = get_local_ip()
        >>> print(result['ip'])
        '192.168.1.100'
    """
    try:
        # Metode 1: Coba connect ke remote server untuk mendapatkan local IP
        # Ini akan memberikan IP interface yang digunakan untuk koneksi keluar
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Connect ke DNS Google (tidak benar-benar mengirim data)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            
        return {
            'success': True,
            'ip': local_ip,
            'method': 'socket_connect',
            'interface': 'active_interface',
            'error': None
        }
        
    except Exception as e:
        # Metode 2: Fallback ke hostname resolution
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            
            # Validasi bahwa IP bukan localhost
            if local_ip.startswith('127.'):
                raise Exception("Got localhost IP, trying alternative method")
            
            return {
                'success': True,
                'ip': local_ip,
                'method': 'hostname_resolution',
                'hostname': hostname,
                'error': None
            }
            
        except Exception as e2:
            # Metode 3: Fallback terakhir - scan network interfaces
            try:
                local_ip = _get_ip_from_interfaces()
                if local_ip:
                    return {
                        'success': True,
                        'ip': local_ip,
                        'method': 'interface_scan',
                        'error': None
                    }
                else:
                    raise Exception("No valid IP found in interfaces")
                    
            except Exception as e3:
                return {
                    'success': False,
                    'ip': None,
                    'error': f'Failed to get local IP: {str(e3)}',
                    'attempted_methods': ['socket_connect', 'hostname_resolution', 'interface_scan']
                }


def _get_ip_from_interfaces():
    """
    Scan network interfaces untuk mencari IP yang valid
    Metode fallback jika metode lain gagal
    """
    try:
        # Untuk Windows, coba gunakan socket.getfqdn
        import platform
        if platform.system().lower() == 'windows':
            # Coba beberapa hostname variations
            possible_hosts = [
                socket.getfqdn(),
                socket.gethostname() + '.local',
                socket.gethostname()
            ]
            
            for host in possible_hosts:
                try:
                    ip = socket.gethostbyname(host)
                    if not ip.startswith('127.') and _is_valid_ip(ip):
                        return ip
                except:
                    continue
        
        return None
    except:
        return None


def _is_valid_ip(ip):
    """
    Validasi format IP address
    """
    try:
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        for part in parts:
            if not 0 <= int(part) <= 255:
                return False
        return True
    except:
        return False


def get_public_ip():
    """
    Mendapatkan IP address publik menggunakan API eksternal
    Mencoba beberapa service untuk redundancy
    
    Returns:
        dict: informasi IP publik
        
    Example:
        >>> result = get_public_ip()
        >>> print(result['ip'])
        '203.194.112.34'
    """
    # Daftar API service untuk mendapatkan IP publik
    services = [
        {
            'name': 'ipify',
            'url': 'https://api.ipify.org?format=json',
            'json_key': 'ip'
        },
        {
            'name': 'ipapi',
            'url': 'https://ipapi.co/json/',
            'json_key': 'ip'
        },
        {
            'name': 'httpbin',
            'url': 'https://httpbin.org/ip',
            'json_key': 'origin'
        },
        {
            'name': 'jsonip',
            'url': 'https://jsonip.com/',
            'json_key': 'ip'
        },
        {
            'name': 'ipify_text',
            'url': 'https://api.ipify.org',
            'json_key': None  # Plain text response
        }
    ]
    
    errors = []
    
    for service in services:
        try:
            # Buat request dengan timeout
            request = urllib.request.Request(
                service['url'],
                headers={
                    'User-Agent': 'netdiag/1.0 (Network Diagnostics Tool)'
                }
            )
            
            with urllib.request.urlopen(request, timeout=10) as response:
                data = response.read().decode('utf-8')
                
                if service['json_key']:
                    # Parse JSON response
                    json_data = json.loads(data)
                    ip = json_data.get(service['json_key'])
                else:
                    # Plain text response
                    ip = data.strip()
                
                # Validasi IP address
                if ip and _is_valid_ip(ip):
                    return {
                        'success': True,
                        'ip': ip,
                        'service': service['name'],
                        'url': service['url'],
                        'error': None
                    }
                else:
                    errors.append(f"{service['name']}: Invalid IP format ({ip})")
                    
        except urllib.error.URLError as e:
            errors.append(f"{service['name']}: Network error - {str(e)}")
        except urllib.error.HTTPError as e:
            errors.append(f"{service['name']}: HTTP error {e.code}")
        except json.JSONDecodeError as e:
            errors.append(f"{service['name']}: JSON parse error - {str(e)}")
        except Exception as e:
            errors.append(f"{service['name']}: {str(e)}")
    
    # Jika semua service gagal
    return {
        'success': False,
        'ip': None,
        'error': 'All IP services failed',
        'service_errors': errors
    }


def get_ip_info(ip=None):
    """
    Mendapatkan informasi tambahan tentang IP address
    Jika IP tidak diberikan, akan menggunakan IP publik
    
    Args:
        ip (str): IP address yang ingin dicek (optional)
    
    Returns:
        dict: informasi detail tentang IP
    """
    if not ip:
        # Dapatkan IP publik terlebih dahulu
        public_ip_result = get_public_ip()
        if not public_ip_result['success']:
            return {
                'success': False,
                'error': 'Failed to get IP for lookup: ' + public_ip_result['error']
            }
        ip = public_ip_result['ip']
    
    try:
        # Gunakan API ipapi.co untuk informasi IP
        url = f'https://ipapi.co/{ip}/json/'
        request = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'netdiag/1.0 (Network Diagnostics Tool)'
            }
        )
        
        with urllib.request.urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            return {
                'success': True,
                'ip': ip,
                'country': data.get('country_name'),
                'country_code': data.get('country_code'),
                'city': data.get('city'),
                'region': data.get('region'),
                'timezone': data.get('timezone'),
                'isp': data.get('org'),
                'latitude': data.get('latitude'),
                'longitude': data.get('longitude'),
                'error': None
            }
            
    except Exception as e:
        return {
            'success': False,
            'ip': ip,
            'error': f'Failed to get IP info: {str(e)}'
        }


if __name__ == "__main__":
    # Test functions jika dijalankan langsung
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "info":
        # Test IP info
        ip = sys.argv[2] if len(sys.argv) > 2 else None
        print(f"Getting IP info for {ip or 'public IP'}...")
        result = get_ip_info(ip)
        
        if result['success']:
            print(f"✅ IP Info:")
            print(f"   IP: {result['ip']}")
            print(f"   Country: {result['country']} ({result['country_code']})")
            print(f"   City: {result['city']}, {result['region']}")
            print(f"   ISP: {result['isp']}")
            print(f"   Timezone: {result['timezone']}")
        else:
            print(f"❌ Failed: {result['error']}")
    else:
        # Test local dan public IP
        print("Testing local IP...")
        local_result = get_local_ip()
        
        if local_result['success']:
            print(f"✅ Local IP: {local_result['ip']} (method: {local_result['method']})")
        else:
            print(f"❌ Local IP failed: {local_result['error']}")
        
        print("\nTesting public IP...")
        public_result = get_public_ip()
        
        if public_result['success']:
            print(f"✅ Public IP: {public_result['ip']} (service: {public_result['service']})")
        else:
            print(f"❌ Public IP failed: {public_result['error']}")
            if 'service_errors' in public_result:
                print("   Service errors:")
                for error in public_result['service_errors']:
                    print(f"   - {error}")
    
    print("\nUsage examples:")
    print("  python iputils.py                    # Get local and public IP")
    print("  python iputils.py info               # Get info for public IP")
    print("  python iputils.py info 8.8.8.8      # Get info for specific IP")