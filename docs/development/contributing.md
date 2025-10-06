# Contributing to NetDiag

## 🤝 Panduan Kontribusi untuk Developer

### Selamat Datang, Kontributor!

Terima kasih atas minat Anda untuk berkontribusi pada NetDiag! Dokumentasi ini akan memandu Anda melalui proses kontribusi yang efektif dan terstruktur.

### Cara Berkontribusi

#### 1. Jenis Kontribusi yang Diterima

**Code Contributions:**
- Bug fixes dan perbaikan
- Fitur baru untuk network analysis
- Optimasi performance
- Peningkatan compatibility
- Documentation improvements

**Non-Code Contributions:**
- Laporan bug dan issue reports
- Feature requests dan suggestions
- Documentation improvements
- Testing dan quality assurance
- Educational content untuk kampus

**Campus-Specific Contributions:**
- Konfigurasi untuk network Polinela
- Use cases untuk pembelajaran
- Lab exercises dan assignments
- Integration dengan sistem kampus

#### 2. Getting Started

**Prerequisites:**
```bash
# Pastikan Python 3.7+ installed
python --version

# Git untuk version control
git --version

# Virtual environment tools
pip install virtualenv
```

**Fork and Clone:**
```bash
# 1. Fork repository di GitHub
# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/netdiag.git
cd netdiag

# 3. Add upstream remote
git remote add upstream https://github.com/ORIGINAL_OWNER/netdiag.git

# 4. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate     # Windows

# 5. Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

#### 3. Development Workflow

**Branch Strategy:**
```bash
# Update your fork
git checkout main
git pull upstream main
git push origin main

# Create feature branch
git checkout -b feature/new-network-analyzer
# atau
git checkout -b bugfix/ping-timeout-issue
# atau
git checkout -b docs/api-documentation
```

**Commit Convention:**
```bash
# Format: type(scope): description
git commit -m "feat(ping): add IPv6 support for ping operations"
git commit -m "fix(dns): resolve timeout issue in DNS queries"
git commit -m "docs(api): update function documentation"
git commit -m "test(network): add unit tests for NetworkAnalyzer"
git commit -m "refactor(core): optimize ping result processing"
```

**Commit Types:**
- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation changes
- `test`: Adding or updating tests
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `style`: Code style changes
- `ci`: CI/CD changes

### Code Standards

#### 1. Python Code Style

**PEP 8 Compliance:**
```python
# Good: Clear naming dan formatting
class NetworkAnalyzer:
    """Analyzer untuk operasi network diagnostics."""
    
    def __init__(self, timeout: int = 5, retries: int = 3):
        self.timeout = timeout
        self.retries = retries
        self._logger = logging.getLogger(__name__)
    
    def ping_host(self, host: str, count: int = 4) -> PingResult:
        """
        Ping target host dan return hasil analysis.
        
        Args:
            host: Target hostname atau IP address
            count: Jumlah ping packets yang dikirim
            
        Returns:
            PingResult object dengan detailed metrics
            
        Raises:
            NetworkError: Jika ping operation gagal
        """
        try:
            # Implementation here
            return self._execute_ping(host, count)
        except Exception as e:
            self._logger.error(f"Ping failed for {host}: {e}")
            raise NetworkError(f"Failed to ping {host}") from e

# Avoid: Poor naming dan structure
class na:  # Bad naming
    def p(self, h, c=4):  # Bad naming, no types
        pass  # No implementation
```

**Type Hints:**
```python
from typing import List, Dict, Optional, Union, Protocol
from dataclasses import dataclass

@dataclass
class PingResult:
    """Structured ping result data."""
    host: str
    ip_address: Optional[str] = None
    avg_latency: float = 0.0
    packet_loss: float = 0.0
    timestamps: List[float] = field(default_factory=list)

def analyze_network_range(
    network: str,
    scan_type: str = "ping",
    concurrent_threads: int = 4,
    timeout: float = 5.0
) -> Dict[str, PingResult]:
    """Analyze entire network range dengan parallel processing."""
    pass

# Protocol untuk extension points
class Pingable(Protocol):
    def ping(self, timeout: float) -> PingResult:
        """Ping operation protocol."""
        ...
