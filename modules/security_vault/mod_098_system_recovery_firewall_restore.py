import os
import platform
import subprocess

BACKUP_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "memory_db", "firewall_backup"
)


def backup_firewall_rules() -> str:
    os.makedirs(BACKUP_DIR, exist_ok=True)
    system = platform.system()
    output_path = os.path.join(BACKUP_DIR, f"firewall_rules_{system.lower()}.txt")

    try:
        if system == "Windows":
            subprocess.run(
                ["netsh", "advfirewall", "export", output_path],
                check=True,
                capture_output=True,
                text=True,
                timeout=30,
            )
        elif system == "Linux":
            with open(output_path, "w") as f:
                subprocess.run(
                    ["iptables-save"],
                    stdout=f,
                    check=True,
                    timeout=30,
                )
        else:
            return "Firewall backup not supported on this OS."
        return f"Rules saved to {output_path}"
    except Exception as e:
        return f"Backup failed: {e}"


def restore_firewall_defaults() -> str:
    print("\n[SECURITY] This will reset firewall to default settings.")
    answer = input("Continue? (yes/no): ").strip().lower()
    if answer != "yes":
        return "Cancelled."

    system = platform.system()
    try:
        if system == "Windows":
            subprocess.run(
                ["netsh", "advfirewall", "set", "allprofiles", "state", "on"],
                check=True,
                capture_output=True,
                text=True,
                timeout=30,
            )
            return "Firewall enabled on all profiles."
        elif system == "Linux":
            subprocess.run(
                ["ufw", "--force", "reset"],
                check=True,
                capture_output=True,
                text=True,
                timeout=30,
            )
            return "UFW reset to defaults."
        return "Not supported on this OS."
    except Exception as e:
        return f"Reset failed: {e}"
