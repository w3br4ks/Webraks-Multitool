import os
import time
import subprocess

def get_current_ip():
    try:
        # curl kullanarak timeout ve sessiz mod ile IP çekme
        cmd = "curl -s --max-time 5 https://api.ipify.org || curl -s --max-time 5 https://ifconfig.me"
        output = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
        return output if output else "IP Could Not Be Fetched"
    except Exception:
        return "IP Could Not Be Fetched"

def change_ip_tor():
    print(f"\n[+] Current IP: {get_current_ip()}")
    print("[*] Requesting new IP via Tor service...")
    os.system("sudo anonsurf change 2>/dev/null || sudo service tor reload 2>/dev/null")
    time.sleep(3)
    print(f"[✓] New IP Address: {get_current_ip()}\n")

def auto_rotate_ip(interval):
    print(f"\n[*] Auto IP rotation started (Every {interval}s).")
    print("[!] Press CTRL + C to stop.\n")
    try:
        while True:
            change_ip_tor()
            # Sinyal kesintilerini (CTRL+C) anında yakalamak için parçalı uyku
            for _ in range(interval):
                time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] Auto IP changer stopped successfully.")

def ip_changer_menu():
    while True:
        print("\n=== WEBRAKS IP CHANGER ===")
        print("[1] Show Current IP Address")
        print("[2] Change IP Manually (Tor / Anonsurf)")
        print("[3] Automatic IP Changer (Loop)")
        print("[0] Return to Main Menu")
        
        try:
            secim = input("\nSelect choice: ")
        except KeyboardInterrupt:
            print("\n[!] Returning to main menu...")
            break

        if secim == "1":
            print(f"\n[+] Active IP: {get_current_ip()}")
        elif secim == "2":
            change_ip_tor()
        elif secim == "3":
            try:
                sec = int(input("Enter rotation interval in seconds: "))
                auto_rotate_ip(sec)
            except ValueError:
                print("[!] Please enter a valid number.")
            except KeyboardInterrupt:
                print("\n[!] Operation cancelled.")
        elif secim == "0":
            break
        else:
            print("[!] Invalid choice.")

if __name__ == "__main__":
    ip_changer_menu()
