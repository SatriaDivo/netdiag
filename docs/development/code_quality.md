# Code Quality Guide

## 📊 Maintaining High Code Quality Standards

### Overview

Code quality dalam NetDiag tidak hanya tentang functionality, tetapi juga tentang maintainability, readability, dan educational value untuk mahasiswa dan pengembang di lingkungan kampus Politeknik Negeri Lampung.

### Code Quality Metrics

#### 1. Quantitative Metrics

**Coverage Targets:**
```python
# Target coverage berdasarkan komponen
COVERAGE_TARGETS = {
    'core_functionality': 95,    # Core network operations
    'utilities': 90,             # Helper functions
    'models': 85,                # Data models
    'integrations': 80,          # External integrations
    'campus_specific': 85,       # Campus-specific features
    'overall': 85               # Overall target
}
```

**Complexity Limits:**
```python
# Cyclomatic complexity limits
COMPLEXITY_LIMITS = {
    'functions': 10,             # Maximum complexity per function
    'classes': 15,               # Maximum complexity per class
    'modules': 20                # Maximum complexity per module
}

# Line count limits
LINE_LIMITS = {
    'function': 50,              # Maximum lines per function
    'class': 300,                # Maximum lines per class
    'module': 500                # Maximum lines per module
}
```

#### 2. Qualitative Standards

**Code Review Checklist:**
- [ ] **Functionality** - Does code work as intended?
- [ ] **Readability** - Is code easy to understand?
- [ ] **Maintainability** - Can code be easily modified?
- [ ] **Performance** - Is code reasonably efficient?
- [ ] **Educational Value** - Does code teach good practices?
- [ ] **Campus Context** - Is code relevant untuk use cases kampus?

### Coding Standards

#### 1. Python Style Guide

**PEP 8 Compliance:**
```python
# Good: Clear, readable code dengan proper naming
class NetworkAnalyzer:
    """
    Comprehensive network analysis tool untuk campus networking education.
    
    This class provides methods untuk performing various network diagnostics
    yang commonly used dalam network administration dan troubleshooting.
    """
    
    def __init__(self, timeout: int = 5, retries: int = 3, verbose: bool = False):
        """
        Initialize network analyzer dengan specified parameters.
        
        Args:
            timeout: Network operation timeout dalam seconds
            retries: Number of retries untuk failed operations
            verbose: Enable verbose logging untuk educational purposes
        """
        self.timeout = self._validate_timeout(timeout)
        self.retries = self._validate_retries(retries)
        self.verbose = verbose
        self._logger = self._setup_logger()
        
        if self.verbose:
            self._logger.info(
                f"NetworkAnalyzer initialized: timeout={self.timeout}s, "
                f"retries={self.retries}"
            )
    
    def ping_host(
        self, 
        host: str, 
        count: int = 4, 
        packet_size: int = 32
    ) -> PingResult:
        """
        Ping target host dan return comprehensive results.
        
        Educational Context:
            Ping adalah fundamental network diagnostic tool yang sends
            ICMP Echo Request packets ke target host dan measures response time.
            Ini berguna untuk:
            - Testing basic connectivity
            - Measuring network latency
            - Identifying packet loss
            - Troubleshooting network issues
        
        Args:
            host: Target hostname atau IP address untuk ping
            count: Number of ping packets to send
            packet_size: Size of ping packets dalam bytes
            
        Returns:
            PingResult object containing comprehensive metrics
            
        Raises:
            NetworkError: If ping operation fails completely
            ValueError: If invalid parameters provided
            
        Example:
            >>> analyzer = NetworkAnalyzer(verbose=True)
            >>> result = analyzer.ping_host("polinela.ac.id", count=5)
            >>> print(f"Average latency: {result.avg_latency:.1f}ms")
            >>> print(f"Packet loss: {result.packet_loss:.1f}%")
        """
        # Validate inputs
        self._validate_host(host)
        self._validate_count(count)
        self._validate_packet_size(packet_size)
        
        if self.verbose:
            self._logger.info(f"Starting ping operation: {host}")
        
        try:
            # Perform ping operation dengan proper error handling
            result = self._execute_ping(host, count, packet_size)
            
            if self.verbose:
                self._log_ping_results(result)
            
            return result
            
        except Exception as e:
            self._logger.error(f"Ping failed for {host}: {e}")
            raise NetworkError(f"Failed to ping {host}") from e
    
    def _validate_host(self, host: str) -> None:
        """Validate host parameter dengan comprehensive checks."""
        if not host or not isinstance(host, str):
            raise ValueError("Host must be a non-empty string")
        
        if len(host) > 255:
            raise ValueError("Host name too long (max 255 characters)")
        
        # Additional validation bisa ditambahkan di sini
    
    def _validate_timeout(self, timeout: int) -> int:
        """Validate dan normalize timeout value."""
        if not isinstance(timeout, int) or timeout < 1 or timeout > 60:
            raise ValueError("Timeout must be integer between 1 and 60 seconds")
        return timeout
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logger dengan appropriate configuration."""
        logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO if self.verbose else logging.WARNING)
        
        return logger

# Bad: Poor naming, no documentation, no error handling
class na:  # Bad class name
    def __init__(self, t=5):  # Bad parameter naming
        self.t = t  # No validation
    
    def p(self, h):  # Bad method naming, no types, no docs
        import subprocess
        subprocess.run(['ping', h])  # No error handling
```

