from typing import Any

from omada_client.core.base_service import BaseService
from omada_client.types.models import StaticRouteBulkModel, StaticRouteModel
from omada_client.types.responses import ComplexResponseGeneric


class RoutingGroup(BaseService):
        
    def create_static_route(self, route: dict[str, Any]) -> None:
        self.client.Check.site()
        route_model:StaticRouteModel = StaticRouteModel.model_validate(route)

        response_model = self.request.POST(
            path=f"sites/{self.client.site_id}/routing/static-routings",
            data=route_model.model_dump(by_alias=True),
            model=ComplexResponseGeneric[Any] 
        )

        if response_model.msg != 'Success.':
            raise ValueError(f"{response_model.error_code} {response_model.msg}")
        
    def bulk_create_static_routes(self, config: dict[str, Any]) -> None:
        self.client.Check.site()

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