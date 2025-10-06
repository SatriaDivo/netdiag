# Testing Guide

## 🧪 Comprehensive Testing Strategy untuk NetDiag

### Testing Philosophy

NetDiag menggunakan comprehensive testing approach yang mencakup unit tests, integration tests, performance tests, dan campus-specific testing scenarios untuk memastikan reliability dan educational value.

### Testing Framework Overview

#### 1. Testing Stack

**Core Testing Tools:**
```python
# Primary testing framework
pytest>=7.0.0              # Main test runner
pytest-cov>=4.0.0          # Coverage reporting
pytest-asyncio>=0.21.0     # Async testing support
pytest-mock>=3.10.0        # Mocking utilities

# Additional testing tools
pytest-xdist>=3.0.0        # Parallel test execution
pytest-benchmark>=4.0.0    # Performance benchmarking
pytest-timeout>=2.1.0      # Test timeout management
pytest-randomly>=3.12.0    # Random test execution order

# Network testing specific
responses>=0.22.0           # HTTP mocking
freezegun>=1.2.0           # Time mocking untuk network timing tests
```

**Campus Testing Extensions:**
```python
# Campus-specific testing utilities
pytest-campus>=1.0.0       # Custom markers untuk campus tests
pytest-network>=1.0.0      # Network simulation tools
pytest-slow>=1.0.0         # Slow test management
```

#### 2. Test Categories

**Test Markers:**
```python
# pytest.ini configuration
[tool:pytest]
markers =
    unit: Fast unit tests
    integration: Integration tests requiring network
    campus: Campus-specific tests
    slow: Slow tests (>5 seconds)
    security: Security-related tests
    performance: Performance benchmarking tests
    educational: Tests untuk educational scenarios
    mock: Tests using mocked dependencies
    real_network: Tests requiring real network access
```

### Unit Testing

#### 1. Basic Unit Test Structure

**Test Organization:**
```
tests/
├── unit/
│   ├── __init__.py
│   ├── test_ping.py
│   ├── test_dns.py
│   ├── test_bandwidth.py
│   ├── test_network_analyzer.py
│   └── test_utils.py
├── integration/
│   ├── test_end_to_end.py
│   └── test_network_integration.py
├── campus/
│   ├── test_polinela_network.py
│   └── test_campus_scenarios.py
└── fixtures/
    ├── conftest.py
    └── sample_data.py
```

