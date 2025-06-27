import requests

def fetch_proxmox(cfg):
    auth = requests.post(
        f"https://{cfg['host']}:8006/api2/json/access/ticket",
        data={"username": cfg['username'], "password": cfg['password']},
        verify=cfg.get('verify_ssl', True)
    ).json()['data']

    ticket = auth['ticket']
    csrf = auth['CSRFPreventionToken']
    headers = {'CSRFPreventionToken': csrf, 'Cookie': f"PVEAuthCookie={ticket}"}

    resources = requests.get(
        f"https://{cfg['host']}:8006/api2/json/cluster/resources",
        headers=headers,
        verify=cfg.get('verify_ssl', True)
    ).json()

    return resources

def fetch_proxmox_cluster_any(cfg_list):
    for cfg in cfg_list:
        try:
            result = fetch_proxmox(cfg)
            if "data" in result:
                return result
        except Exception as e:
            continue
    return {"error": "All Proxmox nodes are unreachable"}
