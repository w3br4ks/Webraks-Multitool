import os
import re
import subprocess
import time

VENDORS = {
    "1": ("Apple", "00:1C:B3"),
    "2": ("Cisco", "00:40:0B"),
    "3": ("Intel", "00:13:E8"),
    "4": ("Samsung", "00:26:37"),
    "5": ("Dell", "00:14:22")
}

def get_current_mac(interface):
    try:
        output = subprocess.check_output(f"ip link show {interface}", shell=True, stderr=subprocess.DEVNULL).decode('utf-8')
        mac_search = re.search(r"link/ether\s+([0-9a-fa-f:]+)", output)
        return mac_search.group(1) if mac_search else "MAC Not Found"
    except Exception:
        return "Interface Error"

def apply_spoof(interface, mac_address):
    print(f"\n[*] Spoofing MAC address on {interface}...")
    # NetworkManager müdahalesini geçici durdurup hızlıca değiştiriyoruz
    cmd = (
        f"sudo nmcli device set {interface} managed no 2>/dev/null; "
        f"sudo ip link set dev {interface} down && "
        f"sudo ip link set dev {interface} address {mac_address} && "
        f"sudo ip link set dev {interface} up; "
        f"sudo nmcli device set {interface} managed yes 2>/dev/null"
    )
    subprocess.run(cmd, shell=True)
    time.sleep(1)
    print(f"[✓] Spoofed MAC Address: {get_current_mac(interface)}\n")

def vendor_spoof(interface):
    print("\n--- VENDOR SPOOFING ---")
    for key, val in VENDORS.items():
        print(f"[{key}] {val[0]} ({val[1]}:XX:XX:XX)")
    
    choice = input("\nSelect vendor to spoof: ").strip()
    if choice in VENDORS:
        prefix = VENDORS[choice][1]
        import random
        suffix = ":".join([f"{random.randint(0, 255):02x}" for _ in range(3)])
        apply_spoof(interface, f"{prefix}:{suffix}")
    else:
        print("[!] Invalid vendor selection.")

def spoofer_menu():
    interface = input("Enter interface name (e.g., eth0, wlan0) [default: eth0]: ").strip() or "eth0"

    while True:
        print(f"\n=== WEBRAKS MAC SPOOFER ({interface}) ===")
        print(f"Current Active MAC: {get_current_mac(interface)}")
        print("[1] Vendor Spoofing (Apple, Cisco, Intel, etc.)")
        print("[2] Target Device Spoofing (Custom MAC)")
        print("[3] Restore Original Hardware MAC")
        print("[0] Return to Main Menu")

        try:
            secim = input("\nSelect choice: ")
        except KeyboardInterrupt:
            print("\n[!] Returning to main menu...")
            break

        if secim == "1":
            vendor_spoof(interface)
        elif secim == "2":
            target_mac = input("Enter target MAC: ").strip()
            if target_mac:
                apply_spoof(interface, target_mac)
        elif secim == "3":
            print(f"\n[*] Restoring original MAC...")
            cmd = f"sudo macchanger -p {interface} 2>/dev/null"
            subprocess.run(cmd, shell=True)
            print(f"[✓] Original MAC Restored: {get_current_mac(interface)}\n")
        elif secim == "0":
            break
        else:
            print("[!] Invalid choice.")

if __name__ == "__main__":
    spoofer_menu()
