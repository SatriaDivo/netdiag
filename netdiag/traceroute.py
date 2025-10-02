"""
Modul traceroute untuk melakukan trace route ke host target
Menggunakan subprocess untuk memanggil perintah tracert (Windows) atau traceroute (Linux/Mac)
"""

import subprocess
import platform
import re


def traceroute(host, max_hops=30, timeout=5):
    """
    Melakukan traceroute ke host target
    
    Args:
        host (str): hostname atau IP address yang akan di-trace
        max_hops (int): maksimum jumlah hops (default: 30)
        timeout (int): timeout per hop dalam detik (default: 5)
    
    Returns:
        dict: hasil traceroute dengan daftar hops dan informasi lainnya
        
    Example:
        >>> result = traceroute("google.com")
        >>> print(result['success'])
        True
        >>> for hop in result['hops']:
        ...     print(f"Hop {hop['number']}: {hop['ip']} ({hop['avg_time']} ms)")
    """
    try:
        # Deteksi OS untuk menentukan perintah traceroute yang tepat
        system = platform.system().lower()
        
        if system == "windows":
            # Windows menggunakan tracert
            cmd = ["tracert", "-h", str(max_hops), "-w", str(timeout * 1000), host]
        else:
            # Linux/Mac menggunakan traceroute
            cmd = ["traceroute", "-m", str(max_hops), "-w", str(timeout), host]
        
        # Jalankan perintah traceroute
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            timeout=max_hops * timeout + 30  # timeout total
        )
        
        output = result.stdout
        error_output = result.stderr
        
        # Parse hasil traceroute
        parsed_result = _parse_traceroute_output(output, system, host)
        parsed_result['raw_output'] = output
        parsed_result['error_output'] = error_output
        parsed_result['command'] = ' '.join(cmd)
        
        return parsed_result
        
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'error': f'Traceroute timeout after {max_hops * timeout + 30} seconds',
            'host': host,
            'max_hops': max_hops,
            'hops': [],
            'destination_reached': False,
            'total_hops': 0
        }
    except FileNotFoundError:
        return {
            'success': False,
            'error': f'Traceroute command not found. Please install traceroute.',
            'host': host,
            'max_hops': max_hops,
            'hops': [],
            'destination_reached': False,
            'total_hops': 0
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Traceroute failed: {str(e)}',
            'host': host,
            'max_hops': max_hops,
            'hops': [],
            'destination_reached': False,
            'total_hops': 0
        }