**Unit Test Examples:**
```python
# tests/unit/test_ping.py
import pytest
from unittest.mock import patch, MagicMock
import subprocess
import time

from netdiag.core.ping import PingAnalyzer
from netdiag.models import PingResult
from netdiag.exceptions import NetworkError, TimeoutError

class TestPingAnalyzer:
    """Comprehensive unit tests untuk PingAnalyzer."""
    
    def setup_method(self):
        """Setup untuk setiap test method."""
        self.analyzer = PingAnalyzer(timeout=5, retries=3)
    
    @pytest.mark.unit
    def test_ping_successful_response(self):
        """Test successful ping response parsing."""
        # Arrange
        mock_output = """
        PING google.com (172.217.168.206) 56(84) bytes of data.
        64 bytes from lga25s68-in-f14.1e100.net (172.217.168.206): icmp_seq=1 time=25.2 ms
        64 bytes from lga25s68-in-f14.1e100.net (172.217.168.206): icmp_seq=2 time=24.8 ms
        64 bytes from lga25s68-in-f14.1e100.net (172.217.168.206): icmp_seq=3 time=25.1 ms
        64 bytes from lga25s68-in-f14.1e100.net (172.217.168.206): icmp_seq=4 time=24.9 ms
        
        --- google.com ping statistics ---
        4 packets transmitted, 4 received, 0% packet loss, time 3005ms
        rtt min/avg/max/mdev = 24.8/25.0/25.2/0.2 ms
        """
        
        # Act
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                stdout=mock_output,
                stderr="",
                returncode=0
            )
            
            result = self.analyzer.ping_host("google.com", count=4)
        
        # Assert
        assert isinstance(result, PingResult)
        assert result.host == "google.com"
        assert result.ip_address == "172.217.168.206"
        assert result.packets_sent == 4
        assert result.packets_received == 4
        assert result.packet_loss == 0.0
        assert 24.8 <= result.avg_latency <= 25.2
        assert result.min_latency == 24.8
        assert result.max_latency == 25.2
    
    @pytest.mark.unit
    def test_ping_with_packet_loss(self):
        """Test ping dengan packet loss."""
        mock_output = """
        PING unreliable.com (192.168.1.100) 56(84) bytes of data.
        64 bytes from 192.168.1.100: icmp_seq=1 time=50.1 ms
        64 bytes from 192.168.1.100: icmp_seq=3 time=51.2 ms
        
        --- unreliable.com ping statistics ---
        4 packets transmitted, 2 received, 50% packet loss, time 3010ms
        rtt min/avg/max/mdev = 50.1/50.6/51.2/0.6 ms
        """
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                stdout=mock_output,
                stderr="",
                returncode=0
            )
            
            result = self.analyzer.ping_host("unreliable.com")
        
        assert result.packet_loss == 50.0
        assert result.packets_sent == 4
        assert result.packets_received == 2
    
    @pytest.mark.unit
    def test_ping_timeout_handling(self):
        """Test ping timeout scenarios."""
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired('ping', 5)
            
            with pytest.raises(TimeoutError) as exc_info:
                self.analyzer.ping_host("timeout.example.com")
            
            assert "timeout" in str(exc_info.value).lower()
    
    @pytest.mark.unit
    def test_ping_unreachable_host(self):
        """Test ping ke unreachable host."""
        mock_output = """
        PING unreachable.com (192.168.1.200) 56(84) bytes of data.
        
        --- unreachable.com ping statistics ---
        4 packets transmitted, 0 received, 100% packet loss, time 3000ms
        """
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(
                stdout=mock_output,
                stderr="",
                returncode=1
            )
            
            result = self.analyzer.ping_host("unreachable.com")
        
        assert result.packet_loss == 100.0
        assert result.packets_received == 0
    
    @pytest.mark.unit
    @pytest.mark.parametrize("host,expected_error", [
        ("", ValueError),
        (None, ValueError),
        ("invalid..host", NetworkError),
        ("256.256.256.256", NetworkError)
    ])
    def test_ping_invalid_inputs(self, host, expected_error):
        """Test ping dengan invalid inputs."""
        with pytest.raises(expected_error):
            self.analyzer.ping_host(host)
    
    @pytest.mark.unit
    def test_ping_result_properties(self):
        """Test PingResult calculated properties."""
        result = PingResult(
            host="test.com",
            packets_sent=4,
            packets_received=3,
            packet_loss=25.0,
            avg_latency=30.0
        )
        
        assert result.success_rate == 75.0
        assert result.is_healthy(threshold=70.0) is True
        assert result.is_healthy(threshold=80.0) is False

class TestPingResultModel:
    """Test PingResult data model."""
    
    @pytest.mark.unit
    def test_ping_result_creation(self):
        """Test PingResult object creation."""
        timestamp = time.time()
        result = PingResult(
            host="example.com",
            ip_address="192.168.1.1",
            packets_sent=4,
            packets_received=4,
            packet_loss=0.0,
            min_latency=20.0,
            max_latency=30.0,
            avg_latency=25.0,
            timestamp=timestamp
        )
        
        assert result.host == "example.com"
        assert result.ip_address == "192.168.1.1"
        assert result.timestamp == timestamp
        assert result.success_rate == 100.0
    
    @pytest.mark.unit
    def test_ping_result_serialization(self):
        """Test PingResult serialization/deserialization."""
        result = PingResult(
            host="example.com",
            avg_latency=25.0
        )
        
        # Test to_dict
        data = result.to_dict()
        assert data['host'] == "example.com"
        assert data['avg_latency'] == 25.0
        
        # Test from_dict
        restored = PingResult.from_dict(data)
        assert restored.host == result.host
        assert restored.avg_latency == result.avg_latency
```

#### 2. Mocking Network Operations

