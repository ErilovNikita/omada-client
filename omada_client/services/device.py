from omada_client.core.base_service import BaseService
from omada_client.types.models import DeviceModel
from omada_client.types.responses import ComplexResponseGeneric, PaginationResponseGeneric

class DeviceGroup(BaseService):
    def get_list(self, page: int = 1, page_size: int = 1000) -> PaginationResponseGeneric[DeviceModel] | None:
        self.client.check.site()
        self.request.check_pagination_params(page, page_size)

        response_model: ComplexResponseGeneric[PaginationResponseGeneric[DeviceModel]] = self.request.GET(
            path=f"sites/{self.client.site_id}/devices",
            params={"page": page, "pageSize": page_size},
            model=ComplexResponseGeneric[PaginationResponseGeneric[DeviceModel]]
        )

        return response_model.result