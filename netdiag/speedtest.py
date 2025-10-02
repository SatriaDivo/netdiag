"""
Modul speed test untuk mengukur bandwidth dan kecepatan jaringan
Menggunakan HTTP requests untuk mengukur download/upload speed
"""

import urllib.request
import urllib.error
import time
import threading
import json


def bandwidth_test(test_size='1MB', timeout=30):
    """
    Melakukan bandwidth test sederhana dengan mengdownload file test
    
    Args:
        test_size (str): ukuran test file ('1MB', '5MB', '10MB')
        timeout (int): timeout dalam detik (default: 30)
    
    Returns:
        dict: hasil speed test dengan informasi bandwidth
        
    Example:
        >>> result = bandwidth_test('5MB')
        >>> print(f"Download speed: {result['download_speed_mbps']} Mbps")
    """
    
    # Test files dari berbagai provider
    test_files = {
        '1MB': [
            'http://speedtest.ftp.otenet.gr/files/test1Mb.db',
            'http://mirror.internode.on.net/pub/test/1meg.test',
            'https://speed.hetzner.de/1MB.bin'
        ],
        '5MB': [
            'http://speedtest.ftp.otenet.gr/files/test5Mb.db',
            'http://mirror.internode.on.net/pub/test/5meg.test',
            'https://speed.hetzner.de/5MB.bin'
        ],
        '10MB': [
            'http://speedtest.ftp.otenet.gr/files/test10Mb.db',
            'http://mirror.internode.on.net/pub/test/10meg.test',
            'https://speed.hetzner.de/10MB.bin'
        ]
    }
    
    if test_size not in test_files:
        return {
            'success': False,
            'error': f'Invalid test size. Available: {list(test_files.keys())}'
        }
    
    result = {
        'success': False,
        'test_size': test_size,
        'download_speed_mbps': 0,
        'download_time': 0,
        'bytes_downloaded': 0,
        'test_url': None,
        'error': None
    }
    
    # Coba beberapa test file sampai ada yang berhasil
    for test_url in test_files[test_size]:
        try:
            print(f"Testing download speed with {test_url}...")
            
            start_time = time.time()
            
            # Buat request dengan custom headers
            request = urllib.request.Request(
                test_url,
                headers={
                    'User-Agent': 'netdiag/1.1.0 (Network Speed Test)',
                    'Accept': '*/*'
                }
            )
            
            # Download file dan ukur waktu
            with urllib.request.urlopen(request, timeout=timeout) as response:
                # Baca data dalam chunks untuk mengukur progress
                data = b''
                chunk_size = 8192
                
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    data += chunk
            
            end_time = time.time()
            download_time = end_time - start_time
            bytes_downloaded = len(data)
            
            # Hitung speed dalam Mbps
            bits_downloaded = bytes_downloaded * 8
            megabits_downloaded = bits_downloaded / (1024 * 1024)
            speed_mbps = megabits_downloaded / download_time
            
            result.update({
                'success': True,
                'download_speed_mbps': round(speed_mbps, 2),
                'download_time': round(download_time, 2),
                'bytes_downloaded': bytes_downloaded,
                'test_url': test_url
            })
            
            break  # Berhasil, keluar dari loop
            
        except urllib.error.URLError as e:
            last_error = f'URL error: {str(e)}'
            continue
        except urllib.error.HTTPError as e:
            last_error = f'HTTP error {e.code}: {e.reason}'
            continue
        except Exception as e:
            last_error = f'Error: {str(e)}'
            continue
    
    if not result['success']:
        result['error'] = f'All test servers failed. Last error: {last_error}'
    
    return result


