# Konfigurasi Lanjutan NetDiag

## ⚙️ Pengaturan dan Kustomisasi Sistem

### Struktur Konfigurasi

#### File Konfigurasi Utama
```python
# config/netdiag_config.py
import os
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class NetworkConfig:
    """Konfigurasi untuk operasi jaringan"""
    default_timeout: int = 5
    max_retries: int = 3
    concurrent_threads: int = 4
    dns_servers: List[str] = None
    
    def __post_init__(self):
        if self.dns_servers is None:
            self.dns_servers = ["8.8.8.8", "8.8.4.4", "1.1.1.1"]

@dataclass
class DatabaseConfig:
    """Konfigurasi database"""
    db_path: str = "netdiag_results.db"
    connection_pool_size: int = 5
    backup_interval: int = 3600  # seconds
    max_log_entries: int = 100000

@dataclass
class LoggingConfig:
    """Konfigurasi logging"""
    log_level: str = "INFO"
    log_file: str = "netdiag.log"
    max_file_size: int = 10485760  # 10MB
    backup_count: int = 5
    console_output: bool = True

@dataclass
class CampusConfig:
    """Konfigurasi khusus kampus Polinela"""
    campus_domain: str = "polinela.ac.id"
    network_segments: List[str] = None
    critical_services: List[str] = None
    monitoring_intervals: Dict[str, int] = None
    
    def __post_init__(self):
        if self.network_segments is None:
            self.network_segments = [
                "192.168.1.0/24",  # Administrative
                "192.168.2.0/24",  # Academic
                "192.168.3.0/24",  # Student
                "192.168.4.0/24"   # Guest
            ]
        
        if self.critical_services is None:
            self.critical_services = [
                "mail.polinela.ac.id",
                "elearning.polinela.ac.id",
                "library.polinela.ac.id",
                "portal.polinela.ac.id"
            ]
        
        if self.monitoring_intervals is None:
            self.monitoring_intervals = {
                "ping": 30,      # seconds
                "dns": 300,      # 5 minutes
                "http": 60,      # 1 minute
                "bandwidth": 900 # 15 minutes
            }

class NetDiagConfig:
    """Main configuration class"""
    def __init__(self, config_file: Optional[str] = None):
        self.network = NetworkConfig()
        self.database = DatabaseConfig()
        self.logging = LoggingConfig()
        self.campus = CampusConfig()
        
        if config_file:
            self.load_from_file(config_file)
    
    def load_from_file(self, config_file: str):
        """Load configuration from file"""
        # Implementation untuk load dari JSON/YAML
        pass
    
    def save_to_file(self, config_file: str):
        """Save current configuration to file"""
        # Implementation untuk save ke JSON/YAML
        pass
```

#### Environment-Based Configuration
```python
# config/environment.py
import os
from enum import Enum

class Environment(Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"
    CAMPUS = "campus"

class EnvironmentConfig:
    """Configuration berdasarkan environment"""
    
    @staticmethod
    def get_config(env: Environment = None) -> NetDiagConfig:
        if env is None:
            env_str = os.getenv('NETDIAG_ENV', 'development')
            env = Environment(env_str)
        
        config = NetDiagConfig()
        
        if env == Environment.DEVELOPMENT:
            config.logging.log_level = "DEBUG"
            config.logging.console_output = True
            config.network.concurrent_threads = 2
        
        elif env == Environment.TESTING:
            config.database.db_path = ":memory:"
            config.logging.log_level = "WARNING"
            config.network.default_timeout = 1
        
        elif env == Environment.PRODUCTION:
            config.logging.log_level = "ERROR"
            config.logging.console_output = False
            config.network.concurrent_threads = 8
            config.database.backup_interval = 1800
        
        elif env == Environment.CAMPUS:
            config.logging.log_level = "INFO"
            config.network.concurrent_threads = 6
            config.campus.campus_domain = "polinela.ac.id"
        
        return config

# Usage
config = EnvironmentConfig.get_config(Environment.CAMPUS)
```

### Konfigurasi Database

