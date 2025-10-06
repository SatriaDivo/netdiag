# Integrasi NetDiag dengan Sistem Lain

## 🔗 Connecting NetDiag dengan External Systems

### Pengenalan Integrasi

NetDiag dirancang untuk mudah diintegrasikan dengan berbagai sistem monitoring, databases, web applications, dan tools network management lainnya yang umum digunakan di lingkungan kampus dan enterprise.

### Integrasi Database

#### PostgreSQL Integration
```python
import psycopg2
from psycopg2.extras import RealDictCursor
import json
from typing import List, Dict, Any

class PostgreSQLIntegration:
    def __init__(self, connection_config: dict):
        self.config = connection_config
        self.connection = None
    
    def connect(self):
        """Connect to PostgreSQL database"""
        try:
            self.connection = psycopg2.connect(
                host=self.config['host'],
                database=self.config['database'],
                user=self.config['user'],
                password=self.config['password'],
                port=self.config.get('port', 5432)
            )
            return True
        except Exception as e:
            print(f"PostgreSQL connection error: {e}")
            return False
    
    def create_netdiag_tables(self):
        """Create tables for NetDiag data"""
        tables_sql = [
            """
            CREATE TABLE IF NOT EXISTS network_ping_results (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                host VARCHAR(255) NOT NULL,
                ip_address INET,
                packets_sent INTEGER,
                packets_received INTEGER,
                packet_loss DECIMAL(5,2),
                min_latency DECIMAL(8,3),
                max_latency DECIMAL(8,3), 
                avg_latency DECIMAL(8,3),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE INDEX IF NOT EXISTS idx_ping_host ON network_ping_results(host);
            CREATE INDEX IF NOT EXISTS idx_ping_timestamp ON network_ping_results(timestamp);
            """,
            """
            CREATE TABLE IF NOT EXISTS network_bandwidth_results (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                interface VARCHAR(50),
                download_speed BIGINT,
                upload_speed BIGINT,
                bytes_sent BIGINT,
                bytes_received BIGINT,
                duration DECIMAL(8,3),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        ]
        
        with self.connection.cursor() as cursor:
            for sql in tables_sql:
                cursor.execute(sql)
        self.connection.commit()
    
    def insert_ping_result(self, result: PingResult):
        """Insert ping result into PostgreSQL"""
        sql = """
        INSERT INTO network_ping_results 
        (host, ip_address, packets_sent, packets_received, packet_loss, 
         min_latency, max_latency, avg_latency, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, to_timestamp(%s))
        """
        
        with self.connection.cursor() as cursor:
            cursor.execute(sql, (
                result.host,
                result.ip_address,
                result.packets_sent,
                result.packets_received,
                result.packet_loss,
                result.min_latency,
                result.max_latency,
                result.avg_latency,
                result.timestamp
            ))
        self.connection.commit()
    
    def get_host_statistics(self, host: str, days: int = 7) -> Dict[str, Any]:
        """Get statistics for a host over specified days"""
        sql = """
        SELECT 
            COUNT(*) as total_pings,
            AVG(avg_latency) as avg_latency,
            MIN(min_latency) as min_latency,
            MAX(max_latency) as max_latency,
            AVG(packet_loss) as avg_packet_loss
        FROM network_ping_results 
        WHERE host = %s 
        AND timestamp >= CURRENT_TIMESTAMP - INTERVAL '%s days'
        """
        
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql, (host, days))
            return dict(cursor.fetchone())

# Usage
pg_config = {
    'host': 'localhost',
    'database': 'netdiag_db',
    'user': 'netdiag_user',
    'password': 'secure_password'
}

pg_integration = PostgreSQLIntegration(pg_config)
if pg_integration.connect():
    pg_integration.create_netdiag_tables()
    
    # Insert ping result
    ping_result = PingResult("polinela.ac.id", avg_latency=25.5)
    pg_integration.insert_ping_result(ping_result)
    
    # Get statistics
    stats = pg_integration.get_host_statistics("polinela.ac.id")
    print(f"Host statistics: {stats}")
```