def ping_latency_test(host, count=10):
    """
    Test latency dengan ping multiple kali untuk mendapatkan statistik
    
    Args:
        host (str): hostname atau IP yang akan di-test
        count (int): jumlah ping (default: 10)
    
    Returns:
        dict: statistik latency lengkap
    """
    from .ping import ping
    
    result = {
        'success': False,
        'host': host,
        'total_pings': count,
        'successful_pings': 0,
        'failed_pings': 0,
        'latencies': [],
        'avg_latency': 0,
        'min_latency': 0,
        'max_latency': 0,
        'jitter': 0,
        'packet_loss_percent': 0,
        'error': None
    }
    
    latencies = []
    successful = 0
    
    print(f"Running latency test to {host} ({count} pings)...")
    
    for i in range(count):
        ping_result = ping(host, count=1, timeout=3)
        
        if ping_result['success'] and ping_result.get('avg_time'):
            latencies.append(ping_result['avg_time'])
            successful += 1
            print(f"  Ping {i+1}/{count}: {ping_result['avg_time']} ms")
        else:
            print(f"  Ping {i+1}/{count}: Failed")
        
        # Small delay between pings
        time.sleep(0.1)
    
    if latencies:
        result.update({
            'success': True,
            'successful_pings': successful,
            'failed_pings': count - successful,
            'latencies': latencies,
            'avg_latency': round(sum(latencies) / len(latencies), 2),
            'min_latency': round(min(latencies), 2),
            'max_latency': round(max(latencies), 2),
            'packet_loss_percent': round(((count - successful) / count) * 100, 2)
        })
        
        # Hitung jitter (variasi latency)
        if len(latencies) > 1:
            avg = result['avg_latency']
            variance = sum((x - avg) ** 2 for x in latencies) / len(latencies)
            jitter = variance ** 0.5
            result['jitter'] = round(jitter, 2)
    else:
        result['error'] = 'All pings failed'
    
    return result


def connection_quality_test(host):
    """
    Test kualitas koneksi lengkap dengan bandwidth dan latency
    
    Args:
        host (str): hostname untuk latency test
    
    Returns:
        dict: analisis lengkap kualitas koneksi
    """
    print("=== CONNECTION QUALITY TEST ===")
    
    result = {
        'success': False,
        'host': host,
        'bandwidth_test': {},
        'latency_test': {},
        'quality_score': 0,
        'quality_rating': 'Unknown',
        'recommendations': [],
        'error': None
    }
    
    try:
        # 1. Bandwidth Test
        print("\n1. Testing download speed...")
        bandwidth_result = bandwidth_test('5MB')
        result['bandwidth_test'] = bandwidth_result
        
        # 2. Latency Test  
        print(f"\n2. Testing latency to {host}...")
        latency_result = ping_latency_test(host, count=10)
        result['latency_test'] = latency_result
        
        # 3. Analisis kualitas
        if bandwidth_result['success'] and latency_result['success']:
            quality_score = _calculate_quality_score(bandwidth_result, latency_result)
            quality_rating = _get_quality_rating(quality_score)
            recommendations = _get_recommendations(bandwidth_result, latency_result)
            
            result.update({
                'success': True,
                'quality_score': quality_score,
                'quality_rating': quality_rating,
                'recommendations': recommendations
            })
            
    except Exception as e:
        result['error'] = f'Quality test failed: {str(e)}'
    
    return result


def _calculate_quality_score(bandwidth_result, latency_result):
    """Hitung score kualitas koneksi berdasarkan bandwidth dan latency"""
    
    # Score bandwidth (0-50 points)
    speed_mbps = bandwidth_result['download_speed_mbps']
    if speed_mbps >= 100:
        bandwidth_score = 50
    elif speed_mbps >= 50:
        bandwidth_score = 40
    elif speed_mbps >= 25:
        bandwidth_score = 30
    elif speed_mbps >= 10:
        bandwidth_score = 20
    elif speed_mbps >= 5:
        bandwidth_score = 10
    else:
        bandwidth_score = 5
    
    # Score latency (0-30 points)
    avg_latency = latency_result['avg_latency']
    if avg_latency <= 20:
        latency_score = 30
    elif avg_latency <= 50:
        latency_score = 25
    elif avg_latency <= 100:
        latency_score = 20
    elif avg_latency <= 200:
        latency_score = 15
    elif avg_latency <= 500:
        latency_score = 10
    else:
        latency_score = 5
    
    # Score packet loss (0-20 points)
    packet_loss = latency_result['packet_loss_percent']
    if packet_loss == 0:
        loss_score = 20
    elif packet_loss <= 1:
        loss_score = 15
    elif packet_loss <= 5:
        loss_score = 10
    elif packet_loss <= 10:
        loss_score = 5
    else:
        loss_score = 0
    
    total_score = bandwidth_score + latency_score + loss_score
    return min(100, total_score)