**Network Mocking Strategies:**
```python
# tests/unit/test_network_mocking.py
import pytest
from unittest.mock import patch, MagicMock
import requests
import socket

from netdiag.core.network import NetworkAnalyzer
from netdiag.exceptions import NetworkError

class TestNetworkMocking:
    """Tests dengan comprehensive network mocking."""
    
    @pytest.fixture
    def mock_socket(self):
        """Mock socket untuk low-level network operations."""
        with patch('socket.socket') as mock:
            mock_instance = MagicMock()
            mock.return_value = mock_instance
            yield mock_instance
    
    @pytest.fixture
    def mock_dns_resolution(self):
        """Mock DNS resolution."""
        with patch('socket.gethostbyname') as mock:
            mock.return_value = "192.168.1.100"
            yield mock
    
    @pytest.fixture
    def mock_http_requests(self):
        """Mock HTTP requests untuk connectivity tests."""
        with patch('requests.get') as mock:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.elapsed.total_seconds.return_value = 0.5
            mock.return_value = mock_response
            yield mock
    
    @pytest.mark.unit
    def test_port_scan_with_mocked_socket(self, mock_socket):
        """Test port scanning dengan mocked socket."""
        # Setup mock socket behavior
        mock_socket.connect.return_value = None  # Successful connection
        mock_socket.settimeout.return_value = None
        
        analyzer = NetworkAnalyzer()
        result = analyzer.scan_port("example.com", 80)
        
        assert result.is_open is True
        mock_socket.connect.assert_called_once()
        mock_socket.settimeout.assert_called_once_with(5)
    
    @pytest.mark.unit
    def test_dns_lookup_with_mock(self, mock_dns_resolution):
        """Test DNS lookup dengan mocked resolution."""
        analyzer = NetworkAnalyzer()
        ip = analyzer.resolve_hostname("example.com")
        
        assert ip == "192.168.1.100"
        mock_dns_resolution.assert_called_once_with("example.com")
    
    @pytest.mark.unit
    def test_http_connectivity_with_mock(self, mock_http_requests):
        """Test HTTP connectivity dengan mocked requests."""
        analyzer = NetworkAnalyzer()
        result = analyzer.check_http_connectivity("http://example.com")
        
        assert result.is_accessible is True
        assert result.response_time == 0.5
        mock_http_requests.assert_called_once_with(
            "http://example.com",
            timeout=5,
            allow_redirects=True
        )

class TestCampusMockScenarios:
    """Mock scenarios untuk campus network testing."""
    
    @pytest.mark.unit
    @pytest.mark.campus
    def test_campus_network_simulation(self):
        """Simulate campus network conditions."""
        # Mock slow campus network
        with patch('time.sleep') as mock_sleep:
            with patch('subprocess.run') as mock_ping:
                # Simulate slow network response
                mock_ping.return_value = MagicMock(
                    stdout="64 bytes from polinela.ac.id: time=150.0 ms",
                    returncode=0
                )
                
                analyzer = PingAnalyzer()
                result = analyzer.ping_host("polinela.ac.id")
                
                assert result.avg_latency == 150.0
                # Verify slow network handling
                assert not result.is_healthy(threshold=100.0)
    
    @pytest.mark.unit
    @pytest.mark.campus
    def test_campus_network_congestion_simulation(self):
        """Simulate network congestion scenarios."""
        congestion_scenarios = [
            {"packet_loss": 5.0, "latency": 80.0, "severity": "light"},
            {"packet_loss": 15.0, "latency": 200.0, "severity": "moderate"},
            {"packet_loss": 30.0, "latency": 500.0, "severity": "heavy"}
        ]
        
        for scenario in congestion_scenarios:
            with patch('subprocess.run') as mock_ping:
                mock_output = f"""
                --- test.polinela.ac.id ping statistics ---
                10 packets transmitted, {10 - int(scenario['packet_loss'] / 10)} received, 
                {scenario['packet_loss']}% packet loss
                rtt min/avg/max = {scenario['latency']}//{scenario['latency']}/{scenario['latency']} ms
                """
                mock_ping.return_value = MagicMock(
                    stdout=mock_output,
                    returncode=0
                )
                
                analyzer = PingAnalyzer()
                result = analyzer.ping_host("test.polinela.ac.id")
                
                assert result.packet_loss == scenario['packet_loss']
                assert result.avg_latency == scenario['latency']
```

### Integration Testing

#### 1. Network Integration Tests

