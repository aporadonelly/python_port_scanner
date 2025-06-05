# pylint: disable=missing-module-docstring
from ipaddress import ip_network
from colorama import Fore, init
from scapy.all import ARP, Ether, srp, ICMP, IP, sr1 # pylint: disable=no-name-in-module
from scapy.error import Scapy_Exception
from scanner.logger import setup_logger

init(autoreset=True) #
logger = setup_logger()


def arp_scan(subnet):
    """Performs an ARP scan to discover active hosts in the given subnet."""
    logger.info("Scanning %s...", subnet)
    try:
        arp = ARP(pdst=subnet)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp #stacks the E & A layers
        result = srp(packet, timeout=2, verbose=0)[0]
        active_hosts = []

        for _, received in result:
            logger.info("Host %s is up (MAC: %s)", received.psrc, received.hwsrc)

            active_hosts.append(received.psrc)
        return active_hosts

    except Scapy_Exception as e:
        print(Fore.RED + f"❌ ARP scan failed: {e}. Please run with sudo.")
        return []

def icmp_scan(subnet):
    """Defines a function named icmp_scan, which is intended to perform an ICMP scan on a given subnet.."""
    logger.info("Starting ICMP scan on %s", subnet)
    active_hosts = []
    try:
        for ip in ip_network(subnet).hosts():

            pkt = IP(dst=str(ip)) / ICMP() #constructs an ICMP Echo Request | ICMP class from scapy

            resp = sr1(pkt, timeout=0.3, verbose=0)

            if resp:
                logger.info("Host %s is up (ICMP reply)", ip)
                active_hosts.append(str(ip))

    except (PermissionError, Scapy_Exception) as exc:
        error_msg = f"ICMP scan failed: {exc}. Please run with sudo."
        logger.error(error_msg)
        print(Fore.RED + "❌ " + error_msg)
        return []

    return active_hosts
