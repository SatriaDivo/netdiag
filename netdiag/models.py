"""
Data models untuk netdiag package.
Mendefinisikan struktur data yang konsisten untuk hasil operasi.
"""

from dataclasses import dataclass, field
from typing import Any, Optional, Union
import time


@dataclass
class NetworkResult:
    """Base class untuk semua network operation results."""
    success: bool
    timestamp: float = field(default_factory=time.time)
    error: Optional[str] = None
    duration: Optional[float] = None
    
    def to_dict(self) -> dict[str, Any]:
        """Convert result to dictionary format."""
        return {
            'success': self.success,
            'timestamp': self.timestamp,
            'error': self.error,
            'duration': self.duration
        }


@dataclass
class PingResult(NetworkResult):
    """Result dari ping operation."""
    host: str = ""
    target_ip: str = ""
    packets_sent: int = 0
    packets_received: int = 0
    packet_loss: float = 0.0
    min_time: Optional[float] = None
    max_time: Optional[float] = None
    avg_time: Optional[float] = None
    jitter: Optional[float] = None
    raw_output: str = ""
    command: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        """Convert ping result to dictionary format."""
        base_dict = super().to_dict()
        base_dict.update({
            'host': self.host,
            'target_ip': self.target_ip,
            'packets_sent': self.packets_sent,
            'packets_received': self.packets_received,
            'packet_loss': self.packet_loss,
            'min_time': self.min_time,
            'max_time': self.max_time,
            'avg_time': self.avg_time,
            'jitter': self.jitter,
            'raw_output': self.raw_output,
            'command': self.command
        })
        return base_dict


@dataclass
class TracerouteHop:
    """Single hop dalam traceroute result."""
    hop_number: int
    ip_address: str
    hostname: Optional[str] = None
    response_times: list[float] = field(default_factory=list)
    avg_time: Optional[float] = None
    timeout: bool = False
    
    def to_dict(self) -> dict[str, Any]:
        """Convert hop to dictionary format."""
        return {
            'hop_number': self.hop_number,
            'ip_address': self.ip_address,
            'hostname': self.hostname,
            'response_times': self.response_times,
            'avg_time': self.avg_time,
            'timeout': self.timeout
        }


@dataclass
class TracerouteResult(NetworkResult):
    """Result dari traceroute operation."""
    host: str = ""
    target_ip: str = ""
    hops: list[TracerouteHop] = field(default_factory=list)
    destination_reached: bool = False
    total_hops: int = 0
    raw_output: str = ""
    command: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        """Convert traceroute result to dictionary format."""
        base_dict = super().to_dict()
        base_dict.update({
            'host': self.host,
            'target_ip': self.target_ip,
            'hops': [hop.to_dict() for hop in self.hops],
            'destination_reached': self.destination_reached,
            'total_hops': self.total_hops,
            'raw_output': self.raw_output,
            'command': self.command
        })
        return base_dict


@dataclass
class PortService:
    """Information about a port and its service."""
    port: int
    service: str
    status: str
    banner: Optional[str] = None
    
    def to_dict(self) -> dict[str, Any]:
        """Convert port service to dictionary format."""
        return {
            'port': self.port,
            'service': self.service,
            'status': self.status,
            'banner': self.banner
        }


@dataclass
class PortScanResult(NetworkResult):
    """Result dari port scan operation."""
    host: str = ""
    target_ip: str = ""
    open_ports: list[int] = field(default_factory=list)
    closed_ports: list[int] = field(default_factory=list)
    filtered_ports: list[int] = field(default_factory=list)
    open_services: list[PortService] = field(default_factory=list)
    total_ports_scanned: int = 0
    scan_time: float = 0.0
    timeout: float = 1.0
    threads_used: int = 1
    
    def to_dict(self) -> dict[str, Any]:
        """Convert port scan result to dictionary format."""
        base_dict = super().to_dict()
        base_dict.update({
            'host': self.host,
            'target_ip': self.target_ip,
            'open_ports': self.open_ports,
            'closed_ports': self.closed_ports,
            'filtered_ports': self.filtered_ports,
            'open_services': [service.to_dict() for service in self.open_services],
            'total_ports_scanned': self.total_ports_scanned,
            'scan_time': self.scan_time,
            'timeout': self.timeout,
            'threads_used': self.threads_used
        })
        return base_dict