```

#### 2. Documentation Standards

**Docstring Format (Google Style):**
```python
def traceroute_host(self, destination: str, max_hops: int = 30) -> List[TracerouteHop]:
    """
    Perform traceroute ke destination host.
    
    Traceroute menunjukkan jalur yang dilalui packet untuk mencapai destination,
    berguna untuk network troubleshooting dan analysis topology.
    
    Args:
        destination: Target hostname atau IP address untuk traceroute
        max_hops: Maximum number of hops (default: 30)
        
    Returns:
        List dari TracerouteHop objects, masing-masing berisi informasi
        tentang hop dalam jalur ke destination.
        
    Raises:
        NetworkError: Jika traceroute operation gagal completely
        TimeoutError: Jika operation melebihi configured timeout
        
    Example:
        ```python
        analyzer = NetworkAnalyzer()
        hops = analyzer.traceroute_host("polinela.ac.id")
        
        for hop in hops:
            print(f"Hop {hop.number}: {hop.address} ({hop.latency}ms)")
        ```
        
    Note:
        Traceroute memerlukan elevated privileges pada beberapa sistem.
        Pastikan aplikasi dijalankan dengan permission yang sesuai.
    """
    pass
```

**Educational Documentation:**
```python
def bandwidth_test(self, target_server: str, duration: int = 10) -> BandwidthResult:
    """
    Test bandwidth ke target server.
    
    Educational Context:
        Function ini berguna untuk mahasiswa TRI (Teknologi Rekayasa Internet)
        di Polinela untuk memahami:
        - Concept of network bandwidth measurement
        - Difference antara theoretical dan actual throughput
        - Impact dari network congestion pada performance
        
    Practical Application:
        - Lab exercise: Measuring campus network performance
        - Assignment: Comparing bandwidth across different network segments
        - Project: Network capacity planning untuk dormitory network
        
    Args:
        target_server: Server untuk bandwidth testing (contoh: speedtest.net)
        duration: Duration test dalam seconds (recommend 10-30s)
        
    Returns:
        BandwidthResult dengan download/upload speeds, latency metrics
        
    Campus Network Context:
        Saat testing di network Polinela, perhatikan:
        - Peak hours (08:00-10:00, 13:00-15:00) untuk realistic measurements
        - Different segments (admin, academic, student, guest)
        - QoS policies yang mungkin mempengaruhi results
    """
    pass
```

#### 3. Testing Standards

**Unit Tests:**
```python
import unittest
from unittest.mock import patch, MagicMock
import pytest
from netdiag import NetworkAnalyzer, PingResult

class TestNetworkAnalyzer(unittest.TestCase):
    """Test suite untuk NetworkAnalyzer class."""
    
    def setUp(self):
        """Setup test environment."""
        self.analyzer = NetworkAnalyzer(timeout=5, retries=3)
        
    def test_ping_successful_response(self):
        """Test ping dengan successful response."""
        # Arrange
        test_host = "test.example.com"
        expected_latency = 25.5
        
        # Act
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.stdout = "Reply from 192.168.1.1: bytes=32 time=25ms"
            mock_run.return_value.returncode = 0
            
            result = self.analyzer.ping_host(test_host)
            
        # Assert
        self.assertIsInstance(result, PingResult)
        self.assertEqual(result.host, test_host)
        self.assertGreater(result.avg_latency, 0)
        
    def test_ping_timeout_handling(self):
        """Test ping timeout handling."""
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired('ping', 5)
            
            with self.assertRaises(TimeoutError):
                self.analyzer.ping_host("unreachable.host")
    
    @pytest.mark.parametrize("host,expected_ip", [
        ("localhost", "127.0.0.1"),
        ("google.com", None),  # IP akan vary
        ("invalid.host.name", None)
    ])
    def test_ping_various_hosts(self, host, expected_ip):
        """Test ping dengan various host types."""
        result = self.analyzer.ping_host(host)
        
        if expected_ip:
            self.assertEqual(result.ip_address, expected_ip)