#### SQLite Configuration
```python
# config/database_setup.py
import sqlite3
import os
from pathlib import Path

class DatabaseSetup:
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.db_path = Path(config.db_path)
        self.ensure_database_exists()
    
    def ensure_database_exists(self):
        """Pastikan database dan tabel sudah ada"""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            self.create_tables(conn)
            self.create_indexes(conn)
    
    def create_tables(self, conn: sqlite3.Connection):
        """Buat tabel-tabel yang diperlukan"""
        
        # Tabel untuk hasil ping
        conn.execute("""
            CREATE TABLE IF NOT EXISTS ping_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                host TEXT NOT NULL,
                ip_address TEXT,
                packet_loss REAL,
                min_latency REAL,
                max_latency REAL,
                avg_latency REAL,
                packets_sent INTEGER,
                packets_received INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabel untuk traceroute
        conn.execute("""
            CREATE TABLE IF NOT EXISTS traceroute_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                destination TEXT NOT NULL,
                hop_number INTEGER,
                hop_ip TEXT,
                hop_hostname TEXT,
                latency REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabel untuk DNS queries
        conn.execute("""
            CREATE TABLE IF NOT EXISTS dns_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                domain TEXT NOT NULL,
                query_type TEXT,
                response_time REAL,
                record_type TEXT,
                record_value TEXT,
                authoritative BOOLEAN,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabel untuk monitoring bandwidth
        conn.execute("""
            CREATE TABLE IF NOT EXISTS bandwidth_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                interface TEXT,
                download_speed REAL,
                upload_speed REAL,
                bytes_sent INTEGER,
                bytes_received INTEGER,
                duration REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabel untuk konfigurasi sistem
        conn.execute("""
            CREATE TABLE IF NOT EXISTS system_config (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                config_key TEXT UNIQUE NOT NULL,
                config_value TEXT,
                config_type TEXT,
                description TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    
    def create_indexes(self, conn: sqlite3.Connection):
        """Buat index untuk optimasi query"""
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_ping_timestamp ON ping_results(timestamp)",
            "CREATE INDEX IF NOT EXISTS idx_ping_host ON ping_results(host)",
            "CREATE INDEX IF NOT EXISTS idx_traceroute_dest ON traceroute_results(destination)",
            "CREATE INDEX IF NOT EXISTS idx_dns_domain ON dns_results(domain)",
            "CREATE INDEX IF NOT EXISTS idx_bandwidth_timestamp ON bandwidth_results(timestamp)"
        ]
        
        for index_sql in indexes:
            conn.execute(index_sql)
    
    def initialize_default_config(self):
        """Initialize konfigurasi default"""
        default_configs = [
            ('ping_timeout', '5', 'int', 'Default ping timeout in seconds'),
            ('max_concurrent_threads', '4', 'int', 'Maximum concurrent threads'),
            ('log_retention_days', '30', 'int', 'Log retention period in days'),
            ('campus_domain', 'polinela.ac.id', 'str', 'Primary campus domain'),
            ('dns_servers', '8.8.8.8,8.8.4.4', 'list', 'DNS servers list'),
        ]
        
        with sqlite3.connect(self.db_path) as conn:
            for key, value, config_type, description in default_configs:
                conn.execute("""
                    INSERT OR IGNORE INTO system_config 
                    (config_key, config_value, config_type, description)
                    VALUES (?, ?, ?, ?)
                """, (key, value, config_type, description))
```

### Konfigurasi Logging

#### Advanced Logging Setup
```python
# config/logging_setup.py
import logging
import logging.handlers
import json
from pathlib import Path

class NetDiagLogger:
    def __init__(self, config: LoggingConfig):
        self.config = config
        self.setup_logging()
    
    def setup_logging(self):
        """Setup comprehensive logging configuration"""
        
        # Create logs directory
        log_path = Path(self.config.log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Root logger configuration
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, self.config.log_level))
        
        # Clear existing handlers
        root_logger.handlers.clear()
        
        # File handler dengan rotation
        file_handler = logging.handlers.RotatingFileHandler(
            self.config.log_file,
            maxBytes=self.config.max_file_size,
            backupCount=self.config.backup_count
        )
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        if self.config.console_output:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(getattr(logging, self.config.log_level))
            
            # Console formatter (simplified)
            console_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%H:%M:%S'
            )
            console_handler.setFormatter(console_formatter)
            root_logger.addHandler(console_handler)
        
        # File formatter (detailed)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)
        
        # Error handler untuk error yang critical
        error_handler = logging.handlers.RotatingFileHandler(
            str(log_path.parent / 'errors.log'),
            maxBytes=self.config.max_file_size,
            backupCount=3
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(file_formatter)
        root_logger.addHandler(error_handler)
        
        # JSON handler untuk structured logging
        json_handler = logging.handlers.RotatingFileHandler(
            str(log_path.parent / 'structured.log'),
            maxBytes=self.config.max_file_size,
            backupCount=self.config.backup_count
        )
        json_handler.setLevel(logging.INFO)
        json_handler.setFormatter(JSONFormatter())
        root_logger.addHandler(json_handler)

class JSONFormatter(logging.Formatter):
    """JSON formatter untuk structured logging"""
    
    def format(self, record):
        log_entry = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Add exception info if present
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)
        
        # Add extra fields if present
        if hasattr(record, 'host'):
            log_entry['host'] = record.host
        if hasattr(record, 'latency'):
            log_entry['latency'] = record.latency
        if hasattr(record, 'operation'):
            log_entry['operation'] = record.operation
        
        return json.dumps(log_entry)

# Usage
logger_setup = NetDiagLogger(config.logging)
logger = logging.getLogger(__name__)

# Contoh logging dengan extra context
logger.info("Ping completed", extra={
    'host': 'polinela.ac.id',
    'latency': 25.5,
    'operation': 'ping'
})
```

