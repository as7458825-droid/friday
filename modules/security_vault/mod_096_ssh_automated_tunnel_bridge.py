import subprocess


def create_ssh_tunnel(
    remote_host: str,
    remote_port: int,
    local_port: int = 8888,
    ssh_user: str = "root",
    ssh_key: str = None,
) -> str:
    print(f"\n[SECURITY] SSH tunnel to {remote_host}:{remote_port}")
    answer = input("Create tunnel? (yes/no): ").strip().lower()
    if answer != "yes":
        return "Tunnel cancelled."

    try:
        import sshtunnel

        tunnel = sshtunnel.SSHTunnelForwarder(
            (remote_host, 22),
            ssh_username=ssh_user,
            ssh_pkey=ssh_key,
            remote_bind_address=("127.0.0.1", remote_port),
            local_bind_address=("127.0.0.1", local_port),
        )
        tunnel.start()
        return f"Tunnel active: localhost:{local_port} -> {remote_host}:{remote_port}"
    except ImportError:
        return "sshtunnel not installed. Run: pip install sshtunnel"
    except Exception as e:
        return f"Tunnel failed: {e}"


def check_ssh_available() -> bool:
    try:
        subprocess.run(["ssh", "-V"], capture_output=True, text=True, timeout=5)
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False