**Type Hints Best Practices:**
```python
from typing import List, Dict, Optional, Union, Protocol, TypeVar, Generic
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

# Use comprehensive type hints
T = TypeVar('T')

class Pingable(Protocol):
    """Protocol untuk objects yang can be pinged."""
    
    def ping(self, timeout: float) -> 'PingResult':
        """Ping operation protocol."""
        ...

@dataclass
class PingResult:
    """Structured ping result dengan comprehensive metrics."""
    
    host: str
    ip_address: Optional[str] = None
    packets_sent: int = 0
    packets_received: int = 0
    packet_loss: float = 0.0
    min_latency: float = 0.0
    max_latency: float = 0.0
    avg_latency: float = 0.0
    timestamp: float = field(default_factory=time.time)
    additional_metrics: Dict[str, Union[int, float, str]] = field(default_factory=dict)
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate percentage."""
        if self.packets_sent == 0:
            return 0.0
        return (self.packets_received / self.packets_sent) * 100.0
    
    def is_healthy(self, max_latency: float = 100.0, max_loss: float = 5.0) -> bool:
        """
        Determine if ping results indicate healthy connection.
        
        Args:
            max_latency: Maximum acceptable latency dalam ms
            max_loss: Maximum acceptable packet loss dalam percent
            
        Returns:
            True if connection is considered healthy
        """
        return (
            self.avg_latency <= max_latency and 
            self.packet_loss <= max_loss and
            self.packets_received > 0
        )

def analyze_multiple_hosts(
    hosts: List[str],
    analyzer: NetworkAnalyzer,
    concurrent: bool = True,
    max_workers: Optional[int] = None
) -> Dict[str, PingResult]:
    """
    Analyze multiple hosts dengan optional concurrency.
    
    Educational Context:
        This function demonstrates important concepts:
        - Concurrent programming untuk network operations
        - Resource management dengan ThreadPoolExecutor
        - Error handling dalam batch operations
        - Progress tracking untuk user feedback
    
    Args:
        hosts: List of hostnames atau IP addresses
        analyzer: NetworkAnalyzer instance untuk operations
        concurrent: Whether to use concurrent execution
        max_workers: Maximum number of worker threads
        
    Returns:
        Dictionary mapping hosts to their PingResult objects
        
    Example:
        >>> analyzer = NetworkAnalyzer()
        >>> hosts = ["google.com", "polinela.ac.id", "github.com"]
        >>> results = analyze_multiple_hosts(hosts, analyzer)
        >>> for host, result in results.items():
        ...     print(f"{host}: {result.avg_latency:.1f}ms")
    """
    if not hosts:
        return {}
    
    if not concurrent or len(hosts) == 1:
        # Sequential execution
        return {host: analyzer.ping_host(host) for host in hosts}
    
    # Concurrent execution dengan proper resource management
    import concurrent.futures
    
    max_workers = max_workers or min(len(hosts), 8)
    results: Dict[str, PingResult] = {}
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_host = {
            executor.submit(analyzer.ping_host, host): host 
            for host in hosts
        }
        
        # Collect results dengan proper error handling
        for future in concurrent.futures.as_completed(future_to_host):
            host = future_to_host[future]
            try:
                result = future.result()
                results[host] = result
            except Exception as exc:
                # Log error tetapi continue dengan other hosts
                logging.getLogger(__name__).error(
                    f"Host {host} generated exception: {exc}"
                )
                # Create failed result untuk completeness
                results[host] = PingResult(
                    host=host,
                    additional_metrics={'error': str(exc)}
                )
    
    return results
```

#### 2. Documentation Standards

**Docstring Guidelines:**
```python
def traceroute_host(
    self,
    destination: str,
    max_hops: int = 30,
    timeout: float = 5.0,
    packet_size: int = 32
) -> TracerouteResult:
    """
    Perform traceroute to destination dengan comprehensive analysis.
    
    Traceroute shows path packets take to reach destination, berguna untuk:
    - Network topology discovery
    - Identifying routing issues
    - Measuring per-hop latency
    - Understanding network infrastructure
    
    Educational Context:
        Traceroute operation demonstrates several networking concepts:
        
        1. **TTL (Time To Live)**: Each packet starts dengan TTL value yang
           decrements pada setiap router. Ketika TTL reaches 0, router sends
           ICMP Time Exceeded message back to source.
           
        2. **Routing**: Shows actual path packets take, which may differ
           dari expected shortest path due to routing policies.
           
        3. **Network Latency**: Per-hop timing helps identify slow links
           atau congested network segments.
    
    Campus Network Context:
        Dalam environment Polinela, traceroute dapat reveal:
        - Campus network topology
        - Internet gateway configuration  
        - Quality of connection ke external sites
        - Potential bottlenecks dalam campus infrastructure
    
    Args:
        destination: Target hostname atau IP address untuk traceroute
        max_hops: Maximum number of hops to trace (default: 30)
        timeout: Timeout untuk each probe dalam seconds (default: 5.0)
        packet_size: Size of probe packets dalam bytes (default: 32)
        
    Returns:
        TracerouteResult object containing:
        - List of TracerouteHop objects untuk each hop
        - Total path length dan timing
        - Network topology information
        - Analysis dan recommendations
        
    Raises:
        NetworkError: If traceroute operation fails completely
        PermissionError: If elevated privileges required (platform-specific)
        ValueError: If invalid parameters provided
        TimeoutError: If operation exceeds overall timeout
        
    Example:
        Basic traceroute operation:
        
        >>> analyzer = NetworkAnalyzer()
        >>> result = analyzer.traceroute_host("polinela.ac.id")
        >>> print(f"Path to {result.destination}:")
        >>> for hop in result.hops:
        ...     if hop.responds:
        ...         print(f"  {hop.number:2d}. {hop.address:15s} {hop.latency:6.1f}ms")
        ...     else:
        ...         print(f"  {hop.number:2d}. {'*':15s} (timeout)")
        
        Educational analysis:
        
        >>> if result.analysis:
        ...     print(f"\\nNetwork Analysis:")
        ...     print(f"- Total hops: {len(result.hops)}")
        ...     print(f"- Average per-hop latency: {result.avg_hop_latency:.1f}ms") 
        ...     print(f"- Potential issues: {result.analysis.get('issues', 'None')}")
        
    Note:
        - Traceroute may require elevated privileges pada some systems
        - Some routers/firewalls may block atau rate-limit ICMP packets
        - Results dapat vary between runs due to load balancing
        - Campus firewalls may affect external traceroute accuracy
        
    See Also:
        - ping_host(): For basic connectivity testing
        - analyze_network_path(): For comprehensive path analysis
        - Campus Network Guide: docs/campus/network_topology.md
    """
    # Implementation would go here
    pass
```

