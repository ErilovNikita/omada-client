from typing import Any, Generic, TypeVar
from pydantic import BaseModel, Field, ConfigDict#, field_validator
#import time

T = TypeVar("T", bound=BaseModel)

class ComplexResponseGeneric(BaseModel, Generic[T]):
    error_code: int | None = Field(alias="errorCode", default=None)
    msg: str | None = Field(None)
    result: T | None = Field(None)

class PaginationGeneric(BaseModel, Generic[T]):
    total_rows: int = Field(alias="totalRows")
    current_page: int = Field(alias="currentPage")
    current_size: int = Field(alias="currentSize")
    data: list[T] | None = Field(None)

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

# class PrivilegeModel(BaseModel):
#     sites: list[str]
#     all: bool


# class UserModel(BaseModel):
#     id: str
#     role_id: str = Field(None, alias="roleId")
#     role_name: str = Field(None, alias="roleName")
#     name: str
#     email: str
#     omada_id: str = Field(None, alias="omadacId")
#     privilege: PrivilegeModel
#     root: bool


# class WanPortModel(BaseModel):
#     port_uuid: str = Field(None, alias="portUuid")
#     port_name: str = Field(None, alias="portName")
#     port_desc: str = Field(None, alias="portDesc")
#     wan_port_ipv4_setting: dict = Field(None, alias="wanPortIpv4Setting")


# class WlanModel(BaseModel):
#     id: str
#     name: str
#     site: str
#     guest: bool = Field(None, alias="guestNetEnable")
#     psk_setting: dict = Field(None, alias="pskSetting")
#     vlan_id: int = Field(None, alias="vlanId")


# class DeviceModel(BaseModel):
#     type: str
#     mac: str
#     name: str
#     model: str
#     hw_version: str = Field(None, alias="modelVersion")
#     fw_version: str = Field(None, alias="firmwareVersion")
#     ip: str | None
#     uptime: str | None = None
#     uptime_long: int = Field(None, alias="uptimeLong")
#     status: int
#     last_seen: int = Field(None, alias="lastSeen")
#     need_upgrade: bool = Field(None, alias="needUpgrade")
#     fw_download: bool = Field(None, alias="fwDownload")
#     cpu_util: int = Field(None, alias="cpuUtil")
#     mem_util: int = Field(None, alias="memUtil")
#     download: int | None = None
#     upload: int | None = None
#     site: str | None
#     client_num: int = Field(None, alias="clientNum")
#     sn: str | None
#     category: str | None = None
#     poe_remain: float = Field(None, alias="poeRemain")
#     fan_status: int = Field(None, alias="fanStatus")
#     poe_support: bool = Field(None, alias="poeSupport")


# class ClientModel(BaseModel):
#     mac: str
#     name: str
#     host_name: str = Field(None, alias="hostName")
#     device_type: str = Field(None, alias="deviceType")
#     ip: str
#     connect_type: int = Field(None, alias="connectType")
#     connect_dev_type: str = Field(None, alias="connectDevType")
#     connected_to_wireless_router: bool = Field(None, alias="connectedToWirelessRouter")
#     wireless: bool
#     switch_mac: str = Field(None, alias="switchMac")
#     switch_name: str = Field(None, alias="switchName")
#     stackable_switch: bool = Field(None, alias="stackableSwitch")
#     vid: int
#     network_name: str = Field(None, alias="networkName")
#     dot1x_vlan: int = Field(None, alias="dot1xVlan")
#     activity: int
#     traffic_down: int = Field(None, alias="trafficDown")
#     traffic_up: int = Field(None, alias="trafficUp")
#     uptime: int
#     last_seen: int = Field(None, alias="lastSeen")
#     auth_status: int = Field(None, alias="authStatus")
#     guest: bool
#     active: bool
#     manager: bool
#     ip_setting: dict = Field(None, alias="ipSetting")
#     down_packet: int = Field(None, alias="downPacket")
#     up_packet: int = Field(None, alias="upPacket")
#     rate_limit: dict = Field(None, alias="rateLimit")
#     standard_port: str = Field(None, alias="standardPort")
#     system_name: str | None = Field(None, alias="systemName")
#     connect_dev_subtype: int = Field(None, alias="connectDevSubtype")


# class GroupMemberIpv4Model(BaseModel):
#     ip: str
#     mask: int = Field(32)
#     description: str = Field("")
#     key: int = Field(int(time.time())*1000)

# class GroupMemberIpv6Model(BaseModel):
#     ip: str
#     prefix: int
#     key: int = Field(int(time.time())*1000)

# class GroupModel(BaseModel):
    # group_id: str = Field("", alias="groupId")
    # site: str = Field("")
    # build_in: bool = Field(False, alias="buildIn")
    # name: str
    # ip_list: list[GroupMemberIpv4Model] = Field([], alias="ipList")
    # ip_v6_list: list[GroupMemberIpv6Model] = Field([], alias="ipv6List")
    # count: int
    # type: int
    # resource: int
    # domain_name_port: list = Field(None, alias="domainNamePort")
    # port_mask_list: list = Field(None, alias="portMaskList")
    # port_type: int = Field(None, alias="portType")
    # country_list: list = Field(None, alias="countryList")
    # port_list: list = Field(None, alias="portList")
    # mac_address_list: list = Field(None, alias="macAddressList")