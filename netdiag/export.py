"""
Modul export dan logging untuk netdiag
Menyediakan fungsi export hasil ke berbagai format dan logging capabilities
"""

import json
import csv
import time
import os
from datetime import datetime
import sys


def export_results(results, filename=None, format='json', include_timestamp=True):
    """
    Export hasil network diagnostics ke file
    
    Args:
        results (dict): hasil dari fungsi netdiag
        filename (str): nama file output (optional)
        format (str): format export ('json', 'csv', 'txt')
        include_timestamp (bool): sertakan timestamp dalam nama file
    
    Returns:
        dict: informasi hasil export
        
    Example:
        >>> ping_result = ping("google.com")
        >>> export_info = export_results(ping_result, "ping_test", "json")
        >>> print(f"Exported to: {export_info['filename']}")
    """
    
    # Generate filename jika tidak diberikan
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_type = _detect_test_type(results)
        filename = f"netdiag_{test_type}_{timestamp}"
    elif include_timestamp:
        timestamp = datetime.now().strftime("_%Y%m%d_%H%M%S")
        filename = f"{filename}{timestamp}"
    
    # Tambahkan extension
    if not filename.endswith(f'.{format}'):
        filename = f"{filename}.{format}"
    
    result = {
        'success': False,
        'filename': filename,
        'format': format,
        'file_size': 0,
        'records_exported': 0,
        'error': None
    }
    
    try:
        if format.lower() == 'json':
            result = _export_json(results, filename, result)
        elif format.lower() == 'csv':
            result = _export_csv(results, filename, result)
        elif format.lower() == 'txt':
            result = _export_txt(results, filename, result)
        else:
            result['error'] = f'Unsupported format: {format}'
            return result
        
        # Get file size
        if os.path.exists(filename):
            result['file_size'] = os.path.getsize(filename)
        
        result['success'] = True
        
    except Exception as e:
        result['error'] = f'Export failed: {str(e)}'
    
    return result


def _detect_test_type(results):
    """Deteksi tipe test berdasarkan struktur hasil"""
    if isinstance(results, dict):
        if 'hops' in results:
            return 'traceroute'
        elif 'open_ports' in results:
            return 'portscan'
        elif 'download_speed_mbps' in results:
            return 'speedtest'
        elif 'interfaces' in results:
            return 'network_analysis'
        elif 'lookup_time' in results:
            return 'dns'
        elif 'packet_loss' in results:
            return 'ping'
        else:
            return 'general'
    else:
        return 'batch'


def _export_json(results, filename, result_info):
    """Export ke format JSON"""
    
    # Tambahkan metadata
    export_data = {
        'export_info': {
            'timestamp': datetime.now().isoformat(),
            'tool': 'netdiag',
            'version': '1.1.0',
            'format': 'json'
        },
        'test_results': results
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    # Count records
    if isinstance(results, list):
        result_info['records_exported'] = len(results)
    else:
        result_info['records_exported'] = 1
    
    return result_info


def _export_csv(results, filename, result_info):
    """Export ke format CSV"""
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Write metadata header
        writer.writerow(['# Netdiag Export'])
        writer.writerow(['# Timestamp', datetime.now().isoformat()])
        writer.writerow(['# Format', 'CSV'])
        writer.writerow([])  # Empty row
        
        records_count = 0
        
        if isinstance(results, list):
            # Multiple results
            if results:
                # Write headers berdasarkan first result
                headers = _extract_csv_headers(results[0])
                writer.writerow(headers)
                
                # Write data
                for result in results:
                    row = _extract_csv_row(result, headers)
                    writer.writerow(row)
                    records_count += 1
        else:
            # Single result
            headers = _extract_csv_headers(results)
            writer.writerow(headers)
            
            row = _extract_csv_row(results, headers)
            writer.writerow(row)
            records_count = 1
        
        result_info['records_exported'] = records_count
    
    return result_info


def _extract_csv_headers(data):
    """Extract headers untuk CSV dari dict"""
    headers = []
    
    def extract_keys(obj, prefix=''):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, (dict, list)):
                    if isinstance(value, list) and value and not isinstance(value[0], dict):
                        # Simple list
                        headers.append(f"{prefix}{key}")
                    elif isinstance(value, dict):
                        # Nested dict
                        extract_keys(value, f"{prefix}{key}_")
                else:
                    headers.append(f"{prefix}{key}")
        return headers
    
    return extract_keys(data)