@dataclass
class DNSResult(NetworkResult):
    """Result dari DNS lookup operation."""
    hostname: str = ""
    ip_address: str = ""
    query_type: str = "A"
    dns_server: Optional[str] = None
    ttl: Optional[int] = None
    additional_records: dict[str, list[str]] = field(default_factory=dict)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert DNS result to dictionary format."""
        base_dict = super().to_dict()
        base_dict.update({
            'hostname': self.hostname,
            'ip_address': self.ip_address,
            'query_type': self.query_type,
            'dns_server': self.dns_server,
            'ttl': self.ttl,
            'additional_records': self.additional_records
        })
        return base_dict


@dataclass
class SpeedTestResult(NetworkResult):
    """Result dari speed test operation."""
    test_type: str = ""
    host: str = ""
    download_speed: float = 0.0
    upload_speed: float = 0.0
    latency: float = 0.0
    jitter: float = 0.0
    packet_loss: float = 0.0
    quality_score: int = 0
    quality_rating: str = ""
    recommendations: list[str] = field(default_factory=list)
    test_duration: float = 0.0
    bytes_transferred: int = 0
    
    def to_dict(self) -> dict[str, Any]:
        """Convert speed test result to dictionary format."""
        base_dict = super().to_dict()
        base_dict.update({
            'test_type': self.test_type,
            'host': self.host,
            'download_speed': self.download_speed,
            'upload_speed': self.upload_speed,
            'latency': self.latency,
            'jitter': self.jitter,
            'packet_loss': self.packet_loss,
            'quality_score': self.quality_score,
            'quality_rating': self.quality_rating,
            'recommendations': self.recommendations,
            'test_duration': self.test_duration,
            'bytes_transferred': self.bytes_transferred
        })
        return base_dict


@dataclass
class NetworkInterface:
    """Information about a network interface."""
    name: str
    ip_address: str
    netmask: Optional[str] = None
    broadcast: Optional[str] = None
    mac_address: Optional[str] = None
    status: str = "unknown"
    interface_type: str = "unknown"
    mtu: Optional[int] = None
    
    def to_dict(self) -> dict[str, Any]:
        """Convert network interface to dictionary format."""
        return {
            'name': self.name,
            'ip_address': self.ip_address,
            'netmask': self.netmask,
            'broadcast': self.broadcast,
            'mac_address': self.mac_address,
            'status': self.status,
            'interface_type': self.interface_type,
            'mtu': self.mtu
        }


@dataclass
class NetworkInterfaceResult(NetworkResult):
    """Result dari network interface discovery."""
    interfaces: list[NetworkInterface] = field(default_factory=list)
    active_interfaces: list[str] = field(default_factory=list)
    default_interface: Optional[str] = None
    default_gateway: Optional[str] = None
    dns_servers: list[str] = field(default_factory=list)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert network interface result to dictionary format."""
        base_dict = super().to_dict()
        base_dict.update({
            'interfaces': [iface.to_dict() for iface in self.interfaces],
            'active_interfaces': self.active_interfaces,
            'default_interface': self.default_interface,
            'default_gateway': self.default_gateway,
            'dns_servers': self.dns_servers
        })
        return base_dict


@dataclass
class ExportResult(NetworkResult):
    """Result dari export operation."""
    filename: str = ""
    format_type: str = ""
    file_size: int = 0
    records_exported: int = 0
    export_path: str = ""
    
    def to_dict(self) -> dict[str, Any]:
        """Convert export result to dictionary format."""
        base_dict = super().to_dict()
        base_dict.update({
            'filename': self.filename,
            'format_type': self.format_type,
            'file_size': self.file_size,
            'records_exported': self.records_exported,
            'export_path': self.export_path
        })
        return base_dict