**Code Comments Best Practices:**
```python
def _parse_ping_output(self, output: str, host: str) -> PingResult:
    """Parse ping command output dan extract metrics."""
    
    # Initialize result object dengan default values
    result = PingResult(host=host)
    
    try:
        # Split output into lines untuk line-by-line processing
        lines = output.strip().split('\n')
        
        # Parse header untuk IP address extraction
        # Format: "PING google.com (172.217.168.206) 56(84) bytes of data."
        header_line = lines[0] if lines else ""
        ip_match = re.search(r'\(([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)\)', header_line)
        if ip_match:
            result.ip_address = ip_match.group(1)
        
        # Process individual ping responses
        # Format: "64 bytes from 172.217.168.206: icmp_seq=1 time=25.2 ms"
        ping_times = []
        for line in lines:
            if 'bytes from' in line and 'time=' in line:
                # Extract timing information
                time_match = re.search(r'time=([0-9]+\.?[0-9]*)', line)
                if time_match:
                    latency = float(time_match.group(1))
                    ping_times.append(latency)
                    result.packets_received += 1
        
        # Parse statistics line untuk packet loss dan timing summary
        # Format: "4 packets transmitted, 4 received, 0% packet loss, time 3005ms"
        for line in lines:
            if 'packets transmitted' in line:
                # Extract packet counts
                packets_match = re.search(
                    r'([0-9]+) packets transmitted, ([0-9]+) received', 
                    line
                )
                if packets_match:
                    result.packets_sent = int(packets_match.group(1))
                    result.packets_received = int(packets_match.group(2))
                
                # Extract packet loss percentage
                loss_match = re.search(r'([0-9]+\.?[0-9]*)% packet loss', line)
                if loss_match:
                    result.packet_loss = float(loss_match.group(1))
        
        # Parse timing statistics line
        # Format: "rtt min/avg/max/mdev = 24.8/25.0/25.2/0.2 ms"
        for line in lines:
            if 'rtt min/avg/max' in line:
                timing_match = re.search(
                    r'= ([0-9]+\.?[0-9]*)/([0-9]+\.?[0-9]*)/([0-9]+\.?[0-9]*)',
                    line
                )
                if timing_match:
                    result.min_latency = float(timing_match.group(1))
                    result.avg_latency = float(timing_match.group(2))
                    result.max_latency = float(timing_match.group(3))
        
        # Fallback: Calculate statistics dari individual ping times jika needed
        if ping_times and result.avg_latency == 0.0:
            result.min_latency = min(ping_times)
            result.max_latency = max(ping_times)
            result.avg_latency = sum(ping_times) / len(ping_times)
        
        # Validate dan ensure data consistency
        if result.packets_sent > 0:
            calculated_loss = (
                (result.packets_sent - result.packets_received) / result.packets_sent
            ) * 100.0
            
            # Use calculated loss jika parsed value seems incorrect
            if abs(result.packet_loss - calculated_loss) > 1.0:
                result.packet_loss = calculated_loss
        
        return result
        
    except Exception as e:
        # Log parsing error untuk debugging
        self._logger.error(f"Error parsing ping output for {host}: {e}")
        self._logger.debug(f"Raw output: {output}")
        
        # Return minimal result dengan error indication
        return PingResult(
            host=host,
            additional_metrics={'parse_error': str(e)}
        )
```

### Code Analysis Tools

#### 1. Static Analysis Configuration

**Flake8 Configuration:**
```ini
# .flake8
[flake8]
max-line-length = 88
max-complexity = 10
exclude = 
    .git,
    __pycache__,
    build,
    dist,
    .venv,
    venv,
    .tox,
    *.egg-info,
    migrations

# Error codes to ignore
extend-ignore = 
    E203,  # Whitespace before ':' (conflicts dengan black)
    W503,  # Line break before binary operator (outdated)
    E501   # Line too long (handled by black)

# Per-file ignores
per-file-ignores =
    __init__.py: F401, F403  # Allow unused imports dalam __init__.py
    tests/*: S101, D103      # Allow assert statements dan missing docstrings dalam tests
    examples/*: D100, D103   # Relaxed documentation requirements untuk examples

# Docstring requirements
docstring-convention = google
```

