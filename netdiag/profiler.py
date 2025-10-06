"""
Performance monitoring dan profiling untuk netdiag operations.
Menyediakan tools untuk mengukur dan mengoptimalkan performance.
"""

import time
import functools
import threading
from typing import Any, Callable, Optional
from dataclasses import dataclass, field
from collections import defaultdict

from .utils import format_duration


@dataclass
class PerformanceMetrics:
    """Class untuk menyimpan performance metrics."""
    function_name: str
    call_count: int = 0
    total_time: float = 0.0
    avg_time: float = 0.0
    min_time: float = float('inf')
    max_time: float = 0.0
    last_call_time: float = 0.0
    errors: int = 0
    
    def update(self, execution_time: float, success: bool = True):
        """Update metrics dengan execution time baru."""
        self.call_count += 1
        self.total_time += execution_time
        self.avg_time = self.total_time / self.call_count
        self.min_time = min(self.min_time, execution_time)
        self.max_time = max(self.max_time, execution_time)
        self.last_call_time = execution_time
        
        if not success:
            self.errors += 1
    
    def to_dict(self) -> dict[str, Any]:
        """Convert metrics to dictionary."""
        return {
            'function_name': self.function_name,
            'call_count': self.call_count,
            'total_time': self.total_time,
            'avg_time': self.avg_time,
            'min_time': self.min_time if self.min_time != float('inf') else 0,
            'max_time': self.max_time,
            'last_call_time': self.last_call_time,
            'errors': self.errors,
            'error_rate': (self.errors / self.call_count * 100) if self.call_count > 0 else 0
        }


class PerformanceProfiler:
    """
    Performance profiler untuk monitoring function calls dan timing.
    Thread-safe implementation untuk concurrent operations.
    """
    
    def __init__(self):
        self._metrics: dict[str, PerformanceMetrics] = {}
        self._lock = threading.Lock()
        self._enabled = True
    
    def enable(self):
        """Enable performance monitoring."""
        self._enabled = True
    
    def disable(self):
        """Disable performance monitoring."""
        self._enabled = False
    
    def clear(self):
        """Clear all metrics."""
        with self._lock:
            self._metrics.clear()
    
    def record_call(self, function_name: str, execution_time: float, success: bool = True):
        """
        Record function call performance.
        
        Args:
            function_name: Name of the function
            execution_time: Execution time in seconds
            success: Whether the call was successful
        """
        if not self._enabled:
            return
            
        with self._lock:
            if function_name not in self._metrics:
                self._metrics[function_name] = PerformanceMetrics(function_name)
            
            self._metrics[function_name].update(execution_time, success)
    
    def get_metrics(self, function_name: Optional[str] = None) -> dict[str, Any]:
        """
        Get performance metrics.
        
        Args:
            function_name: Specific function name, or None for all
            
        Returns:
            Dictionary with performance metrics
        """
        with self._lock:
            if function_name:
                if function_name in self._metrics:
                    return self._metrics[function_name].to_dict()
                else:
                    return {}
            else:
                return {name: metrics.to_dict() 
                       for name, metrics in self._metrics.items()}
    
    def get_summary(self) -> dict[str, Any]:
        """Get performance summary."""
        with self._lock:
            if not self._metrics:
                return {
                    'total_functions': 0,
                    'total_calls': 0,
                    'total_time': 0.0,
                    'total_errors': 0
                }
            
            total_calls = sum(m.call_count for m in self._metrics.values())
            total_time = sum(m.total_time for m in self._metrics.values())
            total_errors = sum(m.errors for m in self._metrics.values())
            
            # Find slowest and fastest functions
            slowest = max(self._metrics.values(), key=lambda m: m.avg_time)
            fastest = min(self._metrics.values(), key=lambda m: m.avg_time)
            
            return {
                'total_functions': len(self._metrics),
                'total_calls': total_calls,
                'total_time': total_time,
                'total_errors': total_errors,
                'error_rate': (total_errors / total_calls * 100) if total_calls > 0 else 0,
                'slowest_function': {
                    'name': slowest.function_name,
                    'avg_time': slowest.avg_time
                },
                'fastest_function': {
                    'name': fastest.function_name,
                    'avg_time': fastest.avg_time
                }
            }
    
    def print_report(self, detailed: bool = False):
        """Print performance report."""
        summary = self.get_summary()
        
        print("🔍 NETDIAG PERFORMANCE REPORT")
        print("=" * 50)
        print(f"📊 Total Functions Monitored: {summary['total_functions']}")
        print(f"📞 Total Function Calls: {summary['total_calls']}")
        print(f"⏱️  Total Execution Time: {format_duration(summary['total_time'])}")
        print(f"❌ Total Errors: {summary['total_errors']}")
        print(f"📈 Error Rate: {summary['error_rate']:.2f}%")
        
        if summary['total_functions'] > 0:
            print(f"\n🐌 Slowest Function: {summary['slowest_function']['name']} "
                  f"({format_duration(summary['slowest_function']['avg_time'])} avg)")
            print(f"⚡ Fastest Function: {summary['fastest_function']['name']} "
                  f"({format_duration(summary['fastest_function']['avg_time'])} avg)")
        
        if detailed:
            print("\n📋 DETAILED METRICS:")
            print("-" * 50)
            metrics = self.get_metrics()
            
            for func_name, func_metrics in sorted(metrics.items(), 
                                                key=lambda x: x[1]['avg_time'], reverse=True):
                print(f"\n🔧 {func_name}:")
                print(f"   Calls: {func_metrics['call_count']}")
                print(f"   Avg Time: {format_duration(func_metrics['avg_time'])}")
                print(f"   Min/Max: {format_duration(func_metrics['min_time'])} / "
                      f"{format_duration(func_metrics['max_time'])}")
                print(f"   Total Time: {format_duration(func_metrics['total_time'])}")
                print(f"   Errors: {func_metrics['errors']} ({func_metrics['error_rate']:.1f}%)")


