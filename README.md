# omada_client
Python client for Tp-Link Omada Controller ([Omada Software Controller](https://www.tp-link.com/business-networking/omada-sdn-controller/omada-software-controller/)).
Execute API calls to Omada Controller from python code.

## Installation
```bash
pip install omada_client
```

## Examples
### Create class
```python
from omada_client import OmadaClient
omada = OmadaClient( 'OMADA_DOMAIN', 'OMADA_USER', 'OMADA_PASSWORD' )
```
where:
- OMADA_DOMAIN: URL of Omada WebUi page
- OMADA_USER: Username of Omada WebUi
- OMADA_PASSWORD: Password of Omada WebUi

or using environment variables "OMADA_DOMAIN" and "OMADA_USER" and "OMADA_PASSWORD":
```python
import os
from dotenv import load_dotenv
from omada_client import OmadaClient

load_dotenv()

omada = OmadaClient( os.getenv('OMADA_DOMAIN'), os.getenv('OMADA_USER'), os.getenv('OMADA_PASSWORD') )
```

## Methods
```python
# Get a list of WAN ports
omada.get_all_wan_ports()
# Get WAN port by its name
omada.get_wan_ports_by_name("WAN/LAN1")
# Create a static route
omada.create_static_route(...)
# Create a static route from a large amount of data
omada.create_static_route_to_inteface_with_big_data(...)
# Create a group profile
omada.create_profile_group('gpoupName', ['8.8.8.8', '1.1.1.1'])
# Get list of devices
omada.get_devices()
# Get a client by their MAC address
omada.get_client_by_mac('ff:ff:ff:ff:ff:ff')
# Get all clients
omada.get_clients()
# Get a client by its IP address
omada.get_client_by_ip('10.0.0.100')
# Assign a fixed IP address to the client based on its MAC address
omada.set_client_fixed_address_by_mac('ff:ff:ff:ff:ff:ff', '10.0.0.100')
# Assign a fixed IP address to the client based on its IP address
omada.set_client_fixed_address_by_ip('10.0.0.100')
# Assign a dynamic IP address to the client
omada.set_client_dymanic_address_by_mac('ff:ff:ff:ff:ff:ff')
```