# 📦 Installation Guide

This guide will help you install **Netdiag v1.1.0** and set up your development environment for network diagnostics and educational use.

## 📋 Prerequisites

### System Requirements
- **Python**: 3.7 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: Minimum 512MB RAM (1GB+ recommended)
- **Disk Space**: 50MB for installation

### Network Requirements
- Internet connection for installation and updates
- Administrative privileges for network operations (optional)
- Firewall configuration may be needed for advanced features

## 🚀 Quick Installation

### Option 1: pip Installation (Recommended)
```bash
# Install from PyPI (when available)
pip install netdiag

# Verify installation
python -c "import netdiag; print(netdiag.__version__)"
```

### Option 2: GitHub Installation
```bash
# Clone the repository
git clone https://github.com/SatriaDivo/netdiag.git
cd netdiag

# Install in development mode
pip install -e .

# Or install directly
pip install .
```

### Option 3: Download and Install
```bash
# Download the latest release
wget https://github.com/SatriaDivo/netdiag/archive/main.zip
unzip main.zip
cd netdiag-main

# Install
pip install .
```

## 🔧 Development Setup

### For Contributors and Developers

1. **Clone the Repository**
   ```bash
   git clone https://github.com/SatriaDivo/netdiag.git
   cd netdiag
   ```

2. **Create Virtual Environment**
   ```bash
   # Using venv
   python -m venv venv
   
   # Activate on Windows
   venv\Scripts\activate
   
   # Activate on macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   # Install development dependencies
   pip install -r requirements-dev.txt
   
   # Install package in editable mode
   pip install -e .
   ```

4. **Verify Installation**
   ```bash
   # Run tests
   python -m pytest
   
   # Check code quality
   flake8 netdiag/
   black --check netdiag/
   ```

## 📚 Educational Setup

### For Students and Educators

1. **Basic Installation**
   ```bash
   pip install netdiag
   ```

2. **Download Educational Materials**
   ```bash
   # Clone repository for examples
   git clone https://github.com/SatriaDivo/netdiag.git
   cd netdiag/docs/examples
   ```

3. **Jupyter Notebook Setup** (Optional)
   ```bash
   pip install jupyter notebook
   jupyter notebook
   ```

## 🌐 Platform-Specific Instructions

### Windows

1. **Install Python 3.7+**
   - Download from [python.org](https://python.org)
   - Add Python to PATH during installation

2. **Install netdiag**
   ```cmd
   pip install netdiag
   ```

3. **Network Permissions**
   - Some features may require administrator privileges
   - Run Command Prompt as Administrator for full functionality

### macOS

1. **Install Python 3.7+**
   ```bash
   # Using Homebrew
   brew install python
   
   # Or download from python.org
   ```

2. **Install netdiag**
   ```bash
   pip3 install netdiag
   ```

3. **Network Permissions**
   - Grant network access when prompted
   - Some features may require sudo privileges

### Linux (Ubuntu/Debian)

1. **Install Python 3.7+**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```

2. **Install netdiag**
   ```bash
   pip3 install netdiag
   ```

3. **Network Tools** (Optional)
   ```bash
   sudo apt install traceroute nmap
   ```

### Linux (CentOS/RHEL)

1. **Install Python 3.7+**
   ```bash
   sudo yum install python3 python3-pip
   ```

2. **Install netdiag**
   ```bash
   pip3 install netdiag
   ```

## 🔍 Verification and Testing

### Quick Test
```python
import netdiag

# Test basic functionality
print("Netdiag version:", netdiag.__version__)

# Test ping functionality
result = netdiag.ping("8.8.8.8")
print("Ping test:", "SUCCESS" if result else "FAILED")

# Test DNS resolution
dns_result = netdiag.dns_lookup("google.com")
print("DNS test:", "SUCCESS" if dns_result else "FAILED")
```

### Comprehensive Test
```python
import netdiag

# Run basic diagnostics
targets = ["8.8.8.8", "1.1.1.1", "google.com"]

for target in targets:
    print(f"\n=== Testing {target} ===")
    
    # Ping test
    ping_result = netdiag.ping(target)
    print(f"Ping: {'✓' if ping_result else '✗'}")
    
    # DNS lookup
    dns_result = netdiag.dns_lookup(target)
    print(f"DNS: {'✓' if dns_result else '✗'}")
    
    # Port check (HTTP)
    port_result = netdiag.check_port(target, 80)
    print(f"Port 80: {'✓' if port_result else '✗'}")
```

## 🎓 Educational Environment Setup

### Classroom/Lab Setup

1. **Batch Installation Script**
   ```bash
   #!/bin/bash
   # install_netdiag.sh
   
   echo "Installing Netdiag for educational use..."
   
   # Update system
   sudo apt update
   
   # Install Python
   sudo apt install python3 python3-pip -y
   
   # Install netdiag
   pip3 install netdiag
   
   # Verify installation
   python3 -c "import netdiag; print('Netdiag installed successfully!')"
   
   echo "Setup complete!"
   ```

2. **Jupyter Lab Setup**
   ```bash
   # Install JupyterLab
   pip install jupyterlab
   
   # Install additional tools
   pip install matplotlib pandas
   
   # Start JupyterLab
   jupyter lab
   ```

### For Polinela Students

1. **Campus Network Setup**
   ```python
   import netdiag
   
   # Configure for campus network
   campus_config = {
       'timeout': 10,
       'retries': 3,
       'interface': 'auto'
   }
   
   # Test campus connectivity
   result = netdiag.ping("polinela.ac.id", **campus_config)
   print(f"Campus connectivity: {'OK' if result else 'FAILED'}")
   ```

## 🐛 Troubleshooting

### Common Issues

**1. Permission Denied**
```bash
# Solution: Use sudo or run as administrator
sudo pip install netdiag
```

**2. Python Version Error**
```bash
# Check Python version
python --version

# Upgrade Python if needed
# Windows: Download from python.org
# macOS: brew upgrade python
# Linux: sudo apt install python3.8
```

**3. Import Error**
```python
# Verify installation
import sys
print(sys.path)

# Reinstall if needed
pip uninstall netdiag
pip install netdiag
```

**4. Network Features Not Working**
```bash
# Install additional tools (Linux)
sudo apt install traceroute nmap

# Check permissions
ping -c 1 8.8.8.8
```

### Getting Help

- 📧 **Email**: [satriadivop354@gmail.com](mailto:satriadivop354@gmail.com)
- 🐛 **Issues**: [GitHub Issues](https://github.com/SatriaDivo/netdiag/issues)
- 📖 **Documentation**: [docs/FAQ.md](FAQ.md)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/SatriaDivo/netdiag/discussions)

## 📝 Next Steps

After successful installation:

1. **Read the Documentation**: [docs/README.md](README.md)
2. **Try Quick Start**: [tutorials/quickstart.md](tutorials/quickstart.md)
3. **Explore Examples**: [examples/basic_usage.md](examples/basic_usage.md)
4. **Educational Resources**: [educational/](educational/)

---

**Installation complete! Ready to start learning! 🎓**