**Pylint Configuration:**
```ini
# .pylintrc
[MASTER]
extension-pkg-whitelist = pydantic

[MESSAGES CONTROL]
disable = 
    C0111,  # Missing docstring
    R0903,  # Too few public methods
    R0913,  # Too many arguments
    W0613,  # Unused argument (common dalam educational examples)

[FORMAT]
max-line-length = 88
max-module-lines = 500

[DESIGN]
max-args = 7
max-locals = 15
max-returns = 6
max-branches = 12
max-statements = 50

[SIMILARITIES]
min-similarity-lines = 4
ignore-comments = yes
ignore-docstrings = yes
```

**MyPy Configuration:**
```ini
# mypy.ini
[mypy]
python_version = 3.7
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
disallow_incomplete_defs = True
check_untyped_defs = True
disallow_untyped_decorators = True
no_implicit_optional = True
warn_redundant_casts = True
warn_unused_ignores = True
warn_no_return = True
warn_unreachable = True
strict_equality = True
show_error_codes = True

# Allow some flexibility untuk educational code
[mypy-examples.*]
disallow_untyped_defs = False
disallow_incomplete_defs = False

[mypy-tests.*]
disallow_untyped_defs = False

# Third-party libraries tanpa stubs
[mypy-scapy.*]
ignore_missing_imports = True

[mypy-paramiko.*]
ignore_missing_imports = True

[mypy-psutil.*]
ignore_missing_imports = True
```

#### 2. Security Analysis

**Bandit Configuration:**
```yaml
# .bandit
skips: ['B101', 'B601']  # Skip assert_used dan shell_injection untuk educational code

tests: ['B102', 'B103', 'B104', 'B105', 'B106', 'B107', 'B108', 'B109', 'B110', 'B111', 'B112', 'B201', 'B301', 'B302', 'B303', 'B304', 'B305', 'B306', 'B307', 'B308', 'B309', 'B310', 'B311', 'B312', 'B313', 'B314', 'B315', 'B316', 'B317', 'B318', 'B319', 'B320', 'B321', 'B322', 'B323', 'B324', 'B325', 'B401', 'B402', 'B403', 'B404', 'B405', 'B406', 'B407', 'B408', 'B409', 'B410', 'B411', 'B412', 'B413', 'B501', 'B502', 'B503', 'B504', 'B505', 'B506', 'B507', 'B601', 'B602', 'B603', 'B604', 'B605', 'B606', 'B607', 'B608', 'B609', 'B610', 'B611', 'B701', 'B702', 'B703']

exclude_dirs: ['tests', 'venv', '.venv']
```

**Security Best Practices:**
```python
import hashlib
import secrets
import logging
from typing import Optional

class SecureNetworkAnalyzer:
    """Network analyzer dengan security best practices."""
    
    def __init__(self, api_key: Optional[str] = None):
        # Store sensitive data securely
        self._api_key = self._validate_api_key(api_key) if api_key else None
        
        # Setup secure logging (avoid logging sensitive data)
        self._logger = self._setup_secure_logger()
        
        # Input validation patterns
        self._valid_ip_pattern = re.compile(
            r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}'
            r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        )
        self._valid_hostname_pattern = re.compile(
            r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?'
            r'(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
        )
    
    def _validate_api_key(self, api_key: str) -> str:
        """Validate API key dengan secure practices."""
        if not isinstance(api_key, str):
            raise ValueError("API key must be string")
        
        if len(api_key) < 32:
            raise ValueError("API key too short (minimum 32 characters)")
        
        # Hash API key untuk storage (never store plain text)
        hashed_key = hashlib.sha256(api_key.encode()).hexdigest()
        return hashed_key
    
    def _setup_secure_logger(self) -> logging.Logger:
        """Setup logger yang tidak log sensitive information."""
        logger = logging.getLogger(f"{__name__}.secure")
        
        # Create custom formatter yang masks sensitive data
        class SecureFormatter(logging.Formatter):
            def format(self, record):
                # Mask potential sensitive data dalam log messages
                message = super().format(record)
                
                # Mask IP addresses dalam private ranges (untuk privacy)
                message = re.sub(
                    r'\b192\.168\.\d{1,3}\.\d{1,3}\b',
                    'XXX.XXX.XXX.XXX',
                    message
                )
                
                # Mask potential API keys atau passwords
                message = re.sub(
                    r'(?i)(key|password|token|secret)[:=]\s*\S+',
                    r'\1: [MASKED]',
                    message
                )
                
                return message
        
        handler = logging.StreamHandler()
        handler.setFormatter(SecureFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        
        return logger
    
    def validate_host_input(self, host: str) -> str:
        """
        Validate host input untuk prevent injection attacks.
        
        Security Considerations:
            - Prevent command injection dalam subprocess calls
            - Validate format untuk avoid malformed requests
            - Limit input length untuk prevent buffer overflow
            - Sanitize special characters
        """
        if not host or not isinstance(host, str):
            raise ValueError("Host must be non-empty string")
        
        # Length validation
        if len(host) > 253:  # RFC 1035 limit
            raise ValueError("Host name too long")
        
        # Character validation untuk prevent command injection
        if any(char in host for char in ['`', '$', ';', '|', '&', '<', '>']):
            raise ValueError("Host contains invalid characters")
        
        # Format validation
        if not (self._valid_ip_pattern.match(host) or 
                self._valid_hostname_pattern.match(host)):
            raise ValueError("Invalid host format")
        
        return host.lower().strip()
    
    def secure_subprocess_call(self, command: List[str], timeout: int = 30) -> str:
        """
        Execute subprocess dengan security best practices.
        
        Security Features:
            - Command validation untuk prevent injection
            - Timeout untuk prevent hanging processes
            - Output sanitization
            - Error handling yang doesn't expose system info
        """
        import subprocess
        import shlex
        
        # Validate command components
        if not command or not all(isinstance(arg, str) for arg in command):
            raise ValueError("Invalid command format")
        
        # Log command execution (securely)
        safe_command = [shlex.quote(arg) for arg in command]
        self._logger.info(f"Executing command: {' '.join(safe_command)}")
        
        try:
            # Execute dengan security constraints
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,  # Don't raise untuk non-zero exit codes
                shell=False   # Never use shell=True untuk security
            )
            
            # Sanitize output sebelum return
            output = result.stdout.strip()
            
            # Remove potential sensitive information dari output
            output = re.sub(
                r'(?i)(password|key|token|secret)[:=]\s*\S+',
                r'\1: [MASKED]',
                output
            )
            
            return output
            
        except subprocess.TimeoutExpired:
            self._logger.warning(f"Command timeout after {timeout} seconds")
            raise TimeoutError(f"Command execution timeout")
        
        except subprocess.SubprocessError as e:
            self._logger.error(f"Subprocess error: {type(e).__name__}")
            raise NetworkError("Network operation failed") from e
