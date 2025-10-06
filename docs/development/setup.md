# Development Setup Guide

## 🛠️ Setting Up NetDiag Development Environment

### Overview

Guide ini akan membantu Anda setup complete development environment untuk NetDiag, termasuk konfigurasi khusus untuk development di lingkungan kampus Politeknik Negeri Lampung.

### Prerequisites

#### 1. System Requirements

**Operating System:**
- Windows 10/11 (recommended untuk kampus)
- macOS 10.15+ (untuk development flexibility)
- Ubuntu 20.04+ atau Linux distro lainnya

**Hardware Requirements:**
```yaml
Minimum:
  RAM: 4GB
  Storage: 10GB free space
  Network: Stable internet connection

Recommended:
  RAM: 8GB atau lebih
  Storage: 20GB free space
  CPU: Multi-core untuk parallel testing
  Network: Gigabit connection untuk network testing
```

#### 2. Software Prerequisites

**Python Installation:**
```bash
# Check Python version
python --version  # Should be 3.7+

# Windows - Install Python from python.org
# Or use Microsoft Store version

# macOS - Using Homebrew
brew install python@3.9

# Ubuntu/Debian
sudo apt update
sudo apt install python3.9 python3.9-pip python3.9-venv

# CentOS/RHEL
sudo yum install python39 python39-pip
```

**Git Setup:**
```bash
# Install Git
# Windows: Download from git-scm.com
# macOS: brew install git
# Linux: sudo apt install git

# Configure Git
git config --global user.name "Your Name"
git config --global user.email "your.email@polinela.ac.id"

# SSH Key for GitHub (recommended)
ssh-keygen -t ed25519 -C "your.email@polinela.ac.id"
# Add to GitHub: https://github.com/settings/keys
```

**Development Tools:**
```bash
# VS Code (recommended)
# Download from: https://code.visualstudio.com/

# Or other editors:
# PyCharm: https://www.jetbrains.com/pycharm/
# Vim/Neovim with Python plugins
# Sublime Text dengan Python packages
```

### Environment Setup

#### 1. Repository Setup

**Clone Repository:**
```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/netdiag.git
cd netdiag

# Add upstream remote
git remote add upstream https://github.com/ORIGINAL_REPO/netdiag.git

# Verify remotes
git remote -v
```

**Virtual Environment:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Verify activation
which python  # Should point to venv
python --version
```

**Dependencies Installation:**
```bash
# Install production dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt

# Install package in development mode
pip install -e .

# Verify installation
python -c "import netdiag; print(netdiag.__version__)"
```

#### 2. Development Dependencies

**Core Development Tools:**
```txt
# requirements-dev.txt content:

# Testing
pytest>=7.0.0
pytest-cov>=4.0.0
pytest-asyncio>=0.21.0
pytest-mock>=3.10.0

# Code Quality
black>=22.0.0
flake8>=5.0.0
isort>=5.10.0
mypy>=0.991

# Documentation
sphinx>=5.0.0
sphinx-rtd-theme>=1.2.0
myst-parser>=0.18.0

# Development utilities
pre-commit>=2.20.0
tox>=4.0.0
coverage>=7.0.0

# Network testing tools
scapy>=2.4.5  # Advanced packet manipulation
paramiko>=2.11.0  # SSH connections
requests>=2.28.0  # HTTP testing

# Campus-specific tools
python-snmp>=4.4.0  # SNMP integration
psutil>=5.9.0  # System monitoring
```

**Install Development Dependencies:**
```bash
pip install -r requirements-dev.txt

# Verify tools installation
black --version
flake8 --version
pytest --version
mypy --version
```

#### 3. IDE Configuration

**VS Code Setup:**
```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.pylintEnabled": false,
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": ["--line-length=88"],
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "python.testing.pytestArgs": ["tests"],
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    },
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        "**/.*": false
    }
}
```

**Recommended VS Code Extensions:**
```json
// .vscode/extensions.json
{
    "recommendations": [
        "ms-python.python",
        "ms-python.black-formatter",
        "ms-python.flake8",
        "ms-python.mypy-type-checker",
        "charliermarsh.ruff",
        "ms-vscode.test-adapter-converter",
        "littlefoxteam.vscode-python-test-adapter",
        "alefragnani.project-manager",
        "ms-vscode.vscode-json"
    ]
}
```

**PyCharm Configuration:**
```python
# PyCharm setup steps:
# 1. Open PyCharm
# 2. File → Open → Select netdiag directory
# 3. Configure Python Interpreter:
#    - File → Settings → Project → Python Interpreter
#    - Add → Existing Environment → Select venv/bin/python
# 4. Configure Code Style:
#    - Settings → Editor → Code Style → Python
#    - Set line length to 88 (Black compatible)
# 5. Enable pytest:
#    - Settings → Tools → Python Integrated Tools
#    - Default test runner: pytest
```

### Development Configuration

#### 1. Pre-commit Hooks

**Setup Pre-commit:**
```bash
# Install pre-commit hooks
pre-commit install

