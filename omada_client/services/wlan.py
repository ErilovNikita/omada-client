from omada_client.core.base_service import BaseService
from omada_client.types.models import SsidListModel, SsidModel, WlanModel
from omada_client.types.responses import ComplexResponseGeneric


class WlanGroup(BaseService):

    def get_list(self) -> list[WlanModel] | None:
        self.client.Check.site()

        response_model: ComplexResponseGeneric[list[WlanModel]] = self.request.GET(
            path=f"sites/{self.client.site_id}/wireless-network/wlans",
            model=ComplexResponseGeneric[list[WlanModel]]
        )

        return response_model.result
    
    def get_ssids(self, type:int = 1) -> list[SsidListModel] | None:
        self.client.Check.site()
        self.client.Check.ssid_type(type)

        response_model: ComplexResponseGeneric[list[SsidListModel]] = self.request.GET(
            path=f"sites/{self.client.site_id}/wireless-network/ssids",
            params={"type": type},
            model=ComplexResponseGeneric[list[SsidListModel]]
        )

        return response_model.result
    
    def get_ssid_by_id(self, ssid_id:str) -> SsidModel | None:
        self.client.Check.site()
        self.client.Check.wlan()

        response_model: ComplexResponseGeneric[SsidModel] = self.request.GET(
            path=f"sites/{self.client.site_id}/wireless-network/wlans/{self.client.waln_id}/ssids/{ssid_id}",
            params={"type": type},
            model=ComplexResponseGeneric[SsidModel]
        )

        return response_model.result
    