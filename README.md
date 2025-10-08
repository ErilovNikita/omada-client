# omada-client

> Python client for **Tp-Link Omada Controller** ([Omada Software Controller](https://www.tp-link.com/business-networking/omada-sdn-controller/omada-software-controller/)). Allows executing API calls to the Omada Controller from Python code.

[![PyPI Version](https://img.shields.io/pypi/v/omada-client?logo=pypi&label=Release)](https://pypi.org/project/omada-client)
[![PyPI Version](https://img.shields.io/pypi/pyversions/omada-client?logo=python&label=Python)](https://pypi.org/project/omada-client)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/omada-client?logo=pypi&label=PyPI%20-%20Downloads)](https://pypi.org/project/omada-client)
[![Tests](https://github.com/ErilovNikita/omada-client/actions/workflows/tests.yml/badge.svg)](https://github.com/ErilovNikita/omada-client/actions/workflows/tests.yml)

![](docs/preview.png)

Library created for automating and integrating with TP-Link Omada SDN Controllers. Unlike raw HTTP scripts or outdated wrappers, this library provides a clean, typed interface that enables developers and network engineers to manage Omada infrastructure with minimal effort and maximum reliability.

It abstracts away authentication, session handling, CSRF tokens, and endpoint routing, allowing you to focus on logic instead of network plumbing. The library is fully compatible with modern Python environments (>=3.11), supports structured data models via Pydantic, and includes utilities for batching large requests, safely manipulating network routes, and managing connected devices.

## Installation
Using python:
```sh
pip install omada-client
```


## Quick Start
Using direct credentials

```python
from omada_client import OmadaClient

omada = OmadaClient(
    "OMADA_DOMAIN",    # URL of Omada WebUI
    "OMADA_USER",      # Username
    "OMADA_PASSWORD",  # Password
    "SITE_ID"          # Site identify (Optional. Default: First site in list)
)
```

Using environment variables

```python
from dotenv import load_dotenv
import os
from omada_client import OmadaClient

load_dotenv()

omada = OmadaClient(
    os.getenv("OMADA_DOMAIN"),
    os.getenv("OMADA_USER"),
    os.getenv("OMADA_PASSWORD"),
    os.getenv("SITE_ID")
)

print(omada.get_devices())
```

## Methods Reference

| Category | Method | Parameters | Description |
|----------|--------|------------|-------------|
| **WAN Ports** | `get_all_wan_ports()` | None | List all WAN ports |
|  | `get_wan_ports_by_name(name)` | `name: str` | Get WAN port by name |
|  | `get_wan_ports_by_desc(desc)` | `desc: str` | Get WAN port by description |
| **Wireless** | `get_all_wlan()` | None | List all Wi-Fi networks |
|  | `get_wlan_by_ssid(ssid)` | `ssid: str` | Get Wi-Fi network by SSID |
| **Static Routes** | `create_static_route(route_name, destinations, interface_id, next_hop_ip, enable=False, metricId=0)` | `route_name: str`, `destinations: list[str]`, `interface_id: str`, `next_hop_ip: str` | Create a single static route |
|  | `create_static_route_to_inteface_with_big_data(data_static_routes, interface_id, next_hop_ip, enable=False, metricId=0)` | `data_static_routes: list`, `interface_id: str`, `next_hop_ip: str` | Create static routes from large data |
| **Devices & Clients** | `get_devices()` | None | List all devices |
|  | `get_clients()` | None | List all clients |
|  | `get_client_by_mac(mac)` | `mac: str` | Get client by MAC |
|  | `get_client_by_ip(ip_address)` | `ip_address: str` | Get client by IP |
|  | `create_group_ip_v4(group_name, ip_v4_list)` | `group_name: str`, `ip_v4_list: list[GroupMemberIpv4Model]` | Create new group IPv4 addresses |
|  | `delete_ipv4_from_group_by_name(group_name, ip_v4)` | `group_name: str`, `ip_v4: GroupMemberIpv4Model` | Remove IPv4 address from group by name  |
| **Groups** | `get_all_groups()` | | List all groups |
|  | `get_group_by_id(id)` | `id: str` | Get group port by ID |
|  | `get_group_by_name(name)` | `name: str` | Get group port by Name |
| **IP Assignment** | `set_client_fixed_address_by_mac(mac, ip_address=None)` | `mac: str`, `ip_address: str` | Assign fixed IP by MAC |
|  | `set_client_fixed_address_by_ip(ip_address)` | `ip_address: str` | Assign fixed IP by IP |
|  | `set_client_dymanic_address_by_mac(mac)` | `mac: str` | Assign dynamic IP by MAC |

## Advanced Example
Create static routes from large data sets

```python
from dotenv import load_dotenv
import os
from omada_client import OmadaClient

load_dotenv()

omada = OmadaClient(
    os.getenv("OMADA_DOMAIN"),
    os.getenv("OMADA_USER"),
    os.getenv("OMADA_PASSWORD")
)

data = [
    {"name": "group_1", "ips": "99.99.99.99/24, 88.88.88.88/24"},
    {"name": "group_2", "ips": "99.99.99.99/24, 88.88.88.88/24"}
]

wan = omada.get_wan_ports_by_desc("openwrt")

omada.create_static_route_to_inteface_with_big_data(
    data_static_routes=data,
    interface_id=wan.port_uuid,
    next_hop_ip=wan.wan_port_ipv4_setting.get("ipv4Static").get("gateway"),
    enable=False
)
```

## Notes
- Replace all IPs, MAC addresses, and credentials with real values.  
- Environment variables help keep sensitive credentials out of code.  
- Use badges above to quickly check test status and PyPI version.
