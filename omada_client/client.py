from requests import Session
import urllib3

from .core.auth import Auth
from .core.utils import Check, Format, Setting
from .core.request import RequestGroup

from .services.site import SiteGroup
from .services.client import ClientGroup
from .services.wlan import WlanGroup
from .services.wan import WanGroup
from .services.profile import ProfileGroup
from .services.routing import RoutingGroup
from .services.device import DeviceGroup


class OmadaClient:

    def __init__(
        self, 
        base_url:str, 
        omadac_id:str, 
        client_id:str, 
        client_secret:str
    ):
        urllib3.disable_warnings()
        self.session:Session = Session()
        self.base_url:str = base_url
        self.omadac_id:str = omadac_id

        self.site_id:str | None = None
        self.waln_id:str | None = None

        self.auth = Auth(self).authorize(client_id, client_secret)

        self.request = RequestGroup(self)
        self.check = Check(self)
        self.setting = Setting(self)
        self.format = Format(self)

        self.site = SiteGroup(self)
        self.client = ClientGroup(self)
        self.wlan = WlanGroup(self)
        self.wan = WanGroup(self)
        self.profile = ProfileGroup(self)
        self.routing = RoutingGroup(self)
        self.device = DeviceGroup(self)