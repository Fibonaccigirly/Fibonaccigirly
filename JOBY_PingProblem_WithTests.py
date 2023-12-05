import ipaddress
import socket
import concurrent.futures
import unittest
from unittest.mock import patch

def is_reachable(ip, port=80, retries=3):
    """
    Check if an IP address is reachable.
    """
    for _ in range(retries):
        try:
            with socket.create_connection((ip, port), timeout=1):
                return True
        except (socket.timeout, OSError):
            continue
    return False

def compare_ranges(ip_range1, ip_range2, excluded_last_octets=None):
    """
    Compare two IP ranges and report differences in reachability.
    """
    if excluded_last_octets is None:
        excluded_last_octets = set()

    ip_addresses_range1 = [str(ip) for ip in ipaddress.IPv4Network(ip_range1, strict=False).hosts()]
    ip_addresses_range2 = [str(ip) for ip in ipaddress.IPv4Network(ip_range2, strict=False).hosts()]

    different_reachability = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_ip = {executor.submit(is_reachable, ip): ip for ip in ip_addresses_range1 + ip_addresses_range2}
        for future in concurrent.futures.as_completed(future_to_ip):
            ip = future_to_ip[future]
            try:
                reachable = future.result()
                if ip.endswith(tuple(excluded_last_octets)):
                    continue
                if ip in ip_addresses_range1 and reachable != is_reachable(ip, retries=1):
                    different_reachability.append(ip)
            except Exception as e:
                print(f"Error checking {ip}: {e}")
            finally:
                print(f"Checked: {ip}")

    print("Comparison finished")
    return different_reachability

class TestReachabilityComparison(unittest.TestCase):
    def test_reachable_comparison(self):
        # Mocking is_reachable function to simulate reachable and non-reachable scenarios
        with patch('my_script_name.is_reachable') as mock_reachable:
            mock_reachable.side_effect = [True, False]
            result = compare_ranges("192.168.1.0/24", "192.168.2.0/24", excluded_last_octets={'56'})
            self.assertEqual(result, ["192.168.1.0", "192.168.2.0"])

    def test_exception_handling(self):
        # Mocking is_reachable function to simulate an exception during reachability check
        with patch('my_script_name.is_reachable') as mock_reachable:
            mock_reachable.side_effect = Exception("Connection failed")
            result = compare_ranges("192.168.1.0/24", "192.168.2.0/24", excluded_last_octets={'56'})
            self.assertEqual(result, [])

    def test_exclude_last_octets(self):
        # Mocking is_reachable function to simulate reachable and non-reachable scenarios
        with patch('my_script_name.is_reachable') as mock_reachable:
            mock_reachable.side_effect = [True, False]
            result = compare_ranges("192.168.1.0/24", "192.168.2.0/24", excluded_last_octets={'56'})
            self.assertEqual(result, ["192.168.1.0"])

if __name__ == "__main__":
    unittest.main()