class TestNetworkAnalyzerIntegration(unittest.TestCase):
    """Integration tests untuk real network operations."""
    
    @unittest.skipUnless(
        os.getenv('RUN_INTEGRATION_TESTS') == 'true',
        "Integration tests disabled"
    )
    def test_ping_real_host(self):
        """Test ping ke real host (requires network)."""
        analyzer = NetworkAnalyzer()
        result = analyzer.ping_host("google.com")
        
        self.assertIsNotNone(result)
        self.assertGreater(result.packets_sent, 0)

# Campus-specific tests
class TestPolitelaNetworkIntegration(unittest.TestCase):
    """Tests specific untuk Polinela network environment."""
    
    def test_campus_servers_accessibility(self):
        """Test accessibility ke servers penting kampus."""
        campus_servers = [
            "polinela.ac.id",
            "mail.polinela.ac.id",
            "library.polinela.ac.id"
        ]
        
        analyzer = NetworkAnalyzer()
        
        for server in campus_servers:
            with self.subTest(server=server):
                result = analyzer.ping_host(server)
                self.assertIsNotNone(result)
                # Campus network should respond within reasonable time
                self.assertLess(result.avg_latency, 100)
```

**Test Coverage:**
```bash
# Run tests dengan coverage
pytest --cov=netdiag --cov-report=html tests/

# Minimum coverage requirement: 80%
pytest --cov=netdiag --cov-fail-under=80
```

### Pull Request Process

#### 1. Pre-submission Checklist

**Code Quality:**
- [ ] Code follows PEP 8 style guidelines
- [ ] All functions have proper type hints
- [ ] Comprehensive docstrings dengan examples
- [ ] Educational context untuk campus use cases
- [ ] Error handling dan appropriate exceptions

**Testing:**
- [ ] Unit tests untuk new functionality
- [ ] Integration tests jika applicable
- [ ] Test coverage >= 80%
- [ ] All tests passing locally
- [ ] Campus-specific test cases jika relevant

**Documentation:**
- [ ] API documentation updated
- [ ] README updated jika necessary
- [ ] Educational examples included
- [ ] Campus network considerations documented

#### 2. Pull Request Template

```markdown
## Description
Brief description of changes dan motivation behind them.