**Real Network Testing:**
```python
# tests/integration/test_network_integration.py
import pytest
import os
from netdiag import NetworkAnalyzer
from netdiag.exceptions import NetworkError

# Skip jika integration tests tidak enabled
pytestmark = pytest.mark.skipif(
    os.getenv('RUN_INTEGRATION_TESTS') != 'true',
    reason="Integration tests disabled"
)

class TestRealNetworkOperations:
    """Integration tests dengan real network operations."""
    
    @pytest.fixture(scope="class")
    def analyzer(self):
        """Shared analyzer instance untuk integration tests."""
        return NetworkAnalyzer(timeout=10, retries=2)
    
    @pytest.mark.integration
    def test_ping_public_hosts(self, analyzer):
        """Test ping ke well-known public hosts."""
        public_hosts = [
            "google.com",
            "cloudflare.com", 
            "github.com"
        ]
        
        for host in public_hosts:
            result = analyzer.ping_host(host)
            
            assert result is not None
            assert result.host == host
            assert result.packets_sent > 0
            assert result.avg_latency > 0
            # Public hosts should be reliable
            assert result.packet_loss < 10.0
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_dns_resolution_performance(self, analyzer):
        """Test DNS resolution performance."""
        domains = [
            "google.com",
            "wikipedia.org",
            "github.com",
            "stackoverflow.com"
        ]
        
        dns_times = []
        for domain in domains:
            import time
            start = time.time()
            ip = analyzer.resolve_hostname(domain)
            dns_time = time.time() - start
            
            assert ip is not None
            assert len(ip.split('.')) == 4  # Valid IPv4
            dns_times.append(dns_time)
        
        # DNS resolution should be reasonably fast
        avg_dns_time = sum(dns_times) / len(dns_times)
        assert avg_dns_time < 2.0  # Under 2 seconds average
    
    @pytest.mark.integration
    def test_http_connectivity_real(self, analyzer):
        """Test HTTP connectivity ke real websites."""
        websites = [
            "http://httpbin.org/status/200",
            "https://httpbin.org/status/200",
            "https://www.google.com"
        ]
        
        for url in websites:
            result = analyzer.check_http_connectivity(url)
            
            assert result.is_accessible is True
            assert result.status_code == 200
            assert result.response_time > 0
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_traceroute_to_destination(self, analyzer):
        """Test traceroute ke destination."""
        result = analyzer.traceroute("google.com", max_hops=15)
        
        assert len(result.hops) > 0
        assert result.destination == "google.com"
        
        # Verify hop sequence
        for i, hop in enumerate(result.hops):
            assert hop.number == i + 1
            # Most hops should have reasonable latency
            if hop.latency is not None:
                assert hop.latency < 1000  # Under 1 second

class TestNetworkErrorHandling:
    """Test error handling dalam network operations."""
    
    @pytest.mark.integration
    def test_unreachable_host_handling(self):
        """Test handling unreachable hosts."""
        analyzer = NetworkAnalyzer(timeout=5)
        
        # Try unreachable private IP
        result = analyzer.ping_host("192.168.255.255")
        
        # Should return result dengan 100% packet loss
        assert result.packet_loss == 100.0
        assert result.packets_received == 0
    
    @pytest.mark.integration
    def test_invalid_hostname_handling(self):
        """Test handling invalid hostnames."""
        analyzer = NetworkAnalyzer()
        
        with pytest.raises(NetworkError):
            analyzer.ping_host("this-domain-definitely-does-not-exist-12345.com")
    
    @pytest.mark.integration
    def test_timeout_handling(self):
        """Test timeout handling."""
        analyzer = NetworkAnalyzer(timeout=1)  # Very short timeout
        
        # Test dengan very slow responding host or unreachable
        with pytest.raises((TimeoutError, NetworkError)):
            analyzer.ping_host("192.168.255.254")  # Likely to timeout
```

#### 2. End-to-End Testing

