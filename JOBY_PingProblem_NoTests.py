import ipaddress
import socket
import concurrent.futures

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

if __name__ == "__main__":
    ip_range1 = "192.168.1.0/24"
    ip_range2 = "192.168.2.0/24"
    excluded_last_octets = {'56'}  # Add any excluded last octets here

    result = compare_ranges(ip_range1, ip_range2, excluded_last_octets)
    print("IP addresses with different reachability:", result)

    # Avoid restarting when using the debugger
    if 'pdb' not in globals():
        print("Restarting the program...")
        import sys
        sys.exit(0)
