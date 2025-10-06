"""
Modul ping untuk melakukan ping ke host target.
Menggunakan subprocess untuk memanggil perintah ping system dengan
clean code architecture dan proper error handling.
"""

import platform
import re
import subprocess
import time
from typing import Any, Union

from .exceptions import NetworkError, ValidationError, HostResolutionError
from .models import PingResult
from .utils import validate_hostname, validate_count, validate_timeout, resolve_hostname


def ping(
    host: str, 
    count: Union[int, str] = 4, 
    timeout: Union[int, float, str] = 5
) -> dict[str, Any]:
    """
    Melakukan ping ke host target dengan validation dan error handling yang robust.
    
    Args:
        host: Hostname atau IP address yang akan di-ping
        count: Jumlah ping packets yang dikirim (default: 4, max: 100)
        timeout: Timeout dalam detik (default: 5, max: 300)
    
    Returns:
        Dictionary dengan hasil ping termasuk statistik packet loss, timing, dll
        
    Example:
        >>> result = ping("google.com")
        >>> if result['success']:
        ...     print(f"Average time: {result['avg_time']}ms")
        >>> 
        >>> result = ping("192.168.1.1", count=10, timeout=3)
        >>> print(f"Packet loss: {result['packet_loss']}%")
        
    Raises:
        ValidationError: Jika input parameters tidak valid
        NetworkError: Jika terjadi network-related error
    """
    start_time = time.time()
    
    try:
        # Validate inputs
        validated_host = validate_hostname(host)
        validated_count = validate_count(count)
        validated_timeout = validate_timeout(timeout)
        
        # Resolve hostname untuk mendapatkan target IP
        try:
            target_ip = resolve_hostname(validated_host)
        except ValidationError as e:
            raise HostResolutionError(f"Cannot resolve host {validated_host}: {e.message}")
        
        # Execute ping command
        ping_result = _execute_ping_command(
            target_ip, validated_count, validated_timeout
        )
        
        # Parse results
        parsed_result = _parse_ping_output(ping_result.raw_output, ping_result.system)
        
        # Create result object
        result = PingResult(
            success=parsed_result['success'],
            host=validated_host,
            target_ip=target_ip,
            packets_sent=validated_count,
            packets_received=parsed_result.get('packets_received', 0),
            packet_loss=parsed_result.get('packet_loss', 100.0),
            min_time=parsed_result.get('min_time'),
            max_time=parsed_result.get('max_time'),
            avg_time=parsed_result.get('avg_time'),
            jitter=parsed_result.get('jitter'),
            raw_output=ping_result.raw_output,
            command=ping_result.command,
            duration=time.time() - start_time,
            error=parsed_result.get('error')
        )
        
        return result.to_dict()
        
    except (ValidationError, NetworkError) as e:
        return PingResult(
            success=False,
            host=host,
            error=str(e),
            duration=time.time() - start_time
        ).to_dict()
        
    except Exception as e:
        return PingResult(
            success=False,
            host=host,
            error=f"Unexpected error: {str(e)}",
            duration=time.time() - start_time
        ).to_dict()


class _PingCommandResult:
    """Internal class untuk menyimpan hasil ping command."""
    
    def __init__(self, raw_output: str, command: str, system: str):
        self.raw_output = raw_output
        self.command = command
        self.system = system


def _execute_ping_command(
    target_ip: str, count: int, timeout: float
) -> _PingCommandResult:
    """
    Execute ping command berdasarkan operating system.
    
    Args:
        target_ip: Target IP address
        count: Number of packets
        timeout: Timeout in seconds
        
    Returns:
        _PingCommandResult dengan output dan metadata
        
    Raises:
        NetworkError: Jika ping command gagal
    """
    system = platform.system().lower()
    
    try:
        # Build command berdasarkan OS
        if system == "windows":
            cmd = [
                "ping", "-n", str(count), 
                "-w", str(int(timeout * 1000)), target_ip
            ]
        else:
            # Linux/Mac
            cmd = [
                "ping", "-c", str(count), 
                "-W", str(int(timeout)), target_ip
            ]
        
        # Execute command dengan proper timeout
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout + 30  # Add buffer untuk command execution
        )
        
        return _PingCommandResult(
            raw_output=result.stdout,
            command=' '.join(cmd),
            system=system
        )
        
    except subprocess.TimeoutExpired:
        raise NetworkError(
            f"Ping command timeout after {timeout + 30} seconds",
            host=target_ip, timeout=timeout
        )
    except FileNotFoundError:
        raise NetworkError("Ping command not found on system")
    except Exception as e:
        raise NetworkError(f"Failed to execute ping command: {str(e)}")


