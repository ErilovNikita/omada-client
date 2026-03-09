from typing import Any

from omada_client.core.base_service import BaseService
from omada_client.types.models import ClientModel, IpSettingModel
from omada_client.types.responses import ComplexResponseGeneric, PaginationResponseGeneric


class ClientGroup(BaseService):

    def get_list(self, page: int = 1, page_size: int = 1000) -> PaginationResponseGeneric[ClientModel] | None:
        self.client.Check.site()
        self.request.check_pagination_params(page, page_size)

        response_model: ComplexResponseGeneric[PaginationResponseGeneric[ClientModel]] = self.request.GET(
            path=f"sites/{self.client.site_id}/clients",
            params={"page": page, "pageSize": page_size},
            model=ComplexResponseGeneric[PaginationResponseGeneric[ClientModel]]
        )

        return response_model.result
    
    def get_info_by_mac(self, mac: str) -> ClientModel | None:
        self.client.Check.site()

        response_model: ComplexResponseGeneric[ClientModel] = self.request.GET(
            path=f"sites/{self.client.site_id}/clients/{mac}",
            model=ComplexResponseGeneric[ClientModel]
        )

        return response_model.result
    
    def get_by_ip(self, ip: str) -> ClientModel | None:
        self.client.Check.site()

        page: int = 1
        page_size: int = 100

        while True:
            response: PaginationResponseGeneric[ClientModel] | None = self.get_list(page, page_size)

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
        self.client.Check.site()

        mac_valid:str = self.client.Format.mac_address(mac)
        data_valid:IpSettingModel = IpSettingModel.model_validate(data)

        response_model: ComplexResponseGeneric[Any] = self.request.PATCH(
            path=f"network/sites/{self.client.site_id}/cmd/clients/{mac_valid}/update-ipSetting",
            data=data_valid.model_dump(by_alias=True),
            model=ComplexResponseGeneric[Any]
        )

        return response_model
    
    def __control(self, mac:str, method:str) -> None:
        self.client.Check.site()

        response_model: ComplexResponseGeneric[Any] = self.request.POST(
            path=f"sites/{self.client.site_id}/clients/{mac}/{method}",
            model=ComplexResponseGeneric[Any]
        )

        if response_model.msg != 'Success.':
            raise ValueError(f"{response_model.error_code} {response_model.msg}")

    def disconnect(self, mac: str) -> None:
        self.__control(mac, "disconnect")
    
    def block(self, mac: str) -> None:
        self.__control(mac, "block")

    def unblock(self, mac: str) -> None:
        self.__control(mac, "unblock")
