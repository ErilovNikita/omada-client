import json
import os
from typing import Iterable, Union

from dotenv import load_dotenv
from pydantic import BaseModel

from omada_client import OmadaClient
from omada_client.types.models import DeviceModel, SiteModel
from omada_client.types.responses import PaginationResponseGeneric

load_dotenv()

def dump(model: Union[BaseModel, Iterable[BaseModel]]) -> object:
    if isinstance(model, BaseModel):
        return model.model_dump(by_alias=True)
    return [item.model_dump(by_alias=True) for item in model]

def pretty_print(model: Union[BaseModel, Iterable[BaseModel], None]) -> None:
    if model is None:
        print("None")
        return
    print(json.dumps(dump(model), indent=2, ensure_ascii=False))

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

    device:PaginationResponseGeneric[DeviceModel] | None = omada.device.get_list()
    if device:
        pretty_print(device.data)


if __name__ == "__main__":
    main()