```

### Performance Guidelines

#### 1. Performance Monitoring

**Performance Profiling:**
```python
import cProfile
import pstats
import functools
import time
from typing import Callable, Any

def profile_performance(func: Callable) -> Callable:
    """
    Decorator untuk profile function performance.
    
    Educational Purpose:
        Demonstrates performance monitoring techniques yang essential
        untuk network applications yang must handle multiple operations
        efficiently.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        # Memory profiling
        import psutil
        import os
        process = psutil.Process(os.getpid())
        start_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # CPU profiling
        profiler = cProfile.Profile()
        profiler.enable()
        
        # Time profiling
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            success = True
        except Exception as e:
            result = None
            success = False
            raise
        finally:
            # Stop profiling
            end_time = time.time()
            profiler.disable()
            
            # Memory measurement
            end_memory = process.memory_info().rss / 1024 / 1024
            memory_delta = end_memory - start_memory
            
            # Generate performance report
            execution_time = end_time - start_time
            
            # Log performance metrics
            logger = logging.getLogger(__name__)
            logger.info(
                f"Performance: {func.__name__} - "
                f"Time: {execution_time:.3f}s, "
                f"Memory: {memory_delta:+.1f}MB, "
                f"Success: {success}"
            )
            
            # Optional: Save detailed profile untuk analysis
            if execution_time > 1.0:  # Only untuk slow operations
                stats = pstats.Stats(profiler)
                stats.sort_stats('cumulative')
                # stats.print_stats(10)  # Uncomment untuk debugging
        
        return result
    
    return wrapper

class PerformanceOptimizedAnalyzer:
    """Network analyzer optimized untuk performance."""
    
    def __init__(self):
        self._dns_cache = {}
        self._connection_pool = {}
        self._last_cache_clear = time.time()
        
    @profile_performance
    def ping_host_optimized(self, host: str, count: int = 4) -> PingResult:
        """Optimized ping implementation dengan caching dan batching."""
        
        # DNS caching untuk avoid repeated lookups
        if host not in self._dns_cache:
            self._dns_cache[host] = self._resolve_hostname(host)
        
        # Clear cache periodically untuk avoid stale data
        if time.time() - self._last_cache_clear > 300:  # 5 minutes
            self._dns_cache.clear()
            self._last_cache_clear = time.time()
        
        # Actual ping operation
        return self._execute_optimized_ping(host, count)
    
    def _execute_optimized_ping(self, host: str, count: int) -> PingResult:
        """Execute ping dengan optimizations."""
        
        # Use cached DNS result
        ip_address = self._dns_cache.get(host)
        
        # Batch multiple pings untuk efficiency
        if count > 1:
            return self._batch_ping(host, count)
        else:
            return self._single_ping(host)
```

#### 2. Memory Management

**Memory Efficient Data Structures:**
```python
import array
from collections import deque
from typing import Iterator
import gc

class MemoryEfficientResultStore:
    """Memory-efficient storage untuk network analysis results."""
    
    def __init__(self, max_results: int = 10000):
        self.max_results = max_results
        
        # Use memory-efficient data structures
        self._timestamps = array.array('d')  # Double precision timestamps
        self._latencies = array.array('f')   # Single precision latencies
        self._packet_losses = array.array('f')  # Single precision percentages
        self._hosts = deque(maxlen=max_results)  # Automatic size limiting
        
        # Metadata
        self._result_count = 0
    
    def add_result(self, result: PingResult) -> None:
        """Add result dengan memory management."""
        
        # Check memory limits
        if self._result_count >= self.max_results:
            self._cleanup_old_results()
        
        # Store data efficiently
        self._timestamps.append(result.timestamp)
        self._latencies.append(result.avg_latency)
        self._packet_losses.append(result.packet_loss)
        self._hosts.append(result.host)
        
        self._result_count += 1
        
        # Periodic garbage collection untuk memory optimization
        if self._result_count % 1000 == 0:
            gc.collect()
    
    def _cleanup_old_results(self) -> None:
        """Clean up old results untuk free memory."""
        
        # Remove oldest 10% of results
        cleanup_count = self.max_results // 10
        
        # Remove dari arrays (more complex, so implement carefully)
        if len(self._timestamps) > cleanup_count:
            # Convert to list, slice, convert back (expensive but necessary)
            timestamps_list = list(self._timestamps)[cleanup_count:]
            latencies_list = list(self._latencies)[cleanup_count:]
            losses_list = list(self._packet_losses)[cleanup_count:]
            
            # Clear dan repopulate arrays
            self._timestamps = array.array('d', timestamps_list)
            self._latencies = array.array('f', latencies_list)
            self._packet_losses = array.array('f', losses_list)
        
        self._result_count = len(self._timestamps)
    
    def get_statistics(self) -> Dict[str, float]:
        """Calculate statistics efficiently."""
        if not self._latencies:
            return {}
        
        return {
            'avg_latency': sum(self._latencies) / len(self._latencies),
            'min_latency': min(self._latencies),
            'max_latency': max(self._latencies),
            'avg_packet_loss': sum(self._packet_losses) / len(self._packet_losses),
            'total_results': len(self._latencies)
        }
    
    def iter_recent_results(self, count: int = 100) -> Iterator[Dict[str, Any]]:
        """Iterate over recent results memory-efficiently."""
        
        # Get recent indices
        start_idx = max(0, len(self._timestamps) - count)
        
        for i in range(start_idx, len(self._timestamps)):
            yield {
                'timestamp': self._timestamps[i],
                'host': self._hosts[i] if i < len(self._hosts) else 'unknown',
                'latency': self._latencies[i],
                'packet_loss': self._packet_losses[i]
            }
```

### Educational Quality

#### 1. Code Documentation for Learning

**Educational Comments:**
```python
def calculate_network_statistics(results: List[PingResult]) -> NetworkStatistics:
    """
    Calculate comprehensive network statistics dari ping results.
    
    Educational Purpose:
        This function demonstrates several important statistical concepts
        yang commonly used dalam network analysis dan performance monitoring:
        
        1. **Descriptive Statistics**: Mean, median, standard deviation
        2. **Percentiles**: P95, P99 untuk performance analysis
        3. **Data Quality**: Handling missing atau invalid data
        4. **Trend Analysis**: Identifying patterns dalam network performance
    
    Network Analysis Context:
        - Latency statistics help identify network performance characteristics
        - Packet loss patterns indicate network reliability issues
        - Jitter measurements show network stability
        - Trend analysis helps predict future performance
    """
    
    if not results:
        return NetworkStatistics()  # Return empty statistics
    
    # Extract latency data (skip failed pings)
    # Educational Note: Always validate data sebelum statistical analysis
    valid_latencies = [
        r.avg_latency for r in results 
        if r.packets_received > 0 and r.avg_latency > 0
    ]
    
    if not valid_latencies:
        return NetworkStatistics(error="No valid latency data")
    
    # Basic descriptive statistics
    # Educational Note: These are fundamental statistics untuk any dataset
    mean_latency = statistics.mean(valid_latencies)
    median_latency = statistics.median(valid_latencies)
    
    # Standard deviation measures variability (jitter dalam network terms)
    # Educational Note: High standard deviation indicates inconsistent performance
    if len(valid_latencies) > 1:
        std_dev = statistics.stdev(valid_latencies)
        # Coefficient of variation (CV) normalizes standard deviation
        # CV > 0.3 typically indicates high variability
        cv = std_dev / mean_latency if mean_latency > 0 else 0
    else:
        std_dev = 0.0
        cv = 0.0
    
    # Percentile analysis untuk performance characterization
    # Educational Note: P95 means 95% of measurements are below this value
    sorted_latencies = sorted(valid_latencies)
    p50 = statistics.median(sorted_latencies)  # Same as median
    p95 = sorted_latencies[int(0.95 * len(sorted_latencies))]
    p99 = sorted_latencies[int(0.99 * len(sorted_latencies))]
    
    # Packet loss analysis
    # Educational Note: Packet loss is critical quality metric
    total_packets_sent = sum(r.packets_sent for r in results)
    total_packets_received = sum(r.packets_received for r in results)
    overall_packet_loss = 0.0
    
    if total_packets_sent > 0:
        overall_packet_loss = (
            (total_packets_sent - total_packets_received) / total_packets_sent
        ) * 100.0
    
    # Network quality assessment
    # Educational Note: These thresholds are industry standards
    quality_assessment = _assess_network_quality(
        mean_latency, overall_packet_loss, cv
    )
    
    # Trend analysis (if timestamps available)
    # Educational Note: Trend analysis helps predict future performance
    trend_analysis = _analyze_latency_trends(results)
    
    return NetworkStatistics(
        # Basic statistics
        mean_latency=mean_latency,
        median_latency=median_latency,
        std_dev_latency=std_dev,
        coefficient_of_variation=cv,
        
        # Percentiles
        p50_latency=p50,
        p95_latency=p95,
        p99_latency=p99,
        
        # Packet loss
        overall_packet_loss=overall_packet_loss,
        
        # Quality assessment
        quality_score=quality_assessment.score,
        quality_rating=quality_assessment.rating,
        recommendations=quality_assessment.recommendations,
        
        # Trend analysis
        trend=trend_analysis.direction,
        trend_confidence=trend_analysis.confidence,
        
        # Metadata
        sample_size=len(valid_latencies),
        analysis_timestamp=time.time()
    )

def _assess_network_quality(
    mean_latency: float, 
    packet_loss: float, 
    cv: float
) -> QualityAssessment:
    """
    Assess network quality berdasarkan metrics.
    
    Educational Context:
        Network quality assessment menggunakan industry standards:
        
        Latency Categories (for internet connections):
        - Excellent: < 20ms
        - Good: 20-50ms  
        - Fair: 50-100ms
        - Poor: > 100ms
        
        Packet Loss Categories:
        - Excellent: < 0.1%
        - Good: 0.1-1%
        - Fair: 1-5%
        - Poor: > 5%
        
        Variability (CV) Categories:
        - Stable: < 0.2
        - Moderate: 0.2-0.5
        - Variable: > 0.5
    """
    
    score = 100  # Start dengan perfect score
    recommendations = []
    
    # Latency scoring
    if mean_latency > 100:
        score -= 40
        recommendations.append("High latency detected - check network path")
    elif mean_latency > 50:
        score -= 20
        recommendations.append("Moderate latency - monitor for improvement")
    elif mean_latency > 20:
        score -= 10
    
    # Packet loss scoring
    if packet_loss > 5:
        score -= 30
        recommendations.append("High packet loss - investigate network issues")
    elif packet_loss > 1:
        score -= 15
        recommendations.append("Moderate packet loss - monitor closely")
    elif packet_loss > 0.1:
        score -= 5
    
    # Variability scoring
    if cv > 0.5:
        score -= 20
        recommendations.append("High variability - unstable connection")
    elif cv > 0.2:
        score -= 10
        recommendations.append("Moderate variability - check for congestion")
    
    # Determine rating
    if score >= 90:
        rating = "Excellent"
    elif score >= 75:
        rating = "Good"
    elif score >= 50:
        rating = "Fair"
    else:
        rating = "Poor"
    
    return QualityAssessment(
        score=max(0, score),
        rating=rating,
        recommendations=recommendations
    )
```

### Campus-Specific Quality Standards

#### 1. Educational Code Examples

**Campus Use Case Implementation:**
```python
class PolitelaNetworkQualityMonitor:
    """
    Network quality monitor specific untuk Politeknik Negeri Lampung.
    
    Educational Context:
        This class demonstrates practical application of network monitoring
        dalam campus environment, incorporating:
        
        - Campus network topology understanding
        - Educational use cases (lab exercises, research)
        - Integration dengan campus infrastructure
        - Student-friendly reporting dan analysis
    """
    
    def __init__(self):
        self.campus_config = self._load_campus_configuration()
        self.quality_standards = self._define_campus_quality_standards()
        self.educational_contexts = self._setup_educational_contexts()
    
    def _define_campus_quality_standards(self) -> Dict[str, Dict[str, float]]:
        """
        Define quality standards specific untuk campus environment.
        
        Educational Note:
            Campus networks have different requirements dibanding
            commercial environments:
            - Educational applications need consistent performance
            - Research activities may require higher quality
            - Student access should be fair dan reliable
        """
        return {
            'academic_network': {
                'max_latency': 50.0,      # Academic work needs responsiveness
                'max_packet_loss': 1.0,   # Research data integrity important
                'min_availability': 99.0  # High uptime untuk academic schedules
            },
            'student_network': {
                'max_latency': 100.0,     # More lenient untuk general use
                'max_packet_loss': 3.0,   # Acceptable untuk web browsing
                'min_availability': 95.0  # Good uptime dengan maintenance windows
            },
            'admin_network': {
                'max_latency': 20.0,      # Administrative work needs speed
                'max_packet_loss': 0.5,   # Critical operations need reliability
                'min_availability': 99.5  # Very high uptime untuk operations
            },
            'guest_network': {
                'max_latency': 200.0,     # Basic connectivity sufficient
                'max_packet_loss': 5.0,   # More tolerant untuk visitor use
                'min_availability': 90.0  # Basic service level
            }
        }
    
    def assess_lab_network_quality(
        self, 
        lab_name: str, 
        results: List[PingResult]
    ) -> LabQualityReport:
        """
        Assess network quality untuk specific lab environment.
        
        Educational Purpose:
            Lab network assessment helps:
            - Ensure optimal learning environment
            - Identify issues affecting lab exercises
            - Provide data untuk network improvement
            - Teach students about network performance metrics
        """
        
        # Determine lab network segment
        segment = self._identify_lab_segment(lab_name)
        standards = self.quality_standards.get(segment, self.quality_standards['student_network'])
        
        # Calculate comprehensive statistics
        stats = calculate_network_statistics(results)
        
        # Apply campus-specific analysis
        campus_assessment = self._assess_against_campus_standards(stats, standards)
        
        # Generate educational insights
        educational_insights = self._generate_educational_insights(stats, lab_name)
        
        # Create student-friendly report
        student_report = self._create_student_friendly_report(
            stats, campus_assessment, educational_insights
        )
        
        return LabQualityReport(
            lab_name=lab_name,
            network_segment=segment,
            statistics=stats,
            campus_assessment=campus_assessment,
            educational_insights=educational_insights,
            student_report=student_report,
            timestamp=time.time()
        )
    
    def _generate_educational_insights(
        self, 
        stats: NetworkStatistics, 
        lab_name: str
    ) -> EducationalInsights:
        """
        Generate insights yang valuable untuk educational purposes.
        
        Educational Context:
            These insights help students understand:
            - How network performance affects applications
            - What different metrics mean dalam real-world context
            - How to interpret performance data
            - Best practices untuk network troubleshooting
        """
        
        insights = EducationalInsights()
        
        # Latency insights
        if stats.mean_latency < 20:
            insights.add_insight(
                category="latency",
                level="positive",
                message=(
                    f"Excellent latency ({stats.mean_latency:.1f}ms) - "
                    "Perfect untuk real-time applications seperti video calls "
                    "dan interactive learning tools."
                ),
                learning_point=(
                    "Low latency adalah critical untuk interactive applications. "
                    "Latency under 20ms provides excellent user experience."
                )
            )
        elif stats.mean_latency > 100:
            insights.add_insight(
                category="latency",
                level="concern",
                message=(
                    f"High latency ({stats.mean_latency:.1f}ms) - "
                    "Ini dapat affect responsiveness dari web applications "
                    "dan make lab exercises frustrating."
                ),
                learning_point=(
                    "High latency dapat disebabkan oleh network congestion, "
                    "routing issues, atau overloaded servers. Troubleshooting "
                    "should focus pada identifying bottlenecks dalam network path."
                )
            )
        
        # Variability insights
        if stats.coefficient_of_variation > 0.5:
            insights.add_insight(
                category="stability",
                level="concern", 
                message=(
                    f"High variability (CV: {stats.coefficient_of_variation:.2f}) - "
                    "Network performance tidak consistent, yang dapat disrupt "
                    "streaming video atau file downloads."
                ),
                learning_point=(
                    "Network variability (jitter) indicates unstable connection. "
                    "This dapat disebabkan oleh varying network load, "
                    "interference, atau routing changes."
                )
            )
        
        # Campus-specific insights
        insights.add_campus_context(
            lab_name=lab_name,
            context=(
                f"Untuk {lab_name}, optimal network performance supports "
                "effective learning dan research activities. Monitor these "
                "metrics regularly untuk ensure consistent educational experience."
            )
        )
        
        return insights
```

### Automation Tools

#### 1. Quality Automation Scripts

**Pre-commit Quality Checks:**
```bash
#!/bin/bash
# scripts/quality_check.sh

echo "🔍 Running NetDiag Quality Checks..."

# Code formatting
echo "📝 Checking code formatting..."
black --check netdiag/ || exit 1

# Import sorting
echo "📦 Checking import order..."
isort --check-only netdiag/ || exit 1

# Linting
echo "🔎 Running linter..."
flake8 netdiag/ || exit 1

# Type checking
echo "🏷️  Checking types..."
mypy netdiag/ || exit 1

# Security check
echo "🔒 Security scan..."
bandit -r netdiag/ || exit 1

# Tests
echo "🧪 Running tests..."
pytest tests/unit/ --cov=netdiag --cov-fail-under=80 || exit 1

echo "✅ All quality checks passed!"
```

#### 2. Continuous Quality Monitoring

**Quality Metrics Collection:**
```python
# scripts/collect_quality_metrics.py
"""Collect dan report code quality metrics."""

import subprocess
import json
import os
from datetime import datetime

def collect_coverage_metrics():
    """Collect test coverage metrics."""
    result = subprocess.run(
        ['pytest', '--cov=netdiag', '--cov-report=json'],
        capture_output=True,
        text=True
    )
    
    if os.path.exists('coverage.json'):
        with open('coverage.json', 'r') as f:
            coverage_data = json.load(f)
        return {
            'total_coverage': coverage_data['totals']['percent_covered'],
            'lines_covered': coverage_data['totals']['covered_lines'],
            'lines_missing': coverage_data['totals']['missing_lines']
        }
    return {}

def collect_complexity_metrics():
    """Collect code complexity metrics."""
    result = subprocess.run(
        ['flake8', '--max-complexity=10', '--statistics', 'netdiag/'],
        capture_output=True,
        text=True
    )
    
    # Parse complexity violations
    violations = []
    for line in result.stdout.split('\n'):
        if 'C901' in line:  # Complexity violation
            violations.append(line.strip())
    
    return {
        'complexity_violations': len(violations),
        'details': violations
    }

def generate_quality_report():
    """Generate comprehensive quality report."""
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'coverage': collect_coverage_metrics(),
        'complexity': collect_complexity_metrics(),
        'version': get_project_version()
    }
    
    # Save report
    with open('quality_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    # Print summary
    print("📊 NetDiag Quality Report")
    print(f"📅 Generated: {report['timestamp']}")
    print(f"📈 Coverage: {report['coverage'].get('total_coverage', 'N/A')}%")
    print(f"🔀 Complexity Issues: {report['complexity']['complexity_violations']}")
    
    return report

if __name__ == "__main__":
    generate_quality_report()
```

### Conclusion

Maintaining high code quality dalam NetDiag requires:

1. **Comprehensive Standards** - Clear guidelines untuk code style, documentation, dan testing
2. **Automation Tools** - Automated checks untuk consistency dan quality
3. **Educational Focus** - Code yang serves sebagai learning resource
4. **Campus Context** - Standards yang appropriate untuk academic environment
5. **Continuous Improvement** - Regular review dan improvement dari quality processes

Code quality bukan hanya tentang functional correctness, tetapi juga tentang creating codebase yang educational, maintainable, dan valuable untuk community pembelajaran di Politeknik Negeri Lampung.