### Konfigurasi Jaringan

#### Network Interface Configuration
```python
# config/network_config.py
import psutil
import socket
from typing import List, Dict

class NetworkInterfaceConfig:
    def __init__(self, config: NetworkConfig):
        self.config = config
        self.interfaces = self.discover_interfaces()
    
    def discover_interfaces(self) -> Dict[str, dict]:
        """Discover semua network interfaces"""
        interfaces = {}
        
        for interface_name, addresses in psutil.net_if_addrs().items():
            interface_info = {
                'name': interface_name,
                'addresses': [],
                'stats': None
            }
            
            # Get addresses
            for addr in addresses:
                if addr.family == socket.AF_INET:  # IPv4
                    interface_info['addresses'].append({
                        'type': 'IPv4',
                        'address': addr.address,
                        'netmask': addr.netmask,
                        'broadcast': addr.broadcast
                    })
                elif addr.family == socket.AF_INET6:  # IPv6
                    interface_info['addresses'].append({
                        'type': 'IPv6',
                        'address': addr.address,
                        'netmask': addr.netmask
                    })
            
            # Get statistics
            try:
                stats = psutil.net_if_stats()[interface_name]
                interface_info['stats'] = {
                    'isup': stats.isup,
                    'duplex': stats.duplex,
                    'speed': stats.speed,
                    'mtu': stats.mtu
                }
            except KeyError:
                pass
            
            interfaces[interface_name] = interface_info
        
        return interfaces
    
    def get_primary_interface(self) -> str:
        """Dapatkan primary network interface"""
        # Logic untuk menentukan interface utama
        for name, info in self.interfaces.items():
            if info['stats'] and info['stats']['isup']:
                for addr in info['addresses']:
                    if addr['type'] == 'IPv4' and not addr['address'].startswith('127.'):
                        return name
        return None
    
    def get_campus_interfaces(self) -> List[str]:
        """Dapatkan interfaces yang connect ke network kampus"""
        campus_interfaces = []
        
        for name, info in self.interfaces.items():
            for addr in info['addresses']:
                if addr['type'] == 'IPv4':
                    ip = addr['address']
                    # Check if IP dalam range kampus (assumsi 192.168.x.x)
                    if ip.startswith('192.168.'):
                        campus_interfaces.append(name)
                        break
        
        return campus_interfaces

    def configure_interface_monitoring(self, interface: str) -> dict:
        """Konfigurasi monitoring untuk interface specific"""
        if interface not in self.interfaces:
            raise ValueError(f"Interface {interface} not found")
        
        return {
            'interface': interface,
            'monitoring_enabled': True,
            'sample_interval': 1,  # seconds
            'alert_thresholds': {
                'packet_loss': 5,      # percent
                'latency': 100,        # ms
                'bandwidth_usage': 80  # percent
            }
        }
```

