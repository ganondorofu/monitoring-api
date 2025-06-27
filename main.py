from flask import Flask, jsonify
from fetch import nextcloud_api, proxmox_api
import yaml
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

@app.route('/metrics/nextcloud')
def nextcloud_metrics():
    return jsonify(nextcloud_api.fetch_nextcloud_serverinfo(config['nextcloud']))

@app.route('/metrics/proxmox')
def proxmox_metrics():
    return jsonify(proxmox_api.fetch_proxmox_cluster_any(config['proxmox']))

if __name__ == '__main__':
    print('--- Debug Links ---')
    print('Nextcloud:  http://localhost:5000/metrics/nextcloud')
    print('Proxmox:    http://localhost:5000/metrics/proxmox')
    print('-------------------')
    app.run(host='0.0.0.0', port=5000)
