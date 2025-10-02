"""
CLI interface untuk netdiag package
Memungkinkan pemanggilan fungsi melalui command line:
python -m netdiag.ping google.com
python -m netdiag.traceroute google.com
dll
"""

import sys
import argparse
from .ping import ping
from .traceroute import traceroute
from .iputils import get_local_ip, get_public_ip, get_ip_info
from .portscan import scan_ports, scan_common_ports
from .dnslookup import dns_lookup, reverse_dns_lookup, get_dns_info, dns_bulk_lookup, check_dns_servers


def main():
    """
    Main CLI entry point
    """
    
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1].lower()
    
    # Remove command dari argv untuk parsing arguments
    remaining_args = sys.argv[2:]
    
    try:
        if command == "ping":
            handle_ping(remaining_args)
        elif command == "traceroute" or command == "trace":
            handle_traceroute(remaining_args)
        elif command == "localip":
            handle_local_ip()
        elif command == "publicip":
            handle_public_ip()
        elif command == "portscan" or command == "scan":
            handle_portscan(remaining_args)
        elif command == "dns":
            handle_dns(remaining_args)
        elif command == "ipinfo":
            handle_ip_info(remaining_args)
        elif command == "help" or command == "-h" or command == "--help":
            print_help()
        else:
            print(f"❌ Unknown command: {command}")
            print("Use 'python -m netdiag help' for available commands")
            
    except KeyboardInterrupt:
        print("\n⏹️  Operation cancelled by user")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def handle_ping(args):
    """Handle ping command"""
    if not args:
        print("❌ Error: Please specify a host to ping")
        print("Usage: python -m netdiag ping <host> [count] [timeout]")
        return
    
    host = args[0]
    count = int(args[1]) if len(args) > 1 else 4
    timeout = int(args[2]) if len(args) > 2 else 5
    
    print(f"🏓 Pinging {host} with {count} packets...")
    result = ping(host, count, timeout)
    
    if result['success']:
        print(f"✅ Ping successful!")
        print(f"   Host: {result.get('host', host)}")
        print(f"   Packets: {result['packets_received']}/{result['packets_sent']} received")
        print(f"   Packet Loss: {result['packet_loss']}%")
        if result.get('avg_time'):
            print(f"   Average Time: {result['avg_time']} ms")
        if result.get('min_time') and result.get('max_time'):
            print(f"   Min/Max Time: {result['min_time']}/{result['max_time']} ms")
    else:
        print(f"❌ Ping failed: {result['error']}")


def handle_traceroute(args):
    """Handle traceroute command"""
    if not args:
        print("❌ Error: Please specify a host to trace")
        print("Usage: python -m netdiag traceroute <host> [max_hops] [timeout]")
        return
    
    host = args[0]
    max_hops = int(args[1]) if len(args) > 1 else 30
    timeout = int(args[2]) if len(args) > 2 else 5
    
    print(f"🔍 Tracing route to {host} (max {max_hops} hops)...")
    result = traceroute(host, max_hops, timeout)
    
    if result['success']:
        print(f"✅ Traceroute completed!")
        print(f"   Host: {result['host']}")
        print(f"   Total Hops: {result['total_hops']}")
        print(f"   Destination Reached: {result['destination_reached']}")
        print("\n   Route:")
        
        for hop in result['hops']:
            if hop['status'] == 'timeout':
                print(f"   {hop['number']:2d}. * * * (timeout)")
            else:
                ip_or_host = hop['ip'] or hop['hostname'] or 'unknown'
                avg_time_str = f"{hop['avg_time']:.1f} ms" if hop['avg_time'] else "N/A"
                print(f"   {hop['number']:2d}. {ip_or_host} ({avg_time_str})")
    else:
        print(f"❌ Traceroute failed: {result['error']}")


def handle_local_ip():
    """Handle local IP command"""
    print("🏠 Getting local IP address...")
    result = get_local_ip()
    
    if result['success']:
        print(f"✅ Local IP: {result['ip']}")
        print(f"   Method: {result['method']}")
        if 'hostname' in result:
            print(f"   Hostname: {result['hostname']}")
    else:
        print(f"❌ Failed to get local IP: {result['error']}")


