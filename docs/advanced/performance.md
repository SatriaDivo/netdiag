# Optimasi Performa NetDiag

## 📊 Mengoptimalkan Kinerja Toolkit

### Pengenalan Performa
NetDiag dirancang untuk memberikan performa optimal dalam berbagai skenario penggunaan di lingkungan kampus dan industri.

### Profiling dan Monitoring

#### Mengukur Performa
```python
import time
from netdiag import NetworkAnalyzer, TrafficMonitor

# Profiling analisis jaringan
start_time = time.time()
analyzer = NetworkAnalyzer()
result = analyzer.comprehensive_scan("polinela.ac.id")
execution_time = time.time() - start_time

print(f"Analisis selesai dalam {execution_time:.2f} detik")
```

#### Memory Usage Monitoring
```python
import psutil
import os

def monitor_memory_usage():
    """Monitor penggunaan memori selama analisis"""
    process = psutil.Process(os.getpid())
    memory_usage = process.memory_info().rss / 1024 / 1024  # MB
    return f"Penggunaan memori: {memory_usage:.2f} MB"

# Contoh penggunaan
print(monitor_memory_usage())
traffic_monitor = TrafficMonitor()
traffic_monitor.start_capture("10 minutes")
print(monitor_memory_usage())
```

### Optimasi Jaringan

#### Parallel Processing
```python
import concurrent.futures
from netdiag import NetworkAnalyzer

def scan_multiple_hosts():
    """Scan multiple hosts secara parallel"""
    hosts = [
        "polinela.ac.id",
        "mail.polinela.ac.id", 
        "library.polinela.ac.id",
        "elearning.polinela.ac.id"
    ]
    
    analyzer = NetworkAnalyzer()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        future_to_host = {
            executor.submit(analyzer.ping_host, host): host 
            for host in hosts
        }
        
        results = {}
        for future in concurrent.futures.as_completed(future_to_host):
            host = future_to_host[future]
            try:
                result = future.result()
                results[host] = result
            except Exception as exc:
                print(f'{host} generated an exception: {exc}')
        
        return results

# Contoh penggunaan
scan_results = scan_multiple_hosts()
for host, result in scan_results.items():
    print(f"{host}: {result.average_latency}ms")
```

#### Caching Strategis
```python
from functools import lru_cache
import time

class OptimizedNetworkAnalyzer:
    def __init__(self):
        self.cache_timeout = 300  # 5 menit
        self.dns_cache = {}
    
    @lru_cache(maxsize=128)
    def get_dns_info_cached(self, domain):
        """DNS lookup dengan caching"""
        # Cache DNS results untuk mengurangi query berulang
        return self._perform_dns_lookup(domain)
    
    def _perform_dns_lookup(self, domain):
        """Implementasi actual DNS lookup"""
        # Simulasi DNS lookup
        time.sleep(0.1)  # Simulasi network delay
        return {
            'domain': domain,
            'ip': '192.168.1.100',
            'timestamp': time.time()
        }

# Contoh penggunaan
analyzer = OptimizedNetworkAnalyzer()

# First call - akan melakukan DNS lookup actual
result1 = analyzer.get_dns_info_cached("polinela.ac.id")

# Second call - akan menggunakan cached result
result2 = analyzer.get_dns_info_cached("polinela.ac.id")
```

### Optimasi Database

#### Connection Pooling
```python
import sqlite3
from contextlib import contextmanager

class DatabaseManager:
    def __init__(self, db_path="netdiag_results.db", pool_size=5):
        self.db_path = db_path
        self.pool_size = pool_size
        self.connections = []
        self._init_pool()
    
    def _init_pool(self):
        """Inisialisasi connection pool"""
        for _ in range(self.pool_size):
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            self.connections.append(conn)
    
    @contextmanager
    def get_connection(self):
        """Context manager untuk database connection"""
        if self.connections:
            conn = self.connections.pop()
            try:
                yield conn
            finally:
                self.connections.append(conn)
        else:
            # Fallback jika pool kosong
            conn = sqlite3.connect(self.db_path)
            try:
                yield conn
            finally:
                conn.close()

# Contoh penggunaan
db_manager = DatabaseManager()

with db_manager.get_connection() as conn:
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO scan_results 
        (timestamp, host, latency) 
        VALUES (?, ?, ?)
    """, (time.time(), "polinela.ac.id", 25.5))
    conn.commit()
```