**Complete Workflow Tests:**
```python
# tests/integration/test_end_to_end.py
import pytest
import tempfile
import sqlite3
from pathlib import Path

from netdiag import NetworkAnalyzer
from netdiag.database import DatabaseManager
from netdiag.reporting import ReportGenerator

class TestEndToEndWorkflows:
    """End-to-end testing untuk complete workflows."""
    
    @pytest.fixture
    def temp_database(self):
        """Temporary database untuk testing."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        
        # Setup database
        db_manager = DatabaseManager(db_path)
        db_manager.initialize_database()
        
        yield db_path
        
        # Cleanup
        Path(db_path).unlink(missing_ok=True)
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_complete_network_analysis_workflow(self, temp_database):
        """Test complete network analysis workflow."""
        # Setup
        analyzer = NetworkAnalyzer()
        db_manager = DatabaseManager(temp_database)
        report_generator = ReportGenerator()
        
        # Test targets
        targets = ["google.com", "github.com"]
        
        # Step 1: Perform network analysis
        results = []
        for target in targets:
            result = analyzer.ping_host(target)
            results.append(result)
            
            # Step 2: Store results dalam database
            db_manager.save_ping_result(result)
        
        # Step 3: Retrieve data dari database
        stored_results = db_manager.get_recent_ping_results(limit=10)
        assert len(stored_results) >= len(targets)
        
        # Step 4: Generate report
        report = report_generator.generate_summary_report(results)
        assert report is not None
        assert 'summary' in report
        assert 'details' in report
        
        # Verify report content
        assert len(report['details']) == len(targets)
        for target in targets:
            target_found = any(
                detail['host'] == target 
                for detail in report['details']
            )
            assert target_found
    
    @pytest.mark.integration
    def test_monitoring_workflow(self, temp_database):
        """Test monitoring workflow dengan database persistence."""
        from netdiag.monitoring import NetworkMonitor
        
        monitor = NetworkMonitor(
            database_path=temp_database,
            interval=1  # 1 second untuk testing
        )
        
        # Add monitoring targets
        targets = ["127.0.0.1", "google.com"]
        for target in targets:
            monitor.add_target(target)
        
        # Start monitoring for short duration
        import threading
        import time
        
        monitor_thread = threading.Thread(target=monitor.start, daemon=True)
        monitor_thread.start()
        
        # Let it run for 3 seconds
        time.sleep(3)
        monitor.stop()
        
        # Verify results were stored
        db_manager = DatabaseManager(temp_database)
        results = db_manager.get_recent_ping_results(limit=50)
        
        # Should have multiple results untuk each target
        assert len(results) > 0
        
        # Verify all targets were monitored
        monitored_hosts = {result['host'] for result in results}
        for target in targets:
            assert target in monitored_hosts
```

### Campus-Specific Testing

#### 1. Campus Network Tests

