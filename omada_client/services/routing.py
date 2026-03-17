from typing import Any

from omada_client.core.base_service import BaseService
from omada_client.types.models import StaticRouteBulkModel, StaticRouteModel
from omada_client.types.responses import ComplexResponseGeneric, PaginationResponseGeneric


class RoutingGroup(BaseService):
        
    def create_static_route(self, route: dict[str, Any]) -> None:
        self.client.check.site()
        route_model:StaticRouteModel = StaticRouteModel.model_validate(route)

        response_model = self.request.POST(
            path=f"sites/{self.client.site_id}/routing/static-routings",
            data=route_model.model_dump(by_alias=True),
            model=ComplexResponseGeneric[Any] 
        )

        if response_model.msg != 'Success.':
            raise ValueError(f"{response_model.error_code} {response_model.msg}")
        
    def bulk_create_static_routes(self, config: dict[str, Any]) -> None:
        self.client.check.site()

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

    def get_static_route_list(self, page: int = 1, page_size: int = 1000) -> PaginationResponseGeneric[StaticRouteModel] | None:
        self.client.check.site()
        self.request.check_pagination_params(page, page_size)

        response_model: ComplexResponseGeneric[PaginationResponseGeneric[StaticRouteModel]] = self.request.GET(
            path=f"sites/{self.client.site_id}/routing/static-routings",
            params={"page": page, "pageSize": page_size},
            model=ComplexResponseGeneric[PaginationResponseGeneric[StaticRouteModel]]
        )

        return response_model.result
    
    def get_static_route_by_name(self, name: str) -> StaticRouteModel | None:
        self.client.check.site()

        page: int = 1
        page_size: int = 1000

        while True:
            response: PaginationResponseGeneric[StaticRouteModel] | None = self.get_static_route_list(page, page_size)

            if response is None or not response.data:
                return None

            for route in response.data:
                if route.name == name:
                    return route

            if page * page_size >= response.total_rows:
                break

            page += 1

        return None
    
    def find_static_routes_by_name(self, name: str) -> list[StaticRouteModel]:
        self.client.check.site()

        page: int = 1
        page_size: int = 1000

        result: list[StaticRouteModel] = []
        name_lower = name.lower()

        while True:
            response: PaginationResponseGeneric[StaticRouteModel] | None = self.get_static_route_list(page, page_size)

            if response is None or not response.data:
                break

            for route in response.data:
                if route.name and name_lower in route.name.lower():
                    result.append(route)

            if page * page_size >= response.total_rows:
                break

            page += 1

        return result