# Global profiler instance
_global_profiler = PerformanceProfiler()


def profile_performance(func: Callable) -> Callable:
    """
    Decorator untuk monitoring performance function calls.
    
    Args:
        func: Function to be monitored
        
    Returns:
        Wrapped function with performance monitoring
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        success = True
        
        try:
            result = func(*args, **kwargs)
            
            # Check if result indicates failure
            if isinstance(result, dict) and 'success' in result:
                success = result.get('success', True)
            
            return result
            
        except Exception as e:
            success = False
            raise
            
        finally:
            execution_time = time.time() - start_time
            function_name = f"{func.__module__}.{func.__name__}"
            _global_profiler.record_call(function_name, execution_time, success)
    
    return wrapper


def get_performance_metrics(function_name: Optional[str] = None) -> dict[str, Any]:
    """Get performance metrics from global profiler."""
    return _global_profiler.get_metrics(function_name)


def get_performance_summary() -> dict[str, Any]:
    """Get performance summary from global profiler."""
    return _global_profiler.get_summary()


def print_performance_report(detailed: bool = False):
    """Print performance report from global profiler."""
    _global_profiler.print_report(detailed)


def clear_performance_metrics():
    """Clear all performance metrics."""
    _global_profiler.clear()


def enable_performance_monitoring():
    """Enable global performance monitoring."""
    _global_profiler.enable()


def disable_performance_monitoring():
    """Disable global performance monitoring."""
    _global_profiler.disable()


class NetworkTimer:
    """
    Context manager untuk measuring network operation timing.
    
    Example:
        with NetworkTimer() as timer:
            result = ping("google.com")
        print(f"Operation took: {timer.elapsed}s")
    """
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.elapsed = 0.0
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        self.elapsed = self.end_time - self.start_time


class BenchmarkSuite:
    """
    Benchmark suite untuk comparing performance of different operations.
    """
    
    def __init__(self):
        self.results: dict[str, list[float]] = defaultdict(list)
    
    def benchmark_function(self, name: str, func: Callable, *args, iterations: int = 5, **kwargs):
        """
        Benchmark a function multiple times.
        
        Args:
            name: Benchmark name
            func: Function to benchmark
            iterations: Number of iterations to run
            *args, **kwargs: Arguments for the function
        """
        print(f"🔬 Benchmarking {name} ({iterations} iterations)...")
        
        times = []
        errors = 0
        
        for i in range(iterations):
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                times.append(execution_time)
                
                # Check if operation was successful
                if isinstance(result, dict) and not result.get('success', True):
                    errors += 1
                    
            except Exception as e:
                execution_time = time.time() - start_time
                times.append(execution_time)
                errors += 1
                print(f"   ⚠️  Iteration {i+1} failed: {e}")
        
        self.results[name] = times
        
        # Calculate statistics
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        print(f"   ✅ Completed: {format_duration(avg_time)} avg, "
              f"{format_duration(min_time)}-{format_duration(max_time)} range")
        print(f"   📊 Errors: {errors}/{iterations} ({errors/iterations*100:.1f}%)")
        
        return {
            'name': name,
            'iterations': iterations,
            'avg_time': avg_time,
            'min_time': min_time,
            'max_time': max_time,
            'times': times,
            'errors': errors,
            'error_rate': errors / iterations * 100
        }
    
    def compare_results(self):
        """Compare benchmark results."""
        if not self.results:
            print("No benchmark results to compare.")
            return
        
        print("\n📊 BENCHMARK COMPARISON:")
        print("=" * 60)
        
        # Calculate averages for comparison
        averages = {}
        for name, times in self.results.items():
            averages[name] = sum(times) / len(times)
        
        # Sort by average time
        sorted_results = sorted(averages.items(), key=lambda x: x[1])
        
        fastest_time = sorted_results[0][1]
        
        for name, avg_time in sorted_results:
            relative_speed = avg_time / fastest_time
            print(f"{name:25} : {format_duration(avg_time):>10} "
                  f"({relative_speed:.2f}x slower)" if relative_speed > 1 
                  else f"{name:25} : {format_duration(avg_time):>10} (fastest)")


# Example usage functions
def benchmark_ping_methods(host: str = "8.8.8.8"):
    """Benchmark different ping configurations."""
    from .ping import ping
    
    suite = BenchmarkSuite()
    
    # Benchmark different configurations
    suite.benchmark_function("ping_fast", ping, host, 1, 2)
    suite.benchmark_function("ping_normal", ping, host, 4, 5)
    suite.benchmark_function("ping_thorough", ping, host, 10, 10)
    
    suite.compare_results()


if __name__ == "__main__":
    # Example usage
    print("🔍 Performance Profiler Example")
    
    @profile_performance
    def example_function():
        import time
        time.sleep(0.1)
        return {'success': True}
    
    # Run some test calls
    for _ in range(5):
        example_function()
    
    # Print report
    print_performance_report(detailed=True)