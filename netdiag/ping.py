"""
Modul ping untuk melakukan ping ke host target
Menggunakan subprocess untuk memanggil perintah ping system
"""

import subprocess
import platform
import re


def ping(host, count=4, timeout=5):
    """
    Melakukan ping ke host target
    
    Args:
        host (str): hostname atau IP address yang akan di-ping
        count (int): jumlah ping packets yang dikirim (default: 4)
        timeout (int): timeout dalam detik (default: 5)
    
    Returns:
        dict: hasil ping dengan informasi packet loss, avg time, dll
        
    Example:
        >>> result = ping("google.com")
        >>> print(result['success'])
        True
        >>> print(result['avg_time'])
        25.3
    """
    try:
        # Deteksi OS untuk menentukan perintah ping yang tepat
        system = platform.system().lower()
        
        if system == "windows":
            # Windows menggunakan ping dengan parameter -n untuk count
            cmd = ["ping", "-n", str(count), "-w", str(timeout * 1000), host]
        else:
            # Linux/Mac menggunakan ping dengan parameter -c untuk count
            cmd = ["ping", "-c", str(count), "-W", str(timeout), host]
        
        # Jalankan perintah ping
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            timeout=timeout + 10
        )
        
        output = result.stdout
        
        # Parse hasil ping
        parsed_result = _parse_ping_output(output, system)
        parsed_result['raw_output'] = output
        parsed_result['command'] = ' '.join(cmd)
        
        return parsed_result
        
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'error': f'Ping timeout after {timeout + 10} seconds',
            'host': host,
            'packets_sent': count,
            'packets_received': 0,
            'packet_loss': 100.0,
            'avg_time': None,
            'min_time': None,
            'max_time': None
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Ping failed: {str(e)}',
            'host': host,
            'packets_sent': count,
            'packets_received': 0,
            'packet_loss': 100.0,
            'avg_time': None,
            'min_time': None,
            'max_time': None
        }


def _parse_ping_output(output, system):
    """
    Parse output ping sesuai dengan OS
    
    Args:
        output (str): raw output dari perintah ping
        system (str): nama sistem operasi
    
    Returns:
        dict: hasil parsing ping
    """
    result = {
        'success': False,
        'host': None,
        'packets_sent': 0,
        'packets_received': 0,
        'packet_loss': 100.0,
        'avg_time': None,
        'min_time': None,
        'max_time': None,
        'error': None
    }
    
    try:
        if system == "windows":
            # Parse output Windows
            # Contoh: "Packets: Sent = 4, Received = 4, Lost = 0 (0% loss)"
            packet_match = re.search(r'Sent = (\d+), Received = (\d+), Lost = \d+ \((\d+)% loss\)', output)
            if packet_match:
                result['packets_sent'] = int(packet_match.group(1))
                result['packets_received'] = int(packet_match.group(2))
                result['packet_loss'] = float(packet_match.group(3))
            
            # Parse waktu rata-rata
            # Contoh: "Average = 25ms"
            time_match = re.search(r'Average = (\d+)ms', output)
            if time_match:
                result['avg_time'] = float(time_match.group(1))
                
            # Parse min dan max time
            time_stats_match = re.search(r'Minimum = (\d+)ms, Maximum = (\d+)ms, Average = (\d+)ms', output)
            if time_stats_match:
                result['min_time'] = float(time_stats_match.group(1))
                result['max_time'] = float(time_stats_match.group(2))
                result['avg_time'] = float(time_stats_match.group(3))
                
        else:
            # Parse output Linux/Mac
            # Contoh: "4 packets transmitted, 4 received, 0% packet loss"
            packet_match = re.search(r'(\d+) packets transmitted, (\d+) received, (\d+(?:\.\d+)?)% packet loss', output)
            if packet_match:
                result['packets_sent'] = int(packet_match.group(1))
                result['packets_received'] = int(packet_match.group(2))
                result['packet_loss'] = float(packet_match.group(3))
            
            # Parse waktu statistik
            # Contoh: "rtt min/avg/max/mdev = 23.456/25.789/28.123/1.234 ms"
            time_match = re.search(r'rtt min/avg/max/mdev = ([\d.]+)/([\d.]+)/([\d.]+)/([\d.]+) ms', output)
            if time_match:
                result['min_time'] = float(time_match.group(1))
                result['avg_time'] = float(time_match.group(2))
                result['max_time'] = float(time_match.group(3))
        
        # Tentukan success berdasarkan packet loss
        if result['packet_loss'] < 100.0:
            result['success'] = True
        else:
            result['error'] = 'All packets lost'
            
        # Extract hostname dari output
        host_match = re.search(r'PING ([^\s]+)', output) or re.search(r'Pinging ([^\s]+)', output)
        if host_match:
            result['host'] = host_match.group(1)
            
    except Exception as e:
        result['error'] = f'Failed to parse ping output: {str(e)}'
    
    return result


if __name__ == "__main__":
    # Test function jika dijalankan langsung
    import sys
    
    if len(sys.argv) > 1:
        host = sys.argv[1]
        print(f"Testing ping to {host}...")
        result = ping(host)
        
        if result['success']:
            print(f"✅ Ping successful!")
            print(f"   Host: {result['host']}")
            print(f"   Packets: {result['packets_received']}/{result['packets_sent']} received")
            print(f"   Packet Loss: {result['packet_loss']}%")
            if result['avg_time']:
                print(f"   Average Time: {result['avg_time']} ms")
        else:
            print(f"❌ Ping failed: {result['error']}")
    else:
        print("Usage: python ping.py <host>")
        print("Example: python ping.py google.com")