#### MySQL Integration
```python
import mysql.connector
from mysql.connector import Error

class MySQLIntegration:
    def __init__(self, connection_config: dict):
        self.config = connection_config
        self.connection = None
    
    def connect(self):
        """Connect to MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host=self.config['host'],
                database=self.config['database'],
                user=self.config['user'],
                password=self.config['password'],
                port=self.config.get('port', 3306)
            )
            return True
        except Error as e:
            print(f"MySQL connection error: {e}")
            return False
    
    def create_monitoring_views(self):
        """Create useful views for monitoring"""
        views_sql = [
            """
            CREATE OR REPLACE VIEW host_health_summary AS
            SELECT 
                host,
                COUNT(*) as ping_count,
                AVG(avg_latency) as avg_latency,
                AVG(packet_loss) as avg_packet_loss,
                MAX(timestamp) as last_check
            FROM network_ping_results 
            WHERE timestamp >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
            GROUP BY host;
            """,
            """
            CREATE OR REPLACE VIEW slow_hosts AS
            SELECT 
                host,
                AVG(avg_latency) as avg_latency,
                COUNT(*) as sample_count
            FROM network_ping_results 
            WHERE timestamp >= DATE_SUB(NOW(), INTERVAL 1 HOUR)
            GROUP BY host
            HAVING AVG(avg_latency) > 100
            ORDER BY avg_latency DESC;
            """
        ]
        
        cursor = self.connection.cursor()
        for sql in views_sql:
            cursor.execute(sql)
        self.connection.commit()
        cursor.close()
    
    def get_alerting_data(self) -> List[Dict[str, Any]]:
        """Get data for alerting systems"""
        sql = """
        SELECT 
            host,
            avg_latency,
            avg_packet_loss,
            last_check,
            CASE 
                WHEN avg_packet_loss > 5 THEN 'CRITICAL'
                WHEN avg_latency > 100 THEN 'WARNING'
                ELSE 'OK'
            END as status
        FROM host_health_summary
        """
        
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        
        return results

# Usage
mysql_config = {
    'host': 'mysql.polinela.ac.id',
    'database': 'network_monitoring',
    'user': 'netdiag',
    'password': 'password123'
}

mysql_integration = MySQLIntegration(mysql_config)
if mysql_integration.connect():
    mysql_integration.create_monitoring_views()
    alerts = mysql_integration.get_alerting_data()
    for alert in alerts:
        if alert['status'] != 'OK':
            print(f"Alert: {alert['host']} - {alert['status']}")
```

### Integrasi Web Frameworks