def _parse_traceroute_output(output, system, target_host):
    """
    Parse output traceroute sesuai dengan OS
    
    Args:
        output (str): raw output dari perintah traceroute
        system (str): nama sistem operasi
        target_host (str): hostname target yang di-trace
    
    Returns:
        dict: hasil parsing traceroute
    """
    result = {
        'success': False,
        'host': target_host,
        'hops': [],
        'destination_reached': False,
        'total_hops': 0,
        'error': None
    }
    
    try:
        lines = output.strip().split('\n')
        
        if system == "windows":
            # Parse output Windows tracert
            for line in lines:
                line = line.strip()
                if not line or line.startswith('Tracing route') or line.startswith('over a maximum'):
                    continue
                
                # Format Windows: "  1    <1 ms    <1 ms    <1 ms  192.168.1.1"
                # atau: "  2     *        *        *     Request timed out."
                hop_match = re.match(r'\s*(\d+)\s+(.+)', line)
                if hop_match:
                    hop_num = int(hop_match.group(1))
                    hop_data = hop_match.group(2).strip()
                    
                    hop_info = {
                        'number': hop_num,
                        'ip': None,
                        'hostname': None,
                        'times': [],
                        'avg_time': None,
                        'status': 'success'
                    }
                    
                    if 'Request timed out' in hop_data or '*' in hop_data:
                        hop_info['status'] = 'timeout'
                        hop_info['ip'] = '*'
                        hop_info['times'] = ['*', '*', '*']
                    else:
                        # Parse times dan IP
                        time_pattern = r'(\d+)\s*ms|<(\d+)\s*ms|\*'
                        times = []
                        for match in re.finditer(time_pattern, hop_data):
                            if match.group(1):
                                times.append(float(match.group(1)))
                            elif match.group(2):
                                times.append(float(match.group(2)))
                            else:
                                times.append('*')
                        
                        hop_info['times'] = times
                        if times and all(isinstance(t, (int, float)) for t in times):
                            hop_info['avg_time'] = sum(times) / len(times)
                        
                        # Extract IP address (biasanya di akhir line)
                        ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', hop_data)
                        if ip_match:
                            hop_info['ip'] = ip_match.group(1)
                            
                        # Extract hostname jika ada
                        hostname_match = re.search(r'([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', hop_data)
                        if hostname_match and not ip_match:
                            hop_info['hostname'] = hostname_match.group(1)
                    
                    result['hops'].append(hop_info)
                    
        else:
            # Parse output Linux/Mac traceroute
            for line in lines:
                line = line.strip()
                if not line or line.startswith('traceroute to'):
                    continue
                
                # Format Linux: " 1  192.168.1.1 (192.168.1.1)  0.532 ms  0.518 ms  0.515 ms"
                # atau: " 2  * * *"
                hop_match = re.match(r'\s*(\d+)\s+(.+)', line)
                if hop_match:
                    hop_num = int(hop_match.group(1))
                    hop_data = hop_match.group(2).strip()
                    
                    hop_info = {
                        'number': hop_num,
                        'ip': None,
                        'hostname': None,
                        'times': [],
                        'avg_time': None,
                        'status': 'success'
                    }
                    
                    if hop_data.startswith('*') or '* * *' in hop_data:
                        hop_info['status'] = 'timeout'
                        hop_info['ip'] = '*'
                        hop_info['times'] = ['*', '*', '*']
                    else:
                        # Parse hostname dan IP
                        host_ip_match = re.match(r'([^\s]+)\s+\(([^)]+)\)', hop_data)
                        if host_ip_match:
                            hop_info['hostname'] = host_ip_match.group(1)
                            hop_info['ip'] = host_ip_match.group(2)
                        else:
                            # Hanya IP
                            ip_match = re.match(r'(\d+\.\d+\.\d+\.\d+)', hop_data)
                            if ip_match:
                                hop_info['ip'] = ip_match.group(1)
                        
                        # Parse times
                        time_matches = re.findall(r'(\d+(?:\.\d+)?)\s*ms', hop_data)
                        times = [float(t) for t in time_matches]
                        hop_info['times'] = times
                        
                        if times:
                            hop_info['avg_time'] = sum(times) / len(times)
                    
                    result['hops'].append(hop_info)
        
        # Tentukan apakah destination tercapai
        if result['hops']:
            result['total_hops'] = len(result['hops'])
            last_hop = result['hops'][-1]
            
            # Cek apakah hop terakhir adalah destination
            if last_hop['ip'] and last_hop['ip'] != '*':
                result['destination_reached'] = True
            elif last_hop['hostname'] and target_host.lower() in last_hop['hostname'].lower():
                result['destination_reached'] = True
        
        result['success'] = True if result['hops'] else False
        
    except Exception as e:
        result['error'] = f'Failed to parse traceroute output: {str(e)}'
    
    return result


if __name__ == "__main__":
    # Test function jika dijalankan langsung
    import sys
    
    if len(sys.argv) > 1:
        host = sys.argv[1]
        print(f"Testing traceroute to {host}...")
        result = traceroute(host)
        
        if result['success']:
            print(f"✅ Traceroute successful!")
            print(f"   Host: {result['host']}")
            print(f"   Total Hops: {result['total_hops']}")
            print(f"   Destination Reached: {result['destination_reached']}")
            print("\n   Route:")
            
            for hop in result['hops']:
                if hop['status'] == 'timeout':
                    print(f"   {hop['number']:2d}. * * * (timeout)")
                else:
                    ip_or_host = hop['ip'] or hop['hostname'] or 'unknown'
                    avg_time_str = f"{hop['avg_time']:.1f} ms" if hop['avg_time'] else "N/A"
                    print(f"   {hop['number']:2d}. {ip_or_host} ({avg_time_str})")
        else:
            print(f"❌ Traceroute failed: {result['error']}")
    else:
        print("Usage: python traceroute.py <host>")
        print("Example: python traceroute.py google.com")