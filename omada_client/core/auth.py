from typing import TYPE_CHECKING

from omada_client.core.exception import OmadaAPIError
from omada_client.types.responses import AuthorizationResponse, ComplexResponseGeneric

if TYPE_CHECKING:
    from omada_client.client import OmadaClient

class Auth:
    def __init__(self, client:"OmadaClient"):
        self.client = client

    def authorize(self, client_id:str, client_secret:str) -> AuthorizationResponse:
        response = self.client.session.post(
            f"{self.client.base_url}/openapi/authorize/token",
            params={"grant_type": "client_credentials"},
            json={
                "omadacId": self.client.omadac_id,
                "client_id": client_id,
                "client_secret": client_secret
            },
            verify=False,
        )

        try:
            response.raise_for_status()
        except Exception as e:
            raise OmadaAPIError(f"HTTP error during authorization: {response.text}") from e

        data: ComplexResponseGeneric[AuthorizationResponse] = (
            ComplexResponseGeneric[AuthorizationResponse]
            .model_validate_json(response.text)
        )

        if data.result is None:
            raise OmadaAPIError(f"Omada API authorization failed: {data.msg} (code={data.error_code})")

        return data.result