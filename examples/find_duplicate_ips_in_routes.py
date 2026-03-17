from collections import defaultdict
import ipaddress
import os
from typing import Any

from dotenv import load_dotenv

from omada_client import OmadaClient
from omada_client.types.models import SiteModel, StaticRouteModel
from omada_client.types.responses import PaginationResponseGeneric

load_dotenv()

def get_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Environment variable {name} is not set")
    return value

def main() -> None:
    omada = OmadaClient(
        get_env("OMADA_DOMAIN"),
        get_env("OMADACID"),
        get_env("CLIENT_ID"),
        get_env("CLIENT_SECRET"),
    )

    sites_page: PaginationResponseGeneric[SiteModel] | None = omada.site.get_list()
    if sites_page is None or not sites_page.data:
        raise RuntimeError("No sites returned from API")

    omada.setting.set_site(sites_page.data[0].site_id)


    routes_pagination_response:PaginationResponseGeneric[Any] | None = omada.routing.get_static_route_list()
    if not routes_pagination_response:
        raise RuntimeError("No static routes returned from API")
    
    routes:list[StaticRouteModel] | None = routes_pagination_response.data

    if not routes:
        raise RuntimeError("No static routes returned from API")

    networks: list[tuple[Any, str]] = []

    for route in routes:
        if not route.destinations:
            continue

        for destination in route.destinations:
            try:
                net = ipaddress.ip_network(destination, strict=False)
                networks.append((net, route.name))
            except ValueError:
                continue

    overlaps: dict[Any, set[str]] = defaultdict(set)

    for i in range(len(networks)):
        net1, route1 = networks[i]

        for j in range(i + 1, len(networks)):
            net2, route2 = networks[j]

            if net1.overlaps(net2):
                parent = net1 if net1.prefixlen < net2.prefixlen else net2
                overlaps[parent].update([route1, route2])
       

    if not overlaps:
        print("No overlapping networks found")
    else:
        for nets, route_names in overlaps.items():
            print(f"{nets} -> {', '.join(route_names)}")

if __name__ == "__main__":
    main()