#### DNS Configuration
```python
# config/dns_config.py
import dns.resolver
from typing import List

class DNSConfig:
    def __init__(self, config: NetworkConfig):
        self.config = config
        self.resolver = self.setup_resolver()
    
    def setup_resolver(self) -> dns.resolver.Resolver:
        """Setup custom DNS resolver"""
        resolver = dns.resolver.Resolver()
        
        # Set custom DNS servers
        resolver.nameservers = self.config.dns_servers
        
        # Set timeouts
        resolver.timeout = self.config.default_timeout
        resolver.lifetime = self.config.default_timeout * 2
        
        return resolver
    
    def configure_campus_dns(self):
        """Konfigurasi khusus untuk DNS kampus"""
        # Tambah DNS server kampus jika ada
        campus_dns = ["192.168.1.1", "192.168.1.2"]  # Contoh DNS server kampus
        
        # Prioritaskan DNS server kampus
        self.resolver.nameservers = campus_dns + self.config.dns_servers
    
    def test_dns_servers(self) -> List[dict]:
        """Test semua DNS servers yang dikonfigurasi"""
        results = []
        
        for dns_server in self.resolver.nameservers:
            test_resolver = dns.resolver.Resolver()
            test_resolver.nameservers = [dns_server]
            test_resolver.timeout = 3
            
            try:
                start_time = time.time()
                answer = test_resolver.resolve('google.com', 'A')
                response_time = time.time() - start_time
                
                results.append({
                    'server': dns_server,
                    'status': 'OK',
                    'response_time': response_time,
                    'answer_count': len(answer)
                })
            except Exception as e:
                results.append({
                    'server': dns_server,
                    'status': 'ERROR',
                    'error': str(e)
                })
        
        return results
```

### Konfigurasi Campus-Specific

#### Polinela Network Configuration
```python
# config/campus_network.py
from ipaddress import IPv4Network, IPv4Address
from typing import Dict, List

class PolitelaNetworkConfig:
    def __init__(self):
        self.domain = "polinela.ac.id"
        self.network_segments = self.define_network_segments()
        self.service_map = self.define_service_map()
        self.monitoring_targets = self.define_monitoring_targets()
    
    def define_network_segments(self) -> Dict[str, dict]:
        """Definisikan segmen jaringan kampus"""
        return {
            'admin': {
                'network': IPv4Network('192.168.1.0/24'),
                'description': 'Administrative Network',
                'services': ['domain_controller', 'file_server', 'print_server'],
                'priority': 'high'
            },
            'academic': {
                'network': IPv4Network('192.168.2.0/24'),
                'description': 'Academic Network - Faculty & Staff',
                'services': ['email', 'web_server', 'database'],
                'priority': 'high'
            },
            'student': {
                'network': IPv4Network('192.168.3.0/24'),
                'description': 'Student Network - Computer Labs',
                'services': ['internet_access', 'elearning'],
                'priority': 'medium'
            },
            'guest': {
                'network': IPv4Network('192.168.4.0/24'),
                'description': 'Guest Network - Visitors',
                'services': ['internet_access'],
                'priority': 'low'
            },
            'dmz': {
                'network': IPv4Network('10.0.1.0/24'),
                'description': 'DMZ - Public Services',
                'services': ['web_server', 'mail_server', 'dns'],
                'priority': 'critical'
            }
        }
    
    def define_service_map(self) -> Dict[str, dict]:
        """Definisikan mapping services penting"""
        return {
            'web_server': {
                'hosts': ['polinela.ac.id', 'www.polinela.ac.id'],
                'ports': [80, 443],
                'check_interval': 60,
                'critical': True
            },
            'mail_server': {
                'hosts': ['mail.polinela.ac.id'],
                'ports': [25, 587, 993, 995],
                'check_interval': 300,
                'critical': True
            },
            'elearning': {
                'hosts': ['elearning.polinela.ac.id', 'moodle.polinela.ac.id'],
                'ports': [80, 443],
                'check_interval': 120,
                'critical': True
            },
            'library': {
                'hosts': ['library.polinela.ac.id', 'opac.polinela.ac.id'],
                'ports': [80, 443],
                'check_interval': 300,
                'critical': False
            },
            'portal': {
                'hosts': ['portal.polinela.ac.id', 'siakad.polinela.ac.id'],
                'ports': [80, 443],
                'check_interval': 180,
                'critical': True
            }
        }
    
    def define_monitoring_targets(self) -> List[dict]:
        """Definisikan target monitoring prioritas"""
        targets = []
        
        # Critical infrastructure
        critical_hosts = [
            'polinela.ac.id',
            'mail.polinela.ac.id',
            'elearning.polinela.ac.id',
            'portal.polinela.ac.id'
        ]
        
        for host in critical_hosts:
            targets.append({
                'type': 'ping',
                'target': host,
                'interval': 30,
                'timeout': 5,
                'priority': 'critical'
            })
            
            targets.append({
                'type': 'http',
                'target': f"https://{host}",
                'interval': 60,
                'timeout': 10,
                'priority': 'critical'
            })
        
        # Network gateways
        gateway_ips = ['192.168.1.1', '192.168.2.1', '192.168.3.1']
        for ip in gateway_ips:
            targets.append({
                'type': 'ping',
                'target': ip,
                'interval': 15,
                'timeout': 3,
                'priority': 'high'
            })
        
        return targets
    
    def get_segment_for_ip(self, ip_address: str) -> str:
        """Tentukan segmen network untuk IP address"""
        ip = IPv4Address(ip_address)
        
        for segment_name, segment_info in self.network_segments.items():
            if ip in segment_info['network']:
                return segment_name
        
        return 'unknown'
    
    def get_monitoring_config_for_segment(self, segment: str) -> dict:
        """Dapatkan konfigurasi monitoring untuk segmen"""
        if segment not in self.network_segments:
            return {}
        
        segment_info = self.network_segments[segment]
        priority = segment_info['priority']
        
        # Adjust monitoring frequency based on priority
        interval_map = {
            'critical': 15,
            'high': 30,
            'medium': 60,
            'low': 300
        }
        
        return {
            'ping_interval': interval_map.get(priority, 60),
            'bandwidth_check': priority in ['critical', 'high'],
            'port_scan': priority == 'critical',
            'dns_check': True,
            'alert_threshold': {
                'critical': 1,    # Alert after 1 failure
                'high': 2,        # Alert after 2 failures
                'medium': 3,      # Alert after 3 failures
                'low': 5          # Alert after 5 failures
            }.get(priority, 3)
        }
```

