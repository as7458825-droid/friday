import nmap
from scapy.all import IP, ICMP, sr1, conf
import logging

logger = logging.getLogger(__name__)


class HackingPro:
    """Advanced Network & Security Module for FRIDAY"""

    def scan_network(self, target_range):
        """Scans a network range using Nmap"""
        try:
            nm = nmap.PortScanner()
            logger.info(f"Scanning range: {target_range}")
            nm.scan(hosts=target_range, arguments="-sn")
            hosts = [(x, nm[x]["status"]["state"]) for x in nm.all_hosts()]
            return f"Found {len(hosts)} active hosts in {target_range}."
        except Exception as e:
            return f"Nmap Scan Error: {e}"

    def ping_test(self, target_ip):
        """Sends a custom ICMP packet using Scapy"""
        try:
            conf.verb = 0
            packet = IP(dst=target_ip) / ICMP()
            reply = sr1(packet, timeout=2)
            if reply:
                return f"Host {target_ip} is ALIVE (ICMP Reply received)."
            return f"Host {target_ip} is DOWN or blocking ICMP."
        except Exception as e:
            return f"Scapy Ping Error: {e}"


def hacking_update(command):
    hp = HackingPro()
    if "scan" in command:
        return hp.scan_network("192.168.1.0/24")
    if "ping" in command:
        target = command.split("ping")[-1].strip() or "8.8.8.8"
        return hp.ping_test(target)
    return "Hacking module ready. Commands: scan, ping."
