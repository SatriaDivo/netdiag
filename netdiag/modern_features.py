"""
Modern Python 3.7+ utilities dan features.
Demonstrasi penggunaan fitur-fitur terbaru Python untuk netdiag.
"""

from __future__ import annotations  # Python 3.7+ feature untuk forward references
from dataclasses import dataclass, field, InitVar
from typing import Any, ClassVar, Optional, Protocol, TypedDict, final
from pathlib import Path
import json
from datetime import datetime


class NetworkProtocol(Protocol):
    """Protocol untuk network operations - Python 3.8+ feature untuk structural subtyping."""
    
    def execute(self) -> dict[str, Any]:
        """Execute network operation."""
        ...
    
    def validate_input(self) -> bool:
        """Validate input parameters."""
        ...


class ResultDict(TypedDict):
    """TypedDict untuk strongly typed dictionaries - Python 3.8+ feature."""
    success: bool
    timestamp: float
    error: Optional[str]
    data: dict[str, Any]


@final  # Python 3.8+ feature - class cannot be subclassed
@dataclass(frozen=True, slots=True)  # Python 3.10+ slots feature for memory efficiency
class NetworkConfiguration:
    """Immutable network configuration dengan modern Python features."""
    
    # Class variables
    DEFAULT_TIMEOUT: ClassVar[int] = 5
    MAX_RETRIES: ClassVar[int] = 3
    
    # Instance variables dengan improved type hints
    host: str
    port: int = 80
    timeout: int = field(default_factory=lambda: NetworkConfiguration.DEFAULT_TIMEOUT)
    retries: int = field(default_factory=lambda: NetworkConfiguration.MAX_RETRIES)
    
    # InitVar untuk data yang hanya digunakan saat initialization
    config_file: InitVar[Optional[Path]] = None
    
    def __post_init__(self, config_file: Optional[Path]) -> None:
        """Post-initialization processing."""
        if config_file and config_file.exists():
            self._load_config(config_file)
    
    def _load_config(self, config_file: Path) -> None:
        """Load configuration from file."""
        try:
            with config_file.open() as f:
                config = json.load(f)
                # Note: Frozen dataclass doesn't allow direct assignment
                # This is just for demonstration
                pass
        except (json.JSONDecodeError, FileNotFoundError):
            pass  # Use defaults
    
    @property
    def connection_string(self) -> str:
        """Generate connection string using f-strings (Python 3.6+ but enhanced)."""
        return f"{self.host}:{self.port}?timeout={self.timeout}&retries={self.retries}"
    
    def to_dict(self) -> ResultDict:
        """Convert to TypedDict for type safety."""
        return ResultDict(
            success=True,
            timestamp=datetime.now().timestamp(),
            error=None,
            data={
                'host': self.host,
                'port': self.port,
                'timeout': self.timeout,
                'retries': self.retries,
                'connection_string': self.connection_string
            }
        )


@dataclass
class EnhancedNetworkResult:
    """Enhanced network result dengan Python 3.7+ features."""
    
    success: bool
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    error: Optional[str] = None
    
    # Using newer type hints (Python 3.9+, but works with from __future__ import annotations)
    metadata: dict[str, str | int | float] = field(default_factory=dict)
    tags: set[str] = field(default_factory=set)
    
    def __post_init__(self) -> None:
        """Post-initialization validation."""
        if self.success and self.error:
            raise ValueError("Success cannot be True when error is set")
        
        # Add automatic metadata
        self.metadata.setdefault('created_at', datetime.now().isoformat())
        self.metadata.setdefault('python_version', '3.7+')
    
    def add_tag(self, tag: str) -> EnhancedNetworkResult:
        """Add tag and return self for method chaining."""
        self.tags.add(tag)
        return self
    
    def with_metadata(self, **kwargs: str | int | float) -> EnhancedNetworkResult:
        """Add metadata and return self for method chaining."""
        self.metadata.update(kwargs)
        return self


def create_network_result_factory(
    default_tags: set[str] | None = None
) -> type[EnhancedNetworkResult]:
    """Factory function using modern type hints."""
    
    if default_tags is None:
        default_tags = set()
    
    @dataclass
    class CustomNetworkResult(EnhancedNetworkResult):
        """Customized network result with default tags."""
        
        def __post_init__(self) -> None:
            super().__post_init__()
            self.tags.update(default_tags)
    
    return CustomNetworkResult


# Example usage dengan modern Python features
def demonstrate_modern_features() -> None:
    """Demonstrate Python 3.7+ features in action."""
    
    # Using dataclass dengan slots dan frozen
    config = NetworkConfiguration(
        host="google.com",
        port=443,
        config_file=Path("config.json")  # InitVar example
    )
    
    # Method chaining dengan fluent interface
    result = EnhancedNetworkResult(success=True) \
        .add_tag("ping") \
        .add_tag("production") \
        .with_metadata(latency=25.3, source="automated")
    
    # Using walrus operator (Python 3.8+) 
    # if (connection_str := config.connection_string):
    #     print(f"Connecting to {connection_str}")
    
    # Alternative for Python 3.7 compatibility
    connection_str = config.connection_string
    if connection_str:
        print(f"Connecting to {connection_str}")
    
    print("Modern Python features demonstrated!")


# Constants using Final (Python 3.8+ but works with typing_extensions)
try:
    from typing import Final
    NETWORK_TIMEOUT: Final[int] = 30
    MAX_CONNECTIONS: Final[int] = 100
except ImportError:
    # Fallback untuk Python 3.7
    NETWORK_TIMEOUT = 30
    MAX_CONNECTIONS = 100


# Example custom exception dengan modern features
class NetworkTimeoutError(Exception):
    """Modern exception class dengan rich information."""
    
    def __init__(
        self, 
        message: str, 
        *, 
        timeout: float,
        host: str,
        context: dict[str, Any] | None = None
    ) -> None:
        super().__init__(message)
        self.timeout = timeout
        self.host = host
        self.context = context or {}
        self.timestamp = datetime.now()
    
    def __str__(self) -> str:
        return (
            f"{super().__str__()} "
            f"(host={self.host}, timeout={self.timeout}s, "
            f"at={self.timestamp.isoformat()})"
        )
    
    def to_dict(self) -> dict[str, Any]:
        """Convert exception to dictionary."""
        return {
            'type': self.__class__.__name__,
            'message': str(self),
            'timeout': self.timeout,
            'host': self.host,
            'context': self.context,
            'timestamp': self.timestamp.isoformat()
        }


if __name__ == "__main__":
    demonstrate_modern_features()