def _parse_ping_output(output: str, system: str) -> dict[str, Any]:
    """
    Parse output ping sesuai dengan OS dengan improved error handling.
    
    Args:
        output: Raw output dari perintah ping
        system: Nama sistem operasi (windows/linux/mac)
    
    Returns:
        Dictionary dengan hasil parsing ping
    """
    result = {
        'success': False,
        'packets_received': 0,
        'packet_loss': 100.0,
        'avg_time': None,
        'min_time': None,
        'max_time': None,
        'jitter': None,
        'error': None
    }
    
    if not output or not output.strip():
        result['error'] = "Empty ping output"
        return result
    
    try:
        if system == "windows":
            return _parse_windows_ping(output, result)
        else:
            return _parse_unix_ping(output, result)
    except Exception as e:
        result['error'] = f"Failed to parse ping output: {str(e)}"
        return result


def _parse_windows_ping(output: str, result: dict[str, Any]) -> dict[str, Any]:
    """Parse Windows ping output dengan detailed error handling."""
    
    # Check for common Windows ping errors
    if "could not find host" in output.lower():
        result['error'] = "Host not found"
        return result
    
    if "destination host unreachable" in output.lower():
        result['error'] = "Destination host unreachable"
        return result
    
    if "request timed out" in output.lower():
        result['error'] = "Request timed out"
        return result
    
    # Parse packets statistics
    packets_pattern = r'Packets: Sent = (\d+), Received = (\d+), Lost = (\d+)'
    packets_match = re.search(packets_pattern, output)
    
    if packets_match:
        sent = int(packets_match.group(1))
        received = int(packets_match.group(2))
        lost = int(packets_match.group(3))
        
        result['packets_received'] = received
        if sent > 0:
            result['packet_loss'] = (lost / sent) * 100
        
        if received > 0:
            result['success'] = True
    
    # Parse timing statistics
    timing_pattern = r'Minimum = (\d+)ms, Maximum = (\d+)ms, Average = (\d+)ms'
    timing_match = re.search(timing_pattern, output)
    
    if timing_match:
        result['min_time'] = float(timing_match.group(1))
        result['max_time'] = float(timing_match.group(2))
        result['avg_time'] = float(timing_match.group(3))
        
        # Calculate jitter (approximation)
        if result['min_time'] and result['max_time']:
            result['jitter'] = result['max_time'] - result['min_time']
    
    return result


def _parse_unix_ping(output: str, result: dict[str, Any]) -> dict[str, Any]:
    """Parse Unix/Linux ping output dengan detailed error handling."""
    
    # Check for common Unix ping errors
    if "unknown host" in output.lower() or "name or service not known" in output.lower():
        result['error'] = "Host not found"
        return result
    
    if "network is unreachable" in output.lower():
        result['error'] = "Network unreachable"
        return result
    
    if "no route to host" in output.lower():
        result['error'] = "No route to host"
        return result
    
    # Parse packets statistics
    # Format: "5 packets transmitted, 5 received, 0% packet loss"
    packets_pattern = r'(\d+) packets transmitted, (\d+) (?:packets )?received.*?(\d+(?:\.\d+)?)% packet loss'
    packets_match = re.search(packets_pattern, output)
    
    if packets_match:
        transmitted = int(packets_match.group(1))
        received = int(packets_match.group(2))
        loss_percent = float(packets_match.group(3))
        
        result['packets_received'] = received
        result['packet_loss'] = loss_percent
        
        if received > 0:
            result['success'] = True
    
    # Parse timing statistics
    # Format: "rtt min/avg/max/mdev = 23.908/24.583/25.309/0.572 ms"
    timing_pattern = r'rtt min/avg/max/(?:mdev|stddev) = ([\d.]+)/([\d.]+)/([\d.]+)/([\d.]+) ms'
    timing_match = re.search(timing_pattern, output)
    
    if timing_match:
        result['min_time'] = float(timing_match.group(1))
        result['avg_time'] = float(timing_match.group(2))
        result['max_time'] = float(timing_match.group(3))
        result['jitter'] = float(timing_match.group(4))  # mdev is similar to jitter
    
    return result