def _get_quality_rating(score):
    """Konversi score ke rating kualitas"""
    if score >= 90:
        return 'Excellent'
    elif score >= 80:
        return 'Very Good'
    elif score >= 70:
        return 'Good'
    elif score >= 60:
        return 'Fair'
    elif score >= 50:
        return 'Poor'
    else:
        return 'Very Poor'


def _get_recommendations(bandwidth_result, latency_result):
    """Generate rekomendasi berdasarkan hasil test"""
    recommendations = []
    
    speed_mbps = bandwidth_result['download_speed_mbps']
    avg_latency = latency_result['avg_latency']
    packet_loss = latency_result['packet_loss_percent']
    jitter = latency_result['jitter']
    
    # Bandwidth recommendations
    if speed_mbps < 5:
        recommendations.append("Very slow connection. Consider upgrading your internet plan.")
    elif speed_mbps < 25:
        recommendations.append("Connection may be slow for HD video streaming or large downloads.")
    
    # Latency recommendations
    if avg_latency > 100:
        recommendations.append("High latency detected. May affect real-time applications (gaming, video calls).")
    elif avg_latency > 50:
        recommendations.append("Moderate latency. Gaming and video calls may experience some lag.")
    
    # Packet loss recommendations
    if packet_loss > 5:
        recommendations.append("High packet loss detected. Check network stability and equipment.")
    elif packet_loss > 1:
        recommendations.append("Some packet loss detected. Monitor network for stability issues.")
    
    # Jitter recommendations
    if jitter > 20:
        recommendations.append("High jitter detected. May cause inconsistent performance.")
    
    if not recommendations:
        recommendations.append("Connection quality looks good! No immediate issues detected.")
    
    return recommendations


if __name__ == "__main__":
    # Test functions jika dijalankan langsung
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python speedtest.py bandwidth [size]     # Test bandwidth")
        print("  python speedtest.py latency <host>       # Test latency") 
        print("  python speedtest.py quality <host>       # Full quality test")
        print("\nExamples:")
        print("  python speedtest.py bandwidth 5MB")
        print("  python speedtest.py latency google.com")
        print("  python speedtest.py quality google.com")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "bandwidth":
        size = sys.argv[2] if len(sys.argv) > 2 else '5MB'
        print(f"Testing bandwidth with {size} download...")
        result = bandwidth_test(size)
        
        if result['success']:
            print(f"✅ Bandwidth test successful!")
            print(f"   Download speed: {result['download_speed_mbps']} Mbps")
            print(f"   Download time: {result['download_time']} seconds")
            print(f"   Bytes downloaded: {result['bytes_downloaded']:,}")
            print(f"   Test server: {result['test_url']}")
        else:
            print(f"❌ Bandwidth test failed: {result['error']}")
    
    elif command == "latency" and len(sys.argv) > 2:
        host = sys.argv[2]
        result = ping_latency_test(host)
        
        if result['success']:
            print(f"✅ Latency test successful!")
            print(f"   Host: {result['host']}")
            print(f"   Successful pings: {result['successful_pings']}/{result['total_pings']}")
            print(f"   Average latency: {result['avg_latency']} ms")
            print(f"   Min/Max latency: {result['min_latency']}/{result['max_latency']} ms")
            print(f"   Jitter: {result['jitter']} ms")
            print(f"   Packet loss: {result['packet_loss_percent']}%")
        else:
            print(f"❌ Latency test failed: {result['error']}")
    
    elif command == "quality" and len(sys.argv) > 2:
        host = sys.argv[2]
        result = connection_quality_test(host)
        
        if result['success']:
            print(f"\n✅ Connection quality test completed!")
            print(f"   Overall score: {result['quality_score']}/100")
            print(f"   Quality rating: {result['quality_rating']}")
            
            if result['bandwidth_test']['success']:
                print(f"   Download speed: {result['bandwidth_test']['download_speed_mbps']} Mbps")
            
            if result['latency_test']['success']:
                print(f"   Average latency: {result['latency_test']['avg_latency']} ms")
                print(f"   Packet loss: {result['latency_test']['packet_loss_percent']}%")
            
            print(f"\n   Recommendations:")
            for rec in result['recommendations']:
                print(f"   - {rec}")
        else:
            print(f"❌ Quality test failed: {result['error']}")
    
    else:
        print("❌ Invalid command or missing arguments")