#### Batch Operations
```python
def batch_insert_results(results, batch_size=100):
    """Insert multiple results secara batch"""
    db_manager = DatabaseManager()
    
    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        
        # Prepare batch data
        batch_data = []
        for result in results:
            batch_data.append((
                result.timestamp,
                result.host,
                result.latency,
                result.status
            ))
            
            # Insert batch ketika mencapai batch_size
            if len(batch_data) >= batch_size:
                cursor.executemany("""
                    INSERT INTO scan_results 
                    (timestamp, host, latency, status) 
                    VALUES (?, ?, ?, ?)
                """, batch_data)
                conn.commit()
                batch_data = []
        
        # Insert remaining data
        if batch_data:
            cursor.executemany("""
                INSERT INTO scan_results 
                (timestamp, host, latency, status) 
                VALUES (?, ?, ?, ?)
            """, batch_data)
            conn.commit()
```

### Optimasi Memory

#### Generator Pattern
```python
def stream_large_dataset(file_path):
    """Stream large files tanpa load ke memory"""
    with open(file_path, 'r') as file:
        for line in file:
            yield line.strip()

def process_large_logfile(log_path):
    """Process large log files secara streaming"""
    error_count = 0
    warning_count = 0
    
    for line in stream_large_dataset(log_path):
        if 'ERROR' in line:
            error_count += 1
        elif 'WARNING' in line:
            warning_count += 1
    
    return {
        'errors': error_count,
        'warnings': warning_count
    }

# Contoh penggunaan
stats = process_large_logfile("/var/log/network.log")
print(f"Errors: {stats['errors']}, Warnings: {stats['warnings']}")
```

#### Memory-Efficient Data Structures
```python
import array
from collections import deque

class EfficientDataCollector:
    def __init__(self):
        # Gunakan array untuk data numerik
        self.latencies = array.array('f')  # float array
        self.timestamps = array.array('d')  # double array
        
        # Gunakan deque untuk sliding window
        self.recent_results = deque(maxlen=1000)
    
    def add_measurement(self, timestamp, latency):
        """Tambah measurement dengan efficient storage"""
        self.timestamps.append(timestamp)
        self.latencies.append(latency)
        self.recent_results.append({
            'timestamp': timestamp,
            'latency': latency
        })
    
    def get_average_latency(self):
        """Hitung rata-rata latency efficiently"""
        if not self.latencies:
            return 0
        return sum(self.latencies) / len(self.latencies)
    
    def get_recent_average(self, count=100):
        """Rata-rata dari N measurement terakhir"""
        recent_data = list(self.recent_results)[-count:]
        if not recent_data:
            return 0
        return sum(item['latency'] for item in recent_data) / len(recent_data)
```

### Profiling Tools

#### Custom Profiler
```python
import functools
import time

def profile_function(func):
    """Decorator untuk profiling function execution"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss
        
        try:
            result = func(*args, **kwargs)
            success = True
        except Exception as e:
            result = None
            success = False
            print(f"Function {func.__name__} failed: {e}")
        
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss
        
        execution_time = end_time - start_time
        memory_delta = end_memory - start_memory
        
        print(f"""
Profile Report for {func.__name__}:
- Execution Time: {execution_time:.4f} seconds
- Memory Delta: {memory_delta / 1024:.2f} KB
- Success: {success}
        """)
        
        return result
    return wrapper

# Contoh penggunaan
@profile_function
def analyze_network_performance():
    analyzer = NetworkAnalyzer()
    return analyzer.comprehensive_scan("polinela.ac.id")

result = analyze_network_performance()
```

#### Performance Benchmarking
```python
import statistics
import time

class PerformanceBenchmark:
    def __init__(self):
        self.results = []
    
    def benchmark_function(self, func, iterations=10, *args, **kwargs):
        """Benchmark sebuah function dengan multiple iterations"""
        execution_times = []
        
        for i in range(iterations):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                success = True
            except Exception as e:
                success = False
                print(f"Iteration {i+1} failed: {e}")
                continue
            
            end_time = time.time()
            execution_times.append(end_time - start_time)
        
        if execution_times:
            stats = {
                'function': func.__name__,
                'iterations': len(execution_times),
                'mean': statistics.mean(execution_times),
                'median': statistics.median(execution_times),
                'stdev': statistics.stdev(execution_times) if len(execution_times) > 1 else 0,
                'min': min(execution_times),
                'max': max(execution_times)
            }
            
            self.results.append(stats)
            return stats
        
        return None
    
    def print_benchmark_report(self):
        """Print comprehensive benchmark report"""
        for result in self.results:
            print(f"""
Function: {result['function']}
Iterations: {result['iterations']}
Mean Time: {result['mean']:.4f}s
Median Time: {result['median']:.4f}s
Std Deviation: {result['stdev']:.4f}s
Min Time: {result['min']:.4f}s
Max Time: {result['max']:.4f}s
            """)

# Contoh penggunaan
benchmark = PerformanceBenchmark()

def ping_test():
    analyzer = NetworkAnalyzer()
    return analyzer.ping_host("polinela.ac.id")

# Benchmark ping function
stats = benchmark.benchmark_function(ping_test, iterations=20)
benchmark.print_benchmark_report()
```

