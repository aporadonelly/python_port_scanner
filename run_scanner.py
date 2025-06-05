# pylint: disable=missing-module-docstring

from colorama import init, Fore

from scanner.scanner_utils import parse_port_input, parse_ip_input
from scanner.port_scanner import scan_ports
from scanner.network_scanner import arp_scan, icmp_scan
from scanner.logger import setup_logger

init(autoreset=True)

logger = setup_logger()

def main():
    """Handles user input, initiates selected scan type, and displays results."""
    try:
        print(Fore.CYAN + "\n Welcome to the Python Port Scanner 🔎")

        scan_type = input("Choose scan type [tcp/arp/icmp] (default: tcp): ").strip().lower() or "tcp"

        while scan_type not in ["tcp", "arp", "icmp"]:
            scan_type = input("Invalid type. Choose [tcp/arp/icmp]: ").strip().lower()

        target = input("Enter target IP, range, or subnet [CIDR Notation] (default: 127.0.0.1): ").strip() or "127.0.0.1"

        if scan_type in ["arp", "icmp"]:
            live_hosts = arp_scan(target) if scan_type == "arp" else icmp_scan(target)

            if live_hosts:
                print(Fore.CYAN + f"\nActive hosts ({scan_type.upper()}):")
                for host in live_hosts:
                    print(Fore.GREEN + f" - {host}")
            else:
                print(Fore.RED + "❌ No active hosts found.")
            return

        #  Only runs if scan_type == "tcp"
        port_input = input("Enter port range (e.g. 20-80, 8000-8080, default: 1-1024): ").strip() or "1-1024"

        if "-" in port_input:
            port_start, port_end = parse_port_input(*port_input.split("-")) #Uses the * operator to unpack that list into two arguments.
        else: #Handles single input: If user enters just 443, both start and end are set to 443, scanning a single port.
            port_start, port_end = parse_port_input(port_input, port_input)

        ip_list = parse_ip_input(target)

        for ip in ip_list:
            print(Fore.CYAN + f"\n🔎 Scanning {ip}...")
            open_ports = scan_ports(ip, (port_start, port_end))
            if open_ports:
                print(Fore.GREEN + f"✅ Open ports on {ip}: {open_ports}")
            else:
                print(Fore.YELLOW + f"⚠️  No open ports found on {ip}")

    except KeyboardInterrupt:
        logger.warning("Scan interrupted by user (Ctrl+C)")
        print(Fore.RED + "\n⚠️ Scan canceled by user. Exiting gracefully...")
    except ValueError as e:
        print(Fore.RED + f"Error: {e}")

if __name__ == "__main__":
    main()