## Type of Change
- [ ] Bug fix (non-breaking change yang fix issue)
- [ ] New feature (non-breaking change yang add functionality)
- [ ] Breaking change (fix atau feature yang cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Campus-specific enhancement

## Campus Context
Jika applicable, jelaskan bagaimana changes ini benefit atau impact Polinela network environment:
- Impact pada network monitoring di kampus
- Educational value untuk mahasiswa TRI
- Integration dengan existing campus infrastructure

## Testing
Describe testing yang telah dilakukan:
- [ ] Unit tests
- [ ] Integration tests  
- [ ] Manual testing pada campus network
- [ ] Performance testing

## Screenshots/Output
Jika applicable, tambahkan screenshots atau sample output.

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added dan passing
- [ ] No unnecessary dependencies added
```

#### 3. Review Process

**Code Review Criteria:**
1. **Functionality** - Does code work as intended?
2. **Code Quality** - Is code well-structured dan maintainable?
3. **Testing** - Adequate test coverage dan quality?
4. **Documentation** - Clear dan comprehensive documentation?
5. **Campus Relevance** - Adds value untuk educational context?

**Review Timeline:**
- Initial review: 2-3 business days
- Follow-up reviews: 1-2 business days
- Campus network testing: 1 week (jika required)

### Development Environment

#### 1. Local Development Setup

**Required Tools:**
```bash
# Development dependencies
pip install -r requirements-dev.txt

# Tools yang akan di-install:
# - pytest: Testing framework
# - black: Code formatter
# - flake8: Linting
# - mypy: Type checking
# - sphinx: Documentation generation
# - pre-commit: Git hooks
```

**Pre-commit Hooks:**
```bash
# Install pre-commit hooks
pre-commit install

# Hooks yang akan run:
# - black: Auto-format code
# - flake8: Lint checking
# - mypy: Type checking
# - tests: Quick test run
```

**VS Code Settings:**
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "files.associations": {
        "*.py": "python"
    }
}
```

#### 2. Campus Development Environment

**Network Access Requirements:**
```python
# Configuration untuk development di network kampus
CAMPUS_DEVELOPMENT_CONFIG = {
    'allowed_test_ranges': [
        '192.168.1.0/24',  # Admin network (with permission)
        '192.168.3.0/24',  # Student network
        '127.0.0.1/32'     # Localhost
    ],
    'prohibited_ranges': [
        '192.168.2.0/24',  # Faculty network (no testing)
        '10.0.0.0/8'       # Production systems
    ],
    'test_timeouts': {
        'ping': 10,     # Longer timeout untuk campus network
        'dns': 15,      # DNS bisa slow
        'http': 30      # Web requests
    }
}
```

**Ethical Guidelines:**
- Gunakan hanya network ranges yang diizinkan untuk testing
- Hindari excessive network traffic yang bisa impact performance
- Coordinate dengan IT department untuk major testing
- Respect bandwidth limitations dan peak hours
- Document any testing yang melibatkan production systems

### Release Process

#### 1. Version Management

**Semantic Versioning:**
- MAJOR.MINOR.PATCH (e.g., 1.2.3)
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

**Release Notes Format:**
```markdown
# NetDiag v1.2.0

## New Features
- Added IPv6 support untuk ping operations
- Integration dengan Prometheus metrics
- Campus network templates untuk Polinela

## Improvements  
- Performance optimization untuk concurrent operations
- Enhanced error handling dan logging
- Updated documentation dengan educational examples

## Bug Fixes
- Fixed timeout issue dalam DNS resolution
- Corrected bandwidth calculation untuk high-speed networks

## Campus-Specific Updates
- Added Polinela network configuration templates
- Integration examples untuk campus monitoring systems
- Educational lab exercises untuk TRI students

## Breaking Changes
- None

## Migration Guide
No migration required untuk this release.
```

#### 2. Release Checklist

**Pre-release:**
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Version number updated
- [ ] Release notes prepared
- [ ] Campus testing completed

**Release:**
- [ ] Tag version dalam Git
- [ ] Build dan upload ke PyPI
- [ ] Update documentation website
- [ ] Announce dalam campus communication channels

### Community Guidelines

#### 1. Communication Channels

**GitHub Issues:**
- Bug reports
- Feature requests
- Technical discussions

**Campus Channels:**
- Internal Polinela mailing lists
- Student forums dan discussion groups
- Faculty coordination untuk educational integration

#### 2. Code of Conduct

**Expectations:**
- Be respectful dan inclusive
- Focus pada constructive feedback
- Support educational mission dari project
- Respect campus network policies dan guidelines
- Collaborate effectively dengan diverse backgrounds

**Enforcement:**
Violations akan di-address melalui:
1. Private discussion dengan contributor
2. Warning dalam appropriate channel
3. Temporary restriction dari project participation
4. Permanent ban untuk serious violations

### Getting Help

#### 1. Documentation Resources

- **API Documentation**: `/docs/api/`
- **Tutorial dan Examples**: `/docs/tutorials/`
- **Campus-Specific Guides**: `/docs/educational/`
- **Advanced Topics**: `/docs/advanced/`

#### 2. Support Channels

**Technical Support:**
- GitHub Issues untuk bugs dan feature requests
- Discussion forum untuk general questions
- Campus IT support untuk network-related issues

**Educational Support:**
- Faculty coordination untuk curriculum integration
- Student mentoring untuk project contributions
- Lab assistance untuk hands-on learning

### Recognition

#### 1. Contributor Recognition

Contributors akan diakui melalui:
- Credits dalam README dan documentation
- Contributor spotlight dalam campus newsletters
- Speaking opportunities di campus events
- Recommendation letters untuk outstanding contributions

#### 2. Academic Credit

**Student Contributors:**
- Independent study credit options
- Capstone project opportunities
- Research publication possibilities
- Industry internship recommendations

**Faculty Contributors:**
- Professional development recognition
- Research collaboration opportunities
- Grant application support
- Conference presentation opportunities

---

Terima kasih untuk contribution Anda pada NetDiag! Bersama-sama kita membangun tools yang powerful untuk network analysis dan educational excellence di Politeknik Negeri Lampung.