#### Flask REST API Integration
```python
from flask import Flask, jsonify, request, g
from flask_cors import CORS
import sqlite3
import threading
import time

app = Flask(__name__)
CORS(app)

class FlaskNetDiagAPI:
    def __init__(self, db_path: str = "netdiag.db"):
        self.db_path = db_path
        self.monitoring_active = False
        self.monitoring_thread = None
        self.setup_routes()
    
    def get_db(self):
        """Get database connection"""
        if 'db' not in g:
            g.db = sqlite3.connect(self.db_path)
            g.db.row_factory = sqlite3.Row
        return g.db
    
    def close_db(self, error):
        """Close database connection"""
        db = g.pop('db', None)
        if db is not None:
            db.close()
    
    def setup_routes(self):
        """Setup Flask routes"""
        
        @app.route('/api/ping', methods=['POST'])
        def ping_host():
            """Ping a host via API"""
            data = request.get_json()
            host = data.get('host')
            timeout = data.get('timeout', 5)
            
            if not host:
                return jsonify({'error': 'Host parameter required'}), 400
            
            try:
                # Perform ping
                analyzer = NetworkAnalyzer()
                result = analyzer.ping_host(host, timeout=timeout)
                
                # Save to database
                db = self.get_db()
                db.execute("""
                    INSERT INTO ping_results 
                    (host, ip_address, avg_latency, packet_loss, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    result.host,
                    result.ip_address,
                    result.avg_latency,
                    result.packet_loss,
                    result.timestamp
                ))
                db.commit()
                
                return jsonify({
                    'success': True,
                    'result': {
                        'host': result.host,
                        'ip_address': result.ip_address,
                        'avg_latency': result.avg_latency,
                        'packet_loss': result.packet_loss,
                        'timestamp': result.timestamp
                    }
                })
                
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @app.route('/api/hosts/<host>/history', methods=['GET'])
        def get_host_history(host):
            """Get ping history for a host"""
            limit = request.args.get('limit', 100, type=int)
            
            db = self.get_db()
            cursor = db.execute("""
                SELECT * FROM ping_results 
                WHERE host = ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (host, limit))
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    'timestamp': row['timestamp'],
                    'avg_latency': row['avg_latency'],
                    'packet_loss': row['packet_loss']
                })
            
            return jsonify({
                'host': host,
                'history': results
            })
        
        @app.route('/api/monitoring/start', methods=['POST'])
        def start_monitoring():
            """Start continuous monitoring"""
            data = request.get_json()
            hosts = data.get('hosts', [])
            interval = data.get('interval', 60)
            
            if not hosts:
                return jsonify({'error': 'Hosts list required'}), 400
            
            if self.monitoring_active:
                return jsonify({'error': 'Monitoring already active'}), 409
            
            self.monitoring_active = True
            self.monitoring_thread = threading.Thread(
                target=self._continuous_monitoring,
                args=(hosts, interval),
                daemon=True
            )
            self.monitoring_thread.start()
            
            return jsonify({
                'success': True,
                'message': f'Monitoring started for {len(hosts)} hosts'
            })
        
        @app.route('/api/monitoring/stop', methods=['POST'])
        def stop_monitoring():
            """Stop continuous monitoring"""
            self.monitoring_active = False
            
            return jsonify({
                'success': True,
                'message': 'Monitoring stopped'
            })
        
        @app.route('/api/dashboard/summary', methods=['GET'])
        def dashboard_summary():
            """Get dashboard summary data"""
            db = self.get_db()
            
            # Get recent results for each host
            cursor = db.execute("""
                SELECT 
                    host,
                    AVG(avg_latency) as avg_latency,
                    AVG(packet_loss) as avg_packet_loss,
                    COUNT(*) as ping_count,
                    MAX(timestamp) as last_ping
                FROM ping_results 
                WHERE timestamp > datetime('now', '-1 hour')
                GROUP BY host
                ORDER BY last_ping DESC
            """)
            
            hosts_summary = []
            for row in cursor.fetchall():
                status = 'healthy'
                if row['avg_packet_loss'] > 5:
                    status = 'critical'
                elif row['avg_latency'] > 100:
                    status = 'warning'
                
                hosts_summary.append({
                    'host': row['host'],
                    'avg_latency': round(row['avg_latency'], 2),
                    'packet_loss': round(row['avg_packet_loss'], 2),
                    'ping_count': row['ping_count'],
                    'last_ping': row['last_ping'],
                    'status': status
                })
            
            return jsonify({
                'hosts': hosts_summary,
                'monitoring_active': self.monitoring_active,
                'timestamp': time.time()
            })
        
        # Register teardown handler
        app.teardown_appcontext(self.close_db)
    
    def _continuous_monitoring(self, hosts: List[str], interval: int):
        """Background monitoring thread"""
        analyzer = NetworkAnalyzer()
        
        while self.monitoring_active:
            for host in hosts:
                try:
                    result = analyzer.ping_host(host)
                    
                    # Save to database
                    db = sqlite3.connect(self.db_path)
                    db.execute("""
                        INSERT INTO ping_results 
                        (host, ip_address, avg_latency, packet_loss, timestamp)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        result.host,
                        result.ip_address,
                        result.avg_latency,
                        result.packet_loss,
                        result.timestamp
                    ))
                    db.commit()
                    db.close()
                    
                except Exception as e:
                    print(f"Error monitoring {host}: {e}")
            
            time.sleep(interval)

# Initialize and run
api = FlaskNetDiagAPI()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

#### FastAPI Integration
```python
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import asyncio

