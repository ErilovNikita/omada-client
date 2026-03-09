from typing import TYPE_CHECKING, Any, Type

from omada_client.types.models import HeaderModel
from omada_client.types.responses import M

if TYPE_CHECKING:
    from omada_client.client import OmadaClient

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