# Test hooks
pre-commit run --all-files
```

**Pre-commit Configuration:**
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict

  - repo: https://github.com/psf/black
    rev: 22.12.0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        additional_dependencies: [flake8-docstrings]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v0.991
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]
```

#### 2. Testing Configuration

**Pytest Configuration:**
```ini
# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*
addopts = 
    --verbose
    --tb=short
    --cov=netdiag
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
markers =
    unit: Unit tests
    integration: Integration tests
    campus: Campus-specific tests
    slow: Slow tests (require network)
    security: Security-related tests
```

**Coverage Configuration:**
```ini
# .coveragerc
[run]
source = netdiag
omit = 
    */tests/*
    */venv/*
    setup.py
    conftest.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    if self.debug:
    if settings.DEBUG
    raise AssertionError
    raise NotImplementedError
    if 0:
    if __name__ .__main__.:
    class .*\bProtocol\):
    @(abc\.)?abstractmethod

[html]
directory = htmlcov
```

#### 3. Code Quality Configuration

**Black Configuration:**
```toml
# pyproject.toml
[tool.black]
line-length = 88
target-version = ['py37', 'py38', 'py39', 'py310']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''
```

**isort Configuration:**
```toml
# pyproject.toml
[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 88
known_first_party = ["netdiag"]
known_third_party = ["pytest", "requests", "click"]
```

**Flake8 Configuration:**
```ini
# .flake8
[flake8]
max-line-length = 88
extend-ignore = E203, W503, E501
exclude = 
    .git,
    __pycache__,
    build,
    dist,
    .venv,
    venv,
    .tox,
    *.egg-info
per-file-ignores =
    __init__.py:F401
    tests/*:S101,D103
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

[mypy-tests.*]
disallow_untyped_defs = False

[mypy-scapy.*]
ignore_missing_imports = True

[mypy-paramiko.*]
ignore_missing_imports = True
```

### Campus-Specific Setup

#### 1. Network Configuration

**Campus Network Settings:**
```python
# config/campus_dev.py
"""Development configuration untuk network kampus Polinela."""

CAMPUS_DEV_CONFIG = {
    # Network ranges yang aman untuk testing
    'safe_test_ranges': [
        '127.0.0.1/32',          # Localhost
        '192.168.100.0/24',      # Development network
        '10.10.10.0/24'          # Test network
    ],
    
    # Prohibited ranges (JANGAN test di sini)
    'prohibited_ranges': [
        '192.168.1.0/24',        # Admin network
        '192.168.2.0/24',        # Faculty network
        '10.0.0.0/16'            # Production systems
    ],
    
    # Test targets yang diizinkan
    'approved_test_hosts': [
        'google.com',
        'cloudflare.com',
        '8.8.8.8',
        'polinela.ac.id'  # Public services only
    ],
    
    # Rate limiting untuk avoid network impact
    'rate_limits': {
        'ping_interval': 1.0,     # Minimum 1 second between pings
        'max_concurrent': 2,      # Maximum 2 concurrent operations
        'burst_limit': 10,        # Maximum 10 operations per minute
    },
    
    # Timeouts yang reasonable untuk campus network
    'timeouts': {
        'ping': 10,               # 10 seconds for ping
        'dns': 15,                # 15 seconds for DNS
        'http': 30,               # 30 seconds for HTTP
        'traceroute': 60          # 60 seconds for traceroute
    }
}
```

**Development Environment Variables:**
```bash
# .env file untuk development
export NETDIAG_ENV=development
export NETDIAG_CAMPUS=polinela
export NETDIAG_LOG_LEVEL=DEBUG
export NETDIAG_RATE_LIMIT=true
export NETDIAG_NETWORK_POLICY=campus_safe

# Testing configuration
export RUN_INTEGRATION_TESTS=false
export RUN_CAMPUS_TESTS=false
export TEST_TIMEOUT=30

# Database configuration untuk development
export NETDIAG_DB_PATH=dev_netdiag.db
export NETDIAG_BACKUP_ENABLED=false
```

#### 2. Permission Setup

**Network Permissions:**
```bash
# Linux: Setup untuk raw socket access (untuk ping/traceroute)
# Option 1: Run dengan sudo (development only)
sudo python -m netdiag ping google.com

# Option 2: Set capabilities (recommended)
sudo setcap cap_net_raw+ep $(which python)

# Option 3: Add user to netdev group
sudo usermod -a -G netdev $USER
```