**Polinela Network Testing:**
```python
# tests/campus/test_polinela_network.py
import pytest
import os
from netdiag import NetworkAnalyzer
from netdiag.campus import PolitelaNetworkConfig

# Skip jika campus tests tidak enabled
pytestmark = pytest.mark.skipif(
    os.getenv('RUN_CAMPUS_TESTS') != 'true',
    reason="Campus tests disabled"
)

class TestPolitelaNetworkAccess:
    """Tests specific untuk Polinela network environment."""
    
    @pytest.fixture(scope="class")
    def campus_analyzer(self):
        """Analyzer configured untuk campus network."""
        config = PolitelaNetworkConfig()
        return NetworkAnalyzer(
            timeout=config.get_timeout('ping'),
            retries=3
        )
    
    @pytest.mark.campus
    def test_campus_public_services(self, campus_analyzer):
        """Test accessibility ke public services kampus."""
        campus_services = [
            "polinela.ac.id",
            "www.polinela.ac.id"
        ]
        
        for service in campus_services:
            result = campus_analyzer.ping_host(service)
            
            assert result is not None
            assert result.packets_received > 0
            # Campus services should respond quickly
            assert result.avg_latency < 200.0  # Under 200ms
    
    @pytest.mark.campus
    @pytest.mark.slow
    def test_campus_internal_services(self, campus_analyzer):
        """Test internal campus services (if accessible)."""
        # These tests only run when connected to campus network
        internal_services = [
            "mail.polinela.ac.id",
            "library.polinela.ac.id",
            "elearning.polinela.ac.id"
        ]
        
        for service in internal_services:
            try:
                result = campus_analyzer.ping_host(service)
                
                if result.packets_received > 0:
                    # If accessible, should be reasonably fast
                    assert result.avg_latency < 300.0
                    print(f"✓ {service}: {result.avg_latency:.1f}ms")
                else:
                    print(f"⚠ {service}: Not accessible from current location")
                    
            except Exception as e:
                print(f"⚠ {service}: {e}")
                # Don't fail test jika service tidak accessible
                # Karena bisa tergantung network location
    
    @pytest.mark.campus
    def test_campus_network_performance_baseline(self, campus_analyzer):
        """Establish performance baseline untuk campus network."""
        # Test ke external reliable hosts dari campus
        external_hosts = ["google.com", "cloudflare.com"]
        
        performance_metrics = {}
        
        for host in external_hosts:
            result = campus_analyzer.ping_host(host, count=10)
            performance_metrics[host] = {
                'avg_latency': result.avg_latency,
                'packet_loss': result.packet_loss,
                'jitter': result.max_latency - result.min_latency
            }
        
        # Campus internet should have reasonable performance
        for host, metrics in performance_metrics.items():
            assert metrics['packet_loss'] < 20.0  # Less than 20% loss
            assert metrics['avg_latency'] < 500.0  # Less than 500ms
            
            print(f"{host}: {metrics['avg_latency']:.1f}ms avg, "
                  f"{metrics['packet_loss']:.1f}% loss")

class TestCampusNetworkSegments:
    """Test different campus network segments."""
    
    @pytest.mark.campus
    def test_network_segment_detection(self):
        """Test detection of current network segment."""
        from netdiag.campus import detect_campus_network_segment
        
        segment = detect_campus_network_segment()
        
        if segment:
            print(f"Detected campus network segment: {segment}")
            assert segment in ['admin', 'academic', 'student', 'guest', 'unknown']
        else:
            print("Not connected to campus network")
    
    @pytest.mark.campus
    def test_segment_specific_access_policies(self):
        """Test access policies untuk different segments."""
        from netdiag.campus import get_segment_access_policy
        
        policies = {
            'student': ['internet', 'elearning', 'library'],
            'academic': ['internet', 'admin', 'research', 'elearning'],
            'admin': ['all'],
            'guest': ['internet']
        }
        
        for segment, expected_access in policies.items():
            policy = get_segment_access_policy(segment)
            assert policy is not None
            assert set(expected_access).issubset(set(policy.allowed_services))

class TestEducationalScenarios:
    """Tests untuk educational scenarios dan use cases."""
    
    @pytest.mark.campus
    @pytest.mark.educational
    def test_student_lab_scenario(self):
        """Simulate student lab exercise scenario."""
        # Scenario: Student menganalisis connectivity ke berbagai services
        analyzer = NetworkAnalyzer()
        
        lab_targets = [
            ("google.com", "External Internet"),
            ("polinela.ac.id", "Campus Main Site"),
            ("127.0.0.1", "Localhost")
        ]
        
        results = {}
        for target, description in lab_targets:
            result = analyzer.ping_host(target)
            results[target] = {
                'description': description,
                'latency': result.avg_latency,
                'success': result.packets_received > 0,
                'packet_loss': result.packet_loss
            }
        
        # Generate student-friendly summary
        print("\n=== Lab Exercise Results ===")
        for target, data in results.items():
            status = "✓ SUCCESS" if data['success'] else "✗ FAILED"
            print(f"{data['description']:20} ({target:15}): {status}")
            if data['success']:
                print(f"  → Latency: {data['latency']:.1f}ms, "
                      f"Loss: {data['packet_loss']:.1f}%")
        
        # Verify educational objectives met
        assert results["127.0.0.1"]['success']  # Localhost should always work
        assert len([r for r in results.values() if r['success']]) >= 2
    
    @pytest.mark.campus
    @pytest.mark.educational
    def test_network_troubleshooting_scenario(self):
        """Simulate network troubleshooting exercise."""
        analyzer = NetworkAnalyzer()
        
        # Common troubleshooting steps
        troubleshooting_steps = [
            ("localhost", "Test local networking stack"),
            ("google.com", "Test internet connectivity"),
            ("polinela.ac.id", "Test campus connectivity")
        ]
        
        troubleshooting_results = []
        
        for target, purpose in troubleshooting_steps:
            try:
                result = analyzer.ping_host(target, count=3)
                step_result = {
                    'step': purpose,
                    'target': target,
                    'success': result.packets_received > 0,
                    'latency': result.avg_latency,
                    'diagnosis': self._diagnose_connectivity(result)
                }
            except Exception as e:
                step_result = {
                    'step': purpose,
                    'target': target,
                    'success': False,
                    'error': str(e),
                    'diagnosis': f"Connection failed: {e}"
                }
            
            troubleshooting_results.append(step_result)
        
        # Print troubleshooting report
        print("\n=== Network Troubleshooting Report ===")
        for step in troubleshooting_results:
            status = "PASS" if step['success'] else "FAIL"
            print(f"[{status}] {step['step']}")
            print(f"       Target: {step['target']}")
            print(f"       Diagnosis: {step['diagnosis']}")
        
        # Should successfully diagnose at least localhost
        localhost_result = next(r for r in troubleshooting_results if r['target'] == "localhost")
        assert localhost_result['success']
    
    def _diagnose_connectivity(self, result):
        """Helper method untuk diagnose connectivity issues."""
        if result.packets_received == 0:
            return "Host unreachable or network issue"
        elif result.packet_loss > 20:
            return f"High packet loss ({result.packet_loss:.1f}%) - network congestion"
        elif result.avg_latency > 200:
            return f"High latency ({result.avg_latency:.1f}ms) - slow connection"
        else:
            return f"Good connectivity ({result.avg_latency:.1f}ms avg)"
```

