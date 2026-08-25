import socket
import concurrent.futures
from datetime import datetime

# En çok kullanılan kritik portlar ve servis isimleri
COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    139: "NetBIOS",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    1433: "MSSQL",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    8080: "HTTP-Proxy",
    8443: "HTTPS-Alt"
}

def scan_port(target_ip, port):
    try:
        # Sockets ile hızlı bağlantı denemesi (timeout: 1sn)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        result = s.connect_ex((target_ip, port))
        if result == 0:
            service = COMMON_PORTS.get(port, "Unknown Service")
            s.close()
            return port, service
        s.close()
    except Exception:
        pass
    return None

def run_port_scan(target, ports_to_scan):
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(f"[!] Could not resolve hostname: {target}")
        return

    print(f"\n[*] Target: {target} ({target_ip})")
    print(f"[*] Scan started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("[*] Scanning active ports...\n")

    open_ports = []
    
    # Concurrent scanning with ThreadPool
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(scan_port, target_ip, port) for port in ports_to_scan]
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if res:
                port, service = res
                print(f"[✓] Port {port:<5}/tcp  OPEN  ({service})")
                open_ports.append(res)

    if not open_ports:
        print("[!] No open ports detected in the scanned range.")
    else:
        print(f"\n[+] Total {len(open_ports)} open port(s) found.")

def port_scanner_menu():
    target = input("Enter target IP or Domain (e.g., 192.168.1.1 or example.com): ").strip()
    target = target.replace("https://", "").replace("http://", "").split("/")[0]

    if not target:
        print("[!] Target cannot be empty.")
        return

    while True:
        print(f"\n=== WEBRAKS PORT SCANNER ({target}) ===")
        print("[1] Fast Scan (Top 17 Common Ports)")
        print("[2] Standard Scan (Ports 1 - 1024)")
        print("[3] Custom Port Range (e.g., 80-500)")
        print("[0] Return to Main Menu")

        try:
            secim = input("\nSelect choice: ")
        except KeyboardInterrupt:
            print("\n[!] Returning to main menu...")
            break

        if secim == "1":
            run_port_scan(target, COMMON_PORTS.keys())
        elif secim == "2":
            run_port_scan(target, range(1, 1025))
        elif secim == "3":
            try:
                r_input = input("Enter range (start-end, e.g., 20-100): ").strip()
                start_p, end_p = map(int, r_input.split("-"))
                run_port_scan(target, range(start_p, end_p + 1))
            except ValueError:
                print("[!] Invalid range format. Use start-end format.")
        elif secim == "0":
            break
        else:
            print("[!] Invalid choice.")

if __name__ == "__main__":
    port_scanner_menu()