def calculate_ping_quality_score(ping_result: dict[str, Any]) -> dict[str, Any]:
    """
    Calculate connection quality score berdasarkan ping results.
    
    Args:
        ping_result: Dictionary dari hasil ping
        
    Returns:
        Dictionary dengan quality score dan rating
    """
    if not ping_result.get('success'):
        return {
            'quality_score': 0,
            'quality_rating': 'Failed',
            'recommendations': ['Connection failed or host unreachable']
        }
    
    score = 100
    recommendations = []
    
    # Factor 1: Packet Loss (weight: 40%)
    packet_loss = ping_result.get('packet_loss', 100)
    if packet_loss > 10:
        score -= 40
        recommendations.append("High packet loss detected")
    elif packet_loss > 5:
        score -= 20
        recommendations.append("Moderate packet loss detected")
    elif packet_loss > 1:
        score -= 10
    
    # Factor 2: Average Latency (weight: 35%)
    avg_time = ping_result.get('avg_time')
    if avg_time:
        if avg_time > 200:
            score -= 35
            recommendations.append("Very high latency (>200ms)")
        elif avg_time > 100:
            score -= 25
            recommendations.append("High latency (>100ms)")
        elif avg_time > 50:
            score -= 15
            recommendations.append("Moderate latency (>50ms)")
        elif avg_time > 20:
            score -= 5
    
    # Factor 3: Jitter (weight: 25%)
    jitter = ping_result.get('jitter')
    if jitter:
        if jitter > 50:
            score -= 25
            recommendations.append("High jitter detected")
        elif jitter > 20:
            score -= 15
            recommendations.append("Moderate jitter detected")
        elif jitter > 10:
            score -= 5
    
    # Determine rating
    if score >= 90:
        rating = "Excellent"
    elif score >= 80:
        rating = "Very Good"
    elif score >= 70:
        rating = "Good"
    elif score >= 60:
        rating = "Fair"
    elif score >= 40:
        rating = "Poor"
    else:
        rating = "Very Poor"
    
    if not recommendations:
        recommendations.append("Connection quality looks good!")
    
    return {
        'quality_score': max(0, score),
        'quality_rating': rating,
        'recommendations': recommendations
    }


# Backward compatibility functions
def get_ping_statistics(host: str, count: int = 10) -> dict[str, Any]:
    """
    Get detailed ping statistics dengan multiple pings.
    
    Args:
        host: Target hostname/IP
        count: Number of pings to perform
        
    Returns:
        Dictionary dengan detailed statistics
    """
    result = ping(host, count=count, timeout=10)
    
    if result['success']:
        quality = calculate_ping_quality_score(result)
        result.update(quality)
    
    return result


if __name__ == "__main__":
    # Test function jika dijalankan langsung
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python ping.py <host> [count] [timeout]")
        print("\nExamples:")
        print("  python ping.py google.com")
        print("  python ping.py 8.8.8.8 10 3")
        sys.exit(1)
    
    host = sys.argv[1]
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    timeout = float(sys.argv[3]) if len(sys.argv) > 3 else 5
    
    print(f"Pinging {host} with {count} packets...")
    result = ping(host, count, timeout)
    
    if result['success']:
        print(f"✅ Ping successful!")
        print(f"   Host: {result['host']} ({result.get('target_ip', 'unknown')})")
        print(f"   Packets: {result['packets_received']}/{result['packets_sent']} received")
        print(f"   Packet loss: {result['packet_loss']:.1f}%")
        
        if result.get('avg_time'):
            print(f"   Average time: {result['avg_time']:.2f}ms")
            print(f"   Min/Max time: {result.get('min_time', 0):.2f}/{result.get('max_time', 0):.2f}ms")
            
            if result.get('jitter'):
                print(f"   Jitter: {result['jitter']:.2f}ms")
    else:
        print(f"❌ Ping failed: {result.get('error', 'Unknown error')}")