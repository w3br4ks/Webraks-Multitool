    "admin", "mail", "dev", "test", "api", "staging", "blog", 
    "webmail", "server", "portal", "ns1", "ns2", "smtp", "vpn",
    "shop", "cpanel", "autodiscover", "m", "direct", "ftp"
]

def check_subdomain(target_domain, sub):
    full_domain = f"{sub}.{target_domain}"
    try:
        ip = socket.gethostbyname(full_domain)
        return full_domain, ip
    except socket.gaierror:
        return None

def active_brute_force(domain):
    print(f"\n[*] Starting Active Brute-Force scan for: {domain}")
    print("[*] Checking common subdomains...\n")
    found = []

    # Hızlı tarama için ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(check_subdomain, domain, sub) for sub in DEFAULT_SUBDOMAINS]
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if res:
                full_domain, ip = res
                print(f"[✓] Found: {full_domain} -> {ip}")
                found.append((full_domain, ip))
    
    if not found:
        print("[!] No active subdomains found from default wordlist.")

def passive_crt_sh(domain):
    print(f"\n[*] Requesting passive SSL logs from crt.sh for: {domain}...\n")
    url = f"https://crt.sh/?q=%.{domain}&output=json"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = json.loads(response.text)
            subdomains = set()
            for entry in data:
                name = entry['name_value']
                # Çoklu satır ve wildcard temizliği
                for sub in name.split('\n'):
                    sub = sub.replace("*.", "").strip()
                    if domain in sub:
                        subdomains.add(sub)
            
            print(f"[✓] Discovered {len(subdomains)} unique passive subdomains:")
            for s in sorted(subdomains):
                print(f"  - {s}")
        else:
            print("[!] Could not retrieve data from crt.sh (Server status error).")
    except Exception as e:
        print(f"[!] Error fetching passive logs: {e}")

def subdomain_menu():
    domain = input("Enter target domain (e.g., example.com): ").strip()
    # http:// veya https:// yazıldıysa temizle
    domain = domain.replace("https://", "").replace("http://", "").split("/")[0]

    if not domain:
        print("[!] Target domain cannot be empty.")
        return

    while True:
        print(f"\n=== WEBRAKS SUBDOMAIN ENUMERATOR ({domain}) ===")
        print("[1] Passive Enumeration (crt.sh SSL Logs - Safe)")
        print("[2] Active Brute-Force (DNS Resolution)")
        print("[3] Run Both (Full Scan)")
        print("[0] Return to Main Menu")

        try:
            secim = input("\nSelect choice: ")
        except KeyboardInterrupt:
            print("\n[!] Returning to main menu...")
            break

        if secim == "1":
            passive_crt_sh(domain)
        elif secim == "2":
            active_brute_force(domain)
        elif secim == "3":
            passive_crt_sh(domain)
            active_brute_force(domain)
        elif secim == "0":
            break
        else:
            print("[!] Invalid choice.")

if __name__ == "__main__":
    subdomain_menu()