### Performance Testing

#### 1. Benchmark Tests

**Performance Benchmarking:**
```python
# tests/performance/test_benchmarks.py
import pytest
import time
import statistics
from concurrent.futures import ThreadPoolExecutor

from netdiag import NetworkAnalyzer

class TestPerformanceBenchmarks:
    """Performance benchmarking tests."""
    
    @pytest.mark.performance
    @pytest.mark.slow
    def test_ping_performance_single_host(self):
        """Benchmark single host ping performance."""
        analyzer = NetworkAnalyzer()
        host = "google.com"
        
        # Warm up
        analyzer.ping_host(host)
        
        # Benchmark multiple pings
        times = []
        for _ in range(10):
            start = time.time()
            result = analyzer.ping_host(host, count=1)
            execution_time = time.time() - start
            times.append(execution_time)
            
            assert result is not None
        
        # Calculate statistics
        avg_time = statistics.mean(times)
        median_time = statistics.median(times)
        std_dev = statistics.stdev(times) if len(times) > 1 else 0
        
        print(f"\nPing Performance Benchmark:")
        print(f"Average execution time: {avg_time:.3f}s")
        print(f"Median execution time: {median_time:.3f}s")
        print(f"Standard deviation: {std_dev:.3f}s")
        
        # Performance assertions
        assert avg_time < 5.0  # Should complete dalam 5 seconds
        assert std_dev < 2.0   # Should be reasonably consistent
    
    @pytest.mark.performance
    @pytest.mark.slow
    def test_concurrent_ping_performance(self):
        """Benchmark concurrent ping operations."""
        analyzer = NetworkAnalyzer()
        hosts = ["google.com", "github.com", "stackoverflow.com", "wikipedia.org"]
        
        # Sequential execution
        start_sequential = time.time()
        sequential_results = []
        for host in hosts:
            result = analyzer.ping_host(host)
            sequential_results.append(result)
        sequential_time = time.time() - start_sequential
        
        # Concurrent execution
        start_concurrent = time.time()
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(analyzer.ping_host, host) for host in hosts]
            concurrent_results = [future.result() for future in futures]
        concurrent_time = time.time() - start_concurrent
        
        print(f"\nConcurrency Performance Benchmark:")
        print(f"Sequential time: {sequential_time:.3f}s")
        print(f"Concurrent time: {concurrent_time:.3f}s")
        print(f"Speedup: {sequential_time/concurrent_time:.2f}x")
        
        # Verify results
        assert len(concurrent_results) == len(hosts)
        assert all(result is not None for result in concurrent_results)
        
        # Performance assertions
        assert concurrent_time < sequential_time  # Should be faster
        speedup = sequential_time / concurrent_time
        assert speedup > 1.5  # At least 50% improvement
    
    @pytest.mark.performance
    def test_memory_usage_benchmark(self):
        """Benchmark memory usage selama operations."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        
        # Measure baseline memory
        baseline_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        analyzer = NetworkAnalyzer()
        results = []
        
        # Perform multiple operations
        for i in range(50):
            result = analyzer.ping_host("google.com", count=1)
            results.append(result)
            
            # Measure memory every 10 iterations
            if i % 10 == 0:
                current_memory = process.memory_info().rss / 1024 / 1024
                memory_growth = current_memory - baseline_memory
                print(f"Iteration {i}: {current_memory:.1f}MB (+{memory_growth:.1f}MB)")
        
        # Final memory measurement
        final_memory = process.memory_info().rss / 1024 / 1024
        total_growth = final_memory - baseline_memory
        
        print(f"\nMemory Usage Benchmark:")
        print(f"Baseline memory: {baseline_memory:.1f}MB")
        print(f"Final memory: {final_memory:.1f}MB")
        print(f"Total growth: {total_growth:.1f}MB")
        print(f"Growth per operation: {total_growth/50:.3f}MB")
        
        # Memory assertions
        assert total_growth < 50.0  # Less than 50MB growth
        assert total_growth / 50 < 1.0  # Less than 1MB per operation

class TestScalabilityBenchmarks:
    """Scalability testing untuk large numbers of operations."""
    
    @pytest.mark.performance
    @pytest.mark.slow
    def test_large_host_list_performance(self):
        """Test performance dengan large number of hosts."""
        analyzer = NetworkAnalyzer()
        
        # Generate host list (mix of real dan test hosts)
        hosts = ["google.com", "github.com", "stackoverflow.com"] * 10  # 30 hosts
        
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(analyzer.ping_host, host) for host in hosts]
            results = [future.result() for future in futures]
        
        total_time = time.time() - start_time
        
        successful_pings = sum(1 for r in results if r.packets_received > 0)
        
        print(f"\nScalability Benchmark:")
        print(f"Total hosts: {len(hosts)}")
        print(f"Successful pings: {successful_pings}")
        print(f"Total time: {total_time:.3f}s")
        print(f"Average time per host: {total_time/len(hosts):.3f}s")
        print(f"Hosts per second: {len(hosts)/total_time:.1f}")
        
        # Performance assertions
        assert total_time < 60.0  # Should complete dalam 60 seconds
        assert successful_pings >= len(hosts) * 0.8  # At least 80% success
        assert len(hosts) / total_time > 0.5  # At least 0.5 hosts per second
```

