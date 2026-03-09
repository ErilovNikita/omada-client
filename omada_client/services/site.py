
from omada_client.core.base_service import BaseService
from omada_client.types.models import SiteModel
from omada_client.types.responses import ComplexResponseGeneric, PaginationResponseGeneric

class SiteGroup(BaseService):

    def get_list(self, page: int = 1, page_size: int = 1000) -> PaginationResponseGeneric[SiteModel] | None:
        self.request.check_pagination_params(page, page_size)

        response_model: ComplexResponseGeneric[PaginationResponseGeneric[SiteModel]] = self.request.GET(
            path="sites",
            params={"page": page, "pageSize": page_size},
            model=ComplexResponseGeneric[PaginationResponseGeneric[SiteModel]]
        )

        return response_model.result
    
    def get_info(self, site_id: str) -> SiteModel | None:
        response_model: ComplexResponseGeneric[SiteModel] = self.request.GET(
            path=f"sites/{site_id}",
            model=ComplexResponseGeneric[SiteModel]
        )

        return response_model.result
    