from scapy.all import ARP, Ether, srp
import socket
import logging

log = logging.getLogger("FRIDAY.Security")


def scan_network(ip_range: str = "192.168.1.1/24") -> str:
    """Scan local network for active devices."""
    try:
        log.info(f"Scanning network: {ip_range}")
        arp = ARP(pdst=ip_range)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp

        result = srp(packet, timeout=3, verbose=0)[0]

        devices = []
        for sent, received in result:
            devices.append({"ip": received.psrc, "mac": received.hwsrc})

        if not devices:
            return "No active devices found in range."

        res_str = f"Found {len(devices)} devices:\n"
        for d in devices:
            res_str += f"- {d['ip']} ({d['mac']})\n"
        return res_str
    except Exception as e:
        log.error(f"Network Scan Error: {e}")
        return f"Scan failed: {e}. Note: May require Admin/Sudo privileges."


def audit_local_ports(ports=[80, 443, 3306, 8000, 8080]) -> str:
    """Check if specific local ports are open/vulnerable."""
    open_ports = []
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.1)
            if s.connect_ex(("127.0.0.1", port)) == 0:
                open_ports.append(port)

    if not open_ports:
        return "No common vulnerable ports are open locally."
    return f"Active local ports detected: {open_ports}. Review for security."
