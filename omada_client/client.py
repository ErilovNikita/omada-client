"""
Omada python API client.
Permit send commands to omada controller via http calls
"""

from typing import Any, Type
import requests
import urllib3

from omada_client.types import M, ComplexResponseGeneric, PaginationGeneric, StaticRouteBulkModel, StaticRouteModel
from omada_client.types import AuthorizationModel, ClientModel, HeaderModel, SiteModel, InternetModel, IpSettingModel, ProfileGroupModel, SsidListModel, SsidModel, WanModel, WlanModel

class OmadaClient:
    """
    OmadaClient class.
    Require:
        - base_url: Omada API url
        - omadac_id: Omada API omadac_id
        - client_id: Omada API client_id
        - client_secret: Omada API client_secret
    """

    def __init__(self, base_url:str, omadac_id:str, client_id:str, client_secret:str) -> None:
        urllib3.disable_warnings()
        self.session = requests.Session()
        self.base_url = base_url
        self.omadac_id = omadac_id
        self.__authorize(client_id, client_secret)

        self.Request = self.RequestGroup(self)
        self.Site = self.SiteGroup(self)
        self.Client = self.ClientGroup(self)
        self.Wan = self.WanGroup(self)
        self.Wlan = self.WlanGroup(self)
        self.Profile = self.ProfileGroup(self)
        self.Routing = self.RoutingGroup(self)

    def __authorize(self, client_id:str, client_secret:str) -> None:
        """
        Create session token
        Require:
            - client_id: Omada API client_id
            - client_secret: Omada API client_secret
        """

        response = self.session.post(
            f"{self.base_url}/openapi/authorize/token",
            params={
                "grant_type": "client_credentials"
            },
            json={
                "omadacId": self.omadac_id,
                "client_id": client_id,
                "client_secret": client_secret
            },
            verify=False,
        )

        response.raise_for_status()

        authorization_response_model:ComplexResponseGeneric[AuthorizationModel] = ComplexResponseGeneric[AuthorizationModel].model_validate_json(response.text)
        self.auth = authorization_response_model.result

    def set_site(self, site_id:str) -> None:
        self.site_id = site_id

    def check_site(self) -> None:
       if not self.site_id:
          raise ValueError("\"self.site_id\" is not set")
       
    def set_wlan(self, waln_id:str) -> None:
        self.waln_id = waln_id

    def check_wlan(self) -> None:
       if not self.waln_id:
          raise ValueError("\"self.waln_id\" is not set")

    def check_ssid_type(self, type:int) -> None:
        types:list[int] = [1,2,3]
        if type not in types:
            raise ValueError(F"Available types: {', '.join([str(num) for num in types])}")

    def format_mac_address(self, mac: str) -> str:
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

    class RequestGroup:
        def __init__(self, client:"OmadaClient"):
            self.client = client

        def __get_headers(self) -> dict[str, str]:
            assert self.client.auth is not None, "Authorization failed, result is None"
            return HeaderModel.from_auth(self.client.auth).model_dump(by_alias=True)
    
        def __get_generic_path(self) -> str:
            return f"{self.client.base_url}/openapi/v1/{self.client.omadac_id}"
        
        def check_pagination_params(self, page: int, page_size: int) -> None:
            if page < 1:
                raise ValueError("The \"page\" parameter must be greater than 1.")
            if page_size < 1 or page_size > 1000:
                raise ValueError("The \"page_size\" parameter must be between 1 and 1000.")
       

        def GET(self, path:str, model: Type[M], params: dict[str, Any] = {}) -> M:
            response = self.client.session.get(
                f"{self.__get_generic_path()}/{path}",
                headers=self.__get_headers(),
                params=params,
                verify=False,
            )

            response.raise_for_status()

            return model.model_validate_json(response.text)
        
        def PATCH(self, path:str, model: Type[M], data: dict[str, Any] = {}, params: dict[str, Any] = {}) -> M:
            response = self.client.session.patch(
                f"{self.__get_generic_path()}/{path}",
                headers=self.__get_headers(),
                params=params,
                json=data,
                verify=False,
            )

            response.raise_for_status()

            return model.model_validate_json(response.text)
        
        def POST(self, path:str, model: Type[M], data: dict[str, Any] = {}, params: dict[str, Any] = {}) -> M:
            response = self.client.session.post(
                f"{self.__get_generic_path()}/{path}",
                headers=self.__get_headers(),
                params=params,
                json=data,
                verify=False,
            )

            response.raise_for_status()

            return model.model_validate_json(response.text)

    class SiteGroup:
        def __init__(self, client:"OmadaClient"):
            self.client = client
            self.request = client.Request
            self.base_path = "sites"

        def get_list(self, page: int = 1, page_size: int = 1000) -> PaginationGeneric[SiteModel] | None:
            self.request.check_pagination_params(page, page_size)

            response_model: ComplexResponseGeneric[PaginationGeneric[SiteModel]] = self.request.GET(
                path=f"{self.base_path}",
                params={"page": page, "pageSize": page_size},
                model=ComplexResponseGeneric[PaginationGeneric[SiteModel]]
            )

            return response_model.result
        
        def get_info(self, site_id: str) -> SiteModel | None:
            response_model: ComplexResponseGeneric[SiteModel] = self.request.GET(
                path=f"{self.base_path}/{site_id}",
                model=ComplexResponseGeneric[SiteModel]
            )

            return response_model.result
        
    class ClientGroup:
        def __init__(self, client:"OmadaClient"):
            self.client = client
            self.request = client.Request

        def get_list(self, page: int = 1, page_size: int = 1000) -> PaginationGeneric[ClientModel] | None:
            self.client.check_site()
            self.request.check_pagination_params(page, page_size)

            response_model: ComplexResponseGeneric[PaginationGeneric[ClientModel]] = self.request.GET(
                path=f"sites/{self.client.site_id}/clients",
                params={"page": page, "pageSize": page_size},
                model=ComplexResponseGeneric[PaginationGeneric[ClientModel]]
            )

            return response_model.result
        
        def get_info_by_mac(self, mac: str) -> ClientModel | None:
            self.client.check_site()

            response_model: ComplexResponseGeneric[ClientModel] = self.request.GET(
                path=f"sites/{self.client.site_id}/clients/{mac}",
                model=ComplexResponseGeneric[ClientModel]
            )

            return response_model.result
        
        def get_by_ip(self, ip: str) -> ClientModel | None:
            self.client.check_site()

            page: int = 1
            page_size: int = 100

            while True:
                response: PaginationGeneric[ClientModel] | None = self.get_list(page, page_size)

                if response is None or response.data is None:
                    return None

                for client in response.data:
                    if client.ip == ip:
                        return self.get_info_by_mac(client.mac)

                if page * page_size >= response.total_rows:
                    break

                page += 1

            return None

        def set_ip_settings(self, mac: str, data:dict[str, Any]) -> Any:
            self.client.check_site()

            mac_valid:str = self.client.format_mac_address(mac)
            data_valid:IpSettingModel = IpSettingModel.model_validate(data)

            response_model: ComplexResponseGeneric[Any] = self.request.PATCH(
                path=f"network/sites/{self.client.site_id}/cmd/clients/{mac_valid}/update-ipSetting",
                data=data_valid.model_dump(by_alias=True),
                model=ComplexResponseGeneric[Any]
            )

            return response_model
        

    class WlanGroup:
        def __init__(self, client:"OmadaClient"):
            self.client = client
            self.request = client.Request

        def get_list(self) -> list[WlanModel] | None:
            self.client.check_site()

            response_model: ComplexResponseGeneric[list[WlanModel]] = self.request.GET(
                path=f"sites/{self.client.site_id}/wireless-network/wlans",
                model=ComplexResponseGeneric[list[WlanModel]]
            )

            return response_model.result
        
        def get_ssids(self, type:int = 1) -> list[SsidListModel] | None:
            self.client.check_site()
            self.client.check_ssid_type(type)

            response_model: ComplexResponseGeneric[list[SsidListModel]] = self.request.GET(
                path=f"sites/{self.client.site_id}/wireless-network/ssids",
                params={"type": type},
                model=ComplexResponseGeneric[list[SsidListModel]]
            )

            return response_model.result
        
        def get_ssid_by_id(self, ssid_id:str) -> SsidModel | None:
            self.client.check_site()
            self.client.check_wlan()

            response_model: ComplexResponseGeneric[SsidModel] = self.request.GET(
                path=f"sites/{self.client.site_id}/wireless-network/wlans/{self.client.waln_id}/ssids/{ssid_id}",
                params={"type": type},
                model=ComplexResponseGeneric[SsidModel]
            )

            return response_model.result
        
    class WanGroup:
        def __init__(self, client:"OmadaClient"):
            self.client = client
            self.request = client.Request

        def get_info_all(self) -> InternetModel | None:
            self.client.check_site()

            response_model: ComplexResponseGeneric[InternetModel] = self.request.GET(
                path=f"sites/{self.client.site_id}/internet",
                model=ComplexResponseGeneric[InternetModel]
            )

            return response_model.result
        
        def get_info_by_name(self, wan_name:str) -> WanModel | None:
            response = self.get_info_all()

            if response:
                internet_info:InternetModel = response
                
                for wan in internet_info.wan_port_settings:
                    if wan.port_name == wan_name:
                        return wan

            return None
        
        def get_info_by_description(self, wan_description:str) -> WanModel | None:
            response = self.get_info_all()

            if response:
                internet_info:InternetModel = response
                
                for wan in internet_info.wan_port_settings:
                    if wan.port_description == wan_description:
                        return wan

            return None

    class ProfileGroup:
        def __init__(self, client:"OmadaClient"):
            self.client = client
            self.request = client.Request

        def get_all_group(self) -> list[ProfileGroupModel] | None:
            self.client.check_site()

            response_model: ComplexResponseGeneric[list[ProfileGroupModel]] = self.request.GET(
                path=f"sites/{self.client.site_id}/profiles/groups",
                model=ComplexResponseGeneric[list[ProfileGroupModel]]
            )

            return response_model.result
    
        def get_group_by_id(self, group_id:str) -> ProfileGroupModel | None:
            response = self.get_all_group()

            if response:
                all_group:list[ProfileGroupModel] = response
                
                for group in all_group:
                    if group.group_id == group_id:
                        return group

            return None
        
        def get_group_by_name(self, group_name:str) -> ProfileGroupModel | None:
            response = self.get_all_group()

            if response:
                all_group:list[ProfileGroupModel] = response
                
                for group in all_group:
                    if group.name == group_name:
                        return group

            return None
        
        # TO-DO
        # def create_group(self, group: dict[str, Any]) -> ProfileGroupModel | None:
        #     self.client.check_site()
        #     group_valid = ProfileGroupModel.model_validate(group)

        #     response_model: ComplexResponseGeneric[IdResponseModel] = self.request.POST(
        #         path=f"sites/{self.client.site_id}/profiles/groups",
        #         data=group_valid.model_dump(),
        #         model=ComplexResponseGeneric[IdResponseModel]
        #     )
            
        #     if response_model.result and response_model.result.id:
        #         return self.get_group_by_id(response_model.result.id)

    class RoutingGroup:
        def __init__(self, client:"OmadaClient"):
            self.client = client
            self.request = client.Request
            
        def create_static_route(self, route: dict[str, Any]) -> None:
            self.client.check_site()
            route_model:StaticRouteModel = StaticRouteModel.model_validate(route)

            response_model = self.request.POST(
                path=f"sites/{self.client.site_id}/routing/static-routings",
                data=route_model.model_dump(by_alias=True),
                model=ComplexResponseGeneric[Any] 
            )

            if response_model.msg != 'Success.':
                raise ValueError(f"{response_model.error_code} {response_model.msg}")
            
        def bulk_create_static_routes(self, config: dict[str, Any]) -> None:
            self.client.check_site()

            config_model = StaticRouteBulkModel.model_validate(config)
            for route in config_model.routes:
                ips = route.ips

                parts = [
                    ips[i:i + 16]
                    for i in range(0, len(ips), 16)
                ]

                for index, part in enumerate(parts, start=1):
                    self.create_static_route({
                        "name": route.name if len(parts) == 1 else f"{route.name} {index}",
                        "destinations": part,
                        "interfaceId": config_model.interface_id,
                        "nextHopIp": config_model.next_hop_ip,
                        "status": config_model.status,
                        "metric": config_model.metric
                    })