def handle_public_ip():
    """Handle public IP command"""
    print("🌐 Getting public IP address...")
    result = get_public_ip()
    
    if result['success']:
        print(f"✅ Public IP: {result['ip']}")
        print(f"   Service: {result['service']}")
    else:
        print(f"❌ Failed to get public IP: {result['error']}")


def handle_portscan(args):
    """Handle port scan command"""
    if not args:
        print("❌ Error: Please specify a host to scan")
        print("Usage: python -m netdiag portscan <host> [start_port] [end_port]")
        print("       python -m netdiag portscan <host> common")
        return
    
    host = args[0]
    
    if len(args) > 1 and args[1].lower() == 'common':
        print(f"🔍 Scanning common ports on {host}...")
        result = scan_common_ports(host)
        
        if result['success']:
            print(f"✅ Port scan completed!")
            print(f"   Host: {result['host']} ({result['target_ip']})")
            print(f"   Scan time: {result['scan_time']} seconds")
            
            if result['open_ports']:
                print(f"\n   Open ports ({len(result['open_ports'])}):")
                for service_info in result['open_services']:
                    print(f"   - {service_info['port']}/tcp ({service_info['service']})")
            else:
                print("   No open ports found")
        else:
            print(f"❌ Port scan failed: {result['error']}")
    else:
        start_port = int(args[1]) if len(args) > 1 else 1
        end_port = int(args[2]) if len(args) > 2 else 1024
        
        print(f"🔍 Scanning ports {start_port}-{end_port} on {host}...")
        result = scan_ports(host, start_port, end_port)
        
        if result['success']:
            print(f"✅ Port scan completed!")
            print(f"   Host: {result['host']} ({result['target_ip']})")
            print(f"   Port range: {result['start_port']}-{result['end_port']}")
            print(f"   Scan time: {result['scan_time']} seconds")
            
            if result['open_ports']:
                print(f"\n   Open ports ({len(result['open_ports'])}):")
                for port in result['open_ports']:
                    from .portscan import get_service_name
                    service = get_service_name(port)
                    print(f"   - {port}/tcp ({service})")
            else:
                print("   No open ports found")
        else:
            print(f"❌ Port scan failed: {result['error']}")