app = FastAPI(title="NetDiag API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class PingRequest(BaseModel):
    host: str
    timeout: int = 5
    count: int = 4

class MonitoringRequest(BaseModel):
    hosts: List[str]
    interval: int = 60
    duration: Optional[int] = None

class PingResponse(BaseModel):
    host: str
    ip_address: Optional[str]
    avg_latency: float
    packet_loss: float
    timestamp: float
    success: bool

class FastAPINetDiag:
    def __init__(self):
        self.monitoring_tasks = {}
        self.setup_routes()
    
    def setup_routes(self):
        
        @app.post("/ping", response_model=PingResponse)
        async def ping_host(request: PingRequest):
            """Async ping endpoint"""
            try:
                analyzer = NetworkAnalyzer()
                result = await asyncio.to_thread(
                    analyzer.ping_host,
                    request.host,
                    timeout=request.timeout,
                    count=request.count
                )
                
                return PingResponse(
                    host=result.host,
                    ip_address=result.ip_address,
                    avg_latency=result.avg_latency,
                    packet_loss=result.packet_loss,
                    timestamp=result.timestamp,
                    success=result.packets_received > 0
                )
                
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @app.post("/monitoring/start")
        async def start_monitoring(request: MonitoringRequest, background_tasks: BackgroundTasks):
            """Start background monitoring"""
            task_id = f"monitoring_{hash(tuple(request.hosts))}"
            
            if task_id in self.monitoring_tasks:
                raise HTTPException(status_code=409, detail="Monitoring already running for these hosts")
            
            # Start background task
            task = asyncio.create_task(
                self._background_monitoring(
                    request.hosts,
                    request.interval,
                    request.duration
                )
            )
            
            self.monitoring_tasks[task_id] = task
            
            return {
                "task_id": task_id,
                "message": f"Started monitoring {len(request.hosts)} hosts",
                "hosts": request.hosts
            }
        
        @app.get("/monitoring/status")
        async def monitoring_status():
            """Get monitoring status"""
            active_tasks = []
            for task_id, task in self.monitoring_tasks.items():
                if not task.done():
                    active_tasks.append(task_id)
                else:
                    # Clean up completed tasks
                    del self.monitoring_tasks[task_id]
            
            return {
                "active_monitoring_tasks": len(active_tasks),
                "task_ids": active_tasks
            }
        
        @app.delete("/monitoring/{task_id}")
        async def stop_monitoring(task_id: str):
            """Stop specific monitoring task"""
            if task_id not in self.monitoring_tasks:
                raise HTTPException(status_code=404, detail="Monitoring task not found")
            
            task = self.monitoring_tasks[task_id]
            task.cancel()
            
            try:
                await task
            except asyncio.CancelledError:
                pass
            
            del self.monitoring_tasks[task_id]
            
            return {"message": f"Monitoring task {task_id} stopped"}
        
        @app.get("/health")
        async def health_check():
            """Health check endpoint"""
            return {"status": "healthy", "timestamp": time.time()}
    
    async def _background_monitoring(self, hosts: List[str], interval: int, duration: Optional[int]):
        """Background monitoring coroutine"""
        analyzer = NetworkAnalyzer()
        start_time = time.time()
        
        try:
            while True:
                # Check duration limit
                if duration and (time.time() - start_time) >= duration:
                    break
                
                # Ping all hosts
                for host in hosts:
                    try:
                        result = await asyncio.to_thread(analyzer.ping_host, host)
                        
                        # Log or save result
                        print(f"[{time.strftime('%H:%M:%S')}] {host}: {result.avg_latency:.1f}ms")
                        
                    except Exception as e:
                        print(f"Error pinging {host}: {e}")
                
                # Wait for next interval
                await asyncio.sleep(interval)
                
        except asyncio.CancelledError:
            print("Monitoring task cancelled")
            raise

# Initialize
netdiag_api = FastAPINetDiag()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Integrasi Monitoring Systems

#### Prometheus Integration
```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time
import threading

class PrometheusIntegration:
    def __init__(self, port: int = 8000):
        self.port = port
        
        # Define metrics
        self.ping_counter = Counter(
            'netdiag_ping_total',
            'Total number of ping operations',
            ['host', 'status']
        )
        
        self.ping_latency = Histogram(
            'netdiag_ping_latency_seconds',
            'Ping latency in seconds',
            ['host'],
            buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0, 5.0]
        )
        
        self.packet_loss = Gauge(
            'netdiag_packet_loss_percent',
            'Packet loss percentage',
            ['host']
        )
        
        self.host_status = Gauge(
            'netdiag_host_status',
            'Host status (1=up, 0=down)',
            ['host']
        )
        
        # Start metrics server
        start_http_server(self.port)
        print(f"Prometheus metrics server started on port {self.port}")
    
    def record_ping_result(self, result: PingResult):
        """Record ping result in Prometheus metrics"""
        
        # Record ping attempt
        status = 'success' if result.packets_received > 0 else 'failure'
        self.ping_counter.labels(host=result.host, status=status).inc()
        
        # Record latency if successful
        if result.packets_received > 0:
            self.ping_latency.labels(host=result.host).observe(result.avg_latency / 1000)
        
        # Record packet loss
        self.packet_loss.labels(host=result.host).set(result.packet_loss)
        
        # Record host status
        host_up = 1 if result.packets_received > 0 else 0
        self.host_status.labels(host=result.host).set(host_up)
    
    def start_monitoring_with_metrics(self, hosts: List[str], interval: int = 60):
        """Start monitoring with Prometheus metrics collection"""
        
        def monitoring_loop():
            analyzer = NetworkAnalyzer()
            
            while True:
                for host in hosts:
                    try:
                        result = analyzer.ping_host(host)
                        self.record_ping_result(result)
                        
                    except Exception as e:
                        print(f"Error monitoring {host}: {e}")
                        
                        # Record failure
                        self.ping_counter.labels(host=host, status='error').inc()
                        self.host_status.labels(host=host).set(0)
                
                time.sleep(interval)
        
        # Start monitoring in background thread
        monitoring_thread = threading.Thread(target=monitoring_loop, daemon=True)
        monitoring_thread.start()
        
        return monitoring_thread

# Usage
prometheus = PrometheusIntegration(port=8000)
hosts = ["polinela.ac.id", "mail.polinela.ac.id"]
prometheus.start_monitoring_with_metrics(hosts, interval=30)

# Metrics will be available at http://localhost:8000/metrics
```

#### Grafana Dashboard Configuration
```python
import json
from typing import Dict, Any

class GrafanaDashboardGenerator:
    def __init__(self):
        self.dashboard_template = self._create_dashboard_template()
    
    def _create_dashboard_template(self) -> Dict[str, Any]:
        """Create Grafana dashboard template for NetDiag metrics"""
        return {
            "dashboard": {
                "id": None,
                "title": "NetDiag Network Monitoring",
                "tags": ["netdiag", "network", "monitoring"],
                "timezone": "browser",
                "refresh": "30s",
                "time": {
                    "from": "now-1h",
                    "to": "now"
                },
                "panels": [
                    {
                        "id": 1,
                        "title": "Ping Latency",
                        "type": "graph",
                        "targets": [
                            {
                                "expr": "netdiag_ping_latency_seconds",
                                "legendFormat": "{{host}} latency",
                                "refId": "A"
                            }
                        ],
                        "yAxes": [
                            {
                                "label": "Latency (seconds)",
                                "min": 0
                            }
                        ],
                        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0}
                    },
                    {
                        "id": 2,
                        "title": "Packet Loss",
                        "type": "graph",
                        "targets": [
                            {
                                "expr": "netdiag_packet_loss_percent",
                                "legendFormat": "{{host}} packet loss",
                                "refId": "B"
                            }
                        ],
                        "yAxes": [
                            {
                                "label": "Packet Loss (%)",
                                "min": 0,
                                "max": 100
                            }
                        ],
                        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0}
                    },
                    {
                        "id": 3,
                        "title": "Host Status",
                        "type": "stat",
                        "targets": [
                            {
                                "expr": "netdiag_host_status",
                                "legendFormat": "{{host}}",
                                "refId": "C"
                            }
                        ],
                        "fieldConfig": {
                            "defaults": {
                                "mappings": [
                                    {
                                        "options": {
                                            "0": {"text": "DOWN", "color": "red"},
                                            "1": {"text": "UP", "color": "green"}
                                        },
                                        "type": "value"
                                    }
                                ]
                            }
                        },
                        "gridPos": {"h": 8, "w": 24, "x": 0, "y": 8}
                    }
                ]
            }
        }
    
    def generate_dashboard_json(self, datasource_uid: str = "prometheus") -> str:
        """Generate complete Grafana dashboard JSON"""
        
        # Add datasource to all targets
        for panel in self.dashboard_template["dashboard"]["panels"]:
            for target in panel.get("targets", []):
                target["datasource"] = {"uid": datasource_uid}
        
        return json.dumps(self.dashboard_template, indent=2)
    
    def save_dashboard(self, filename: str = "netdiag_dashboard.json"):
        """Save dashboard to file"""
        with open(filename, 'w') as f:
            f.write(self.generate_dashboard_json())
        
        print(f"Dashboard saved to {filename}")
        print("Import this file in Grafana to create the dashboard")

# Usage
dashboard_gen = GrafanaDashboardGenerator()
dashboard_gen.save_dashboard()
```

### Integrasi SNMP

#### SNMP Integration untuk Network Devices
```python
from pysnmp.hlapi import *
from typing import Dict, List, Optional

class SNMPIntegration:
    def __init__(self, community: str = 'public'):
        self.community = community
        
        # Common SNMP OIDs
        self.oids = {
            'system_name': '1.3.6.1.2.1.1.5.0',
            'system_uptime': '1.3.6.1.2.1.1.3.0',
            'interface_count': '1.3.6.1.2.1.2.1.0',
            'interface_names': '1.3.6.1.2.1.2.2.1.2',
            'interface_status': '1.3.6.1.2.1.2.2.1.8',
            'interface_in_octets': '1.3.6.1.2.1.2.2.1.10',
            'interface_out_octets': '1.3.6.1.2.1.2.2.1.16'
        }
    
    def get_system_info(self, host: str) -> Optional[Dict[str, Any]]:
        """Get basic system information via SNMP"""
        try:
            iterator = getCmd(
                SnmpEngine(),
                CommunityData(self.community),
                UdpTransportTarget((host, 161)),
                ContextData(),
                ObjectType(ObjectIdentity(self.oids['system_name'])),
                ObjectType(ObjectIdentity(self.oids['system_uptime'])),
                ObjectType(ObjectIdentity(self.oids['interface_count']))
            )
            
            errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
            
            if errorIndication or errorStatus:
                return None
            
            return {
                'host': host,
                'system_name': str(varBinds[0][1]),
                'uptime': int(varBinds[1][1]),
                'interface_count': int(varBinds[2][1])
            }
            
        except Exception as e:
            print(f"SNMP error for {host}: {e}")
            return None
    
    def get_interface_info(self, host: str) -> List[Dict[str, Any]]:
        """Get interface information via SNMP"""
        interfaces = []
        
        try:
            # Walk interface table
            for (errorIndication, errorStatus, errorIndex, varBinds) in nextCmd(
                SnmpEngine(),
                CommunityData(self.community),
                UdpTransportTarget((host, 161)),
                ContextData(),
                ObjectType(ObjectIdentity(self.oids['interface_names'])),
                lexicographicMode=False
            ):
                
                if errorIndication or errorStatus:
                    break
                
                for varBind in varBinds:
                    # Extract interface index from OID
                    oid_parts = str(varBind[0]).split('.')
                    if_index = int(oid_parts[-1])
                    if_name = str(varBind[1])
                    
                    # Get interface status
                    status_oid = f"{self.oids['interface_status']}.{if_index}"
                    status_result = self._get_single_oid(host, status_oid)
                    
                    # Get traffic counters
                    in_octets_oid = f"{self.oids['interface_in_octets']}.{if_index}"
                    out_octets_oid = f"{self.oids['interface_out_octets']}.{if_index}"
                    
                    in_octets = self._get_single_oid(host, in_octets_oid)
                    out_octets = self._get_single_oid(host, out_octets_oid)
                    
                    interfaces.append({
                        'index': if_index,
                        'name': if_name,
                        'status': 'up' if status_result == 1 else 'down',
                        'in_octets': in_octets or 0,
                        'out_octets': out_octets or 0
                    })
        
        except Exception as e:
            print(f"Error getting interface info for {host}: {e}")
        
        return interfaces
    
    def _get_single_oid(self, host: str, oid: str) -> Optional[int]:
        """Get single OID value"""
        try:
            iterator = getCmd(
                SnmpEngine(),
                CommunityData(self.community),
                UdpTransportTarget((host, 161)),
                ContextData(),
                ObjectType(ObjectIdentity(oid))
            )
            
            errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
            
            if errorIndication or errorStatus:
                return None
            
            return int(varBinds[0][1])
            
        except:
            return None
    
    def monitor_device_continuously(self, host: str, interval: int = 300):
        """Continuously monitor device via SNMP"""
        import time
        import threading
        
        def monitoring_loop():
            while True:
                # Get system info
                sys_info = self.get_system_info(host)
                if sys_info:
                    print(f"[{host}] System: {sys_info['system_name']}, Uptime: {sys_info['uptime']}")
                
                # Get interface info
                interfaces = self.get_interface_info(host)
                for interface in interfaces:
                    if interface['status'] == 'up':
                        print(f"[{host}] Interface {interface['name']}: {interface['status']}")
                
                time.sleep(interval)
        
        thread = threading.Thread(target=monitoring_loop, daemon=True)
        thread.start()
        return thread

# Usage
snmp = SNMPIntegration(community='public')

# Get device information
device_info = snmp.get_system_info('192.168.1.1')  # Router/Switch IP
if device_info:
    print(f"Device: {device_info}")

# Get interface information
interfaces = snmp.get_interface_info('192.168.1.1')
for interface in interfaces:
    print(f"Interface: {interface}")

# Start continuous monitoring
monitor_thread = snmp.monitor_device_continuously('192.168.1.1', interval=60)
```

### Integrasi Email Notifications

#### SMTP Email Integration
```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import json
from typing import List

class EmailNotificationIntegration:
    def __init__(self, smtp_config: Dict[str, Any]):
        self.config = smtp_config
        self.smtp_server = None
    
    def connect(self) -> bool:
        """Connect to SMTP server"""
        try:
            self.smtp_server = smtplib.SMTP(
                self.config['host'],
                self.config['port']
            )
            
            if self.config.get('use_tls', True):
                self.smtp_server.starttls()
            
            if 'username' in self.config and 'password' in self.config:
                self.smtp_server.login(
                    self.config['username'],
                    self.config['password']
                )
            
            return True
            
        except Exception as e:
            print(f"SMTP connection error: {e}")
            return False
    
    def send_ping_alert(self, result: PingResult, threshold: float = 100.0):
        """Send alert for ping issues"""
        
        if result.avg_latency > threshold or result.packet_loss > 5:
            subject = f"Network Alert: {result.host}"
            
            # Determine severity
            if result.packet_loss > 20:
                severity = "CRITICAL"
            elif result.packet_loss > 5 or result.avg_latency > 200:
                severity = "WARNING"
            else:
                severity = "INFO"
            
            # Create email content
            body = f"""
Network monitoring alert for {result.host}

Severity: {severity}
Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(result.timestamp))}

Metrics:
- Average Latency: {result.avg_latency:.2f}ms
- Packet Loss: {result.packet_loss:.1f}%
- Packets Sent: {result.packets_sent}
- Packets Received: {result.packets_received}

Host IP: {result.ip_address or 'Unknown'}

This alert was generated by NetDiag monitoring system.
            """
            
            self.send_email(
                to=self.config['alert_recipients'],
                subject=subject,
                body=body,
                priority='high' if severity == 'CRITICAL' else 'normal'
            )
    
    def send_daily_report(self, hosts_data: List[Dict[str, Any]]):
        """Send daily monitoring report"""
        
        subject = f"Daily Network Report - {time.strftime('%Y-%m-%d')}"
        
        # Generate HTML report
        html_body = self._generate_html_report(hosts_data)
        
        # Also create text version
        text_body = self._generate_text_report(hosts_data)
        
        self.send_email(
            to=self.config['report_recipients'],
            subject=subject,
            body=text_body,
            html_body=html_body
        )
    
    def send_email(self, to: List[str], subject: str, body: str, 
                   html_body: str = None, priority: str = 'normal'):
        """Send email with optional HTML content"""
        
        if not self.smtp_server:
            if not self.connect():
                return False
        
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.config['from_email']
            msg['To'] = ', '.join(to)
            msg['Subject'] = subject
            
            # Set priority
            if priority == 'high':
                msg['X-Priority'] = '1'
                msg['X-MSMail-Priority'] = 'High'
            
            # Add text part
            text_part = MIMEText(body, 'plain')
            msg.attach(text_part)
            
            # Add HTML part if provided
            if html_body:
                html_part = MIMEText(html_body, 'html')
                msg.attach(html_part)
            
            # Send email
            self.smtp_server.send_message(msg)
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def _generate_html_report(self, hosts_data: List[Dict[str, Any]]) -> str:
        """Generate HTML report"""
        
        html = """
        <html>
        <body>
        <h2>NetDiag Daily Network Report</h2>
        <p>Generated on: {date}</p>
        
        <table border="1" style="border-collapse: collapse; width: 100%;">
        <tr>
            <th>Host</th>
            <th>Status</th>
            <th>Avg Latency (ms)</th>
            <th>Packet Loss (%)</th>
            <th>Uptime (%)</th>
        </tr>
        """.format(date=time.strftime('%Y-%m-%d %H:%M:%S'))
        
        for host_data in hosts_data:
            status_color = 'green' if host_data['status'] == 'OK' else 'red'
            
            html += f"""
            <tr>
                <td>{host_data['host']}</td>
                <td style="color: {status_color};">{host_data['status']}</td>
                <td>{host_data['avg_latency']:.2f}</td>
                <td>{host_data['packet_loss']:.1f}</td>
                <td>{host_data['uptime']:.1f}</td>
            </tr>
            """
        
        html += """
        </table>
        
        <p><small>This report was generated by NetDiag monitoring system.</small></p>
        </body>
        </html>
        """
        
        return html
    
    def _generate_text_report(self, hosts_data: List[Dict[str, Any]]) -> str:
        """Generate text report"""
        
        report = f"NetDiag Daily Network Report - {time.strftime('%Y-%m-%d')}\n"
        report += "=" * 60 + "\n\n"
        
        for host_data in hosts_data:
            report += f"Host: {host_data['host']}\n"
            report += f"  Status: {host_data['status']}\n"
            report += f"  Avg Latency: {host_data['avg_latency']:.2f}ms\n"
            report += f"  Packet Loss: {host_data['packet_loss']:.1f}%\n"
            report += f"  Uptime: {host_data['uptime']:.1f}%\n\n"
        
        return report

# Usage
email_config = {
    'host': 'mail.polinela.ac.id',
    'port': 587,
    'use_tls': True,
    'username': 'netdiag@polinela.ac.id',
    'password': 'password123',
    'from_email': 'netdiag@polinela.ac.id',
    'alert_recipients': ['admin@polinela.ac.id', 'tech@polinela.ac.id'],
    'report_recipients': ['admin@polinela.ac.id']
}

email_notifier = EmailNotificationIntegration(email_config)

# Send alert for problematic ping
problematic_result = PingResult(
    "slow.server.com",
    avg_latency=150.0,
    packet_loss=10.0
)
email_notifier.send_ping_alert(problematic_result)

# Send daily report
daily_data = [
    {
        'host': 'polinela.ac.id',
        'status': 'OK',
        'avg_latency': 25.5,
        'packet_loss': 0.0,
        'uptime': 99.9
    }
]
email_notifier.send_daily_report(daily_data)
```

### Kesimpulan

Integrasi NetDiag dengan sistem eksternal meliputi:

1. **Database Integration** - PostgreSQL, MySQL untuk data persistence
2. **Web Framework Integration** - Flask, FastAPI untuk REST APIs
3. **Monitoring Systems** - Prometheus, Grafana untuk visualization
4. **SNMP Integration** - Network device monitoring
5. **Email Notifications** - Alert dan reporting system

Implementasikan integrasi sesuai dengan infrastruktur yang ada di lingkungan kampus atau enterprise Anda.