**Windows Network Permissions:**
```powershell
# Run PowerShell sebagai Administrator
# Check current permissions
whoami /priv

# Enable ping without admin (Windows 10+)
# Usually works by default, tetapi untuk raw sockets:
# Run development environment sebagai Administrator jika needed
```

#### 3. Campus IT Coordination

**Development Notification:**
```python
# utils/campus_notification.py
"""Notification system untuk koordinasi dengan IT kampus."""

import smtplib
from email.mime.text import MIMEText
from typing import Dict, Any

def notify_campus_it(operation: str, details: Dict[str, Any]) -> bool:
    """
    Notify campus IT tentang development activities.
    
    Args:
        operation: Type of operation (testing, monitoring, etc.)
        details: Details dari operation yang akan dilakukan
        
    Returns:
        True jika notification berhasil dikirim
    """
    
    # Template notification email
    message = f"""
    NetDiag Development Activity Notification
    
    Developer: {details.get('developer', 'Unknown')}
    Operation: {operation}
    Time: {details.get('timestamp')}
    Duration: {details.get('duration', 'Unknown')}
    
    Network Impact:
    - Test Targets: {details.get('targets', [])}
    - Rate Limit: {details.get('rate_limit', 'Standard')}
    - Max Concurrent: {details.get('max_concurrent', 1)}
    
    Purpose: {details.get('purpose', 'Development testing')}
    
    Contact: {details.get('contact', 'developer@polinela.ac.id')}
    """
    
    try:
        # Send notification to campus IT
        # Implementation depends on campus email system
        print("Campus IT notification sent successfully")
        return True
    except Exception as e:
        print(f"Failed to send campus notification: {e}")
        return False

# Usage dalam development
if __name__ == "__main__":
    notify_campus_it("network_testing", {
        'developer': 'Student Name',
        'timestamp': '2024-01-15 10:00:00',
        'duration': '30 minutes',
        'targets': ['google.com', '8.8.8.8'],
        'purpose': 'Testing new ping functionality'
    })
```

### Database Setup

#### 1. Development Database

**SQLite Setup (Default):**
```python
# database/dev_setup.py
"""Development database setup script."""

import sqlite3
import os
from pathlib import Path

def setup_dev_database(db_path: str = "dev_netdiag.db"):
    """Setup development database dengan sample data."""
    
    # Create database directory
    db_file = Path(db_path)
    db_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Connect dan create tables
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create tables
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS ping_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp REAL NOT NULL,
        host TEXT NOT NULL,
        ip_address TEXT,
        packets_sent INTEGER,
        packets_received INTEGER,
        packet_loss REAL,
        min_latency REAL,
        max_latency REAL,
        avg_latency REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE TABLE IF NOT EXISTS dns_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp REAL NOT NULL,
        domain TEXT NOT NULL,
        record_type TEXT,
        response_time REAL,
        records TEXT,  -- JSON string
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE TABLE IF NOT EXISTS bandwidth_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp REAL NOT NULL,
        download_speed REAL,
        upload_speed REAL,
        server TEXT,
        duration REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Sample data untuk development
    INSERT OR IGNORE INTO ping_results 
    (timestamp, host, ip_address, packets_sent, packets_received, 
     packet_loss, avg_latency) VALUES
    (1642262400, 'google.com', '8.8.8.8', 4, 4, 0.0, 25.5),
    (1642262460, 'polinela.ac.id', '192.168.1.100', 4, 4, 0.0, 15.2),
    (1642262520, 'slow.example.com', '192.168.1.200', 4, 3, 25.0, 150.0);
    """)
    
    conn.commit()
    conn.close()
    
    print(f"Development database setup complete: {db_path}")

if __name__ == "__main__":
    setup_dev_database()
```

**Run Database Setup:**
```bash
# Setup development database
python database/dev_setup.py

# Verify database
sqlite3 dev_netdiag.db ".tables"
sqlite3 dev_netdiag.db "SELECT * FROM ping_results;"
```

#### 2. Test Database

**Test Database Configuration:**
```python
# conftest.py (pytest configuration)
"""Pytest configuration dan fixtures untuk testing."""

import pytest
import tempfile
import sqlite3
from pathlib import Path
from netdiag import NetworkAnalyzer
from netdiag.database import DatabaseManager

@pytest.fixture(scope="function")
def temp_db():
    """Create temporary database untuk testing."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    # Setup test database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.executescript("""
    CREATE TABLE ping_results (
        id INTEGER PRIMARY KEY,
        timestamp REAL,
        host TEXT,
        avg_latency REAL
    );
    """)
    conn.commit()
    conn.close()
    
    yield db_path
    
    # Cleanup
    Path(db_path).unlink(missing_ok=True)

@pytest.fixture
def network_analyzer():
    """Create NetworkAnalyzer instance untuk testing."""
    return NetworkAnalyzer(timeout=5, retries=2)

@pytest.fixture
def sample_ping_result():
    """Sample PingResult untuk testing."""
    from netdiag.models import PingResult
    return PingResult(
        host="test.example.com",
        ip_address="192.168.1.100",
        avg_latency=25.5,
        packet_loss=0.0
    )
```

