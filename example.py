#!/usr/bin/env python3
"""
Contoh penggunaan library netdiag
Network Diagnostics Toolkit

File ini mendemonstrasikan semua fungsi yang tersedia dalam library netdiag
untuk keperluan educational dan testing.
"""

import time
import sys
from netdiag import (
    ping, 
    traceroute, 
    get_local_ip, 
    get_public_ip, 
    scan_ports, 
    dns_lookup,
    # New v1.1.0 features
    get_ip_info,
    scan_common_ports,
    bandwidth_test,
    ping_latency_test,
    connection_quality_test,
    get_network_interfaces,
    get_default_gateway,
    analyze_network_config,
    export_results,
    create_logger
)
from netdiag.portscan import scan_common_ports
from netdiag.dnslookup import reverse_dns_lookup, get_dns_info, dns_bulk_lookup
from netdiag.iputils import get_ip_info


def print_section(title):
    """Helper function untuk print section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def demo_ping():
    """Demo fungsi ping"""
    print_section("DEMO: PING")
    
    hosts = ["google.com", "github.com", "8.8.8.8"]
    
    for host in hosts:
        print(f"\n🏓 Pinging {host}...")
        result = ping(host, count=3, timeout=3)
        
        if result['success']:
            print(f"   ✅ SUCCESS: {result['packets_received']}/{result['packets_sent']} packets received")
            print(f"   📊 Packet Loss: {result['packet_loss']}%")
            if result.get('avg_time'):
                print(f"   ⏱️  Average Time: {result['avg_time']} ms")
        else:
            print(f"   ❌ FAILED: {result['error']}")
        
        time.sleep(0.5)  # Delay singkat untuk mengurangi load


def demo_traceroute():
    """Demo fungsi traceroute"""
    print_section("DEMO: TRACEROUTE")
    
    host = "google.com"
    print(f"\n🔍 Tracing route to {host}...")
    result = traceroute(host, max_hops=15, timeout=3)
    
    if result['success']:
        print(f"   ✅ SUCCESS: Route traced with {result['total_hops']} hops")
        print(f"   🎯 Destination reached: {result['destination_reached']}")
        print("\n   Route path:")
        
        for i, hop in enumerate(result['hops'][:10]):  # Show first 10 hops
            if hop['status'] == 'timeout':
                print(f"   {hop['number']:2d}. * * * (timeout)")
            else:
                ip_or_host = hop['ip'] or hop['hostname'] or 'unknown'
                avg_time_str = f"{hop['avg_time']:.1f} ms" if hop['avg_time'] else "N/A"
                print(f"   {hop['number']:2d}. {ip_or_host} ({avg_time_str})")
        
        if len(result['hops']) > 10:
            print(f"   ... and {len(result['hops']) - 10} more hops")
    else:
        print(f"   ❌ FAILED: {result['error']}")


def demo_ip_utils():
    """Demo fungsi IP utilities"""
    print_section("DEMO: IP UTILITIES")
    
    # Local IP
    print("\n🏠 Getting local IP address...")
    local_result = get_local_ip()
    
    if local_result['success']:
        print(f"   ✅ Local IP: {local_result['ip']}")
        print(f"   📡 Method: {local_result['method']}")
    else:
        print(f"   ❌ Failed: {local_result['error']}")
    
    # Public IP
    print("\n🌐 Getting public IP address...")
    public_result = get_public_ip()
    
    if public_result['success']:
        print(f"   ✅ Public IP: {public_result['ip']}")
        print(f"   🔗 Service: {public_result['service']}")
        
        # IP Info for public IP
        print(f"\n🌍 Getting info for public IP {public_result['ip']}...")
        ip_info_result = get_ip_info(public_result['ip'])
        
        if ip_info_result['success']:
            print(f"   ✅ IP Info:")
            print(f"   🗺️  Country: {ip_info_result['country']} ({ip_info_result['country_code']})")
            print(f"   🏙️  City: {ip_info_result['city']}, {ip_info_result['region']}")
            print(f"   🏢 ISP: {ip_info_result['isp']}")
            print(f"   🕐 Timezone: {ip_info_result['timezone']}")
        else:
            print(f"   ❌ IP Info failed: {ip_info_result['error']}")
    else:
        print(f"   ❌ Failed: {public_result['error']}")


def demo_port_scan():
    """Demo fungsi port scanning"""
    print_section("DEMO: PORT SCANNING")
    
    host = "google.com"
    
    # Common ports scan
    print(f"\n🔍 Scanning common ports on {host}...")
    result = scan_common_ports(host, timeout=2)
    
    if result['success']:
        print(f"   ✅ SUCCESS: Scanned {result['total_ports_scanned']} ports in {result['scan_time']} seconds")
        
        if result['open_ports']:
            print(f"   🔓 Open ports ({len(result['open_ports'])}):")
            for service_info in result['open_services'][:5]:  # Show first 5
                print(f"      - {service_info['port']}/tcp ({service_info['service']})")
            if len(result['open_services']) > 5:
                print(f"      ... and {len(result['open_services']) - 5} more")
        else:
            print("   🔒 No open ports found")
    else:
        print(f"   ❌ FAILED: {result['error']}")
    
    # Quick range scan
    print(f"\n🔍 Quick scan ports 20-100 on {host}...")
    result = scan_ports(host, start_port=20, end_port=100, timeout=1)
    
    if result['success']:
        print(f"   ✅ SUCCESS: Scanned {result['total_ports_scanned']} ports in {result['scan_time']} seconds")
        
        if result['open_ports']:
            print(f"   🔓 Open ports: {result['open_ports']}")
        else:
            print("   🔒 No open ports found in range 20-100")
    else:
        print(f"   ❌ FAILED: {result['error']}")


def demo_dns():
    """Demo fungsi DNS lookup"""
    print_section("DEMO: DNS LOOKUP")
    
    # Basic DNS lookup
    hostnames = ["google.com", "github.com", "stackoverflow.com"]
    
    print("\n🔍 Basic DNS lookups...")
    for hostname in hostnames:
        result = dns_lookup(hostname)
        
        if result['success']:
            print(f"   ✅ {hostname}: {result['ip']}")
            if len(result['ips']) > 1:
                print(f"      (Total {len(result['ips'])} IPs: {', '.join(result['ips'][:3])}...)")
        else:
            print(f"   ❌ {hostname}: {result['error']}")
    
    # Bulk DNS lookup
    print(f"\n🔍 Bulk DNS lookup for {len(hostnames)} hostnames...")
    bulk_result = dns_bulk_lookup(hostnames)
    
    if bulk_result['success']:
        print(f"   ✅ SUCCESS: {bulk_result['successful_lookups']}/{bulk_result['total_hostnames']} successful")
        print(f"   ⏱️  Total time: {bulk_result['total_time']} seconds")
    else:
        print(f"   ❌ FAILED: {bulk_result['error']}")
    
    # Reverse DNS lookup
    test_ips = ["8.8.8.8", "1.1.1.1"]
    print(f"\n🔍 Reverse DNS lookups...")
    
    for ip in test_ips:
        result = reverse_dns_lookup(ip)
        
        if result['success']:
            print(f"   ✅ {ip}: {result['hostname']}")
        else:
            print(f"   ❌ {ip}: {result['error']}")
    
    # Full DNS info
    print(f"\n🔍 Full DNS info for google.com...")
    dns_info_result = get_dns_info("google.com")
    
    if dns_info_result['success']:
        print(f"   ✅ SUCCESS:")
        print(f"   📋 IPv4 addresses ({len(dns_info_result['ipv4_addresses'])}): {', '.join(dns_info_result['ipv4_addresses'][:3])}...")
        if dns_info_result['ipv6_addresses']:
            print(f"   📋 IPv6 addresses: {len(dns_info_result['ipv6_addresses'])} found")
    else:
        print(f"   ❌ FAILED: {dns_info_result['error']}")


def demo_integration():
    """Demo integrasi beberapa fungsi untuk analisis host lengkap"""
    print_section("DEMO: INTEGRATED NETWORK ANALYSIS")
    
    host = "github.com"
    print(f"\n🔬 Comprehensive analysis for {host}...")
    print(f"{'─'*40}")
    
    # Step 1: DNS Lookup
    print(f"1️⃣ DNS Resolution...")
    dns_result = dns_lookup(host)
    if dns_result['success']:
        target_ip = dns_result['ip']
        print(f"   ✅ Resolved to: {target_ip}")
    else:
        print(f"   ❌ DNS failed: {dns_result['error']}")
        return
    
    # Step 2: Ping test
    print(f"\n2️⃣ Connectivity test (ping)...")
    ping_result = ping(target_ip, count=3, timeout=3)
    if ping_result['success']:
        print(f"   ✅ Host is reachable (avg: {ping_result.get('avg_time', 'N/A')} ms)")
    else:
        print(f"   ❌ Host unreachable: {ping_result['error']}")
    
    # Step 3: Common ports check
    print(f"\n3️⃣ Service discovery (common ports)...")
    port_result = scan_common_ports(host, timeout=2)
    if port_result['success'] and port_result['open_ports']:
        print(f"   ✅ Found {len(port_result['open_ports'])} open services:")
        for service in port_result['open_services'][:3]:
            print(f"      🔓 {service['port']}/tcp ({service['service']})")
    else:
        print(f"   🔒 No common services found")
    
    # Step 4: Traceroute (simplified)
    print(f"\n4️⃣ Network path analysis...")
    trace_result = traceroute(host, max_hops=10, timeout=2)
    if trace_result['success']:
        print(f"   ✅ Route traced ({trace_result['total_hops']} hops)")
        print(f"   🎯 Destination reached: {trace_result['destination_reached']}")
    else:
        print(f"   ❌ Traceroute failed: {trace_result['error']}")
    
    print(f"\n✅ Analysis complete for {host}")


def demo_speedtest():
    """Demo fitur speed test yang baru"""
    print_section("DEMO: SPEED TEST (NEW)")
    
    # Quick latency test
    host = "google.com"
    print(f"\n🏓 Quick latency test to {host}...")
    latency_result = ping_latency_test(host, count=5)
    
    if latency_result['success']:
        print(f"   ✅ SUCCESS: {latency_result['successful_pings']}/5 pings successful")
        print(f"   📊 Average latency: {latency_result['avg_latency']} ms")
        print(f"   📊 Jitter: {latency_result['jitter']} ms")
        print(f"   📊 Packet loss: {latency_result['packet_loss_percent']}%")
    else:
        print(f"   ❌ FAILED: {latency_result['error']}")
    
    # Small bandwidth test (commented out to avoid long wait)
    print(f"\n🚀 Bandwidth test (NOTE: Skipped in demo to save time)")
    print(f"   💡 To run: bandwidth_test('1MB')")
    print(f"   💡 Example output: Download speed: 25.3 Mbps")
    
    # Connection quality assessment (using latency only)
    print(f"\n🔍 Connection quality assessment (based on latency)...")
    if latency_result['success']:
        avg_latency = latency_result['avg_latency']
        packet_loss = latency_result['packet_loss_percent']
        
        if avg_latency <= 50 and packet_loss == 0:
            quality = "Excellent"
        elif avg_latency <= 100 and packet_loss <= 1:
            quality = "Good"
        elif avg_latency <= 200 and packet_loss <= 5:
            quality = "Fair"
        else:
            quality = "Poor"
        
        print(f"   📈 Connection quality: {quality}")
        print(f"   💡 Based on latency: {avg_latency} ms, packet loss: {packet_loss}%")


def demo_interfaces():
    """Demo fitur network interfaces yang baru"""
    print_section("DEMO: NETWORK INTERFACES (NEW)")
    
    # Get network interfaces
    print(f"\n🔍 Scanning network interfaces...")
    interfaces_result = get_network_interfaces()
    
    if interfaces_result['success']:
        print(f"   ✅ SUCCESS: Found {interfaces_result['total_interfaces']} interfaces")
        print(f"   📊 Active interfaces: {len(interfaces_result['active_interfaces'])}")
        print(f"   💻 System: {interfaces_result['system']}")
        
        print(f"\n   Active interfaces:")
        for interface in interfaces_result['active_interfaces'][:5]:  # Show max 5
            status_icon = "🟢" if interface['status'] == 'up' else "🔴"
            print(f"   {status_icon} {interface['name']} ({interface['type']})")
            if interface['ip']:
                print(f"      📍 IP: {interface['ip']}")
        
        if len(interfaces_result['active_interfaces']) > 5:
            remaining = len(interfaces_result['active_interfaces']) - 5
            print(f"   ... and {remaining} more interfaces")
    else:
        print(f"   ❌ FAILED: {interfaces_result['error']}")
    
    # Get default gateway
    print(f"\n🌐 Getting default gateway...")
    gateway_result = get_default_gateway()
    
    if gateway_result['success']:
        print(f"   ✅ SUCCESS: Gateway found")
        print(f"   🚪 Gateway IP: {gateway_result['gateway_ip']}")
        if gateway_result.get('interface'):
            print(f"   🔗 Interface: {gateway_result['interface']}")
    else:
        print(f"   ❌ FAILED: {gateway_result['error']}")
    
    # Network analysis summary
    print(f"\n📋 Quick network analysis...")
    print(f"   💡 For full analysis, use: analyze_network_config()")
    print(f"   💡 This provides comprehensive network configuration analysis")


def main():
    """Main function untuk menjalankan semua demo"""
    print("🔧 NETDIAG - Network Diagnostics Toolkit v1.1.0")
    print("📚 Demo penggunaan library untuk educational purposes")
    print("⚠️  Note: Beberapa test mungkin membutuhkan koneksi internet yang stabil")
    
    # List demo functions
    demos = [
        ("IP Utilities", demo_ip_utils),
        ("DNS Lookup", demo_dns),
        ("Ping Test", demo_ping),
        ("Port Scanning", demo_port_scan),
        ("Traceroute", demo_traceroute),
        ("Speed Test (NEW)", demo_speedtest),
        ("Network Interfaces (NEW)", demo_interfaces),
        ("Integrated Analysis", demo_integration),
    ]
    
    # Jika ada argument, jalankan demo spesifik
    if len(sys.argv) > 1:
        demo_name = sys.argv[1].lower()
        demo_map = {
            'ip': demo_ip_utils,
            'dns': demo_dns,
            'ping': demo_ping,
            'port': demo_port_scan,
            'trace': demo_traceroute,
            'speed': demo_speedtest,
            'interfaces': demo_interfaces,
            'integration': demo_integration,
        }
        
        if demo_name in demo_map:
            print(f"\n🎯 Running specific demo: {demo_name}")
            demo_map[demo_name]()
        else:
            print(f"\n❌ Unknown demo: {demo_name}")
            print("Available demos: ip, dns, ping, port, trace, speed, interfaces, integration")
        return
    
    # Jalankan semua demo
    for demo_name, demo_func in demos:
        try:
            print(f"\n🚀 Starting {demo_name} demo...")
            demo_func()
            print(f"✅ {demo_name} demo completed")
            time.sleep(1)  # Pause between demos
        except KeyboardInterrupt:
            print(f"\n⏹️  Demo interrupted by user")
            break
        except Exception as e:
            print(f"\n❌ Error in {demo_name} demo: {str(e)}")
            continue
    
    print(f"\n🎉 All demos completed!")
    print(f"\nUsage examples:")
    print(f"  python example.py           # Run all demos")
    print(f"  python example.py ip        # Run IP utilities demo only")
    print(f"  python example.py dns       # Run DNS demo only")
    print(f"  python example.py ping      # Run ping demo only")
    print(f"  python example.py port      # Run port scan demo only")
    print(f"  python example.py trace     # Run traceroute demo only")
    print(f"  python example.py speed       # Run speed test demo only")
    print(f"  python example.py interfaces  # Run interfaces demo only")
    print(f"  python example.py integration # Run integration demo only")


if __name__ == "__main__":
    main()