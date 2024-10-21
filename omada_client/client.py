"""
Omada python API client.
Permit send commands to omada controller via http calls
"""
import requests
from json import loads
import math
import urllib3

class OmadaClient:
    """
    OmadaClient class.
    Require:
        - base_url: Omada instanse url
        - login: Omada password
        - password: Omada password
    """

    def __init__(self, base_url, login, password):
        urllib3.disable_warnings()
        self.session = requests.Session()
        self.base_url = base_url
        self.__auth(login, password)

    def __auth(self, login, password):
        """
        Create session token
        Require:
            - login: Omada password
            - password: Omada password
        """
        response = self.session.post(
            f"{self.base_url}/api/v2/login",
            json={"username": login, "password": password},
            verify=False
        )
        data = loads(response.text)

        self.session_id = response.cookies.get('TPOMADA_SESSIONID')
        self.csrf = data['result']['token']
        self.user_id = self.__get_user_data()["result"]["omadacId"]
        self.sites = self.__get_user_data()["result"]["privilege"]["sites"]
        self.default_site = self.sites[0]
        # print("Login successful. CSRF Token:", self.csrf)

    def __get_headers(self) -> object:
        """Get headers for a request with a CSRF token"""
        headers =  {
            'Cookie' : 'TPOMADA_SESSIONID=' + self.session_id,
            'Csrf-Token' : self.csrf,
        }
        return headers

    def __get_user_data(self) -> object:
        """Get information about the current user"""
        request = self.session.get(
            f"{self.base_url}/api/v2/current/users",
            headers=self.__get_headers(),
            verify=False
        )
        return loads(request.text)

    def __divider(self, data:str, separator:str, size:int = 16) -> object:
        """
        Divides lists into blocks with the required number
        Require:
            - data: Data for creating a route
            - separator: Separator symbol
            - size: Block size (default 16)
        """
        result = []
        part_count = math.ceil(len(data.split(separator))/ size)

        for part_number in range(part_count):
            data_part = []
            end = 16 + (16 * part_number) - 1

            if end > (len(data.split(separator)) - 1): end = len(data.split(separator)) - 1
            
            i = 0 + (16 * part_number)
            while i <= end:
                data_part.append( data.split(separator)[i] )
                i += 1

            result.append(data_part)
        return result
    
    def __format_mac_address(self, mac: str) -> str:
        """
        Formats the mac address in the required format
        Require:
            - mac: String value of MAC address
        """
        # Убираем все лишние символы, оставляя только буквы и цифры
        mac_cleaned = ''.join(c for c in mac if c.isalnum())
        
        # Проверяем, что длина MAC адреса верная
        if len(mac_cleaned) != 12:
            raise ValueError("Неверный MAC-адрес: длина должна быть 12 символов.")
        
        # Преобразуем в верхний регистр и разделяем на пары символов
        mac_formatted = '-'.join(mac_cleaned[i:i+2].upper() for i in range(0, len(mac_cleaned), 2))
        
        return mac_formatted

    def get_all_wan_ports(self) -> list:
        """Get a list of WAN ports"""
        response = self.session.get(
            f"{self.base_url}/{self.user_id}/api/v2/sites/{self.default_site}/setting/wan/networks",
            headers=self.__get_headers(),
            verify=False
        )
        data = response.json()

        result_data = None
        if data['errorCode'] == 0 and data['msg'] == 'Success.':
            result_data = []
            wan_data = data['result']['wanPortSettings']
            for item in wan_data:
                result_data.append({
                    'portUuid' : item['portUuid'],
                    'port_name' : item['port_name'],
                    'portDesc' : item['portDesc']
                })
        else:
            result_data = data['msg']

        return result_data
    
    def get_wan_ports_by_name(self, port_name:str):
        """
        Get WAN port by its name
        Require:
            - port_name: WAN port name
        """
        allPorts = self.get_all_wan_ports()
        for item in allPorts:
            if item["port_name"].lower() == port_name.lower():
                return item
        return None

    def create_static_route(self, route_name:str, destinations:list, interface_id:str, next_hop_ip:str, routeEnable:bool = True, metricId:int = 0) -> object:
        """
        Create a static route
        Require:
            - route_name: Name of the new route
            - destinations: Array with route data
            - interface_id: Output interface identifier
            - next_hop_ip: Next address (Usually the gateway address of the selected WAN port)
            - routeEnable: Enable route immediately
            - metricId: Metric identifier
        """
        response = self.session.post(
            f"{self.base_url}/{self.user_id}/api/v2/sites/{self.default_site}/setting/transmission/staticRoutings",
            headers=self.__get_headers(),
            json={
                "name": route_name,
                "status": routeEnable,
                "destinations": destinations,
                "routeType": 1,
                "interfaceId": interface_id,
                "interfaceType": 0,
                "nextHopIp": next_hop_ip,
                "metric": metricId
            }
        )
        return response.json()

    def create_static_route_to_inteface_with_big_data(self, data_static_routes:list, interface_id:str, next_hop_ip:str, routeEnable:bool = True, metricId:int = 0) -> object:
        """
        Create a static route from a large amount of data
        Require:
            - route_name: Name of the new route
            - data_static_routes: Array with route data
            - interface_id: Output interface identifier
            - next_hop_ip: Next address (Usually the gateway address of the selected WAN port)
            - routeEnable: Enable route immediately
            - metricId: Metric identifier
        """
        for static_route in data_static_routes:
            parts = self.__divider(static_route['ips'], 16, ', ')

            if len(parts) == 1:
                request = self.create_static_route(
                    static_route['name'], 
                    parts[0],
                    interface_id,
                    next_hop_ip,
                    routeEnable,
                    metricId
                )
                print( static_route['name'] + ': ' + request['msg'] )
            else:
                for part_number in range(len(parts)):
                    part_name = static_route['name'] + ' ' + str(part_number + 1)
                    request = self.create_static_route(
                        part_name, 
                        parts[part_number],
                        interface_id,
                        next_hop_ip,
                        routeEnable,
                        metricId
                    )
                    print( part_name + ': ' + request['msg'] )

    def create_profile_group(self, group_name:str, ip_list:list) -> object:
        """
        Create a group profile
        Require:
            - group_name: Name of the new group
            - ip_list: Array with data
        """
        body = {
            "name": group_name,
            "type": 0,
            "ipList": [],
            "ipv6List":None,
            "macAddressList":None,
            "portList":None,
            "countryList":None,
            "description":"",
            "portType":None,
            "portMaskList":None,
            "domainNamePort": None
        }

        for ipWithMask in ip_list:
            body['ipList'].append({'ip' : ipWithMask.split('/')[0], "mask": ipWithMask.split('/')[1], "description":""})

        response = self.session.post(
            self.base_url + '/' + self.user_id + '/api/v2/sites/' + self.default_site + '/setting/profiles/groups',
            headers=self.__get_headers(),
            json=body
        )
        return response.json()

    def get_devices(self) -> list:
        """Get list of devices"""
        url = f"{self.base_url}/{self.user_id}/api/v2/sites/{self.default_site}/devices"
        response = self.session.get(url, headers=self.__get_headers(), verify=False)
        response.raise_for_status()
        return response.json()

    def get_client_by_mac(self, mac:str) -> object:
        """
        Get a client by their MAC address
        Require:
            - mac: String value of MAC address
        """
        correct_mac = self.__format_mac_address(mac)
        url = f"{self.base_url}/{self.user_id}/api/v2/sites/{self.default_site}/clients/{correct_mac}"
        response = self.session.get(url, headers=self.__get_headers(), verify=False)
        response.raise_for_status()
        return response.json()
    
    def get_clients(self) -> list:
        """Get all clients"""
        url = f"{self.base_url}/{self.user_id}/api/v2/sites/{self.default_site}/clients?currentPage=1&currentPageSize=100&filters.active=true"
        response = self.session.get(url, headers=self.__get_headers(), verify=False)
        response.raise_for_status()
        return response.json()['result']['data']

    def get_client_by_ip(self, ip_address:str) -> object:
        """
        Get a client by its IP address
        Require:
            - ip_address: String value of IP address
        """
        clients = self.get_clients()
        for client in clients:
            if client.get("ip") == ip_address:
                return client
        return None

    def set_client_fixed_address_by_mac(self, mac:str, ip_address:str = None) -> object:
        """
        Assign a fixed IP address to the client based on its MAC address
        Require:
            - mac: String value of MAC address
            - ip_address: String value of IP address
        """
        client_data = self.get_client_by_mac(mac)

        if not ip_address: ip_address = client_data['result']['ip']

        body = {
            "ipSetting": {
                "useFixedAddr": True,
                "netId": client_data['result']['ipSetting']['netId'],
                "ip": ip_address
            }
        }
        
        url = f"{self.base_url}/{self.user_id}/api/v2/sites/{self.default_site}/clients/{client_data['result']['mac']}"
        response = self.session.patch(url, headers=self.__get_headers(), json=body, verify=False)
        return response.json()
    
    def set_client_fixed_address_by_ip(self, ip_address:str) -> object:
        """
        Assign a fixed IP address to the client based on its IP address
        Require:
            - ip_address: String value of IP address
        """
        client = self.get_client_by_ip(ip_address)

        if client:
            mac_address = client.get('mac')
            return self.set_client_fixed_address_by_mac(mac_address)
        return None
    
    def set_client_dymanic_address_by_mac(self, mac:str) -> object:
        """
        Assign a dynamic IP address to the client
        Require:
            - mac: String value of MAC address
        """
        client_data = self.get_client_by_mac(mac)
        body = { "ipSetting": { "useFixedAddr": False } }
        url = f"{self.base_url}/{self.user_id}/api/v2/sites/{self.default_site}/clients/{self.__format_mac_address(mac)}"
        response = self.session.patch(url, headers=self.__get_headers(), json=body, verify=False)
        return response.json()

    # def reboot_device(self, device_id):
    #     """Reboot device by its ID"""
    #     url = f"{self.base_url}/{self.user_id}/api/v2/sites/{self.default_site}/devices/{device_id}/reboot"
    #     response = self.session.post(url, headers=self.__get_headers(), verify=False)
    #     response.raise_for_status()
    #     return response.json()['result']

    # def upgrade_firmware(self, device_id):
    #     """Update firmware on the device"""
    #     url = f"{self.base_url}/{self.user_id}.api/v2/sites/{self.default_site}/devices/{device_id}/upgrade"
    #     response = self.session.post(url, headers=self.__get_headers(), verify=False)
    #     response.raise_for_status()
    #     return response.json()['result']