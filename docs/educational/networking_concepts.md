# 🌐 Networking Concepts

Essential networking concepts explained through practical examples using the Netdiag toolkit. This guide bridges theoretical knowledge with hands-on experience.

## 📚 Table of Contents

- [OSI Model in Practice](#-osi-model-in-practice)
- [TCP/IP Protocol Suite](#-tcpip-protocol-suite)
- [IP Addressing and Subnetting](#-ip-addressing-and-subnetting)
- [Domain Name System (DNS)](#-domain-name-system-dns)
- [Network Ports and Services](#-network-ports-and-services)
- [Routing and Path Discovery](#-routing-and-path-discovery)
- [Network Performance](#-network-performance)
- [Security Fundamentals](#-security-fundamentals)

---

## 🏗️ OSI Model in Practice

### Understanding the 7-Layer Model

The OSI (Open Systems Interconnection) model provides a framework for understanding network communication. Let's explore each layer with practical Netdiag examples:

#### Layer 1: Physical Layer
**Concept**: Physical transmission of raw bits over communication channels.
**Real-world**: Ethernet cables, Wi-Fi radio waves, fiber optic light.

```python
# While we can't directly test Layer 1 with software,
# we can check physical connectivity symptoms
interfaces = netdiag.get_network_interfaces()
for interface in interfaces:
    print(f"Interface {interface.name}: {interface.status}")
    if interface.status == 'down':
        print("  ⚠️ Possible physical layer issue")
```

#### Layer 2: Data Link Layer
**Concept**: Node-to-node delivery, MAC addresses, frame formatting.
**Real-world**: Ethernet frames, ARP protocol, switch operations.

```python
# Check ARP table (MAC address mappings)
arp_table = netdiag.get_arp_table()
print("🔗 Layer 2 - Data Link Information:")
for entry in arp_table[:5]:  # Show first 5 entries
    print(f"  IP: {entry.ip} -> MAC: {entry.mac}")

# MAC address vendor lookup
mac_info = netdiag.mac_address_lookup("00:1B:44:11:3A:B7")
print(f"  Vendor: {mac_info.vendor}")
```

#### Layer 3: Network Layer
**Concept**: Routing between networks, IP addressing, packet forwarding.
**Real-world**: IP protocol, routing tables, ICMP.

```python
# Layer 3 testing with ping (ICMP)
print("🌐 Layer 3 - Network Layer Testing:")
targets = ["127.0.0.1", "192.168.1.1", "8.8.8.8", "polinela.ac.id"]

for target in targets:
    try:
        result = netdiag.ping(target, count=1)
        print(f"  {target}: ✅ Reachable ({result.avg_time:.1f}ms)")
    except Exception as e:
        print(f"  {target}: ❌ Unreachable ({e})")

# Check routing table
routes = netdiag.get_routing_table()
print(f"  Active routes: {len(routes)}")
```

#### Layer 4: Transport Layer
**Concept**: End-to-end delivery, port numbers, TCP/UDP protocols.
**Real-world**: TCP connections, UDP datagrams, port management.

```python
# Layer 4 testing with port connections
print("🚚 Layer 4 - Transport Layer Testing:")
transport_tests = [
    ("polinela.ac.id", 80, "TCP"),   # HTTP
    ("polinela.ac.id", 443, "TCP"),  # HTTPS
    ("8.8.8.8", 53, "UDP"),         # DNS
]

for host, port, protocol in transport_tests:
    try:
        result = netdiag.check_port(host, port, protocol=protocol.lower())
        status = "✅ Open" if result.is_open else "❌ Closed"
        print(f"  {host}:{port}/{protocol}: {status}")
    except Exception as e:
        print(f"  {host}:{port}/{protocol}: ⚠️ Error")
```

#### Layer 5-7: Session, Presentation, Application Layers
**Concept**: Session management, data formatting, application protocols.
**Real-world**: HTTP, HTTPS, FTP, SSH, SMTP.

```python
# Application layer testing
print("📱 Layer 5-7 - Application Layer Testing:")

# HTTP/HTTPS service detection
web_services = [
    ("polinela.ac.id", 80, "HTTP"),
    ("polinela.ac.id", 443, "HTTPS")
]

for host, port, service in web_services:
    try:
        result = netdiag.service_detection(host, port)
        if result.service:
            print(f"  {service}: ✅ {result.service} {result.version or ''}")
        else:
            print(f"  {service}: ❌ Service not detected")
    except Exception as e:
        print(f"  {service}: ⚠️ Detection failed")
```

---

## 🌍 TCP/IP Protocol Suite

### The Internet Protocol Stack

Understanding how modern networks actually work using the TCP/IP model:

#### Application Layer Protocols
```python
def demonstrate_application_protocols():
    """Demonstrate various application layer protocols."""
    
    print("📡 Application Layer Protocol Demonstration")
    print("=" * 50)
    
    target = "polinela.ac.id"
    
    # DNS (Domain Name System)
    print("\n1. DNS Protocol:")
    try:
        dns_result = netdiag.dns_lookup(target)
        print(f"   Query: {target} -> {dns_result.ip_address}")
        print(f"   DNS Server: {dns_result.dns_server}")
        print(f"   Query Time: {dns_result.query_time:.2f}ms")
    except Exception as e:
        print(f"   DNS Error: {e}")
    
    # HTTP Protocol
    print("\n2. HTTP Protocol:")
    try:
        http_result = netdiag.check_port(target, 80)
        if http_result.is_open:
            print(f"   HTTP Service: Available")
            if http_result.banner:
                print(f"   Server Banner: {http_result.banner[:50]}...")
        else:
            print(f"   HTTP Service: Not available")
    except Exception as e:
        print(f"   HTTP Error: {e}")
    
    # HTTPS Protocol
    print("\n3. HTTPS Protocol:")
    try:
        https_result = netdiag.check_port(target, 443)
        if https_result.is_open:
            print(f"   HTTPS Service: Available")
            # SSL certificate check
            ssl_info = netdiag.ssl_certificate_check(target)
            print(f"   SSL Certificate: {'Valid' if ssl_info.is_valid else 'Invalid'}")
            print(f"   Certificate Issuer: {ssl_info.issuer}")
        else:
            print(f"   HTTPS Service: Not available")
    except Exception as e:
        print(f"   HTTPS Error: {e}")

# Run demonstration
demonstrate_application_protocols()
```

#### Transport Layer: TCP vs UDP
```python
def compare_tcp_udp():
    """Compare TCP and UDP characteristics."""
    
    print("🚚 TCP vs UDP Comparison")
    print("=" * 40)
    
    # TCP characteristics demonstration
    print("\n📡 TCP (Transmission Control Protocol):")
    print("   ✅ Connection-oriented")
    print("   ✅ Reliable delivery")
    print("   ✅ Error correction")
    print("   ❌ Higher overhead")
    
    # Test TCP services
    tcp_services = [
        ("polinela.ac.id", 80, "HTTP"),
        ("polinela.ac.id", 443, "HTTPS"),
        ("polinela.ac.id", 22, "SSH")
    ]
    
    print("\n   TCP Service Tests:")
    for host, port, service in tcp_services:
        result = netdiag.check_port(host, port, protocol='tcp')
        status = "✅" if result.is_open else "❌"
        print(f"     {service} ({port}/tcp): {status}")
    
    # UDP characteristics demonstration
    print("\n📡 UDP (User Datagram Protocol):")
    print("   ✅ Connectionless")
    print("   ✅ Low overhead")
    print("   ✅ Fast transmission")
    print("   ❌ No delivery guarantee")
    
    # Test UDP services
    udp_services = [
        ("8.8.8.8", 53, "DNS"),
        ("1.1.1.1", 53, "DNS"),
    ]
    
    print("\n   UDP Service Tests:")
    for host, port, service in udp_services:
        try:
            result = netdiag.check_port(host, port, protocol='udp')
            status = "✅" if result.is_open else "❌"
            print(f"     {service} ({port}/udp): {status}")
        except Exception:
            print(f"     {service} ({port}/udp): ⚠️ Test inconclusive")

# Run comparison
compare_tcp_udp()
```

---

## 🏠 IP Addressing and Subnetting

### Understanding IP Address Classes and CIDR

```python
def ip_addressing_tutorial():
    """Interactive IP addressing and subnetting tutorial."""
    
    print("🏠 IP Addressing and Subnetting Tutorial")
    print("=" * 50)
    
    # IP Address Classification
    test_ips = [
        "10.0.0.1",        # Class A Private
        "172.16.0.1",      # Class B Private  
        "192.168.1.1",     # Class C Private
        "8.8.8.8",         # Class A Public
        "172.217.14.110",  # Class B Public
        "203.113.130.45",  # Class C Public
        "127.0.0.1",       # Loopback
        "169.254.1.1"      # Link-local
    ]
    
    print("\n1. IP Address Classification:")
    for ip in test_ips:
        validation = netdiag.validate_ip(ip)
        print(f"   {ip:15s} -> {validation.type:12s} (IPv{validation.version})")
    
    # Subnet Calculations
    print("\n2. Subnet Analysis:")
    networks = [
        "192.168.1.0/24",    # Typical home network
        "10.0.0.0/16",       # Medium enterprise
        "172.16.0.0/12",     # Large enterprise
        "192.168.100.0/28"   # Small subnet
    ]
    
    for network in networks:
        subnet = netdiag.subnet_calculator(network)
        print(f"\n   Network: {network}")
        print(f"     Network Address: {subnet.network}")
        print(f"     Broadcast Address: {subnet.broadcast}")
        print(f"     Netmask: {subnet.netmask}")
        print(f"     Available Hosts: {subnet.num_hosts}")
        print(f"     First Host: {subnet.first_host}")
        print(f"     Last Host: {subnet.last_host}")
        print(f"     Network Class: {subnet.network_class}")
    
    # CIDR and Netmask Conversion
    print("\n3. CIDR and Netmask Conversion:")
    cidr_examples = [8, 16, 24, 28, 30]
    
    for cidr in cidr_examples:
        netmask = netdiag.cidr_to_netmask(cidr)
        back_to_cidr = netdiag.netmask_to_cidr(netmask)
        print(f"   /{cidr} = {netmask} = /{back_to_cidr}")

# Run tutorial
ip_addressing_tutorial()
```

### Practical Subnetting Exercise
```python
def campus_network_design():
    """Design a campus network using subnetting."""
    
    print("🏫 Campus Network Design Exercise")
    print("=" * 40)
    print("Scenario: Politeknik Negeri Lampung needs to subnet 192.168.0.0/16")
    print()
    
    # Campus departments and their requirements
    departments = [
        ("Administration", 50, "/26"),    # 62 hosts available
        ("Computer Lab", 30, "/27"),      # 30 hosts available  
        ("Library", 20, "/27"),           # 30 hosts available
        ("Student WiFi", 100, "/25"),     # 126 hosts available
        ("Faculty", 15, "/28"),           # 14 hosts available
        ("Servers", 10, "/28")            # 14 hosts available
    ]
    
    base_network = "192.168.0.0"
    subnet_counter = 0
    
    print("Proposed Subnetting Plan:")
    print("-" * 60)
    
    for dept, hosts_needed, cidr in departments:
        # Calculate subnet
        network_ip = f"192.168.{subnet_counter}.0{cidr}"
        subnet = netdiag.subnet_calculator(network_ip)
        
        print(f"\n{dept}:")
        print(f"  Network: {subnet.network}{cidr}")
        print(f"  Hosts needed: {hosts_needed}")
        print(f"  Hosts available: {subnet.num_hosts}")
        print(f"  IP Range: {subnet.first_host} - {subnet.last_host}")
        print(f"  Sufficient: {'✅ Yes' if subnet.num_hosts >= hosts_needed else '❌ No'}")
        
        # Increment for next subnet
        subnet_counter += (256 >> int(cidr[1:]))
    
    print(f"\nTotal subnets used: {len(departments)}")
    print(f"Remaining address space: 192.168.{subnet_counter}.0 - 192.168.255.255")

# Run network design
campus_network_design()
```

---

## 🌐 Domain Name System (DNS)

### DNS Hierarchy and Resolution Process

```python
def dns_deep_dive():
    """Comprehensive DNS system exploration."""
    
    print("🌐 DNS System Deep Dive")
    print("=" * 30)
    
    domain = "polinela.ac.id"
    
    # 1. DNS Hierarchy Exploration
    print(f"\n1. DNS Hierarchy for {domain}:")
    print("   Root (.) -> Top Level Domain (.id) -> Second Level (ac.id) -> Domain (polinela)")
    
    # 2. Different Record Types
    print(f"\n2. DNS Record Types for {domain}:")
    record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME']
    
    for record_type in record_types:
        try:
            result = netdiag.dns_lookup(domain, record_type=record_type)
            print(f"   {record_type:5s}: {result.data}")
        except Exception:
            print(f"   {record_type:5s}: Not found or not accessible")
    
    # 3. DNS Server Performance
    print(f"\n3. DNS Server Performance Comparison:")
    dns_servers = [
        ("Google DNS", "8.8.8.8"),
        ("Cloudflare DNS", "1.1.1.1"),
        ("OpenDNS", "208.67.222.222"),
        ("Quad9", "9.9.9.9")
    ]
    
    for name, dns_ip in dns_servers:
        try:
            result = netdiag.dns_lookup(domain, dns_server=dns_ip)
            print(f"   {name:15s} ({dns_ip:15s}): {result.query_time:6.2f}ms")
        except Exception as e:
            print(f"   {name:15s} ({dns_ip:15s}): Error - {e}")
    
    # 4. Reverse DNS Lookup
    print(f"\n4. Reverse DNS Examples:")
    well_known_ips = ["8.8.8.8", "1.1.1.1", "208.67.222.222"]
    
    for ip in well_known_ips:
        try:
            reverse_result = netdiag.reverse_dns(ip)
            print(f"   {ip:15s} -> {reverse_result.hostname}")
        except Exception:
            print(f"   {ip:15s} -> No reverse DNS record")

# Run DNS exploration
dns_deep_dive()
```

### DNS Troubleshooting Scenarios
```python
def dns_troubleshooting_lab():
    """DNS troubleshooting laboratory scenarios."""
    
    print("🔧 DNS Troubleshooting Lab")
    print("=" * 30)
    
    # Scenario 1: Compare local vs external DNS
    print("\nScenario 1: DNS Server Comparison")
    test_domain = "polinela.ac.id"
    
    # Get system DNS
    local_dns = netdiag.get_network_config().dns_servers[0]
    external_dns = "8.8.8.8"
    
    for dns_name, dns_server in [("Local DNS", local_dns), ("Google DNS", external_dns)]:
        try:
            result = netdiag.dns_lookup(test_domain, dns_server=dns_server)
            print(f"   {dns_name}: {result.ip_address} ({result.query_time:.2f}ms)")
        except Exception as e:
            print(f"   {dns_name}: Failed - {e}")
    
    # Scenario 2: DNS Cache Analysis
    print("\nScenario 2: DNS Cache Analysis")
    cache_info = netdiag.dns_cache_analysis()
    print(f"   Cache entries: {len(cache_info.entries)}")
    print(f"   Cache hit ratio: {cache_info.hit_ratio:.1f}%")
    
    # Scenario 3: DNS Propagation Check
    print("\nScenario 3: DNS Consistency Check")
    multiple_dns = ["8.8.8.8", "1.1.1.1", "208.67.222.222"]
    results = {}
    
    for dns in multiple_dns:
        try:
            result = netdiag.dns_lookup(test_domain, dns_server=dns)
            results[dns] = result.ip_address
        except Exception:
            results[dns] = "Failed"
    
    # Check consistency
    unique_results = set(results.values())
    if len(unique_results) == 1:
        print("   ✅ All DNS servers return consistent results")
    else:
        print("   ⚠️ Inconsistent DNS results detected:")
        for dns, ip in results.items():
            print(f"      {dns}: {ip}")

# Run troubleshooting lab
dns_troubleshooting_lab()
```

---

## 🔌 Network Ports and Services

### Understanding Port Numbers and Services

```python
def port_services_education():
    """Educational exploration of ports and services."""
    
    print("🔌 Network Ports and Services Education")
    print("=" * 45)
    
    # Well-known ports (0-1023)
    print("\n1. Well-Known Ports (0-1023):")
    well_known_ports = {
        20: "FTP Data Transfer",
        21: "FTP Control",
        22: "SSH (Secure Shell)",
        23: "Telnet",
        25: "SMTP (Email)",
        53: "DNS",
        67: "DHCP Server",
        68: "DHCP Client", 
        80: "HTTP",
        110: "POP3 (Email)",
        143: "IMAP (Email)",
        443: "HTTPS",
        993: "IMAPS (Secure IMAP)",
        995: "POP3S (Secure POP3)"
    }
    
    target = "polinela.ac.id"
    
    for port, service in well_known_ports.items():
        try:
            result = netdiag.check_port(target, port, timeout=2)
            status = "🟢 Open" if result.is_open else "🔴 Closed"
            print(f"   Port {port:3d} ({service:20s}): {status}")
        except Exception:
            print(f"   Port {port:3d} ({service:20s}): ⚠️ Timeout")
    
    # Registered ports (1024-49151)
    print("\n2. Registered Ports (1024-49151) - Examples:")
    registered_ports = {
        1433: "Microsoft SQL Server",
        3306: "MySQL Database",
        3389: "Remote Desktop (RDP)",
        5432: "PostgreSQL Database",
        8080: "HTTP Alternate",
        8443: "HTTPS Alternate"
    }
    
    for port, service in registered_ports.items():
        try:
            result = netdiag.check_port(target, port, timeout=1)
            status = "🟢 Open" if result.is_open else "🔴 Closed"
            print(f"   Port {port:4d} ({service:20s}): {status}")
        except Exception:
            print(f"   Port {port:4d} ({service:20s}): ⚠️ Timeout")
    
    # Service Detection
    print(f"\n3. Service Detection on {target}:")
    open_ports = []
    
    # Quick scan of common ports
    common_ports = [21, 22, 25, 53, 80, 110, 143, 443, 993, 995]
    for port in common_ports:
        try:
            result = netdiag.check_port(target, port, timeout=1)
            if result.is_open:
                open_ports.append(port)
        except Exception:
            pass
    
    for port in open_ports:
        try:
            service_info = netdiag.service_detection(target, port)
            print(f"   Port {port}: {service_info.service} {service_info.version or ''}")
        except Exception:
            print(f"   Port {port}: Service detection failed")

# Run port education
port_services_education()
```

---

This comprehensive networking concepts guide provides practical, hands-on learning experiences using the Netdiag toolkit. Students can explore fundamental networking concepts while working with real network infrastructure, making abstract concepts concrete and understandable.

The guide emphasizes:
- **Practical Application**: Every concept is demonstrated with working code
- **Educational Focus**: Explanations are tailored for learning
- **Real-world Context**: Uses campus network (Polinela) as examples
- **Progressive Complexity**: Builds from basic to advanced concepts
- **Interactive Learning**: Students can modify and experiment with code

---

**Educational Value: 🎓 | Practical Application: 💼 | Hands-on Learning: 🛠️**