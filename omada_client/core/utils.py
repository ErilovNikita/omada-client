from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from omada_client.client import OmadaClient

class Check:
        def __init__(self, client:"OmadaClient"):
                self.client = client
                
        def site(self) -> None:
                if not self.client.site_id:
                        raise ValueError("\"self.site_id\" is not set")
                
        def wlan(self) -> None:
                if not self.client.waln_id:
                        raise ValueError("\"self.waln_id\" is not set")
                
        def ssid_type(self, type:int) -> None:
                types:list[int] = [1,2,3]
                if type not in types:
                        raise ValueError(F"Available types: {', '.join([str(num) for num in types])}")
        
class Setting:
        def __init__(self, client:"OmadaClient"):
                self.client = client

        def set_site(self, site_id:str) -> None:
                self.client.site_id = site_id

        def set_wlan(self, waln_id:str) -> None:
                self.client.waln_id = waln_id

class Format:
        def __init__(self, client:"OmadaClient"):
                self.client = client
                
        def mac_address(self, mac: str) -> str:
                mac_cleaned = "".join(c for c in mac if c.isalnum())
                if len(mac_cleaned) != 12:
                        raise ValueError("Invalid MAC address: length must be 12 characters.")

                mac_formatted = "-".join(
                        mac_cleaned[i : i + 2].upper() for i in range(0, len(mac_cleaned), 2)
                )

                return mac_formatted
