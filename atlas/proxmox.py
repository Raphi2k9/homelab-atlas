import urllib3
from proxmoxer import ProxmoxAPI

from atlas import config

# Warnung von Proxmox ausblenden ausblenden
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_client() -> ProxmoxAPI:
    """Verbindung zur Proxmox-API mit dem Token aus der .env."""
    user, token_name = config.PVE_TOKEN_ID.split("!")
    return ProxmoxAPI(
        config.PVE_HOST,
        user=user,
        token_name=token_name,
        token_value=config.PVE_TOKEN_SECRET,
        verify_ssl=False,
        timeout=10,
    )


def get_guests() -> list[dict]:
    """Alle Container und VMs mit Status und Auslastung."""
    resources = get_client().cluster.resources.get(type="vm")
    guests = []
    for r in resources:
        guests.append({
            "id": r["vmid"],
            "name": r.get("name", ""),
            "type": "CT" if r["type"] == "lxc" else "VM",
            "status": r["status"],
            "cpu_percent": round(r.get("cpu", 0) * 100, 1),
            "mem_used_mb": round(r.get("mem", 0) / 1024**2),
            "mem_max_mb": round(r.get("maxmem", 0) / 1024**2),
            "uptime_h": round(r.get("uptime", 0) / 3600, 1),
        })
    return sorted(guests, key=lambda g: g["id"])


def get_node_status(node: str = "pve") -> dict:
    """Auslastung des Proxmox-Hosts."""
    s = get_client().nodes(node).status.get()
    return {
        "cpu_percent": round(s["cpu"] * 100, 1),
        "mem_used_gb": round(s["memory"]["used"] / 1024**3, 2),
        "mem_total_gb": round(s["memory"]["total"] / 1024**3, 2),
        "uptime_h": round(s["uptime"] / 3600, 1),
        "pve_version": s.get("pveversion", ""),
    }