### Dynamic Configuration

#### Runtime Configuration Updates
```python
# config/dynamic_config.py
import threading
import time
import json
from pathlib import Path

class DynamicConfigManager:
    def __init__(self, config: NetDiagConfig):
        self.config = config
        self.config_file = "runtime_config.json"
        self.last_modified = 0
        self.lock = threading.Lock()
        self.monitoring = False
        self.monitor_thread = None
    
    def start_monitoring(self):
        """Start monitoring config file untuk changes"""
        if self.monitoring:
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_config_file,
            daemon=True
        )
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop monitoring config file"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1)
    
    def _monitor_config_file(self):
        """Monitor config file untuk perubahan"""
        while self.monitoring:
            try:
                config_path = Path(self.config_file)
                if config_path.exists():
                    current_modified = config_path.stat().st_mtime
                    
                    if current_modified > self.last_modified:
                        self.last_modified = current_modified
                        self._reload_config()
                
                time.sleep(5)  # Check every 5 seconds
                
            except Exception as e:
                logger = logging.getLogger(__name__)
                logger.error(f"Error monitoring config file: {e}")
                time.sleep(10)
    
    def _reload_config(self):
        """Reload configuration from file"""
        try:
            with self.lock:
                with open(self.config_file, 'r') as f:
                    new_config = json.load(f)
                
                self._apply_config_updates(new_config)
                
                logger = logging.getLogger(__name__)
                logger.info("Configuration reloaded successfully")
                
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"Error reloading config: {e}")
    
    def _apply_config_updates(self, new_config: dict):
        """Apply new configuration values"""
        
        # Update network config
        if 'network' in new_config:
            net_config = new_config['network']
            if 'default_timeout' in net_config:
                self.config.network.default_timeout = net_config['default_timeout']
            if 'concurrent_threads' in net_config:
                self.config.network.concurrent_threads = net_config['concurrent_threads']
        
        # Update logging config
        if 'logging' in new_config:
            log_config = new_config['logging']
            if 'log_level' in log_config:
                self.config.logging.log_level = log_config['log_level']
                # Update logger level
                logging.getLogger().setLevel(
                    getattr(logging, log_config['log_level'])
                )
        
        # Update campus config
        if 'campus' in new_config:
            campus_config = new_config['campus']
            if 'monitoring_intervals' in campus_config:
                self.config.campus.monitoring_intervals.update(
                    campus_config['monitoring_intervals']
                )
    
    def export_current_config(self) -> dict:
        """Export current configuration to dict"""
        return {
            'network': {
                'default_timeout': self.config.network.default_timeout,
                'max_retries': self.config.network.max_retries,
                'concurrent_threads': self.config.network.concurrent_threads,
                'dns_servers': self.config.network.dns_servers
            },
            'database': {
                'db_path': self.config.database.db_path,
                'connection_pool_size': self.config.database.connection_pool_size,
                'backup_interval': self.config.database.backup_interval
            },
            'logging': {
                'log_level': self.config.logging.log_level,
                'log_file': self.config.logging.log_file,
                'console_output': self.config.logging.console_output
            },
            'campus': {
                'campus_domain': self.config.campus.campus_domain,
                'monitoring_intervals': self.config.campus.monitoring_intervals
            }
        }
    
    def save_config(self):
        """Save current config to file"""
        with self.lock:
            config_dict = self.export_current_config()
            with open(self.config_file, 'w') as f:
                json.dump(config_dict, f, indent=2)

# Usage example
config_manager = DynamicConfigManager(config)
config_manager.start_monitoring()

# Config akan otomatis reload ketika file berubah
# Untuk update manual:
config_manager.save_config()
```