### Test Automation

#### 1. Continuous Integration

**GitHub Actions Configuration:**
```yaml
# .github/workflows/tests.yml
name: NetDiag Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.7, 3.8, 3.9, "3.10"]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run unit tests
      run: |
        pytest tests/unit/ -v --cov=netdiag --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  integration-tests:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run integration tests
      env:
        RUN_INTEGRATION_TESTS: true
      run: |
        pytest tests/integration/ -v --timeout=60

  performance-tests:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run performance tests
      run: |
        pytest tests/performance/ -v --timeout=300
```

#### 2. Local Test Automation

**Makefile untuk Test Automation:**
```makefile
# Makefile
.PHONY: test test-unit test-integration test-campus test-performance clean coverage

# Default test command
test:
	pytest tests/unit/ -v

# Unit tests only
test-unit:
	pytest tests/unit/ -v --cov=netdiag

# Integration tests (requires network)
test-integration:
	RUN_INTEGRATION_TESTS=true pytest tests/integration/ -v --timeout=60

# Campus tests (requires campus network)
test-campus:
	RUN_CAMPUS_TESTS=true pytest tests/campus/ -v -m campus

# Performance tests
test-performance:
	pytest tests/performance/ -v -m performance --timeout=300

# All tests
test-all:
	RUN_INTEGRATION_TESTS=true pytest tests/ -v

# Coverage report
coverage:
	pytest tests/unit/ --cov=netdiag --cov-report=html --cov-report=term

# Clean up
clean:
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Install development dependencies
dev-install:
	pip install -r requirements-dev.txt
	pre-commit install

# Code quality checks
quality:
	black --check netdiag/
	flake8 netdiag/
	mypy netdiag/

# Fix code formatting
format:
	black netdiag/
	isort netdiag/
```

### Test Reporting

#### 1. Coverage Reporting

**Coverage Configuration:**
```python
# Generate comprehensive coverage reports
pytest --cov=netdiag --cov-report=html --cov-report=term --cov-report=xml

# View coverage report
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
```

#### 2. Test Documentation

**Test Result Documentation:**
```python
# Generate test documentation
pytest --html=test_report.html --self-contained-html

# Campus-specific test report
RUN_CAMPUS_TESTS=true pytest tests/campus/ --html=campus_test_report.html
```

### Best Practices

#### 1. Test Organization

- **Separate test types** - unit, integration, performance
- **Use appropriate markers** - untuk selective test running
- **Mock external dependencies** - untuk reliable unit tests
- **Campus-aware testing** - respect network policies

#### 2. Test Quality

- **Comprehensive assertions** - verify all expected behaviors
- **Error condition testing** - test failure scenarios
- **Performance benchmarks** - establish performance baselines
- **Educational value** - tests should demonstrate best practices

#### 3. Maintenance

- **Regular test review** - keep tests updated dengan code changes
- **Performance monitoring** - track test execution times
- **Campus coordination** - coordinate network testing dengan IT
- **Documentation updates** - keep test documentation current

Testing adalah fundamental untuk maintaining NetDiag quality dan ensuring reliable operation dalam educational environment di Politeknik Negeri Lampung.