def handle_dns(args):
    """Handle DNS lookup command"""
    if not args:
        print("❌ Error: Please specify a hostname or command")
        print("Usage: python -m netdiag dns <hostname>")
        print("       python -m netdiag dns reverse <ip>")
        print("       python -m netdiag dns info <hostname>")
        print("       python -m netdiag dns bulk <host1,host2,host3>")
        print("       python -m netdiag dns check")
        return
    
    subcommand = args[0].lower()
    
    if subcommand == "reverse" and len(args) > 1:
        ip = args[1]
        print(f"🔍 Reverse DNS lookup for {ip}...")
        result = reverse_dns_lookup(ip)
        
        if result['success']:
            print(f"✅ Reverse lookup successful!")
            print(f"   IP: {result['ip']}")
            print(f"   Hostname: {result['hostname']}")
            print(f"   Lookup time: {result['lookup_time']} seconds")
        else:
            print(f"❌ Reverse lookup failed: {result['error']}")
    
    elif subcommand == "info" and len(args) > 1:
        hostname = args[1]
        print(f"🔍 Getting full DNS info for {hostname}...")
        result = get_dns_info(hostname)
        
        if result['success']:
            print(f"✅ DNS info successful!")
            print(f"   Hostname: {result['hostname']}")
            
            if result['ipv4_addresses']:
                print(f"   IPv4 addresses ({len(result['ipv4_addresses'])}):")
                for ip in result['ipv4_addresses']:
                    reverse_host = result['reverse_lookups'].get(ip, 'N/A')
                    print(f"   - {ip} (reverse: {reverse_host})")
            
            if result['ipv6_addresses']:
                print(f"   IPv6 addresses ({len(result['ipv6_addresses'])}):")
                for ip in result['ipv6_addresses']:
                    print(f"   - {ip}")
        else:
            print(f"❌ DNS info failed: {result['error']}")
    
    elif subcommand == "bulk" and len(args) > 1:
        hostnames = [h.strip() for h in args[1].split(',')]
        print(f"🔍 Bulk DNS lookup for {len(hostnames)} hostnames...")
        result = dns_bulk_lookup(hostnames)
        
        if result['success']:
            print(f"✅ Bulk lookup completed!")
            print(f"   Total: {result['total_hostnames']}")
            print(f"   Successful: {result['successful_lookups']}")
            print(f"   Failed: {result['failed_lookups']}")
            
            print(f"\n   Results:")
            for host_result in result['results']:
                if host_result['success']:
                    print(f"   ✅ {host_result['hostname']}: {host_result['ip']}")
                else:
                    print(f"   ❌ {host_result['hostname']}: {host_result['error']}")
        else:
            print(f"❌ Bulk lookup failed: {result['error']}")
    
    elif subcommand == "check":
        print("🔍 Checking DNS servers...")
        result = check_dns_servers()
        
        print(f"✅ DNS server check completed!")
        print(f"\n   Common DNS servers:")
        for provider, ips in result['common_dns_servers'].items():
            print(f"   {provider}: {', '.join(ips)}")
    
    else:
        # Standard DNS lookup
        hostname = subcommand
        print(f"🔍 DNS lookup for {hostname}...")
        result = dns_lookup(hostname)
        
        if result['success']:
            print(f"✅ DNS lookup successful!")
            print(f"   Hostname: {result['hostname']}")
            print(f"   Primary IP: {result['ip']}")
            if len(result['ips']) > 1:
                print(f"   All IPs ({len(result['ips'])}): {', '.join(result['ips'])}")
            print(f"   Lookup time: {result['lookup_time']} seconds")
        else:
            print(f"❌ DNS lookup failed: {result['error']}")


def handle_ip_info(args):
    """Handle IP info command"""
    ip = args[0] if args else None
    
    if ip:
        print(f"🔍 Getting IP info for {ip}...")
    else:
        print("🔍 Getting IP info for your public IP...")
    
    result = get_ip_info(ip)
    
    if result['success']:
        print(f"✅ IP info successful!")
        print(f"   IP: {result['ip']}")
        print(f"   Country: {result['country']} ({result['country_code']})")
        print(f"   City: {result['city']}, {result['region']}")
        print(f"   ISP: {result['isp']}")
        print(f"   Timezone: {result['timezone']}")
        if result.get('latitude') and result.get('longitude'):
            print(f"   Location: {result['latitude']}, {result['longitude']}")
    else:
        print(f"❌ IP info failed: {result['error']}")


def print_help():
    """Print help information"""
    print("""
🔧 Netdiag - Network Diagnostics Toolkit

Usage: python -m netdiag <command> [arguments]

Available Commands:

  ping <host> [count] [timeout]
    Ping a host with specified count and timeout
    Example: python -m netdiag ping google.com 4 5

  traceroute <host> [max_hops] [timeout]
    Trace route to a host
    Example: python -m netdiag traceroute google.com 30 5

  localip
    Get local IP address
    Example: python -m netdiag localip

  publicip
    Get public IP address
    Example: python -m netdiag publicip

  portscan <host> [start_port] [end_port]
  portscan <host> common
    Scan ports on a host
    Example: python -m netdiag portscan google.com 1 100
    Example: python -m netdiag portscan google.com common

  dns <hostname>
  dns reverse <ip>
  dns info <hostname>
  dns bulk <host1,host2,host3>
  dns check
    DNS lookup operations
    Example: python -m netdiag dns google.com
    Example: python -m netdiag dns reverse 8.8.8.8

  ipinfo [ip]
    Get detailed information about an IP address
    Example: python -m netdiag ipinfo 8.8.8.8
    Example: python -m netdiag ipinfo (uses your public IP)

  help
    Show this help message

For more information, see the README.md file.
""")


if __name__ == "__main__":
    main()