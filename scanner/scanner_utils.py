import ipaddress #ip
def validate_port_range(start, end):
    if 0 < start <= 65535 and 0 < end <= 65535 and start <= end:
        return True #means validation passed
    raise ValueError("Port range must be between 1 and 65535 and start <= end")

def parse_port_input(start_str, end_str, default_start=1, default_end=1024):
    start = int(start_str) if start_str else default_start
    end = int(end_str) if end_str else default_end

    validate_port_range(start, end)

    return start, end #Returns the cleaned and validated range as integers

def parse_ip_input(ip_input):
    ip_input = ip_input.strip()

    if "-" in ip_input:
        start_ip, end_ip = ip_input.split("-")
        try:
            start = ipaddress.IPv4Address(start_ip) #IPv4Address class
            end = ipaddress.IPv4Address(end_ip)
            if start > end:
                raise ValueError("Start IP must be less than or equal to end IP")
            networks = list(ipaddress.summarize_address_range(start, end))
            hosts = []
            for network in networks:
                hosts.extend([str(ip) for ip in network.hosts()])
            return hosts

        except ipaddress.AddressValueError as exc: #192.168.1.999
            raise ValueError("Invalid IP range format") from exc

    #If user entered a CIDR subnet or a single IP
    try: #first attempt to parse ip_input
        network = ipaddress.ip_network(ip_input, strict=False) #convert to IPv4N
        return [str(ip) for ip in network.hosts()]
    except ValueError as exc:
        try: #tries again assuming the ip is single ip
            ip = ipaddress.IPv4Address(ip_input)
            return [str(ip)] #if wokrs, returns the IP as 1 item list of str
        except ipaddress.AddressValueError: #not a valid ip either
            raise ValueError("Invalid IP address or subnet.") from exc
