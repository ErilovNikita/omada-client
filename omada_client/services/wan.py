from omada_client.core.base_service import BaseService
from omada_client.types.models import InternetModel, WanModel
from omada_client.types.responses import ComplexResponseGeneric


class WanGroup(BaseService):

    def get_info_all(self) -> InternetModel | None:
        self.client.Check.site()

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
