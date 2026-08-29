        mac_search = re.search(r"link/ether\s+([0-9a-fa-f:]+)", output)
        if mac_search:
            return mac_search.group(1)
        return "MAC Not Found"
    except Exception:
        return "Interface Error"

def change_mac(interface, new_mac):
    print(f"\n[*] Changing MAC address for {interface}...")
    os.system(f"sudo ip link set dev {interface} down")
    os.system(f"sudo macchanger -m {new_mac} {interface} 2>/dev/null || sudo ip link set dev {interface} address {new_mac}")
    os.system(f"sudo ip link set dev {interface} up")
    print(f"[✓] MAC address updated to: {get_current_mac(interface)}\n")

def random_mac(interface):
    print(f"\n[*] Assigning random MAC address for {interface}...")
    os.system(f"sudo ip link set dev {interface} down")
    os.system(f"sudo macchanger -r {interface} 2>/dev/null")
    os.system(f"sudo ip link set dev {interface} up")
    print(f"[✓] New Random MAC: {get_current_mac(interface)}\n")

def reset_mac(interface):
    print(f"\n[*] Resetting MAC address to original for {interface}...")
    os.system(f"sudo ip link set dev {interface} down")
    os.system(f"sudo macchanger -p {interface} 2>/dev/null")
    os.system(f"sudo ip link set dev {interface} up")
    print(f"[✓] Original MAC restored: {get_current_mac(interface)}\n")

def mac_changer_menu():
    interface = input("Enter interface name (e.g., eth0, wlan0): ").strip()
    if not interface:
        interface = "eth0"

    while True:
        print(f"\n=== WEBRAKS MAC CHANGER ({interface}) ===")
        print(f"Current MAC: {get_current_mac(interface)}")
        print("[1] Set Custom MAC Address")
        print("[2] Set Random MAC Address")
        print("[3] Reset to Original MAC Address")
        print("[0] Return to Main Menu")

        try:
            secim = input("\nSelect choice: ")
        except KeyboardInterrupt:
            print("\n[!] Returning to main menu...")
            break

        if secim == "1":
            custom_mac = input("Enter new MAC (e.g., 00:11:22:33:44:55): ").strip()
            if custom_mac:
                change_mac(interface, custom_mac)
            else:
                print("[!] Invalid MAC address.")
        elif secim == "2":
            random_mac(interface)
        elif secim == "3":
            reset_mac(interface)
        elif secim == "0":
            break
        else:
            print("[!] Invalid choice.")

if __name__ == "__main__":
    mac_changer_menu()
