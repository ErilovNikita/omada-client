# omada-client
[![PyPI Version](https://img.shields.io/pypi/v/omada-client)](https://pypi.org/project/omada-client)

Python client for Tp-Link Omada Controller ([Omada Software Controller](https://www.tp-link.com/business-networking/omada-sdn-controller/omada-software-controller/)).
Execute API calls to Omada Controller from python code.

## Installation
```bash
pip install omada-client
```

## Examples
### Create class
```python
from omada_client import OmadaClient
omada = OmadaClient( "OMADA_DOMAIN", "OMADA_USER", "OMADA_PASSWORD" )
```
where:
- OMADA_DOMAIN: URL of Omada WebUi page
- OMADA_USER: Username of Omada WebUi
- OMADA_PASSWORD: Password of Omada WebUi

or using environment variables "OMADA_DOMAIN" and "OMADA_USER" and "OMADA_PASSWORD":
```python
from dotenv import load_dotenv
import os
from omada_client import OmadaClient
load_dotenv()

def main():
    omadaClient = OmadaClient( 
        os.getenv("OMADA_DOMAIN"), 
        os.getenv("OMADA_USER"), 
        os.getenv("OMADA_PASSWORD")
    )

    print( omadaClient.get_devices() )
if __name__ == "__main__":
    main() 
```

## Methods
```python
# Get a list of WAN ports
omadaClient.get_all_wan_ports()
# Get WAN port by its name
omadaClient.get_wan_ports_by_name("WAN/LAN1")
# Get WAN port by its name
omadaClient.get_wan_ports_by_desc("domru")
# Create a static route
omadaClient.create_static_route(
    route_name="test",
    destinations=["8.8.8.8/24", "1.1.1.1/24"],
    interface_id=omadaClient.get_wan_ports_by_desc("openwrt").port_uuid,
    next_hop_ip="192.168.1.1",
    enable=False
)
# Get list of devices
omadaClient.get_devices()
# Get a client by their MAC address
omadaClient.get_client_by_mac("ff:ff:ff:ff:ff:ff")
# Get all clients
omadaClient.get_clients()
# Get a client by its IP address
omadaClient.get_client_by_ip("10.0.0.100")
# Assign a fixed IP address to the client based on its MAC address
omadaClient.set_client_fixed_address_by_mac("ff:ff:ff:ff:ff:ff", "10.0.0.100")
# Assign a fixed IP address to the client based on its IP address
omadaClient.set_client_fixed_address_by_ip("10.0.0.100")
# Assign a dynamic IP address to the client
omadaClient.set_client_dymanic_address_by_mac("ff:ff:ff:ff:ff:ff")
```

## Advanced methods
### Create a static route from a large amount of data
```python
from dotenv import load_dotenv
import os
from omada_client import OmadaClient
load_dotenv()

def main():
    omadaClient = OmadaClient( 
        os.getenv("OMADA_DOMAIN"), 
        os.getenv("OMADA_USER"), 
        os.getenv("OMADA_PASSWORD")
    )

    data = [
        {
            "name" : "group_1",
            "ips" : "99.99.99.99/24, 88.88.88.88/24"
        },
        {
            "name" : "group_2",
            "ips" : "99.99.99.99/24, 88.88.88.88/24"
        }
    ]
    wan = omadaClient.get_wan_ports_by_desc("openwrt")
    omadaClient.create_static_route_to_inteface_with_big_data(
        data_static_routes=data,
        interface_id=wan.port_uuid,
        next_hop_ip=wan.wan_port_ipv4_setting.get("ipv4Static").get("gateway"),
        enable=False
    )
if __name__ == "__main__":
    main() 
```