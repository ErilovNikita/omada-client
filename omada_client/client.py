"""
Omada python API client.
Permit send commands to omada controller via http calls
"""

import requests
import math
import urllib3
from omada_client.types import HeaderModel, ComplexResponse, UserModel, WanPortModel, DeviceModel, ClientModel, WlanModel, GroupModel, GroupMemberIpv4Model, GroupMemberIpv6Model


class OmadaClient:
    """
    OmadaClient class.
    Require:
        - base_url: Omada instanse url
        - login: Omada password
        - password: Omada password
        - site: Omada location (Default: First location on list)
    """

    def __init__(self, base_url:str, login:str, password:str, site:str|None = None) -> None:
        urllib3.disable_warnings()
        self.session = requests.Session()
        self.base_url = base_url
        self.__auth(login, password, site)

    def __auth(self, login:str, password:str, site:str|None = None):
        """
        Create session token
        Require:
            - login: Omada password
            - password: Omada password
            - site: Omada location (Default: First location on list)
        """
        response = self.session.post(
            f"{self.base_url}/api/v2/login",
            json={"username": login, "password": password},
            verify=False,
        )
        response.raise_for_status()
        data = ComplexResponse.model_validate_json(response.text).result

        self.session_id = response.cookies.get("TPOMADA_SESSIONID")
        self.csrf = data.get("token")

        self.user_id = self.__get_user_data().omada_id
        self.sites = self.__get_user_data().privilege.sites

        if not site: 
            self.site = self.sites[0]
        else:
            self.site = site

    def __get_headers(self) -> dict[str, str]:
        """Get headers for a request with a CSRF token"""
        header = HeaderModel(token=self.csrf, cookie=self.session_id)
        return header.model_dump(by_alias=True)

    def __send_get_request(self, path):
        """Basic method for sending GET requests"""
        response = self.session.get(
            f"{self.base_url}{path}",
            headers=self.__get_headers(),
            verify=False,
        )
        response.raise_for_status()
        return ComplexResponse.model_validate_json(response.text)

    def __get_user_data(self) -> dict:
        """Get information about the current user"""
        response = self.__send_get_request("/api/v2/current/users").result
        return UserModel.model_validate(response)

    def __divider(self, data: str, separator: str, size: int = 16) -> dict:
        """
        Divides lists into blocks with the required number
        Require:
            - data: Data for creating a route
            - separator: Separator symbol
            - size: Block size (default 16)
        """
        result = []
        part_count = math.ceil(len(data.split(separator)) / size)

        for part_number in range(part_count):
            data_part = []
            end = 16 + (16 * part_number) - 1

            if end > (len(data.split(separator)) - 1):
                end = len(data.split(separator)) - 1

            i = 0 + (16 * part_number)
            while i <= end:
                data_part.append(data.split(separator)[i])
                i += 1

            result.append(data_part)
        return result

    def __format_mac_address(self, mac: str) -> str:
        """
        Formats the mac address in the required format
        Require:
            - mac: String value of MAC address
        """
        mac_cleaned = "".join(c for c in mac if c.isalnum())
        if len(mac_cleaned) != 12:
            raise ValueError("Invalid MAC address: length must be 12 characters.")

        mac_formatted = "-".join(
            mac_cleaned[i : i + 2].upper() for i in range(0, len(mac_cleaned), 2)
        )

        return mac_formatted

    def get_all_wan_ports(self) -> list[WanPortModel]:
        """Get a list of WAN ports"""
        response = self.__send_get_request(
            f"/{self.user_id}/api/v2/sites/{self.site}/setting/wan/networks"
        ).result
        wan_list = []
        for item in response.get("wanPortSettings"):
            wan_list.append(WanPortModel.model_validate(item))
        return wan_list

    def get_all_wlan(self) -> list[WlanModel]:
        """Get a list of Wifi Networks"""
        response = self.__send_get_request(
            f"/{self.user_id}/api/v2/sites/{self.site}/setting/wlans/660fccd41f61064468ff7f30/ssids?currentPage=1&currentPageSize=1000"
        ).result
        wlan_list = []
        for item in response.get("data"):
            wlan_list.append(WlanModel.model_validate(item))
        return wlan_list

    def get_all_groups(self) -> list[GroupModel]:
        """Get a list of groups"""
        response = self.__send_get_request(
            f"/{self.user_id}/api/v2/sites/{self.site}/setting/profiles/groups?currentPage=1&currentPageSize=1000"
        ).result
        group_list = []
        for item in response.get("data"):
            group_list.append(GroupModel.model_validate(item))
        return group_list
    
    def get_group_by_id(self, id:str) -> GroupModel:
        """Get group by ID"""
        group = next(
            (group for group in self.get_all_groups() if group.group_id.lower() == id.lower()),
            None,
        )
        if group: 
            return GroupModel.model_validate(group)
        else:
            raise ValueError(f"Not found group with id is {id}")
        
    def get_group_by_name(self, name:str) -> GroupModel:
        """Get group by name"""
        group = next(
            (group for group in self.get_all_groups() if group.name == name),
            None,
        )
        if group: 
            return GroupModel.model_validate(group)
        else:
            raise ValueError(f"Not found group with name is {name}")

    def create_group_ip_v4(self, group_name:str, ip_v4_list:list[GroupMemberIpv4Model]) -> None:
        """Create group"""
        data = {
            "type" : 0,
            "name": group_name,
            "ipList": [member.model_dump() for member in ip_v4_list]
        }

        url = f"{self.base_url}/{self.user_id}/api/v2/sites/{self.site}/setting/profiles/groups"
        response = self.session.post( url, headers=self.__get_headers(), json=data, verify=False)
        response.raise_for_status()
    
    def __patch_group(
        self, 
        group_name:str,
        ip_v4_list:list[GroupMemberIpv4Model] = [],
        ip_v6_list:list[GroupMemberIpv6Model] = [],
    ) -> None:
        """Update group"""
        current_group:GroupModel = self.get_group_by_name(group_name)

        if not current_group:
            raise ValueError(f"Not found group with name is {group_name}")
        else:
            data = {
                "resource" : current_group.resource,
                "type" : current_group.type,
                "name": current_group.name,
                "ipList": [member.model_dump() for member in ip_v4_list],
                "ipv6List": [member.model_dump() for member in ip_v6_list],
                "macAddressList": current_group.mac_address_list,
                "portList": current_group.port_list,
                "countryList": current_group.country_list,
                "portType": current_group.port_type,
                "portMaskList": current_group.port_mask_list,
                "domainNamePort":current_group.domain_name_port,
            }

            url = f"{self.base_url}/{self.user_id}/api/v2/sites/{self.site}/setting/profiles/groups/0/{current_group.group_id}"
            response = self.session.patch( url, headers=self.__get_headers(), json=data, verify=False)
            response.raise_for_status()

    def add_ipv4_on_group_by_name(self, group_name:str, ip_v4_list:list[GroupMemberIpv4Model]) -> None:
        """Add ip addres on group"""
        current_group:GroupModel = self.get_group_by_name(group_name)

        if not current_group:
            raise ValueError(f"Not found group with name is {group_name}")
        else:
            current_list:list[GroupMemberIpv4Model] = current_group.ip_list

            for ip in ip_v4_list:
                current_list.append(ip)

            self.__patch_group(current_group.name, ip_v4_list=current_list)

    def delete_ipv4_from_group_by_name(self, group_name:str, ip_v4:GroupMemberIpv4Model) -> None:
        """Remove ip addres from group"""
        current_group:GroupModel = self.get_group_by_name(group_name)
        if not current_group:
            raise ValueError(f"Not found group with name is {group_name}")
        else:
            current_list:list[GroupMemberIpv4Model] = current_group.ip_list

            for ip in current_list:
                if ip_v4.ip == ip.ip:
                    current_list.remove(ip)

            self.__patch_group(current_group.name, ip_v4_list=current_list)

    def get_wlan_by_ssid(self, ssid: str) -> WlanModel:
        """
        Get a Wlan by SSID
        Require:
            - ssid: Wi-Fi SSID
        """
        wlan_list = self.get_all_wlan()
        return next(
            (wlan for wlan in wlan_list if wlan.name.lower() == ssid.lower()),
            None,
        )

    def get_wan_ports_by_name(self, port_name: str) -> WanPortModel:
        """
        Get WAN port by its name
        Require:
            - port_name: WAN port name
        """
        wan_list = self.get_all_wan_ports()
        return next(
            (wan for wan in wan_list if wan.port_name.lower() == port_name.lower()),
            None,
        )

    def get_wan_ports_by_desc(self, port_decr: str) -> WanPortModel:
        """
        Get WAN port by description field
        Require:
            - port_decr: Description field in WAN
        """
        wan_list = self.get_all_wan_ports()
        return next(
            (wan for wan in wan_list if wan.port_desc.lower() == port_decr.lower()),
            None,
        )

    def create_static_route(
        self,
        route_name: str,
        destinations: list[str],
        interface_id: str,
        next_hop_ip: str,
        enable: bool = True,
        metricId: int = 0,
    ) -> None:
        """
        Create a static route
        Require:
            - route_name: Name of the new route
            - destinations: Array with route data
            - interface_id: Output interface identifier
            - next_hop_ip: Next address (Usually the gateway address of the selected WAN port)
            - enable: Enable route immediately
            - metricId: Metric identifier
        """
        response = self.session.post(
            f"{self.base_url}/{self.user_id}/api/v2/sites/{self.site}/setting/transmission/staticRoutings",
            headers=self.__get_headers(),
            json={
                "name": route_name,
                "status": enable,
                "destinations": destinations,
                "routeType": 1,
                "interfaceId": interface_id,
                "interfaceType": 0,
                "nextHopIp": next_hop_ip,
                "metric": metricId,
            },
            verify=False
        )
        response.raise_for_status()

    def create_static_route_to_inteface_with_big_data(
        self,
        data_static_routes: list,
        interface_id: str,
        next_hop_ip: str,
        enable: bool = True,
        metricId: int = 0,
    ) -> None:
        """
        Create a static route from a large amount of data
        Require:
            - route_name: Name of the new route
            - data_static_routes: Array with route data
            - interface_id: Output interface identifier
            - next_hop_ip: Next address (Usually the gateway address of the selected WAN port)
            - enable: Enable route immediately
            - metricId: Metric identifier
        """
        for static_route in data_static_routes:
            parts = self.__divider(
                data=static_route["ips"],
                size=16,
                separator=", "
            )

            if len(parts) == 1:
                self.create_static_route(
                    static_route["name"],
                    parts[0],
                    interface_id,
                    next_hop_ip,
                    enable,
                    metricId,
                )
            else:
                for part_number in range(len(parts)):
                    part_name = static_route["name"] + " " + str(part_number + 1)
                    self.create_static_route(
                        part_name,
                        parts[part_number],
                        interface_id,
                        next_hop_ip,
                        enable,
                        metricId,
                    )

    def get_devices(self) -> list[DeviceModel]:
        """Get list of devices"""
        response = self.__send_get_request(f"/{self.user_id}/api/v2/sites/{self.site}/devices").result
        device_list = []
        for item in response:
            device_list.append(DeviceModel.model_validate(item))
        return device_list

    def get_clients(self) -> list[ClientModel]:
        """Get all clients"""
        response = self.__send_get_request(
            f"/{self.user_id}/api/v2/sites/{self.site}/clients?currentPage=1&currentPageSize=1000&filters.active=true"
        ).result
        client_list = []
        for item in response.get("data"):
            client_list.append(ClientModel.model_validate(item))
        return client_list

    def get_client_by_mac(self, mac: str) -> ClientModel:
        """
        Get a client by their MAC address
        Require:
            - mac: String value of MAC address
        """
        correct_mac = self.__format_mac_address(mac)
        response = self.__send_get_request(
            f"/{self.user_id}/api/v2/sites/{self.site}/clients/{correct_mac}"
        ).result
        return ClientModel.model_validate(response)

    def get_client_by_ip(self, ip_address: str) -> ClientModel:
        """
        Get a client by its IP address
        Require:
            - ip_address: String value of IP address
        """
        for client in self.get_clients():
            if client.ip == ip_address:
                return ClientModel.model_validate(client)
        return None

    def set_client_fixed_address_by_mac(self, mac: str, ip_address: str = None) -> None:
        """
        Assign a fixed IP address to the client based on its MAC address
        Require:
            - mac: String value of MAC address
            - ip_address: String value of IP address
        """
        correct_mac = self.__format_mac_address(mac)
        client = self.get_client_by_mac(correct_mac)

        if not client:
            raise ValueError(f"Not found device with MAC address is {mac}")
        else:
            if not ip_address:
                ip_address = client.ip

            body = {
                "ipSetting": {
                    "useFixedAddr": True,
                    "netId": client.ip_setting.get("netId"),
                    "ip": ip_address,
                }
            }

            url = f"{self.base_url}/{self.user_id}/api/v2/sites/{self.site}/clients/{client.mac}"
            response = self.session.patch( url, headers=self.__get_headers(), json=body, verify=False )
            response.raise_for_status()
            
    def set_client_fixed_address_by_ip(self, ip_address: str) -> None:
        """
        Assign a fixed IP address to the client based on its IP address
        Require:
            - ip_address: String value of IP address
        """
        client = self.get_client_by_ip(ip_address)
        if not client:
            raise ValueError(f"Not found device with IP address is {ip_address}")
        else:
            self.set_client_fixed_address_by_mac(client.mac)
            
    def set_client_dymanic_address_by_mac(self, mac: str) -> None:
        """
        Assign a dynamic IP address to the client
        Require:
            - mac: String value of MAC address
        """
        correct_mac = self.__format_mac_address(mac)
        client = self.get_client_by_mac(correct_mac)

        if not client:
            raise ValueError(f"Not found device with MAC address is {mac}")
        else:
            body = {"ipSetting": {"useFixedAddr": False}}
            url = f"{self.base_url}/{self.user_id}/api/v2/sites/{self.site}/clients/{correct_mac}"
            response = self.session.patch(url, headers=self.__get_headers(), json=body, verify=False)
            response.raise_for_status()