### Best Practices

#### 1. Gunakan Async untuk I/O Operations
```python
import asyncio
import aiohttp

async def async_http_check(url):
    """Async HTTP connectivity check"""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=5) as response:
                return {
                    'url': url,
                    'status': response.status,
                    'response_time': response.headers.get('X-Response-Time', 'N/A')
                }
        except Exception as e:
            return {
                'url': url,
                'status': 'error',
                'error': str(e)
            }

async def check_multiple_urls():
    """Check multiple URLs concurrently"""
    urls = [
        "http://polinela.ac.id",
        "http://mail.polinela.ac.id",
        "http://library.polinela.ac.id"
    ]
    
    tasks = [async_http_check(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results

# Contoh penggunaan
results = asyncio.run(check_multiple_urls())
for result in results:
    print(f"{result['url']}: {result['status']}")
```

#### 2. Resource Management
```python
import contextlib
import socket

class NetworkResourceManager:
    def __init__(self):
        self.active_connections = []
        self.max_connections = 10
    
    @contextlib.contextmanager
    def get_socket(self, host, port):
        """Context manager untuk socket connections"""
        if len(self.active_connections) >= self.max_connections:
            raise Exception("Maximum connections reached")
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.active_connections.append(sock)
        
        try:
            sock.connect((host, port))
            yield sock
        finally:
            sock.close()
            self.active_connections.remove(sock)
    
    def cleanup_all_connections(self):
        """Cleanup all active connections"""
        for sock in self.active_connections:
            try:
                sock.close()
            except:
                pass
        self.active_connections.clear()

# Contoh penggunaan
resource_manager = NetworkResourceManager()

try:
    with resource_manager.get_socket("polinela.ac.id", 80) as sock:
        sock.send(b"GET / HTTP/1.1\r\nHost: polinela.ac.id\r\n\r\n")
        response = sock.recv(1024)
        print("Response received:", len(response), "bytes")
finally:
    resource_manager.cleanup_all_connections()
```

### Monitoring dan Alerting

#### Performance Alerts
```python
import logging

class PerformanceMonitor:
    def __init__(self, thresholds=None):
        self.thresholds = thresholds or {
            'latency': 100,  # ms
            'memory': 512,   # MB
            'cpu': 80        # percent
        }
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('performance.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def check_latency(self, latency_ms):
        """Check if latency exceeds threshold"""
        if latency_ms > self.thresholds['latency']:
            self.logger.warning(
                f"High latency detected: {latency_ms}ms "
                f"(threshold: {self.thresholds['latency']}ms)"
            )
            return False
        return True
    
    def check_memory_usage(self):
        """Check current memory usage"""
        process = psutil.Process()
        memory_mb = process.memory_info().rss / 1024 / 1024
        
        if memory_mb > self.thresholds['memory']:
            self.logger.warning(
                f"High memory usage: {memory_mb:.2f}MB "
                f"(threshold: {self.thresholds['memory']}MB)"
            )
            return False
        return True
    
    def generate_performance_report(self):
        """Generate comprehensive performance report"""
        process = psutil.Process()
        
        report = {
            'timestamp': time.time(),
            'memory_mb': process.memory_info().rss / 1024 / 1024,
            'cpu_percent': process.cpu_percent(),
            'num_threads': process.num_threads(),
            'open_files': len(process.open_files()),
            'connections': len(process.connections())
        }
        
        self.logger.info(f"Performance Report: {report}")
        return report

# Contoh penggunaan
monitor = PerformanceMonitor()

# Monitor selama analisis
analyzer = NetworkAnalyzer()
result = analyzer.ping_host("polinela.ac.id")

monitor.check_latency(result.average_latency)
monitor.check_memory_usage()
monitor.generate_performance_report()
```

### Kesimpulan

Optimasi performa NetDiag melibatkan:

1. **Parallel Processing** - Untuk operasi I/O yang intensif
2. **Caching** - Untuk mengurangi operasi berulang
3. **Memory Management** - Untuk handling dataset besar
4. **Resource Pooling** - Untuk efisiensi connection
5. **Profiling** - Untuk identifikasi bottleneck
6. **Monitoring** - Untuk tracking performa real-time

Implementasikan strategi ini sesuai kebutuhan spesifik aplikasi Anda di lingkungan kampus atau produksi.