### Validation dan Testing

#### Configuration Validation
```python
# config/validation.py
from typing import List, Dict, Any

class ConfigValidator:
    def __init__(self):
        self.validation_rules = self._define_validation_rules()
    
    def _define_validation_rules(self) -> Dict[str, dict]:
        """Define validation rules untuk setiap config parameter"""
        return {
            'network.default_timeout': {
                'type': int,
                'min': 1,
                'max': 60,
                'description': 'Network timeout in seconds'
            },
            'network.concurrent_threads': {
                'type': int,
                'min': 1,
                'max': 20,
                'description': 'Number of concurrent threads'
            },
            'database.connection_pool_size': {
                'type': int,
                'min': 1,
                'max': 50,
                'description': 'Database connection pool size'
            },
            'logging.log_level': {
                'type': str,
                'allowed_values': ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                'description': 'Logging level'
            }
        }
    
    def validate_config(self, config: NetDiagConfig) -> List[str]:
        """Validate entire configuration"""
        errors = []
        
        # Validate network config
        errors.extend(self._validate_network_config(config.network))
        
        # Validate database config
        errors.extend(self._validate_database_config(config.database))
        
        # Validate logging config
        errors.extend(self._validate_logging_config(config.logging))
        
        # Validate campus config
        errors.extend(self._validate_campus_config(config.campus))
        
        return errors
    
    def _validate_network_config(self, network_config: NetworkConfig) -> List[str]:
        """Validate network configuration"""
        errors = []
        
        # Validate timeout
        if not (1 <= network_config.default_timeout <= 60):
            errors.append("Network timeout must be between 1 and 60 seconds")
        
        # Validate thread count
        if not (1 <= network_config.concurrent_threads <= 20):
            errors.append("Concurrent threads must be between 1 and 20")
        
        # Validate DNS servers
        if not network_config.dns_servers:
            errors.append("At least one DNS server must be configured")
        
        return errors
    
    def _validate_database_config(self, db_config: DatabaseConfig) -> List[str]:
        """Validate database configuration"""
        errors = []
        
        # Validate connection pool size
        if not (1 <= db_config.connection_pool_size <= 50):
            errors.append("Connection pool size must be between 1 and 50")
        
        # Validate backup interval
        if db_config.backup_interval < 300:  # 5 minutes minimum
            errors.append("Backup interval must be at least 300 seconds")
        
        return errors
    
    def _validate_logging_config(self, log_config: LoggingConfig) -> List[str]:
        """Validate logging configuration"""
        errors = []
        
        # Validate log level
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if log_config.log_level not in valid_levels:
            errors.append(f"Log level must be one of: {valid_levels}")
        
        # Validate file size
        if log_config.max_file_size < 1024:  # 1KB minimum
            errors.append("Max file size must be at least 1024 bytes")
        
        return errors
    
    def _validate_campus_config(self, campus_config: CampusConfig) -> List[str]:
        """Validate campus configuration"""
        errors = []
        
        # Validate domain
        if not campus_config.campus_domain:
            errors.append("Campus domain must be specified")
        
        # Validate monitoring intervals
        for service, interval in campus_config.monitoring_intervals.items():
            if interval < 10:  # 10 seconds minimum
                errors.append(f"Monitoring interval for {service} must be at least 10 seconds")
        
        return errors

# Usage
validator = ConfigValidator()
validation_errors = validator.validate_config(config)

if validation_errors:
    for error in validation_errors:
        print(f"Configuration Error: {error}")
else:
    print("Configuration is valid")
```

### Kesimpulan

Sistem konfigurasi NetDiag menyediakan:

1. **Flexible Configuration** - Multiple config sources dan environments
2. **Dynamic Updates** - Runtime configuration changes
3. **Validation** - Comprehensive config validation
4. **Campus-Specific** - Optimized untuk environment Polinela
5. **Monitoring Integration** - Seamless integration dengan monitoring systems

Implementasikan sesuai kebutuhan spesifik lingkungan deployment Anda.