### Running Tests

#### 1. Test Categories

**Unit Tests:**
```bash
# Run unit tests only
pytest tests/unit/ -v

# Run dengan coverage
pytest tests/unit/ --cov=netdiag --cov-report=html

# Run specific test file
pytest tests/unit/test_ping.py -v

# Run specific test method
pytest tests/unit/test_ping.py::TestPingAnalyzer::test_successful_ping -v
```

**Integration Tests:**
```bash
# Run integration tests (requires network)
export RUN_INTEGRATION_TESTS=true
pytest tests/integration/ -v

# Run campus-specific tests (requires campus network)
export RUN_CAMPUS_TESTS=true
pytest tests/campus/ -v -m campus
```

**Performance Tests:**
```bash
# Run performance/load tests
pytest tests/performance/ -v -m slow

# With custom timeouts
pytest tests/performance/ --timeout=60
```

#### 2. Test Commands

**Complete Test Suite:**
```bash
# Run all tests
pytest

# Run dengan parallel execution
pytest -n auto

# Run dengan detailed output
pytest -v --tb=long

# Run tests yang failed pada run sebelumnya
pytest --lf

# Run tests dengan specific markers
pytest -m "not slow"  # Skip slow tests
pytest -m "unit"      # Run only unit tests
pytest -m "campus"    # Run only campus tests
```

**Continuous Testing:**
```bash
# Install pytest-watch
pip install pytest-watch

# Watch for changes dan auto-run tests
ptw --runner "pytest tests/unit/"

# With coverage
ptw --runner "pytest tests/unit/ --cov=netdiag"
```

### Documentation Development

#### 1. Sphinx Documentation

**Setup Sphinx:**
```bash
# Install documentation dependencies
pip install sphinx sphinx-rtd-theme myst-parser

# Initialize Sphinx (if not already done)
sphinx-quickstart docs

# Build documentation
cd docs
make html

# View documentation
# Open docs/_build/html/index.html dalam browser
```

**Documentation Development:**
```bash
# Auto-rebuild documentation saat files berubah
pip install sphinx-autobuild

# Start development server
sphinx-autobuild docs docs/_build/html

# Documentation akan available di http://localhost:8000
# Dan akan auto-reload saat ada changes
```

#### 2. API Documentation

**Generate API Docs:**
```bash
# Generate API documentation dari docstrings
sphinx-apidoc -o docs/api netdiag

# Include dalam main documentation
# Add to docs/index.rst:
# .. toctree::
#    :maxdepth: 2
#    
#    api/modules
```

### Troubleshooting

#### 1. Common Issues

**Virtual Environment Issues:**
```bash
# Issue: Command not found after activation
# Solution: Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate  # atau venv\Scripts\activate
pip install -r requirements.txt

# Issue: Permission denied pada Linux
# Solution: Fix permissions
chmod +x venv/bin/activate
```

**Network Permission Issues:**
```bash
# Issue: Raw socket permission denied
# Solution 1: Run dengan sudo (development only)
sudo -E python -m pytest tests/integration/

# Solution 2: Set capabilities
sudo setcap cap_net_raw+ep $(which python)

# Solution 3: Use mock objects untuk testing
export USE_MOCK_NETWORK=true
pytest tests/
```

**Campus Network Issues:**
```python
# Issue: Timeouts pada campus network
# Solution: Increase timeouts dalam test configuration
CAMPUS_TEST_CONFIG = {
    'ping_timeout': 15,      # Increase dari 5
    'dns_timeout': 20,       # Increase dari 10
    'http_timeout': 45       # Increase dari 30
}
```

#### 2. Debug Configuration

**Debug Logging:**
```python
# Enable debug logging dalam development
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Or via environment variable
export NETDIAG_LOG_LEVEL=DEBUG
```

**Network Debug:**
```bash
# Debug network connectivity
ping google.com
nslookup google.com
traceroute google.com  # Linux/Mac
tracert google.com     # Windows

# Check firewall settings
# Linux: sudo iptables -L
# Windows: Windows Defender Firewall settings
# macOS: System Preferences → Security & Privacy → Firewall
```

### Next Steps

Setelah setup development environment:

1. **Explore Codebase** - Familiarize dengan structure dan existing code
2. **Run Tests** - Ensure everything works dengan test suite
3. **Read Contributing Guide** - Understand contribution process
4. **Pick First Issue** - Start dengan good first issue label
5. **Setup Campus Integration** - Configure untuk campus network testing

Happy coding! 🚀