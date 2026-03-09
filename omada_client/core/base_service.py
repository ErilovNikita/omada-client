from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from omada_client.client import OmadaClient

class BaseService:
    def __init__(self, client:"OmadaClient"):
        self.client = client
        self.request = client.Request