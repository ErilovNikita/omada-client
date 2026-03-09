import time
from typing import Any, Generic, TypeVar
from pydantic import BaseModel, Field, ConfigDict

M = TypeVar("M", bound=BaseModel)
T = TypeVar("T")

class ComplexResponseGeneric(BaseModel, Generic[T]):
    error_code: int | None = Field(alias="errorCode", default=None)
    msg: str | None = Field(None)
    result: T | None = Field(None)

class PaginationGeneric(BaseModel, Generic[T]):
    total_rows: int = Field(alias="totalRows")
    current_page: int = Field(alias="currentPage")
    current_size: int = Field(alias="currentSize")
    data: list[T] | None = Field(None)

class IdResponseModel(BaseModel):
    id: str

class AuthorizationModel(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    access_token: str = Field(alias="accessToken")
    expires_in: int = Field(alias="expiresIn")
    refresh_token: str = Field(alias="refreshToken")

class SiteModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    site_id: str = Field(alias="siteId")
    name: str
    region: str
    time_zone: str = Field(alias="timeZone")
    scenario: str
    type: int
    support_es: bool = Field(alias="supportES")
    support_l2: bool = Field(alias="supportL2")
    site_public_ip: str | None = Field(default=None, alias="sitePublicIp")

class IpSettingModel(BaseModel):
    use_fixed_addr: bool | None = Field(default=None, alias="useFixedAddr")
    net_id: str | None = Field(default=None, alias="netId")
    ip: str | None

class ClientModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    mac: str
    name: str | None = None
    host_name: str | None = Field(default=None, alias="hostName")
    vendor: str | None = None
    device_type: str | None = Field(default=None, alias="deviceType")
    device_category: str | None = Field(default=None, alias="deviceCategory")
    ip: str | None = None
    connect_type: str | int | None = Field(default=None, alias="connectType")
    connected_to_wireless_router: bool | None = Field(default=None, alias="connectedToWirelessRouter")
    wireless: bool | None = None
    ssid: str | None = None
    ip_setting: IpSettingModel | None = Field(default=None, alias="ipSetting")
    signal_level: int | None = Field(default=None, alias="signalLevel")
    ap_name: str | None = Field(default=None, alias="apName")
    uptime: int | None = None
    last_seen: int | None = Field(default=None, alias="lastSeen")
    blocked: bool | None = None
    guest: bool | None = None
    active: bool | None = None
    system_name: str | None = Field(default=None, alias="systemName")
    dhcp_lease_time: int | None = Field(default=None, alias="dhcpLeaseTime")

class HeaderModel(BaseModel):
    Authorization: str

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=None
    )
    
    @classmethod
    def from_auth(cls, auth:AuthorizationModel) -> "HeaderModel":
        return cls(Authorization=f"AccessToken={auth.access_token}")

    def get_headers(self) -> dict[str, str]:
        return self.model_dump(by_alias=True)

class WanModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    class Ipv4SettingModel(BaseModel):
        model_config = ConfigDict(extra="ignore")

        class DhcpModel(BaseModel):
            model_config = ConfigDict(extra="ignore")

            unicast_dhcp: bool | None = Field(default=None, alias="unicastDhcp")
            primary_dns: str | None = Field(default=None, alias="primaryDns")
            secondary_dns: str | None = Field(default=None, alias="secondaryDns")
            mtu: int | None = None
            wan_multiple_ips: list[Any] = Field(default_factory=list, alias="wanMultipleIps")
            dhcp_options: list[Any] = Field(default_factory=list, alias="dhcpOptions")

        proto_type: int | None = Field(default=None, alias="protoType")
        vlan_id: int | None = Field(default=None, alias="vlanId")
        qos_tag_enable: bool | None = Field(default=None, alias="qosTagEnable")
        vlan_priority: int | None = Field(default=None, alias="vlanPriority")
        ipv4_static: Any | None = Field(default=None, alias="ipv4Static")
        ipv4_dhcp: DhcpModel | None = Field(default=None, alias="ipv4Dhcp")
        ipv4_pppoe: Any | None = Field(default=None, alias="ipv4Pppoe")
        ipv4_l2tp: Any | None = Field(default=None, alias="ipv4L2tp")
        ipv4_pptp: Any | None = Field(default=None, alias="ipv4Pptp")
        ipv4_pppoa: Any | None = Field(default=None, alias="ipv4Pppoa")
        ipv4_ipoa: Any | None = Field(default=None, alias="ipv4Ipoa")

    class Ipv6SettingModel(BaseModel):
        model_config = ConfigDict(extra="ignore")

        enable: bool | None = None
        proto_type: int | None = Field(default=None, alias="protoType")
        ipv6_dynamic: Any | None = Field(default=None, alias="ipv6Dynamic")
        ipv6_pppoe: Any | None = Field(default=None, alias="ipv6Pppoe")
        ipv6_tunnel: Any | None = Field(default=None, alias="ipv6Tunnel")
        ipv6_static: Any | None = Field(default=None, alias="ipv6Static")

    class MacSettingModel(BaseModel):
        model_config = ConfigDict(extra="ignore")

        method: int | None = None
        mac: str | None = None

    port_id: str | None = Field(default=None, alias="portId")
    port_name: str | None = Field(default=None, alias="portName")
    port_description: str | None = Field(default=None, alias="portDescription")
    wan_port_ipv4_setting: Ipv4SettingModel | None = Field(default=None, alias="wanPortIpv4Setting")
    wan_port_ipv6_setting: Ipv6SettingModel | None = Field(default=None, alias="wanPortIpv6Setting")
    wan_port_mac_setting: MacSettingModel | None = Field(default=None, alias="wanPortMacSetting")

class InternetModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    class WanBalanceModel(BaseModel):
        model_config = ConfigDict(extra="ignore")

        weights: list[int] = Field(default_factory=list)
        app_opt_routing: bool | None = Field(default=None, alias="appOptRouting")
        link_backup: bool | None = Field(default=None, alias="linkBackup")

    omadac_id: str | None = Field(default=None, alias="omadacId")
    site_id: str | None = Field(default=None, alias="siteId")
    enable: bool | None = None
    osg_port_info: dict[str, Any] = Field(default_factory=dict, alias="osgPortInfo")
    port_uuids: list[str] = Field(default_factory=list, alias="portUuids")
    interval: int | None = None
    support_wan_multiple_ip: bool | None = Field(default=None, alias="supportWanMultipleIp")
    support_lte: bool | None = Field(default=None, alias="supportLte")
    support_dual_sim: int | None = Field(default=None, alias="supportDualSim")
    support_dsl: bool | None = Field(default=None, alias="supportDsl")
    support_virtual_wan: bool | None = Field(default=None, alias="supportVirtualWan")
    support_network_isolation: bool | None = Field(default=None, alias="supportNetworkIsolation")
    support_dhcp_options: bool | None = Field(default=None, alias="supportDhcpOptions")
    support_usb_dhcp_options: bool | None = Field(default=None, alias="supportUsbDhcpOptions")
    wan_port_settings: list[WanModel] = Field(default_factory=list, alias="wanPortSettings")
    usb_lte_settings: list[dict[str, Any]] = Field(default_factory=list, alias="usbLteSettings")
    lte_wan_settings: list[dict[str, Any]] = Field(default_factory=list, alias="lteWanSettings")
    wan_load_balance: WanBalanceModel | None = Field(default=None, alias="wanLoadBalance")
    gateway_mac: str | None = Field(default=None, alias="gatewayMac")

class WlanModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    wlan_id: str = Field(alias="wlanId")
    name: str
    primary: bool

class SsidListModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    class SsidModel(BaseModel):
        model_config = ConfigDict(extra="ignore")

        ssid_id: str = Field(alias="ssidId")
        ssid_name: str = Field(alias="ssidName")

    wlan_id: str = Field(alias="wlanId")
    wlan_name: str = Field(alias="wlanName")
    ssid_list: list[SsidModel] = Field(alias="ssidList")

class SsidModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    class PskSettingModel(BaseModel):
        model_config = ConfigDict(extra="ignore")

        security_key: str | None = Field(default=None, alias="securityKey")
        version_psk: int | None = Field(default=None, alias="versionPsk")
        encryption_psk: int | None = Field(default=None, alias="encryptionPsk")
        gik_rekey_psk_enable: bool | None = Field(default=None, alias="gikRekeyPskEnable")

    ssid_id: str | None = Field(default=None, alias="ssidId")
    name: str | None = None
    band: int | None = None
    auto_wan_access: bool | None = Field(default=None, alias="autoWanAccess")
    guest_net_enable: bool | None = Field(default=None, alias="guestNetEnable")
    security: int | None = None
    broadcast: bool | None = None
    vlan_enable: bool | None = Field(default=None, alias="vlanEnable")
    psk_setting: PskSettingModel | None = Field(default=None, alias="pskSetting")
    device_type: int | None = Field(default=None, alias="deviceType")

class ProfileGroupModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    class GroupMemberIpv4Model(BaseModel):
        ip: str
        mask: int = Field(32)
        description: str = Field("")
        key: int = Field(int(time.time())*1000)

    class GroupMemberIpv6Model(BaseModel):
        ip: str
        prefix: int
        key: int = Field(int(time.time())*1000)

    group_id: str = Field("", alias="groupId")
    site: str = Field("")
    build_in: bool = Field(False, alias="buildIn")
    name: str
    ip_list: list[GroupMemberIpv4Model] = Field([], alias="ipList")
    ip_v6_list: list[GroupMemberIpv6Model] = Field([], alias="ipv6List")
    count: int
    type: int
    domain_name_port: list[Any] = Field(None, alias="domainNamePort")
    port_mask_list: list[Any] = Field(None, alias="portMaskList")
    port_type: int = Field(None, alias="portType")
    country_list: list[Any] = Field(None, alias="countryList")
    port_list: list[Any] = Field(None, alias="portList")
    mac_address_list: list[Any] = Field(None, alias="macAddressList")

class GroupRequestModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    class IpModel(BaseModel):
        model_config = ConfigDict(extra="ignore")

        ip: str | None = None
        mask: int | None = None
        description: str | None = None

    class Ipv6Model(BaseModel):
        model_config = ConfigDict(extra="ignore")

        ip: str | None = None
        prefix: int | None = None
        description: str | None = None

    class PortMaskModel(BaseModel):
        model_config = ConfigDict(extra="ignore")

        port: int | None = None
        mask: str | None = None

    class MacAddressModel(BaseModel):
        model_config = ConfigDict(extra="ignore")

        name: str | None = None
        mac_address: str | None = Field(default=None, alias="macAddress")

    class DomainNamePortModel(BaseModel):
        model_config = ConfigDict(extra="ignore")

        address: str | None = None
        port: str | None = None
        description: str | None = None

    name: str | None = None
    type: int | None = None
    ip_list: list[IpModel] = Field(default_factory=list, alias="ipList")
    ipv6_list: list[Ipv6Model] = Field(default_factory=list, alias="ipv6List")
    port_type: int | None = Field(default=None, alias="portType")
    port_list: list[int] = Field(default_factory=list, alias="portList")
    port_mask_list: list[PortMaskModel] = Field(default_factory=list, alias="portMaskList")
    mac_address_list: list[MacAddressModel] = Field(default_factory=list, alias="macAddressList")
    country_list: list[str] = Field(default_factory=list, alias="countryList")
    description: str | None = None
    domain_name_port: list[DomainNamePortModel] = Field(
        default_factory=list,
        alias="domainNamePort"
    )

class StaticRouteModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: str
    status: bool = True
    destinations: list[str]
    route_type: int = Field(default=0, alias="routeType")
    interface_id: str = Field(default="", alias="interfaceId")
    interface_type: int = Field(default=0, alias="interfaceType")
    next_hop_ip: str = Field(default="", alias="nextHopIp")
    metric: int = 0


class StaticRouteBulkModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    class StaticRouteBulkItemModel(BaseModel):
        model_config = ConfigDict(extra="ignore")

        name: str
        ips: list[str]

    routes: list[StaticRouteBulkItemModel]
    interface_id: str = Field(alias="interfaceId")
    next_hop_ip: str = Field(alias="nextHopIp")
    status: bool = True
    metric: int = 0