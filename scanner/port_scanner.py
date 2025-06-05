# pylint: disable=missing-module-docstring

import socket
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from scanner.logger import setup_logger

logger = setup_logger()

def scan_port(ip, port, timeout=1):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout) #1 sec
        result = sock.connect_ex((ip, port))
        if result == 0:
            logger.info("[+] Port %s is open on %s)", port, ip)
            return port
    return None

def scan_ports(target_ip, port_range=(1, 1024), timeout=1, max_threads=100, rate_limit=0.01):
    logger.info("Starting scan on %s from port %s to %s", target_ip, port_range[0], port_range[1])
    start_time = datetime.now() # for duration tracking
    open_ports = []

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [] #holds Future objects representing pending tasks from executor.submit() method
        for port in range(port_range[0], port_range[1] + 1):
            futures.append(executor.submit(scan_port, target_ip, port, timeout))
            time.sleep(rate_limit)  # wait for 10milliseconds before continuing to the next tasks. This adds a small pause between submissions to avoid overloading the system or triggering detection mechanisms like firewalls or IDS.

        for f in futures:
            result = f.result() #method to get and wait for the actual scan
            if result:
                open_ports.append(result)

    duration = datetime.now() - start_time #calc how long it took to scan
    logger.info("Finished scan on %s in %s. Open ports: %s", target_ip, duration, open_ports)
    return sorted(open_ports)