def _extract_csv_row(data, headers):
    """Extract row data untuk CSV"""
    row = []
    
    def get_nested_value(obj, key_path):
        keys = key_path.split('_')
        current = obj
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return ''
        
        if isinstance(current, list):
            return ', '.join(str(x) for x in current)
        else:
            return str(current) if current is not None else ''
    
    for header in headers:
        value = get_nested_value(data, header)
        row.append(value)
    
    return row


def _export_txt(results, filename, result_info):
    """Export ke format text yang human-readable"""
    
    with open(filename, 'w', encoding='utf-8') as f:
        # Write header
        f.write("="*60 + "\n")
        f.write("NETDIAG NETWORK DIAGNOSTICS REPORT\n")
        f.write("="*60 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Tool: netdiag v1.1.0\n")
        f.write("="*60 + "\n\n")
        
        records_count = 0
        
        if isinstance(results, list):
            # Multiple results
            for i, result in enumerate(results, 1):
                f.write(f"TEST RESULT #{i}\n")
                f.write("-" * 40 + "\n")
                _write_dict_to_txt(result, f)
                f.write("\n")
                records_count += 1
        else:
            # Single result
            f.write("TEST RESULT\n")
            f.write("-" * 40 + "\n")
            _write_dict_to_txt(results, f)
            records_count = 1
        
        f.write("\n" + "="*60 + "\n")
        f.write("END OF REPORT\n")
        f.write("="*60 + "\n")
        
        result_info['records_exported'] = records_count
    
    return result_info


def _write_dict_to_txt(data, file, indent=0):
    """Write dictionary ke text file dengan format yang rapi"""
    indent_str = "  " * indent
    
    for key, value in data.items():
        if isinstance(value, dict):
            file.write(f"{indent_str}{key}:\n")
            _write_dict_to_txt(value, file, indent + 1)
        elif isinstance(value, list):
            file.write(f"{indent_str}{key}:\n")
            for item in value:
                if isinstance(item, dict):
                    _write_dict_to_txt(item, file, indent + 1)
                    file.write("\n")
                else:
                    file.write(f"{indent_str}  - {item}\n")
        else:
            file.write(f"{indent_str}{key}: {value}\n")


class NetdiagLogger:
    """
    Logger class untuk netdiag dengan berbagai level logging
    """
    
    def __init__(self, log_file=None, level='INFO', console_output=True):
        """
        Initialize logger
        
        Args:
            log_file (str): path file log (optional)
            level (str): level logging ('DEBUG', 'INFO', 'WARNING', 'ERROR')
            console_output (bool): output ke console
        """
        self.log_file = log_file
        self.level = level.upper()
        self.console_output = console_output
        self.levels = {'DEBUG': 0, 'INFO': 1, 'WARNING': 2, 'ERROR': 3}
        
        # Create log directory jika tidak ada
        if self.log_file:
            log_dir = os.path.dirname(self.log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)
    
    def _should_log(self, level):
        """Check apakah message harus di-log berdasarkan level"""
        return self.levels.get(level.upper(), 0) >= self.levels.get(self.level, 1)
    
    def _format_message(self, level, message):
        """Format message dengan timestamp dan level"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return f"[{timestamp}] [{level}] {message}"
    
    def _write_log(self, level, message):
        """Write log message ke file dan/atau console"""
        if not self._should_log(level):
            return
        
        formatted_message = self._format_message(level, message)
        
        # Console output
        if self.console_output:
            if level == 'ERROR':
                print(f"❌ {formatted_message}", file=sys.stderr)
            elif level == 'WARNING':
                print(f"⚠️  {formatted_message}")
            elif level == 'INFO':
                print(f"ℹ️  {formatted_message}")
            else:  # DEBUG
                print(f"🔍 {formatted_message}")
        
        # File output
        if self.log_file:
            try:
                with open(self.log_file, 'a', encoding='utf-8') as f:
                    f.write(formatted_message + '\n')
            except Exception as e:
                print(f"❌ Failed to write log: {e}", file=sys.stderr)
    
    def debug(self, message):
        """Log debug message"""
        self._write_log('DEBUG', message)
    
    def info(self, message):
        """Log info message"""
        self._write_log('INFO', message)
    
    def warning(self, message):
        """Log warning message"""
        self._write_log('WARNING', message)
    
    def error(self, message):
        """Log error message"""
        self._write_log('ERROR', message)
    
    def log_test_result(self, test_name, result):
        """Log hasil test dengan format standar"""
        if result.get('success'):
            self.info(f"{test_name} completed successfully")
            self.debug(f"{test_name} result: {result}")
        else:
            self.error(f"{test_name} failed: {result.get('error', 'Unknown error')}")


def create_logger(log_file=None, level='INFO'):
    """
    Factory function untuk membuat logger
    
    Args:
        log_file (str): path file log
        level (str): level logging
    
    Returns:
        NetdiagLogger: instance logger
    """
    return NetdiagLogger(log_file, level)


def batch_export(results_list, base_filename, formats=['json', 'csv']):
    """
    Export multiple results dalam batch
    
    Args:
        results_list (list): list hasil test
        base_filename (str): base nama file
        formats (list): list format export
    
    Returns:
        dict: informasi batch export
    """
    
    export_info = {
        'success': False,
        'total_results': len(results_list),
        'exported_files': [],
        'failed_exports': [],
        'error': None
    }
    
    try:
        for format_type in formats:
            export_result = export_results(
                results_list, 
                f"{base_filename}_batch", 
                format_type
            )
            
            if export_result['success']:
                export_info['exported_files'].append({
                    'filename': export_result['filename'],
                    'format': format_type,
                    'size': export_result['file_size'],
                    'records': export_result['records_exported']
                })
            else:
                export_info['failed_exports'].append({
                    'format': format_type,
                    'error': export_result['error']
                })
        
        export_info['success'] = len(export_info['exported_files']) > 0
        
    except Exception as e:
        export_info['error'] = f'Batch export failed: {str(e)}'
    
    return export_info


if __name__ == "__main__":
    # Test functions jika dijalankan langsung
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python export.py test-export      # Test export functionality")
        print("  python export.py test-logger      # Test logger functionality")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "test-export":
        print("Testing export functionality...")
        
        # Sample test result
        sample_result = {
            'success': True,
            'host': 'google.com',
            'packets_sent': 4,
            'packets_received': 4,
            'packet_loss': 0.0,
            'avg_time': 25.3,
            'test_time': datetime.now().isoformat()
        }
        
        # Test JSON export
        json_result = export_results(sample_result, "test_ping", "json")
        if json_result['success']:
            print(f"✅ JSON export: {json_result['filename']} ({json_result['file_size']} bytes)")
        else:
            print(f"❌ JSON export failed: {json_result['error']}")
        
        # Test CSV export
        csv_result = export_results(sample_result, "test_ping", "csv")
        if csv_result['success']:
            print(f"✅ CSV export: {csv_result['filename']} ({csv_result['file_size']} bytes)")
        else:
            print(f"❌ CSV export failed: {csv_result['error']}")
        
        # Test TXT export
        txt_result = export_results(sample_result, "test_ping", "txt")
        if txt_result['success']:
            print(f"✅ TXT export: {txt_result['filename']} ({txt_result['file_size']} bytes)")
        else:
            print(f"❌ TXT export failed: {txt_result['error']}")
    
    elif command == "test-logger":
        print("Testing logger functionality...")
        
        # Create logger
        logger = create_logger("netdiag_test.log", "DEBUG")
        
        # Test different log levels
        logger.debug("This is a debug message")
        logger.info("This is an info message")
        logger.warning("This is a warning message")
        logger.error("This is an error message")
        
        # Test result logging
        sample_result = {'success': True, 'data': 'test'}
        logger.log_test_result("Test Function", sample_result)
        
        failed_result = {'success': False, 'error': 'Test error'}
        logger.log_test_result("Failed Test", failed_result)
        
        print("✅ Logger test completed. Check netdiag_test.log file.")
    
    else:
        print("❌ Unknown command")